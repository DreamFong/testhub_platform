import json
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from apps.api_testing.models import ApiProject, Environment, TestSuite

User = get_user_model()


class TestRagflowExtractionHelpers(TestCase):
    def test_extract_json_object_ignores_thinking_process_examples(self):
        from apps.api_testing.services.ragflow_scenario_runner import extract_json_object

        text = '''
Thinking Process:
Use {"type":"json","data":{"foo":"bar"}} format.
Ready to generate.
{
  "schema_version": "1.0.0",
  "project": {"name": "用户管理"},
  "environment": {"name": "ragflow-generated", "scope": "LOCAL", "variables": {}},
  "collections": [],
  "suites": []
}
'''

        extracted = extract_json_object(text)

        self.assertEqual(extracted["schema_version"], "1.0.0")
        self.assertEqual(extracted["project"]["name"], "用户管理")

    def test_extract_json_object_prefers_last_full_candidate(self):
        from apps.api_testing.services.ragflow_scenario_runner import extract_json_object

        text = '''
示例：
{"schema_version":"1.0.0","project":{"name":"示例"},"environment":{"name":"env","variables":{}},"collections":[],"suites":[]}
最终结果：
{"schema_version":"1.0.0","project":{"name":"正式结果"},"environment":{"name":"env2","variables":{}},"collections":[{"name":"接口集合","requests":[]}],"suites":[{"name":"场景","steps":[]}]}
'''

        extracted = extract_json_object(text)

        self.assertEqual(extracted["project"]["name"], "正式结果")

    def test_extract_json_object_prefers_recoverable_candidate_over_larger_irrelevant_object(self):
        from apps.api_testing.services.ragflow_scenario_runner import extract_json_object

        text = '''
示例：
{"foo":{"bar":{"baz":1}},"note":"示例对象"}
最终结果：
{"schema_version":"1.0.0","project":{"name":"可恢复结果","environment":{"name":"env","variables":{}},"requests":[],"suite":{"name":"主流程","steps":[]}}}
'''

        extracted = extract_json_object(text)

        self.assertEqual(extracted["project"]["name"], "可恢复结果")

    @patch("apps.api_testing.services.ragflow_scenario_runner._post_json")
    def test_generate_candidate_accepts_recoverable_nested_structure(
        self,
        mock_post_json,
    ):
        from apps.api_testing.services.ragflow_scenario_runner import (
            generate_candidate_from_ragflow,
        )

        nested_candidate = {
            "schema_version": "1.0.0",
            "project": {
                "name": "用户管理",
                "environment": {
                    "name": "ruoyi-dev",
                    "variables": {},
                },
                "requests": [],
                "suite": {"name": "主流程", "steps": []},
            },
        }
        mock_post_json.side_effect = [
            {"data": {"id": "session-1"}},
            {"data": {"data": {"content": json.dumps(nested_candidate, ensure_ascii=False)}}},
            {"data": {"data": {"content": json.dumps(nested_candidate, ensure_ascii=False)}}},
        ]

        candidate = generate_candidate_from_ragflow(
            api_base_url="http://ragflow.example/api/v1",
            api_key="secret",
            agent_id="agent-1",
            question="新增用户",
            user_id="runner",
        )

        self.assertEqual(candidate["project"]["name"], "用户管理")
        self.assertGreaterEqual(mock_post_json.call_count, 2)

    @patch("apps.api_testing.services.ragflow_scenario_runner._post_json")
    def test_generate_candidate_retries_when_first_completion_is_not_pure_json(
        self,
        mock_post_json,
    ):
        from apps.api_testing.services.ragflow_scenario_runner import (
            generate_candidate_from_ragflow,
        )

        mock_post_json.side_effect = [
            {"data": {"id": "session-1"}},
            {
                "data": {
                    "data": {
                        "content": (
                            'Thinking Process:\n'
                            'Use {"type":"json","data":{"foo":"bar"}} format.\n'
                            'Final answer follows.'
                        )
                    }
                }
            },
            {
                "data": {
                    "data": {
                        "content": json.dumps(
                            {
                                "schema_version": "1.0.0",
                                "project": {"name": "用户管理"},
                                "environment": {
                                    "name": "ragflow-generated",
                                    "scope": "LOCAL",
                                    "variables": {},
                                },
                                "collections": [],
                                "suites": [],
                            },
                            ensure_ascii=False,
                        )
                    }
                }
            },
        ]

        candidate = generate_candidate_from_ragflow(
            api_base_url="http://ragflow.example/api/v1",
            api_key="secret",
            agent_id="agent-1",
            question="新增用户",
            user_id="runner",
        )

        self.assertEqual(candidate["schema_version"], "1.0.0")
        self.assertEqual(mock_post_json.call_count, 3)
        self.assertIn("合法 JSON", mock_post_json.call_args_list[2].args[1]["question"])

    @patch("apps.api_testing.services.ragflow_scenario_runner._post_json")
    def test_generate_candidate_raises_clear_error_when_retrieval_is_empty_after_retry(
        self,
        mock_post_json,
    ):
        from apps.api_testing.services.ragflow_scenario_runner import (
            generate_candidate_from_ragflow,
        )

        mock_post_json.side_effect = [
            {"data": {"id": "session-1"}},
            {
                "data": {
                    "data": {
                        "content": (
                            "Thinking Process:\n"
                            'Retrieved Content: "未检索到相关内容"\n'
                            "No API documentation is available."
                        )
                    }
                }
            },
            {
                "data": {
                    "data": {
                        "content": "未检索到足够的 SRS 或 API 文档。"
                    }
                }
            },
        ]

        with self.assertRaisesRegex(ValueError, "检索结果为空"):
            generate_candidate_from_ragflow(
                api_base_url="http://ragflow.example/api/v1",
                api_key="secret",
                agent_id="agent-1",
                question="新增用户",
                user_id="runner",
            )

        self.assertEqual(mock_post_json.call_count, 3)

    @patch("apps.api_testing.services.ragflow_scenario_runner._post_json")
    def test_generate_candidate_accepts_valid_json_even_if_reasoning_mentions_empty_retrieval(
        self,
        mock_post_json,
    ):
        from apps.api_testing.services.ragflow_scenario_runner import (
            generate_candidate_from_ragflow,
        )

        candidate_payload = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ragflow-generated", "scope": "LOCAL", "variables": {}},
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "管理员登录",
                            "method": "POST",
                            "url": "{{baseUrl}}/admin-api/system/auth/login",
                        }
                    ],
                }
            ],
            "suites": [{"name": "主流程", "steps": [{"request_name": "管理员登录"}]}],
        }
        mock_post_json.side_effect = [
            {"data": {"id": "session-1"}},
            {
                "data": {
                    "data": {
                        "content": (
                            "Thinking Process:\n"
                            'Retrieved Content: "未检索到相关内容"\n'
                            "Final answer:\n"
                            f"{json.dumps(candidate_payload, ensure_ascii=False)}"
                        )
                    }
                }
            },
        ]

        candidate = generate_candidate_from_ragflow(
            api_base_url="http://ragflow.example/api/v1",
            api_key="secret",
            agent_id="agent-1",
            question="新增用户",
            user_id="runner",
        )

        self.assertEqual(candidate["project"]["name"], "用户管理")
        self.assertEqual(mock_post_json.call_count, 2)


