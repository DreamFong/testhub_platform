from __future__ import annotations

import copy
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from apps.ui_automation.models import TestCase as UiTestCase, TestSuite
from apps.ui_automation.services.scenario_import import SCHEMA_PATH, import_scenario
from apps.ui_automation.test_executor import TestExecutor

_ALLOWED_METADATA_FIELDS = {"source", "generated_at", "requirement_doc", "ui_design_doc"}
_ACTION_ALIASES = {
    "input": ("fill", None),
    "input_text": ("fill", None),
    "type": ("fill", None),
    "waitfor": ("waitFor", None),
    "wait_for": ("waitFor", None),
    "switchtab": ("switchTab", None),
    "switch_tab": ("switchTab", None),
    "assert_text_contains": ("assert", "textContains"),
    "assert_text_equals": ("assert", "textEquals"),
    "assert_visible": ("assert", "isVisible"),
    "assert_exists": ("assert", "exists"),
}
_ASSERT_TYPE_ALIASES = {
    "text_contains": "textContains",
    "textcontains": "textContains",
    "text_equals": "textEquals",
    "textequals": "textEquals",
    "is_visible": "isVisible",
    "isvisible": "isVisible",
}

logger = logging.getLogger(__name__)


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


def normalize_candidate_scenario(candidate: dict[str, Any]) -> tuple[dict[str, Any], NormalizationReport]:
    normalized = copy.deepcopy(candidate)
    report = NormalizationReport()

    _normalize_metadata(normalized, report)
    _normalize_steps(normalized, report)
    _normalize_case_assertions(normalized, report)
    _normalize_suites(normalized, report)

    return normalized, report


def validate_scenario(
    scenario: dict[str, Any],
    schema_path: Path = SCHEMA_PATH,
) -> list[ScenarioValidationError]:
    import jsonschema

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    errors = sorted(validator.iter_errors(scenario), key=lambda err: list(err.absolute_path))
    validation_errors = [
        ScenarioValidationError(
            path="/".join(str(part) for part in error.absolute_path) or "<root>",
            message=error.message,
        )
        for error in errors
    ]

    base_url = scenario.get("project", {}).get("base_url")
    if base_url:
        validator = URLValidator()
        try:
            validator(base_url)
        except ValidationError as exc:
            validation_errors.append(
                ScenarioValidationError(
                    path="project/base_url",
                    message="; ".join(exc.messages),
                )
            )

    return validation_errors


def run_candidate_scenario(
    candidate: dict[str, Any],
    *,
    user: AbstractBaseUser,
    execute: bool = False,
    engine: str = "playwright",
    browser: str = "chrome",
    headless: bool = False,
    schema_path: Path = SCHEMA_PATH,
) -> ScenarioRunResult:
    normalized, report = normalize_candidate_scenario(candidate)
    schema_errors = validate_scenario(normalized, schema_path)
    if schema_errors:
        return ScenarioRunResult(
            success=False,
            normalized=normalized,
            report=report,
            schema_errors=schema_errors,
            error="生成结果不符合 TestHub UI 场景契约",
        )

    import_result = import_scenario(normalized, user)
    if not import_result.get("success"):
        return ScenarioRunResult(
            success=False,
            normalized=normalized,
            report=report,
            schema_errors=[],
            import_result=import_result,
            error=import_result.get("error", "导入 UI 场景失败"),
        )

    execution_result = None
    if execute:
        execution_result = _execute_first_imported_suite(
            import_result,
            user,
            engine=engine,
            browser=browser,
            headless=headless,
        )
        if not execution_result.get("success"):
            cleanup_error = _cleanup_imported_resources(import_result)
            if cleanup_error:
                execution_result["cleanup_error"] = cleanup_error
            else:
                execution_result["cleanup_performed"] = True
            return ScenarioRunResult(
                success=False,
                normalized=normalized,
                report=report,
                schema_errors=[],
                import_result=import_result,
                execution_result=execution_result,
                error=execution_result.get("error", "执行 UI 测试套件失败"),
            )

    return ScenarioRunResult(
        success=True,
        normalized=normalized,
        report=report,
        schema_errors=[],
        import_result=import_result,
        execution_result=execution_result,
    )


def _normalize_metadata(scenario: dict[str, Any], report: NormalizationReport) -> None:
    metadata = scenario.get("metadata")
    if not isinstance(metadata, dict):
        return

    filtered = {key: value for key, value in metadata.items() if key in _ALLOWED_METADATA_FIELDS}
    if filtered != metadata:
        scenario["metadata"] = filtered
        report.changes.append("移除 metadata 中 schema 不允许的字段")


def _normalize_steps(scenario: dict[str, Any], report: NormalizationReport) -> None:
    for case in scenario.get("test_cases", []) or []:
        for step in case.get("steps", []) or []:
            _normalize_step_aliases(case.get("name", "未命名用例"), step, report)


