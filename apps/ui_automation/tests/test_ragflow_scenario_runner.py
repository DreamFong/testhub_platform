import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from apps.ui_automation.models import (
    Element,
    LocatorStrategy,
    TestCase as UiTestCase,
    TestSuite,
    TestSuiteTestCase,
    UiProject,
)

User = get_user_model()


def _build_candidate(project_name: str = "UI 项目") -> dict:
    return {
        "schema_version": "1.0.0",
        "scenario_title": "登录冒烟",
        "project": {"name": project_name},
        "test_cases": [
            {
                "name": "管理员登录成功",
                "priority": "high",
                "steps": [
                    {
                        "page": "登录页",
                        "element_name": "用户名输入框",
                        "action": "input",
                        "input": "admin",
                    },
                    {
                        "page": "登录页",
                        "element_name": "密码输入框",
                        "action": "input_text",
                        "input": "secret",
                    },
                    {
                        "page": "登录页",
                        "element_name": "登录按钮",
                        "action": "click",
                    },
                ],
                "assertions": [
                    {
                        "page_ref": "首页",
                        "element_ref": "欢迎标语",
                        "type": "text_contains",
                        "expected": "欢迎",
                    }
                ],
            }
        ],
        "metadata": {"source": "ragflow", "extra": "drop-me"},
    }


class TestUiRagflowScenarioNormalizer(TestCase):
    def test_normalize_candidate_adds_default_suite_and_step_aliases(self):
        from apps.ui_automation.services.ragflow_scenario_runner import normalize_candidate_scenario

        normalized, report = normalize_candidate_scenario(_build_candidate())

        self.assertEqual(normalized["test_cases"][0]["steps"][0]["action"], "fill")
        self.assertEqual(normalized["test_cases"][0]["steps"][0]["page_ref"], "登录页")
        self.assertEqual(normalized["test_cases"][0]["steps"][0]["element_ref"], "用户名输入框")
        self.assertEqual(normalized["test_cases"][0]["steps"][0]["input_value"], "admin")
        self.assertEqual(normalized["test_cases"][0]["steps"][3]["action"], "assert")
        self.assertEqual(normalized["test_cases"][0]["steps"][3]["assert_type"], "textContains")
        self.assertEqual(normalized["test_cases"][0]["steps"][3]["assert_value"], "欢迎")
        self.assertEqual(normalized["suites"][0]["name"], "登录冒烟")
        self.assertEqual(normalized["suites"][0]["test_case_names"], ["管理员登录成功"])
        self.assertEqual(normalized["metadata"], {"source": "ragflow"})
        self.assertTrue(report.changes)

    def test_validate_scenario_reports_contract_errors(self):
        from apps.ui_automation.services.ragflow_scenario_runner import validate_scenario

        errors = validate_scenario({"schema_version": "1.0.0"})

        self.assertGreater(len(errors), 0)
        self.assertIn("project", " ".join(error.message for error in errors))

    def test_validate_scenario_rejects_invalid_project_base_url_format(self):
        from apps.ui_automation.services.ragflow_scenario_runner import (
            normalize_candidate_scenario,
            validate_scenario,
        )

        candidate = _build_candidate()
        candidate["project"]["base_url"] = "http://[invalid"
        normalized, _ = normalize_candidate_scenario(candidate)
        errors = validate_scenario(normalized)

        self.assertGreater(len(errors), 0)
        self.assertIn("project/base_url", " ".join(error.path for error in errors))