class TestRagflowScenarioNormalizer(TestCase):
    def test_normalize_candidate_to_contract_shape(self):
        from apps.api_testing.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
        )

        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {
                "name": "ruoyi-dev",
                "scope": "global",
                "variables": {
                    "baseUrl": "{{baseUrl}}",
                    "tenantId": "",
                    "adminUsername": "{{adminUsername}}",
                    "adminPassword": "{{adminPassword}}",
                },
            },
            "requests": [
                {
                    "name": "管理员登录",
                    "method": "POST",
                    "url": "{{baseUrl}}/admin-api/system/auth/login",
                    "headers": [],
                    "body": {"type": "json", "data": {}},
                    "assertions": [{"type": "status_code", "expected": 200}],
                    "variable_extractions": [
                        {
                            "variable_name": "accessToken",
                            "source": "body",
                            "json_path": "$.data.accessToken",
                        }
                    ],
                },
                {
                    "name": "查询用户详情",
                    "method": "GET",
                    "url": "{{baseUrl}}/admin-api/system/user/get",
                    "params": [{"key": "id", "value": "{{newUserId}}"}],
                    "body": {"type": "none"},
                    "assertions": [{"type": "status_code", "expected": 200}],
                },
            ],
            "suites": [
                {
                    "name": "用户管理最小主流程",
                    "steps": [
                        {"request_name": "管理员登录"},
                        {"request_name": "查询用户详情"},
                    ],
                }
            ],
            "metadata": {"description": "非契约字段", "source": "ragflow"},
        }

        normalized, report = normalize_candidate_scenario(
            candidate,
            environment_variables={
                "baseUrl": "http://81.70.235.9:48080",
                "tenantId": "1",
                "adminUsername": "admin",
                "adminPassword": "secret",
            },
        )

        self.assertNotIn("requests", normalized)
        self.assertEqual(len(normalized["collections"]), 1)
        self.assertEqual(normalized["environment"]["scope"], "GLOBAL")
        self.assertEqual(
            normalized["environment"]["variables"]["baseUrl"],
            "http://81.70.235.9:48080",
        )
        extraction = normalized["collections"][0]["requests"][0][
            "variable_extractions"
        ][0]
        self.assertEqual(extraction["variable"], "accessToken")
        self.assertNotIn("variable_name", extraction)
        normalized["collections"][0]["requests"][0]["variable_extractions"].append(
            {
                "name": "newUserId",
                "source": "body",
                "json_path": "$.data",
            }
        )
        normalized, report = normalize_candidate_scenario(
            normalized,
            environment_variables={
                "baseUrl": "http://81.70.235.9:48080",
                "tenantId": "1",
                "adminUsername": "admin",
                "adminPassword": "secret",
            },
        )
        second_extraction = normalized["collections"][0]["requests"][0][
            "variable_extractions"
        ][1]
        self.assertEqual(second_extraction["variable"], "newUserId")
        self.assertNotIn("name", second_extraction)
        self.assertEqual(
            normalized["collections"][0]["requests"][1]["params"],
            {"id": "{{newUserId}}"},
        )

    def test_normalize_path_and_expression_to_contract_fields(self):
        from apps.api_testing.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
        )

        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "创建用户",
                            "method": "POST",
                            "path": "/admin-api/system/user/create",
                            "variable_extractions": [
                                {"variable": "newUserId", "expression": "$.data"}
                            ],
                        }
                    ],
                }
            ],
            "suites": [{"name": "主流程", "steps": [{"request_name": "创建用户"}]}],
        }

        normalized, report = normalize_candidate_scenario(
            candidate,
            environment_variables={"baseUrl": "http://example.test"},
        )

        request = normalized["collections"][0]["requests"][0]
        self.assertEqual(request["url"], "{{baseUrl}}/admin-api/system/user/create")
        self.assertNotIn("path", request)
        extraction = request["variable_extractions"][0]
        self.assertEqual(extraction["source"], "body")
        self.assertEqual(extraction["json_path"], "$.data")
        self.assertNotIn("expression", extraction)
        self.assertTrue(report.changes)

    def test_normalize_hoists_nested_project_fields_and_singular_suite(self):
        from apps.api_testing.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
        )

        candidate = {
            "schema_version": "1.0.0",
            "project": {
                "name": "用户管理",
                "description": "最小主流程",
                "environment": {"name": "nested-env", "scope": "global", "variables": {}},
                "requests": [
                    {
                        "name": "创建用户",
                        "method": "POST",
                        "url": "{{baseUrl}}/admin-api/system/user/create",
                    }
                ],
                "suite": {
                    "name": "创建用户套件",
                    "steps": [{"request_name": "创建用户"}],
                },
            },
        }

        normalized, report = normalize_candidate_scenario(
            candidate,
            environment_variables={"baseUrl": "http://example.test"},
        )

        self.assertEqual(normalized["project"], {"name": "用户管理", "description": "最小主流程"})
        self.assertEqual(normalized["environment"]["name"], "nested-env")
        self.assertEqual(len(normalized["collections"]), 1)
        self.assertEqual(normalized["collections"][0]["requests"][0]["name"], "创建用户")
        self.assertEqual(len(normalized["suites"]), 1)
        self.assertEqual(normalized["suites"][0]["name"], "创建用户套件")
        self.assertTrue(report.changes)

    def test_normalize_environment_variables_from_non_object(self):
        from apps.api_testing.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
        )

        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": []},
            "collections": [],
            "suites": [],
        }

        normalized, report = normalize_candidate_scenario(
            candidate,
            environment_variables={"baseUrl": "http://example.test"},
        )

        self.assertEqual(normalized["environment"]["variables"], {"baseUrl": "http://example.test"})
        self.assertTrue(report.changes)

    def test_normalize_environment_from_non_object(self):
        from apps.api_testing.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
        )

        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": [],
            "collections": [],
            "suites": [],
        }

        normalized, report = normalize_candidate_scenario(
            candidate,
            environment_variables={"baseUrl": "http://example.test"},
        )

        self.assertEqual(normalized["environment"]["name"], "ragflow-generated")
        self.assertEqual(normalized["environment"]["variables"], {"baseUrl": "http://example.test"})
        self.assertTrue(report.changes)

    def test_preserve_expression_when_source_is_not_body(self):
        from apps.api_testing.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
        )

        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "创建用户",
                            "method": "POST",
                            "url": "{{baseUrl}}/admin-api/system/user/create",
                            "variable_extractions": [
                                {"variable": "traceId", "source": "header", "expression": "X-Trace-Id"}
                            ],
                        }
                    ],
                }
            ],
            "suites": [{"name": "主流程", "steps": [{"request_name": "创建用户"}]}],
        }

        normalized, _ = normalize_candidate_scenario(
            candidate,
            environment_variables={"baseUrl": "http://example.test"},
        )

        extraction = normalized["collections"][0]["requests"][0]["variable_extractions"][0]
        self.assertEqual(extraction["source"], "header")
        self.assertEqual(extraction["expression"], "X-Trace-Id")
        self.assertNotIn("json_path", extraction)

    def test_preserve_expression_when_source_missing_and_not_json_path(self):
        from apps.api_testing.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
        )

        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "创建用户",
                            "method": "POST",
                            "url": "{{baseUrl}}/admin-api/system/user/create",
                            "variable_extractions": [
                                {"variable": "traceId", "expression": "X-Trace-Id"}
                            ],
                        }
                    ],
                }
            ],
            "suites": [{"name": "主流程", "steps": [{"request_name": "创建用户"}]}],
        }

        normalized, _ = normalize_candidate_scenario(
            candidate,
            environment_variables={"baseUrl": "http://example.test"},
        )

        extraction = normalized["collections"][0]["requests"][0]["variable_extractions"][0]
        self.assertEqual(extraction["expression"], "X-Trace-Id")
        self.assertNotIn("json_path", extraction)

    def test_validate_schema_reports_contract_errors(self):
        from apps.api_testing.services.ragflow_scenario_runner import validate_scenario

        errors = validate_scenario({"schema_version": "1.0.0"})

        self.assertGreater(len(errors), 0)
        self.assertIn("collections", " ".join(error.message for error in errors))


