import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.api_testing.models import ApiProject, Environment, TestSuite

User = get_user_model()


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
        self.assertEqual(
            normalized["collections"][0]["requests"][1]["params"],
            {"id": "{{newUserId}}"},
        )
        self.assertEqual(normalized["metadata"], {"source": "ragflow"})
        self.assertTrue(report.changes)

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