def _normalize_step_aliases(case_name: str, step: dict[str, Any], report: NormalizationReport) -> None:
    action = str(step.get("action", "")).strip()
    normalized_action, implied_assert_type = _normalize_action(action)
    if normalized_action and normalized_action != action:
        step["action"] = normalized_action
        report.changes.append(f"{case_name} 的步骤动作 {action} 归一化为 {normalized_action}")

    if "page" in step and "page_ref" not in step:
        step["page_ref"] = step.pop("page")
        report.changes.append(f"{case_name} 的步骤字段 page 改为 page_ref")

    if "element_name" in step and "element_ref" not in step:
        step["element_ref"] = step.pop("element_name")
        report.changes.append(f"{case_name} 的步骤字段 element_name 改为 element_ref")

    action_after_normalize = step.get("action")
    if action_after_normalize in {"fill", "switchTab"}:
        if "input" in step and "input_value" not in step:
            step["input_value"] = step.pop("input")
            report.changes.append(f"{case_name} 的步骤字段 input 改为 input_value")
        if "value" in step and "input_value" not in step:
            step["input_value"] = step.pop("value")
            report.changes.append(f"{case_name} 的步骤字段 value 改为 input_value")

    if action_after_normalize == "assert":
        if "assertion_type" in step and "assert_type" not in step:
            step["assert_type"] = step.pop("assertion_type")
            report.changes.append(f"{case_name} 的步骤字段 assertion_type 改为 assert_type")
        if implied_assert_type and not step.get("assert_type"):
            step["assert_type"] = implied_assert_type
            report.changes.append(f"{case_name} 的断言动作补齐 assert_type={implied_assert_type}")
        if step.get("assert_type"):
            normalized_assert_type = _normalize_assert_type(step["assert_type"])
            if normalized_assert_type != step["assert_type"]:
                step["assert_type"] = normalized_assert_type
                report.changes.append(f"{case_name} 的断言类型归一化为 {normalized_assert_type}")
        if "expected" in step and "assert_value" not in step:
            step["assert_value"] = step.pop("expected")
            report.changes.append(f"{case_name} 的步骤字段 expected 改为 assert_value")


def _normalize_case_assertions(scenario: dict[str, Any], report: NormalizationReport) -> None:
    for case in scenario.get("test_cases", []) or []:
        assertions = case.pop("assertions", None)
        if not assertions:
            continue

        for assertion in assertions:
            step = {
                "action": "assert",
                "page_ref": assertion.get("page_ref") or assertion.get("page"),
                "element_ref": assertion.get("element_ref") or assertion.get("element_name"),
                "assert_type": _normalize_assert_type(assertion.get("assert_type") or assertion.get("type", "")),
                "assert_value": assertion.get("assert_value") or assertion.get("expected", ""),
                "description": assertion.get("description", ""),
            }
            if assertion.get("evidence"):
                step["evidence"] = assertion["evidence"]
            case.setdefault("steps", []).append(step)
        report.changes.append(f"{case.get('name', '未命名用例')} 的 assertions 追加为 assert 步骤")


def _normalize_suites(scenario: dict[str, Any], report: NormalizationReport) -> None:
    if "suites" not in scenario and isinstance(scenario.get("test_suite"), dict):
        scenario["suites"] = [scenario.pop("test_suite")]
        report.changes.append("将 test_suite 归一化为 suites 数组")

    suites = scenario.get("suites")
    if suites:
        for suite in suites:
            if "test_cases" in suite and "test_case_names" not in suite:
                suite["test_case_names"] = suite.pop("test_cases")
                report.changes.append(f"套件 {suite.get('name', '未命名套件')} 的 test_cases 改为 test_case_names")
        return

    case_names = [case["name"] for case in scenario.get("test_cases", []) or []]
    if not case_names:
        return
    suite_name = scenario.get("scenario_title") or f"{case_names[0]} 套件"
    scenario["suites"] = [{"name": suite_name, "test_case_names": case_names}]
    report.changes.append("补齐默认 suites 定义")


def _normalize_action(action: str) -> tuple[str, str | None]:
    lowered = action.lower().replace("-", "_")
    if lowered in _ACTION_ALIASES:
        return _ACTION_ALIASES[lowered]
    return action, None


def _normalize_assert_type(assert_type: str) -> str:
    lowered = str(assert_type).strip().replace("-", "_")
    return _ASSERT_TYPE_ALIASES.get(lowered, assert_type)


def _cleanup_imported_resources(import_result: dict[str, Any]) -> str | None:
    from django.db import transaction

    try:
        suite_ids = import_result.get("suite_ids") or []
        test_case_ids = import_result.get("test_case_ids") or []
        with transaction.atomic():
            if suite_ids:
                TestSuite.objects.filter(id__in=suite_ids).delete()
            if test_case_ids:
                UiTestCase.objects.filter(id__in=test_case_ids).delete()
    except Exception as exc:
        logger.exception("清理导入的 UI 场景失败")
        return str(exc)
    return None


def _execute_first_imported_suite(
    import_result: dict[str, Any],
    user: AbstractBaseUser,
    *,
    engine: str,
    browser: str,
    headless: bool,
) -> dict[str, Any]:
    suite_ids = import_result.get("suite_ids") or []
    if not suite_ids:
        return {"success": False, "error": "导入结果中没有 suite_ids"}

    try:
        test_suite = TestSuite.objects.get(id=suite_ids[0])
    except TestSuite.DoesNotExist:
        return {"success": False, "error": f"测试套件不存在: {suite_ids[0]}"}

    try:
        executor = TestExecutor(
            test_suite=test_suite,
            engine=engine,
            browser=browser,
            headless=headless,
            executed_by=user,
        )
        executor.run()
    except Exception as exc:
        logger.exception("执行 UI 测试套件失败，suite_id=%s", suite_ids[0])
        return {"success": False, "error": f"执行测试套件失败: {exc}"}

    execution = executor.execution
    if not execution:
        return {"success": False, "error": "执行器未生成执行记录"}

    return {
        "success": execution.status == "SUCCESS",
        "execution_id": execution.id,
        "status": execution.status,
        "passed_count": execution.passed_cases,
        "failed_count": execution.failed_cases,
        "total_count": execution.total_cases,
        "error": execution.error_message,
        "summary": (execution.result_data or {}).get("summary", {}),
    }
