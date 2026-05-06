from __future__ import annotations

from pathlib import Path
from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import transaction
from django.db.models import Q

from apps.ui_automation.models import (
    Element,
    TestCase,
    TestCaseStep,
    TestSuite,
    TestSuiteTestCase,
    UiProject,
)

SCHEMA_DIR = Path(__file__).parent.parent.parent.parent / "contracts"
SCHEMA_PATH = SCHEMA_DIR / "ragflow-testhub-ui-scenario-schema.json"

_SUPPORTED_VERSIONS = {"1.0.0"}
_SUPPORTED_ACTIONS = {"click", "fill", "getText", "waitFor", "hover", "scroll", "screenshot", "assert", "wait", "switchTab"}
_ELEMENT_REQUIRED_ACTIONS = {"click", "fill", "getText", "waitFor", "hover", "scroll", "assert"}
_ASSERTIONS_REQUIRING_VALUE = {"textContains", "textEquals"}
_SUPPORTED_ASSERT_TYPES = {"textContains", "textEquals", "isVisible", "exists"}
_SUPPORTED_PRIORITIES = {"high", "medium", "low"}


class ImportScenarioError(Exception):
    pass


def _validate_schema_version(data: dict[str, Any]) -> str | None:
    version = data.get("schema_version", "")
    if version not in _SUPPORTED_VERSIONS:
        return f"不支持的 schema_version: {version}，当前仅支持 {_SUPPORTED_VERSIONS}"
    return None


def _validate_structure(data: dict[str, Any]) -> str | None:
    for field in ("project", "test_cases"):
        if field not in data:
            return f"缺少必填字段: {field}"

    if not data["test_cases"]:
        return "test_cases 不能为空"
    return None


def _validate_test_case_name_uniqueness(data: dict[str, Any]) -> str | None:
    names = [case["name"] for case in data.get("test_cases", [])]
    if len(names) != len(set(names)):
        return "test_cases 中存在重复用例名称"
    return None


def _validate_suite_references(data: dict[str, Any]) -> str | None:
    case_names = {case["name"] for case in data.get("test_cases", [])}
    for suite in data.get("suites", []) or []:
        seen: set[str] = set()
        for case_name in suite.get("test_case_names", []):
            if case_name not in case_names:
                return f"套件 '{suite['name']}' 引用了不存在的测试用例: '{case_name}'"
            if case_name in seen:
                return f"套件 '{suite['name']}' 重复引用了测试用例: '{case_name}'"
            seen.add(case_name)
    return None


def _validate_steps(data: dict[str, Any]) -> str | None:
    for case in data.get("test_cases", []):
        steps = case.get("steps", [])
        if not steps:
            return f"测试用例 '{case['name']}' 的 steps 不能为空"

        for step in steps:
            action = step.get("action")
            if action not in _SUPPORTED_ACTIONS:
                return f"测试用例 '{case['name']}' 使用了不支持的 action: {action}"
            if action in _ELEMENT_REQUIRED_ACTIONS and not step.get("element_ref"):
                return f"测试用例 '{case['name']}' 的动作 '{action}' 需要 element_ref"
            if action == "assert":
                assert_type = step.get("assert_type")
                if assert_type not in _SUPPORTED_ASSERT_TYPES:
                    return f"测试用例 '{case['name']}' 使用了不支持的 assert_type: {assert_type}"
                if assert_type in _ASSERTIONS_REQUIRING_VALUE and not step.get("assert_value"):
                    return f"测试用例 '{case['name']}' 的断言类型 '{assert_type}' 需要 assert_value"
    return None


def _validate(data: dict[str, Any]) -> str | None:
    for validator in (
        _validate_schema_version,
        _validate_structure,
        _validate_test_case_name_uniqueness,
        _validate_suite_references,
        _validate_steps,
    ):
        error = validator(data)
        if error:
            return error
    return None


def _resolve_project(
    data: dict[str, Any],
    user: AbstractBaseUser,
) -> tuple[UiProject | None, str | None]:
    project_def = data["project"]
    accessible_projects = UiProject.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    project_id = project_def.get("id")
    if project_id:
        project = accessible_projects.filter(id=project_id).first()
        if project:
            return project, None
        return None, f"找不到可访问的 UI 项目 ID: {project_id}"

    project_name = project_def.get("name", "")
    matches = list(accessible_projects.filter(name=project_name))
    if not matches:
        return None, f"找不到可访问的 UI 项目: {project_name}"
    if len(matches) > 1:
        return None, f"存在多个同名 UI 项目，请在 candidate.project.id 中指定项目 ID: {project_name}"
    return matches[0], None


