import copy
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from django.contrib.auth import get_user_model

from apps.api_testing.models import Environment, TestSuite
from apps.api_testing.services.scenario_import import SCHEMA_PATH, import_scenario
from apps.api_testing.utils import execute_test_suite

User = get_user_model()

_ALLOWED_METADATA_FIELDS = {"source", "generated_at", "requirement_doc", "api_doc"}


@dataclass
class NormalizationReport:
    changes: list[str] = field(default_factory=list)


@dataclass
class ScenarioValidationError:
    path: str
    message: str


@dataclass
class ScenarioRunResult:
    success: bool
    normalized: dict[str, Any]
    report: NormalizationReport
    schema_errors: list[ScenarioValidationError]
    import_result: dict[str, Any] | None = None
    execution_result: dict[str, Any] | None = None
    error: str = ""


def extract_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("RAGFlow 输出中未找到 JSON 对象")

    return json.loads(cleaned[start : end + 1])


def normalize_candidate_scenario(
    candidate: dict[str, Any],
    *,
    environment_variables: dict[str, str],
) -> tuple[dict[str, Any], NormalizationReport]:
    normalized = copy.deepcopy(candidate)
    report = NormalizationReport()

    _normalize_top_level_requests(normalized, report)
    _normalize_environment(normalized, environment_variables, report)
    _normalize_metadata(normalized, report)
    _normalize_requests(normalized, report)
    _normalize_suite_steps(normalized)

    return normalized, report


def validate_scenario(
    scenario: dict[str, Any],
    schema_path: Path = SCHEMA_PATH,
) -> list[ScenarioValidationError]:
    import jsonschema

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(scenario), key=lambda err: list(err.absolute_path))
    return [
        ScenarioValidationError(
            path="/".join(str(part) for part in error.absolute_path) or "<root>",
            message=error.message,
        )
        for error in errors
    ]


def run_candidate_scenario(
    candidate: dict[str, Any],
    *,
    user,
    environment_variables: dict[str, str],
    execute: bool = True,
    schema_path: Path = SCHEMA_PATH,
) -> ScenarioRunResult:
    normalized, report = normalize_candidate_scenario(
        candidate,
        environment_variables=environment_variables,
    )
    schema_errors = validate_scenario(normalized, schema_path)
    if schema_errors:
        return ScenarioRunResult(
            success=False,
            normalized=normalized,
            report=report,
            schema_errors=schema_errors,
            error="生成结果不符合 TestHub 场景契约",
        )

    import_result = import_scenario(normalized, user)
    if not import_result.get("success"):
        return ScenarioRunResult(
            success=False,
            normalized=normalized,
            report=report,
            schema_errors=[],
            import_result=import_result,
            error=import_result.get("error", "导入场景失败"),
        )

    execution_result = None
    if execute:
        execution_result = _execute_first_imported_suite(import_result, user)
        if not execution_result.get("success"):
            return ScenarioRunResult(
                success=False,
                normalized=normalized,
                report=report,
                schema_errors=[],
                import_result=import_result,
                execution_result=execution_result,
                error=execution_result.get("error", "执行测试套件失败"),
            )

    return ScenarioRunResult(
        success=True,
        normalized=normalized,
        report=report,
        schema_errors=[],
        import_result=import_result,
        execution_result=execution_result,
    )


def generate_candidate_from_ragflow(
    *,
    api_base_url: str,
    api_key: str,
    agent_id: str,
    question: str,
    user_id: str,
) -> dict[str, Any]:
    encoded_user_id = urllib.parse.quote(user_id, safe="")
    session = _post_json(
        f"{api_base_url.rstrip('/')}/agents/{agent_id}/sessions?user_id={encoded_user_id}",
        {"user_id": user_id},
        api_key,
        timeout=60,
    )
    session_id = _extract_session_id(session)
    completion = _post_json(
        f"{api_base_url.rstrip('/')}/agents/{agent_id}/completions",
        {
            "question": question,
            "stream": False,
            "session_id": session_id,
            "user_id": user_id,
        },
        api_key,
        timeout=420,
    )
    content = _extract_completion_content(completion)
    return extract_json_object(content)


def _normalize_top_level_requests(
    scenario: dict[str, Any],
    report: NormalizationReport,
) -> None:
    requests = scenario.get("requests")
    if "collections" not in scenario and isinstance(requests, list):
        project = scenario.get("project") if isinstance(scenario.get("project"), dict) else {}
        scenario["collections"] = [
            {
                "name": project.get("name", "RAGFlow 生成接口集合"),
                "requests": requests,
            }
        ]
        scenario.pop("requests", None)
        report.changes.append("将顶层 requests 移入 collections[0].requests")