class TestRagflowScenarioRunner(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="runner", password="pass")

    @patch("apps.api_testing.services.ragflow_scenario_runner.execute_test_suite")
    @patch("apps.api_testing.services.ragflow_scenario_runner.import_scenario")
    def test_run_candidate_imports_then_executes_first_suite(
        self,
        mock_import_scenario,
        mock_execute_test_suite,
    ):
        from apps.api_testing.services.ragflow_scenario_runner import (
            run_candidate_scenario,
        )

        project = ApiProject.objects.create(
            name="用户管理",
            project_type="HTTP",
            status="IN_PROGRESS",
            owner=self.user,
        )
        environment = Environment.objects.create(
            name="ruoyi-dev",
            scope="GLOBAL",
            variables={},
            project=project,
            created_by=self.user,
        )
        suite = TestSuite.objects.create(
            name="用户管理最小主流程",
            project=project,
            environment=environment,
            created_by=self.user,
        )
        mock_import_scenario.return_value = {
            "success": True,
            "project_id": project.id,
            "environment_id": environment.id,
            "collection_ids": [1],
            "suite_ids": [suite.id],
        }
        mock_execute_test_suite.return_value = {
            "success": True,
            "execution_id": 26,
            "passed_count": 4,
            "failed_count": 0,
            "total_count": 4,
        }
        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "管理员登录",
                            "method": "POST",
                            "url": "{{baseUrl}}/admin-api/system/auth/login",
                        }
                    ],
                }
            ],
            "suites": [
                {"name": "用户管理最小主流程", "steps": [{"request_name": "管理员登录"}]}
            ],
        }

        result = run_candidate_scenario(
            candidate,
            user=self.user,
            environment_variables={"baseUrl": "http://example.test"},
            execute=True,
        )

        self.assertTrue(result.success)
        mock_import_scenario.assert_called_once()
        imported_payload = mock_import_scenario.call_args.args[0]
        self.assertEqual(
            imported_payload["environment"]["variables"]["baseUrl"],
            "http://example.test",
        )
        mock_execute_test_suite.assert_called_once_with(suite, environment, self.user)
        self.assertEqual(result.execution_result["execution_id"], 26)

    @patch("apps.api_testing.services.ragflow_scenario_runner.import_scenario")
    def test_run_candidate_returns_failure_when_imported_suite_missing(
        self,
        mock_import_scenario,
    ):
        from apps.api_testing.services.ragflow_scenario_runner import (
            run_candidate_scenario,
        )

        mock_import_scenario.return_value = {
            "success": True,
            "environment_id": None,
            "collection_ids": [],
            "suite_ids": [999999],
        }
        candidate = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "管理员登录",
                            "method": "POST",
                            "url": "{{baseUrl}}/admin-api/system/auth/login",
                        }
                    ],
                }
            ],
            "suites": [
                {"name": "用户管理最小主流程", "steps": [{"request_name": "管理员登录"}]}
            ],
        }

        result = run_candidate_scenario(
            candidate,
            user=self.user,
            environment_variables={},
            execute=True,
        )

        self.assertFalse(result.success)
        self.assertIn("测试套件不存在", result.error)

    @patch("apps.api_testing.services.ragflow_scenario_runner.import_scenario")
    def test_run_candidate_rejects_invalid_schema_without_import(self, mock_import_scenario):
        from apps.api_testing.services.ragflow_scenario_runner import (
            run_candidate_scenario,
        )

        result = run_candidate_scenario(
            {"schema_version": "1.0.0"},
            user=self.user,
            environment_variables={},
        )

        self.assertFalse(result.success)
        self.assertTrue(result.schema_errors)
        mock_import_scenario.assert_not_called()