class TestUiScenarioImport(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ui_importer", password="pass")
        self.project = UiProject.objects.create(
            name="UI 项目",
            description="用于 UI 正线导入测试",
            status="IN_PROGRESS",
            base_url="http://example.test",
            owner=self.user,
        )
        self.css = LocatorStrategy.objects.create(name="css", description="CSS")
        Element.objects.create(
            project=self.project,
            name="用户名输入框",
            element_type="INPUT",
            locator_strategy=self.css,
            locator_value="#username",
            page="登录页",
            created_by=self.user,
        )
        Element.objects.create(
            project=self.project,
            name="密码输入框",
            element_type="INPUT",
            locator_strategy=self.css,
            locator_value="#password",
            page="登录页",
            created_by=self.user,
        )
        Element.objects.create(
            project=self.project,
            name="登录按钮",
            element_type="BUTTON",
            locator_strategy=self.css,
            locator_value="#submit",
            page="登录页",
            created_by=self.user,
        )
        Element.objects.create(
            project=self.project,
            name="欢迎标语",
            element_type="TEXT",
            locator_strategy=self.css,
            locator_value="#welcome",
            page="首页",
            created_by=self.user,
        )

    def test_import_scenario_binds_elements_and_creates_suite(self):
        from apps.ui_automation.services.ragflow_scenario_runner import normalize_candidate_scenario
        from apps.ui_automation.services.scenario_import import import_scenario

        normalized, _ = normalize_candidate_scenario(_build_candidate())
        result = import_scenario(normalized, self.user)

        self.assertTrue(result["success"])
        self.assertEqual(UiTestCase.objects.count(), 1)
        test_case = UiTestCase.objects.first()
        self.assertEqual(test_case.status, "ready")
        self.assertEqual(test_case.priority, "high")

        steps = list(test_case.steps.order_by("step_number"))
        self.assertEqual([step.action_type for step in steps], ["fill", "fill", "click", "assert"])
        self.assertEqual(steps[0].element.name, "用户名输入框")
        self.assertEqual(steps[3].assert_type, "textContains")
        self.assertEqual(steps[3].assert_value, "欢迎")

        suite = TestSuite.objects.first()
        self.assertIsNotNone(suite)
        self.assertEqual(suite.name, "登录冒烟")
        relation = TestSuiteTestCase.objects.get(test_suite=suite, test_case=test_case)
        self.assertEqual(relation.order, 0)

    def test_import_scenario_rejects_unknown_element_binding(self):
        from apps.ui_automation.services.ragflow_scenario_runner import normalize_candidate_scenario
        from apps.ui_automation.services.scenario_import import import_scenario

        candidate = _build_candidate()
        candidate["test_cases"][0]["steps"][0]["element_name"] = "不存在的元素"
        normalized, _ = normalize_candidate_scenario(candidate)
        result = import_scenario(normalized, self.user)

        self.assertFalse(result["success"])
        self.assertIn("元素", result["error"])

    def test_import_scenario_rolls_back_on_binding_failure(self):
        from apps.ui_automation.services.ragflow_scenario_runner import normalize_candidate_scenario
        from apps.ui_automation.services.scenario_import import import_scenario

        candidate = _build_candidate()
        candidate["test_cases"][0]["steps"].append(
            {
                "page": "登录页",
                "element_name": "不存在的元素",
                "action": "click",
            }
        )
        normalized, _ = normalize_candidate_scenario(candidate)
        result = import_scenario(normalized, self.user)

        self.assertFalse(result["success"])
        self.assertEqual(UiTestCase.objects.count(), 0)
        self.assertEqual(TestSuite.objects.count(), 0)

    def test_import_scenario_rejects_unsupported_action(self):
        from apps.ui_automation.services.ragflow_scenario_runner import normalize_candidate_scenario
        from apps.ui_automation.services.scenario_import import import_scenario

        candidate = _build_candidate()
        candidate["test_cases"][0]["steps"][0]["action"] = "unsupportedAction"
        normalized, _ = normalize_candidate_scenario(candidate)
        result = import_scenario(normalized, self.user)

        self.assertFalse(result["success"])
        self.assertIn("不支持的 action", result["error"])


class TestUiRagflowScenarioRunner(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ui_runner", password="pass")
        self.project = UiProject.objects.create(
            name="UI 项目",
            description="用于 UI 正线执行测试",
            status="IN_PROGRESS",
            base_url="http://example.test",
            owner=self.user,
        )
        self.css = LocatorStrategy.objects.create(name="css", description="CSS")
        for name, locator, page, element_type in (
            ("用户名输入框", "#username", "登录页", "INPUT"),
            ("密码输入框", "#password", "登录页", "INPUT"),
            ("登录按钮", "#submit", "登录页", "BUTTON"),
            ("欢迎标语", "#welcome", "首页", "TEXT"),
        ):
            Element.objects.create(
                project=self.project,
                name=name,
                element_type=element_type,
                locator_strategy=self.css,
                locator_value=locator,
                page=page,
                created_by=self.user,
            )

    @patch("apps.ui_automation.services.ragflow_scenario_runner._execute_first_imported_suite")
    def test_run_candidate_imports_then_executes_first_suite(self, mock_execute_suite):
        from apps.ui_automation.services.ragflow_scenario_runner import run_candidate_scenario

        mock_execute_suite.return_value = {
            "success": True,
            "execution_id": 8,
            "passed_count": 1,
            "failed_count": 0,
            "total_count": 1,
            "error": "",
        }

        result = run_candidate_scenario(
            _build_candidate(),
            user=self.user,
            execute=True,
            engine="playwright",
            browser="chrome",
            headless=True,
        )

        self.assertTrue(result.success)
        self.assertIsNotNone(result.import_result)
        self.assertEqual(result.import_result["project_id"], self.project.id)
        self.assertEqual(result.execution_result["execution_id"], 8)
        mock_execute_suite.assert_called_once()

    @patch("apps.ui_automation.services.ragflow_scenario_runner._execute_first_imported_suite")
    def test_run_candidate_cleans_up_imported_data_when_execution_fails(self, mock_execute_suite):
        from apps.ui_automation.services.ragflow_scenario_runner import run_candidate_scenario

        mock_execute_suite.return_value = {
            "success": False,
            "error": "执行失败",
        }

        result = run_candidate_scenario(
            _build_candidate(),
            user=self.user,
            execute=True,
            engine="playwright",
            browser="chrome",
            headless=True,
        )

        self.assertFalse(result.success)
        self.assertTrue(result.execution_result["cleanup_performed"])
        self.assertEqual(UiTestCase.objects.count(), 0)
        self.assertEqual(TestSuite.objects.count(), 0)


class TestRunUiRagflowScenarioCommand(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ui_command_user", password="pass")

    @patch("apps.ui_automation.management.commands.run_ragflow_testhub_ui_scenario.run_candidate_scenario")
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
            "project": {"name": "UI 项目"},
            "test_cases": [
                {
                    "name": "管理员登录成功",
                    "steps": [{"action": "wait", "wait_time": 1000}],
                }
            ],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as file:
            json.dump(payload, file, ensure_ascii=False)
            candidate_path = file.name

        try:
            call_command(
                "run_ragflow_testhub_ui_scenario",
                "--candidate-json",
                candidate_path,
                "--username",
                self.user.username,
                "--execute",
                "--engine",
                "playwright",
                "--browser",
                "chrome",
                "--headless",
            )
        finally:
            Path(candidate_path).unlink(missing_ok=True)

        mock_run_candidate.assert_called_once()
        self.assertEqual(mock_run_candidate.call_args.kwargs["execute"], True)
        self.assertEqual(mock_run_candidate.call_args.kwargs["engine"], "playwright")
        self.assertEqual(mock_run_candidate.call_args.kwargs["browser"], "chrome")
        self.assertEqual(mock_run_candidate.call_args.kwargs["headless"], True)

    def test_command_rejects_invalid_json_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as file:
            file.write("{invalid json")
            candidate_path = file.name

        try:
            with self.assertRaises(CommandError):
                call_command(
                    "run_ragflow_testhub_ui_scenario",
                    "--candidate-json",
                    candidate_path,
                    "--username",
                    self.user.username,
                )
        finally:
            Path(candidate_path).unlink(missing_ok=True)

    def test_command_rejects_non_object_json_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as file:
            json.dump([1, 2, 3], file)
            candidate_path = file.name

        try:
            with self.assertRaises(CommandError):
                call_command(
                    "run_ragflow_testhub_ui_scenario",
                    "--candidate-json",
                    candidate_path,
                    "--username",
                    self.user.username,
                )
        finally:
            Path(candidate_path).unlink(missing_ok=True)