def _normalize_environment(
    scenario: dict[str, Any],
    environment_variables: dict[str, str],
    report: NormalizationReport,
) -> None:
    environment = scenario.setdefault("environment", {})
    environment.setdefault("name", "ragflow-generated")

    scope = environment.get("scope")
    if scope not in {"GLOBAL", "LOCAL"}:
        environment["scope"] = "GLOBAL" if str(scope).lower() == "global" else "LOCAL"
        report.changes.append("将 environment.scope 归一化为 schema 枚举值")

    variables = environment.setdefault("variables", {})
    for key, value in environment_variables.items():
        existing = variables.get(key)
        if not existing or str(existing).startswith("{{"):
            variables[key] = value
            report.changes.append(f"填充 environment.variables.{key}")


def _normalize_metadata(scenario: dict[str, Any], report: NormalizationReport) -> None:
    metadata = scenario.get("metadata")
    if not isinstance(metadata, dict):
        return

    filtered = {
        key: value
        for key, value in metadata.items()
        if key in _ALLOWED_METADATA_FIELDS
    }
    if filtered != metadata:
        scenario["metadata"] = filtered
        report.changes.append("移除 metadata 中 schema 不允许的字段")


def _normalize_requests(scenario: dict[str, Any], report: NormalizationReport) -> None:
    for request in _iter_requests(scenario):
        _normalize_extractions(request, report)
        _normalize_params(request, report)


def _normalize_extractions(
    request: dict[str, Any],
    report: NormalizationReport,
) -> None:
    for extraction in request.get("variable_extractions", []) or []:
        if "variable_name" in extraction and "variable" not in extraction:
            extraction["variable"] = extraction.pop("variable_name")
            report.changes.append(
                f"{request.get('name', '未命名请求')} 的 variable_extractions 字段 variable_name 改为 variable"
            )


def _normalize_params(request: dict[str, Any], report: NormalizationReport) -> None:
    params = request.get("params")
    if not isinstance(params, list):
        return

    converted = {}
    for item in params:
        if isinstance(item, dict) and item.get("key"):
            converted[str(item["key"])] = str(item.get("value", ""))
    request["params"] = converted
    report.changes.append(f"{request.get('name', '未命名请求')} 的 params 由数组转为对象")


def _normalize_suite_steps(scenario: dict[str, Any]) -> None:
    for suite in scenario.get("suites", []) or []:
        for step in suite.get("steps", []) or []:
            step.setdefault("enabled", True)


def _iter_requests(scenario: dict[str, Any]):
    for collection in scenario.get("collections", []) or []:
        for request in collection.get("requests", []) or []:
            yield request


def _execute_first_imported_suite(import_result: dict[str, Any], user) -> dict[str, Any]:
    suite_ids = import_result.get("suite_ids") or []
    if not suite_ids:
        return {"success": False, "error": "导入结果中没有 suite_ids"}

    try:
        test_suite = TestSuite.objects.get(id=suite_ids[0])
    except TestSuite.DoesNotExist:
        return {"success": False, "error": f"测试套件不存在: {suite_ids[0]}"}

    environment = None
    environment_id = import_result.get("environment_id")
    if environment_id:
        try:
            environment = Environment.objects.get(id=environment_id)
        except Environment.DoesNotExist:
            return {"success": False, "error": f"环境不存在: {environment_id}"}
    return execute_test_suite(test_suite, environment, user)


def _post_json(
    url: str,
    payload: dict[str, Any],
    api_key: str,
    *,
    timeout: int,
) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="ignore"))


def _extract_session_id(response: dict[str, Any]) -> str:
    data = response.get("data") or {}
    nested_data = data.get("data") if isinstance(data, dict) else {}
    session_id = None
    if isinstance(data, dict):
        session_id = data.get("id") or data.get("session_id")
    if not session_id and isinstance(nested_data, dict):
        session_id = nested_data.get("id") or nested_data.get("session_id")
    if not session_id:
        raise ValueError(f"无法从 RAGFlow session 响应中提取 session_id: {response.get('message', '')}")
    return str(session_id)


def _extract_completion_content(response: dict[str, Any]) -> str:
    data = response.get("data") or {}
    nested_data = data.get("data") if isinstance(data, dict) else {}
    if isinstance(nested_data, dict):
        content = nested_data.get("content")
        if isinstance(content, str):
            return content
        outputs = nested_data.get("outputs")
        if isinstance(outputs, dict) and isinstance(outputs.get("content"), str):
            return outputs["content"]
    if isinstance(data, dict) and isinstance(data.get("content"), str):
        return data["content"]
    raise ValueError("RAGFlow completion 响应中未找到 content")