class TestRunRagflowScenarioCommand(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="command_user", password="pass")

    @patch("apps.api_testing.management.commands.run_ragflow_testhub_scenario.run_candidate_scenario")
    def test_command_loads_candidate_json_and_invokes_runner(self, mock_run_candidate):
        mock_run_candidate.return_value = Mock(
            success=True,
            normalized={"schema_version": "1.0.0"},
            report=Mock(changes=[]),
            schema_errors=[],
            import_result={"suite_ids": [1]},
            execution_result=None,
        )
        payload = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [],
            "suites": [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as file:
            json.dump(payload, file)
            candidate_path = file.name

        try:
            call_command(
                "run_ragflow_testhub_scenario",
                "--candidate-json",
                candidate_path,
                "--username",
                self.user.username,
                "--env-var",
                "baseUrl=http://example.test",
            )
        finally:
            Path(candidate_path).unlink(missing_ok=True)

        mock_run_candidate.assert_called_once()
        self.assertEqual(
            mock_run_candidate.call_args.kwargs["environment_variables"],
            {"baseUrl": "http://example.test"},
        )

    @patch("apps.api_testing.management.commands.run_ragflow_testhub_scenario.run_candidate_scenario")
    def test_command_redacts_sensitive_values_in_normalized_output(self, mock_run_candidate):
        normalized = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {
                "name": "ruoyi-dev",
                "scope": "GLOBAL",
                "variables": {
                    "baseUrl": "http://example.test",
                    "adminPassword": "secret-pass",
                    "apiKey": "secret-key",
                },
            },
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "管理员登录",
                            "method": "POST",
                            "url": "{{baseUrl}}/admin-api/system/auth/login",
                            "headers": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer secret-token",
                                    "enabled": True,
                                }
                            ],
                        }
                    ],
                }
            ],
            "suites": [{"name": "主流程", "steps": [{"request_name": "管理员登录"}]}],
        }
        mock_run_candidate.return_value = Mock(
            success=True,
            normalized=normalized,
            report=Mock(changes=[]),
            schema_errors=[],
            import_result={"suite_ids": [1]},
            execution_result=None,
        )
        payload = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [],
            "suites": [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as candidate_file, tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as normalized_file:
            json.dump(payload, candidate_file)
            candidate_path = candidate_file.name
            normalized_output = normalized_file.name

        try:
            call_command(
                "run_ragflow_testhub_scenario",
                "--candidate-json",
                candidate_path,
                "--username",
                self.user.username,
                "--normalized-output",
                normalized_output,
            )
            written = Path(normalized_output).read_text(encoding="utf-8")
        finally:
            Path(candidate_path).unlink(missing_ok=True)
            Path(normalized_output).unlink(missing_ok=True)

        self.assertNotIn("secret-pass", written)
        self.assertNotIn("secret-key", written)
        self.assertNotIn("secret-token", written)
        self.assertIn("[REDACTED]", written)

    @patch("apps.api_testing.management.commands.run_ragflow_testhub_scenario.run_candidate_scenario")
    def test_command_preserves_placeholders_but_redacts_mixed_sensitive_values(self, mock_run_candidate):
        normalized = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {
                "name": "ruoyi-dev",
                "scope": "GLOBAL",
                "variables": {
                    "adminPassword": "{{adminPassword}}",
                    "apiKey": "secret-key{{suffix}}",
                },
            },
            "collections": [
                {
                    "name": "用户管理接口",
                    "requests": [
                        {
                            "name": "管理员登录",
                            "method": "POST",
                            "url": "{{baseUrl}}/admin-api/system/auth/login",
                            "headers": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{token}}",
                                    "enabled": True,
                                }
                            ],
                        }
                    ],
                }
            ],
            "suites": [{"name": "主流程", "steps": [{"request_name": "管理员登录"}]}],
        }
        mock_run_candidate.return_value = Mock(
            success=True,
            normalized=normalized,
            report=Mock(changes=[]),
            schema_errors=[],
            import_result={"suite_ids": [1]},
            execution_result=None,
        )
        payload = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [],
            "suites": [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as candidate_file, tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as normalized_file:
            json.dump(payload, candidate_file)
            candidate_path = candidate_file.name
            normalized_output = normalized_file.name

        try:
            call_command(
                "run_ragflow_testhub_scenario",
                "--candidate-json",
                candidate_path,
                "--username",
                self.user.username,
                "--normalized-output",
                normalized_output,
            )
            written = Path(normalized_output).read_text(encoding="utf-8")
        finally:
            Path(candidate_path).unlink(missing_ok=True)
            Path(normalized_output).unlink(missing_ok=True)

        self.assertIn("{{adminPassword}}", written)
        self.assertIn("Bearer {{token}}", written)
        self.assertIn("{{suffix}}", written)
        self.assertNotIn("secret-key", written)

    @patch("apps.api_testing.management.commands.run_ragflow_testhub_scenario.run_candidate_scenario")
    def test_command_redacts_sensitive_values_inside_report_errors(self, mock_run_candidate):
        mock_run_candidate.return_value = Mock(
            success=False,
            normalized={"schema_version": "1.0.0"},
            report=Mock(changes=[]),
            schema_errors=[],
            import_result={"success": False, "error": "Authorization: Bearer secret-token"},
            execution_result={"success": False, "error": "apiKey=secret-key"},
            error="request failed with password=secret-pass",
        )
        payload = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [],
            "suites": [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as candidate_file, tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as report_file:
            json.dump(payload, candidate_file)
            candidate_path = candidate_file.name
            report_output = report_file.name

        try:
            with self.assertRaises(CommandError):
                call_command(
                    "run_ragflow_testhub_scenario",
                    "--candidate-json",
                    candidate_path,
                    "--username",
                    self.user.username,
                    "--report-output",
                    report_output,
                )
            written = Path(report_output).read_text(encoding="utf-8")
        finally:
            Path(candidate_path).unlink(missing_ok=True)
            Path(report_output).unlink(missing_ok=True)

        self.assertNotIn("secret-token", written)
        self.assertNotIn("secret-key", written)
        self.assertNotIn("secret-pass", written)
        self.assertIn("[REDACTED]", written)

    def test_redact_sensitive_data_supports_name_value_pairs(self):
        from apps.api_testing.management.commands.run_ragflow_testhub_scenario import (
            _redact_sensitive_data,
        )

        redacted = _redact_sensitive_data({"name": "apiKey", "value": "secret-key"})

        self.assertEqual(redacted["name"], "apiKey")
        self.assertEqual(redacted["value"], "[REDACTED]")

    @patch("apps.api_testing.management.commands.run_ragflow_testhub_scenario.run_candidate_scenario")
    def test_command_redacts_sensitive_values_in_failure_output_and_exception(
        self,
        mock_run_candidate,
    ):
        mock_run_candidate.return_value = Mock(
            success=False,
            normalized={"schema_version": "1.0.0"},
            report=Mock(changes=[]),
            schema_errors=[],
            import_result={"success": False, "error": "Authorization: Bearer secret-token"},
            execution_result={"success": False, "error": "apiKey=secret-key"},
            error="request failed with password=secret-pass",
        )
        payload = {
            "schema_version": "1.0.0",
            "project": {"name": "用户管理"},
            "environment": {"name": "ruoyi-dev", "variables": {}},
            "collections": [],
            "suites": [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as candidate_file:
            json.dump(payload, candidate_file)
            candidate_path = candidate_file.name

        stdout = StringIO()
        stderr = StringIO()
        try:
            with self.assertRaises(CommandError) as context:
                call_command(
                    "run_ragflow_testhub_scenario",
                    "--candidate-json",
                    candidate_path,
                    "--username",
                    self.user.username,
                    stdout=stdout,
                    stderr=stderr,
                )
        finally:
            Path(candidate_path).unlink(missing_ok=True)

        output = stdout.getvalue() + stderr.getvalue()
        self.assertNotIn("secret-token", output)
        self.assertNotIn("secret-key", output)
        self.assertNotIn("secret-pass", output)
        self.assertNotIn("secret-pass", str(context.exception))
        self.assertIn("[REDACTED]", output)
        self.assertIn("[REDACTED]", str(context.exception))
