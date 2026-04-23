"""场景用例导入接口测试

TDD RED 阶段：定义 RAGFlow → TestHub 场景导入接口的预期行为。
"""
import json
from pathlib import Path
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "contracts" / "ragflow-testhub-scenario-schema.json"
EXAMPLE_PATH = Path(__file__).parent.parent.parent.parent / "contracts" / "examples" / "ruoyi-user-mgmt-scenario.json"


def _load_example() -> dict:
    with open(EXAMPLE_PATH) as f:
        return json.load(f)


class TestImportScenarioService(TestCase):
    """测试 import_scenario 服务函数"""

    def setUp(self):
        self.user = User.objects.create_user(username="importer", password="pass")

    def test_import_creates_project(self):
        """导入后应创建对应的 ApiProject"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        result = import_scenario(data, self.user)

        self.assertTrue(result["success"])
        from apps.api_testing.models import ApiProject
        self.assertEqual(ApiProject.objects.count(), 1)
        project = ApiProject.objects.first()
        self.assertEqual(project.name, data["project"]["name"])
        self.assertEqual(project.project_type, "HTTP")

    def test_import_creates_environment(self):
        """导入后应创建对应的环境变量"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        result = import_scenario(data, self.user)

        self.assertTrue(result["success"])
        from apps.api_testing.models import Environment
        env = Environment.objects.first()
        self.assertIsNotNone(env)
        self.assertEqual(env.variables["baseUrl"], "http://81.70.235.9:48080")
        self.assertEqual(env.variables["tenantId"], "1")

    def test_import_creates_collection_with_requests(self):
        """导入后应创建集合及所有请求"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        result = import_scenario(data, self.user)

        self.assertTrue(result["success"])
        from apps.api_testing.models import ApiCollection, ApiRequest
        collection = ApiCollection.objects.first()
        self.assertIsNotNone(collection)
        self.assertEqual(collection.requests.count(), 5)

        # 检查关键请求属性
        login_req = ApiRequest.objects.get(name="管理员登录")
        self.assertEqual(login_req.method, "POST")
        self.assertEqual(len(login_req.variable_extractions), 1)
        self.assertEqual(login_req.variable_extractions[0]["variable"], "token")

    def test_import_creates_suites_with_steps(self):
        """导入后应创建套件及步骤"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        result = import_scenario(data, self.user)

        self.assertTrue(result["success"])
        from apps.api_testing.models import TestSuite, TestSuiteRequest
        suite = TestSuite.objects.first()
        self.assertIsNotNone(suite)
        self.assertEqual(suite.name, "用户管理完整CRUD场景")

        steps = TestSuiteRequest.objects.filter(test_suite=suite).order_by("order")
        self.assertEqual(steps.count(), 5)
        step_names = [s.request.name for s in steps]
        self.assertEqual(step_names, [
            "管理员登录", "创建用户", "查询用户详情", "更新用户", "删除用户"
        ])

    def test_import_request_has_correct_assertions(self):
        """导入的请求应包含正确的断言规则"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        import_scenario(data, self.user)

        from apps.api_testing.models import ApiRequest
        login_req = ApiRequest.objects.get(name="管理员登录")
        assertions = login_req.assertions
        self.assertEqual(len(assertions), 2)
        self.assertEqual(assertions[0]["type"], "status_code")
        self.assertEqual(assertions[0]["expected"], 200)
        self.assertEqual(assertions[1]["type"], "json_path")
        self.assertEqual(assertions[1]["expected"], 0)

    def test_import_request_has_headers_with_variables(self):
        """导入的请求头应保留 {{变量}} 占位符"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        import_scenario(data, self.user)

        from apps.api_testing.models import ApiRequest
        create_req = ApiRequest.objects.get(name="创建用户")
        auth_header = next(
            h for h in create_req.headers if h["key"] == "Authorization"
        )
        self.assertEqual(auth_header["value"], "Bearer {{token}}")

    def test_import_suite_linked_to_environment(self):
        """套件应关联到导入的环境"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        import_scenario(data, self.user)

        from apps.api_testing.models import TestSuite
        suite = TestSuite.objects.first()
        self.assertIsNotNone(suite.environment)
        self.assertEqual(suite.environment.name, "ruoyi-dev")

    def test_import_returns_created_ids(self):
        """返回结果应包含所有创建资源的 ID"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        result = import_scenario(data, self.user)

        self.assertTrue(result["success"])
        self.assertIn("project_id", result)
        self.assertIn("environment_id", result)
        self.assertIn("collection_ids", result)
        self.assertIn("suite_ids", result)
        self.assertEqual(len(result["collection_ids"]), 1)
        self.assertEqual(len(result["suite_ids"]), 1)


class TestImportValidation(TestCase):
    """测试导入校验逻辑"""

    def setUp(self):
        self.user = User.objects.create_user(username="validator", password="pass")

    def test_reject_invalid_schema_version(self):
        """拒绝不支持的 schema 版本"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        data["schema_version"] = "99.0.0"
        result = import_scenario(data, self.user)

        self.assertFalse(result["success"])
        self.assertIn("schema_version", result["error"])

    def test_reject_duplicate_request_names_in_collection(self):
        """拒绝集合内有重复请求名称"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        data["collections"][0]["requests"].append(
            data["collections"][0]["requests"][0].copy()
        )
        result = import_scenario(data, self.user)

        self.assertFalse(result["success"])
        self.assertIn("重复", result["error"])

    def test_reject_step_referencing_nonexistent_request(self):
        """拒绝引用不存在请求的步骤"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        data["suites"][0]["steps"].append({"request_name": "不存在的请求"})
        result = import_scenario(data, self.user)

        self.assertFalse(result["success"])
        self.assertIn("不存在", result["error"])

    def test_reject_duplicate_request_in_same_suite(self):
        """拒绝同一套件中重复引用同一请求（模型 unique_together 约束）"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = _load_example()
        data["suites"][0]["steps"].append(
            {"request_name": "管理员登录"}
        )
        result = import_scenario(data, self.user)

        self.assertFalse(result["success"])
        self.assertIn("重复引用", result["error"])

    def test_reject_missing_required_fields(self):
        """拒绝缺少必填字段"""
        from apps.api_testing.services.scenario_import import import_scenario

        data = {"schema_version": "1.0.0"}
        result = import_scenario(data, self.user)

        self.assertFalse(result["success"])


class TestImportAPIEndpoint(TestCase):
    """测试导入 REST API 端点"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="api_user", password="pass")
        self.client.force_authenticate(user=self.user)

    def test_post_import_returns_201(self):
        """POST 导入接口应返回 201"""
        data = _load_example()
        response = self.client.post(
            "/api/api-testing/import/scenario/",
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])

    def test_post_invalid_data_returns_400(self):
        """POST 无效数据应返回 400"""
        response = self.client.post(
            "/api/api-testing/import/scenario/",
            data={"schema_version": "99.0.0"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_returns_401(self):
        """未认证请求应返回 401"""
        self.client.force_authenticate(user=None)
        data = _load_example()
        response = self.client.post(
            "/api/api-testing/import/scenario/",
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_import_idempotency_creates_separate_projects(self):
        """重复导入应创建独立的项目（不做去重）"""
        data = _load_example()
        resp1 = self.client.post(
            "/api/api-testing/import/scenario/",
            data=data,
            format="json",
        )
        resp2 = self.client.post(
            "/api/api-testing/import/scenario/",
            data=data,
            format="json",
        )
        self.assertEqual(resp1.status_code, 201)
        self.assertEqual(resp2.status_code, 201)
        self.assertNotEqual(resp1.data["project_id"], resp2.data["project_id"])
