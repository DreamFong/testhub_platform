import json
from pathlib import Path
from typing import Any

from django.db import transaction

from apps.api_testing.models import (
    ApiCollection,
    ApiProject,
    ApiRequest,
    Environment,
    TestSuite,
    TestSuiteRequest,
)

SCHEMA_DIR = Path(__file__).parent.parent.parent.parent / "contracts"
SCHEMA_PATH = SCHEMA_DIR / "ragflow-testhub-scenario-schema.json"

_SUPPORTED_VERSIONS = {"1.0.0"}


def _validate_schema_version(data: dict) -> str | None:
    version = data.get("schema_version", "")
    if version not in _SUPPORTED_VERSIONS:
        return f"不支持的 schema_version: {version}，当前仅支持 {_SUPPORTED_VERSIONS}"


def _validate_structure(data: dict) -> str | None:
    for field in ("project", "environment", "collections", "suites"):
        if field not in data:
            return f"缺少必填字段: {field}"

    if not data["collections"]:
        return "collections 不能为空"
    if not data["suites"]:
        return "suites 不能为空"


def _validate_request_name_uniqueness(data: dict) -> str | None:
    all_names: list[str] = []
    for collection in data["collections"]:
        names = [r["name"] for r in collection.get("requests", [])]
        seen: set[str] = set()
        for name in names:
            if name in seen:
                return f"集合 '{collection['name']}' 中存在重复请求名称: '{name}'"
            seen.add(name)
        all_names.extend(names)

    if len(all_names) != len(set(all_names)):
        return "跨集合存在重复请求名称"


def _validate_step_references(data: dict) -> str | None:
    all_request_names = set()
    for collection in data["collections"]:
        for request in collection.get("requests", []):
            all_request_names.add(request["name"])

    for suite in data["suites"]:
        step_names_in_suite: list[str] = []
        for step in suite.get("steps", []):
            name = step["request_name"]
            if name not in all_request_names:
                return f"套件 '{suite['name']}' 引用了不存在的请求: '{name}'"
            step_names_in_suite.append(name)

        # 检查同一套件内重复引用（模型 unique_together 约束）
        seen: set[str] = set()
        for name in step_names_in_suite:
            if name in seen:
                return f"套件 '{suite['name']}' 重复引用了请求: '{name}'"
            seen.add(name)


def _validate(data: dict) -> str | None:
    err = _validate_schema_version(data)
    if err:
        return err
    err = _validate_structure(data)
    if err:
        return err
    err = _validate_request_name_uniqueness(data)
    if err:
        return err
    return _validate_step_references(data)


def _build_request_data(request_def: dict) -> dict:
    fields: dict[str, Any] = {
        "name": request_def["name"],
        "description": request_def.get("description", ""),
        "request_type": "HTTP",
        "method": request_def["method"],
        "url": request_def["url"],
        "headers": request_def.get("headers", []),
        "params": request_def.get("params", {}),
        "body": request_def.get("body", {}),
        "auth": {},
        "pre_request_script": "",
        "post_request_script": "",
        "assertions": request_def.get("assertions", []),
        "variable_extractions": request_def.get("variable_extractions", []),
    }
    return fields


@transaction.atomic
def import_scenario(data: dict, user) -> dict:
    err = _validate(data)
    if err:
        return {"success": False, "error": err}

    # 1. 创建项目
    project_def = data["project"]
    project = ApiProject.objects.create(
        name=project_def["name"],
        description=project_def.get("description", ""),
        project_type="HTTP",
        status="IN_PROGRESS",
        owner=user,
    )

    # 2. 创建环境
    env_def = data["environment"]
    environment = Environment.objects.create(
        name=env_def["name"],
        scope=env_def.get("scope", "LOCAL"),
        variables=env_def.get("variables", {}),
        is_active=True,
        project=project,
        created_by=user,
    )

    # 3. 创建集合和请求
    request_map: dict[str, ApiRequest] = {}
    collection_ids: list[int] = []
    for coll_def in data["collections"]:
        collection = ApiCollection.objects.create(
            name=coll_def["name"],
            description=coll_def.get("description", ""),
            project=project,
        )
        collection_ids.append(collection.id)

        for idx, req_def in enumerate(coll_def.get("requests", [])):
            api_request = ApiRequest.objects.create(
                collection=collection,
                created_by=user,
                order=idx,
                **_build_request_data(req_def),
            )
            request_map[api_request.name] = api_request

    # 4. 创建套件和步骤
    suite_ids: list[int] = []
    for suite_def in data["suites"]:
        suite = TestSuite.objects.create(
            name=suite_def["name"],
            description=suite_def.get("description", ""),
            project=project,
            environment=environment,
            created_by=user,
        )
        suite_ids.append(suite.id)

        for idx, step_def in enumerate(suite_def.get("steps", [])):
            step_assertions = step_def.get("assertions", [])
            TestSuiteRequest.objects.create(
                test_suite=suite,
                request=request_map[step_def["request_name"]],
                order=idx,
                assertions=step_assertions,
                enabled=step_def.get("enabled", True),
            )

    return {
        "success": True,
        "project_id": project.id,
        "environment_id": environment.id,
        "collection_ids": collection_ids,
        "suite_ids": suite_ids,
    }