def _resolve_element(project: UiProject, step_def: dict[str, Any]) -> tuple[Element | None, str | None]:
    element_ref = step_def.get("element_ref")
    if not element_ref:
        return None, None

    query = Element.objects.filter(project=project, name=element_ref)
    page_ref = step_def.get("page_ref")
    if page_ref:
        query = query.filter(page=page_ref)

    matches = list(query)
    if not matches:
        if page_ref:
            return None, f"页面 '{page_ref}' 下未找到元素 '{element_ref}'"
        return None, f"未找到元素 '{element_ref}'"
    if len(matches) > 1:
        if page_ref:
            return None, f"页面 '{page_ref}' 下存在多个同名元素 '{element_ref}'"
        return None, f"存在多个同名元素 '{element_ref}'，请补充 page_ref"
    return matches[0], None


def _build_case_description(case_def: dict[str, Any]) -> str:
    description = str(case_def.get("description", "")).strip()
    preconditions = [str(item).strip() for item in case_def.get("preconditions", []) if str(item).strip()]
    if not preconditions:
        return description

    preconditions_text = "前置条件: " + "；".join(preconditions)
    return "\n".join(part for part in (description, preconditions_text) if part)


def _build_step_description(step_def: dict[str, Any]) -> str:
    description = str(step_def.get("description", "")).strip()
    evidence = str(step_def.get("evidence", "")).strip()
    if not evidence:
        return description

    evidence_text = f"证据: {evidence}"
    return "\n".join(part for part in (description, evidence_text) if part)


def _build_suite_description(data: dict[str, Any], suite_def: dict[str, Any]) -> str:
    parts: list[str] = []
    description = str(suite_def.get("description", "")).strip()
    if description:
        parts.append(description)

    page_names = [
        str(page.get("name", "")).strip()
        for page in data.get("pages", []) or []
        if str(page.get("name", "")).strip()
    ]
    if page_names:
        parts.append("候选页面: " + "、".join(page_names))

    confidence = data.get("confidence")
    if confidence is not None:
        parts.append(f"候选置信度: {confidence}")

    ambiguities = [
        str(item).strip()
        for item in data.get("ambiguities", []) or []
        if str(item).strip()
    ]
    if ambiguities:
        parts.append("候选歧义: " + "；".join(ambiguities))

    return "\n".join(parts)


def _validate_project_base_url(project: UiProject, data: dict[str, Any]) -> str | None:
    candidate_base_url = str(data.get("project", {}).get("base_url", "")).strip()
    if candidate_base_url and candidate_base_url != project.base_url:
        return (
            "candidate.project.base_url 与现有 UI 项目 base_url 不一致: "
            f"{candidate_base_url} != {project.base_url}"
        )
    return None


def _build_step_fields(step_def: dict[str, Any], element: Element | None) -> dict[str, Any]:
    return {
        "action_type": step_def["action"],
        "element": element,
        "input_value": step_def.get("input_value", ""),
        "wait_time": step_def.get("wait_time", 1000),
        "assert_type": step_def.get("assert_type", ""),
        "assert_value": step_def.get("assert_value", ""),
        "description": _build_step_description(step_def),
    }


@transaction.atomic
def _import_scenario(data: dict[str, Any], user: AbstractBaseUser) -> dict[str, Any]:
    error = _validate(data)
    if error:
        raise ImportScenarioError(error)

    project, project_error = _resolve_project(data, user)
    if project_error or not project:
        raise ImportScenarioError(project_error or "无法确定 UI 项目")

    base_url_error = _validate_project_base_url(project, data)
    if base_url_error:
        raise ImportScenarioError(base_url_error)

    test_cases_map: dict[str, TestCase] = {}
    test_case_ids: list[int] = []
    for case_def in data.get("test_cases", []):
        priority = case_def.get("priority", "medium")
        if priority not in _SUPPORTED_PRIORITIES:
            priority = "medium"

        test_case = TestCase.objects.create(
            name=case_def["name"],
            description=_build_case_description(case_def),
            project=project,
            status="ready",
            priority=priority,
            created_by=user,
        )
        test_cases_map[test_case.name] = test_case
        test_case_ids.append(test_case.id)

        for index, step_def in enumerate(case_def.get("steps", []), start=1):
            element, element_error = _resolve_element(project, step_def)
            if element_error:
                raise ImportScenarioError(f"测试用例 '{test_case.name}' 绑定失败: {element_error}")

            TestCaseStep.objects.create(
                test_case=test_case,
                step_number=index,
                **_build_step_fields(step_def, element),
            )

    suite_ids: list[int] = []
    for suite_def in data.get("suites", []) or []:
        suite = TestSuite.objects.create(
            name=suite_def["name"],
            description=_build_suite_description(data, suite_def),
            project=project,
        )
        suite_ids.append(suite.id)

        for order, case_name in enumerate(suite_def.get("test_case_names", [])):
            TestSuiteTestCase.objects.create(
                test_suite=suite,
                test_case=test_cases_map[case_name],
                order=order,
            )

    return {
        "success": True,
        "project_id": project.id,
        "test_case_ids": test_case_ids,
        "suite_ids": suite_ids,
    }


def import_scenario(data: dict[str, Any], user: AbstractBaseUser) -> dict[str, Any]:
    try:
        return _import_scenario(data, user)
    except ImportScenarioError as exc:
        return {"success": False, "error": str(exc)}
