"""变量提取功能测试

TDD RED 阶段：定义变量提取和步骤间变量传递的预期行为。
所有测试在实现完成前应当失败。
"""
import json
from unittest.mock import MagicMock, patch
from django.test import TestCase

from apps.api_testing.utils import extract_variables_from_response


class TestExtractVariablesFromResponse(TestCase):
    """测试 extract_variables_from_response 函数"""

    def _make_response(
        self,
        body: dict | None = None,
        headers: dict | None = None,
        status_code: int = 200,
    ) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        response.headers = headers or {}
        response.text = json.dumps(body) if body else ""
        response.json.return_value = body
        return response

    # --- JSONPath 提取 ---

    def test_extract_string_from_json_body(self):
        """从响应体通过 JSONPath 提取字符串值"""
        response = self._make_response(
            body={"code": 0, "data": {"accessToken": "abc123"}}
        )
        extractions = [
            {"variable": "token", "source": "body", "json_path": "$.data.accessToken"}
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertEqual(result["token"], "abc123")

    def test_extract_integer_from_json_body(self):
        """从响应体提取整数值（如 userId）"""
        response = self._make_response(body={"code": 0, "data": 42})
        extractions = [
            {"variable": "userId", "source": "body", "json_path": "$.data"}
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertEqual(result["userId"], 42)

    def test_extract_nested_jsonpath(self):
        """提取深层嵌套的 JSONPath"""
        response = self._make_response(
            body={"data": {"user": {"profile": {"id": 99}}}}
        )
        extractions = [
            {
                "variable": "profileId",
                "source": "body",
                "json_path": "$.data.user.profile.id",
            }
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertEqual(result["profileId"], 99)

    # --- 响应头提取 ---

    def test_extract_from_response_header(self):
        """从响应头提取值"""
        response = self._make_response(
            body={},
            headers={"X-Request-Id": "req-001", "Content-Type": "application/json"},
        )
        extractions = [
            {"variable": "requestId", "source": "header", "header_name": "X-Request-Id"}
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertEqual(result["requestId"], "req-001")

    # --- 状态码提取 ---

    def test_extract_status_code(self):
        """提取 HTTP 状态码"""
        response = self._make_response(body={}, status_code=201)
        extractions = [
            {"variable": "statusCode", "source": "status_code"}
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertEqual(result["statusCode"], 201)

    # --- 边界情况 ---

    def test_extract_missing_jsonpath_returns_none(self):
        """JSONPath 匹配不到时，变量值为 None"""
        response = self._make_response(body={"code": 0, "data": None})
        extractions = [
            {"variable": "missing", "source": "body", "json_path": "$.data.token"}
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertIsNone(result["missing"])

    def test_extract_missing_header_returns_none(self):
        """响应头不存在时，变量值为 None"""
        response = self._make_response(body={}, headers={})
        extractions = [
            {"variable": "notFound", "source": "header", "header_name": "X-Missing"}
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertIsNone(result["notFound"])

    def test_extract_multiple_variables(self):
        """一次提取多个变量"""
        response = self._make_response(
            body={"code": 0, "data": {"accessToken": "tok", "userId": 5}},
            headers={"X-Trace-Id": "trace-abc"},
        )
        extractions = [
            {"variable": "token", "source": "body", "json_path": "$.data.accessToken"},
            {"variable": "uid", "source": "body", "json_path": "$.data.userId"},
            {"variable": "traceId", "source": "header", "header_name": "X-Trace-Id"},
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertEqual(result["token"], "tok")
        self.assertEqual(result["uid"], 5)
        self.assertEqual(result["traceId"], "trace-abc")

    def test_extract_empty_extractions_returns_empty_dict(self):
        """空的提取规则返回空字典"""
        response = self._make_response(body={"code": 0})

        result = extract_variables_from_response(response, [])

        self.assertEqual(result, {})

    def test_extract_none_extractions_returns_empty_dict(self):
        """None 提取规则返回空字典"""
        response = self._make_response(body={"code": 0})

        result = extract_variables_from_response(response, None)

        self.assertEqual(result, {})

    def test_extract_non_json_response(self):
        """非 JSON 响应体时，body 提取返回 None"""
        response = MagicMock()
        response.status_code = 200
        response.headers = {"Content-Type": "text/html"}
        response.text = "<html>Not JSON</html>"
        response.json.side_effect = ValueError("No JSON")

        extractions = [
            {"variable": "token", "source": "body", "json_path": "$.data.token"}
        ]

        result = extract_variables_from_response(response, extractions)

        self.assertIsNone(result["token"])


class TestVariablePassingInSuite(TestCase):
    """测试测试套件执行中的步骤间变量传递"""

    def _make_response(
        self,
        body: dict | None = None,
        headers: dict | None = None,
        status_code: int = 200,
        response_time: float = 100.0,
    ) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        response.headers = headers or {}
        response.text = json.dumps(body) if body else ""
        response.json.return_value = body
        response_time_obj = MagicMock()
        response_time_obj.total_seconds.return_value = response_time / 1000.0
        return response

    @patch("apps.api_testing.utils.http_client.request")
    def test_step1_extracts_variable_step2_uses_it_in_url(self, mock_request):
        """步骤1提取变量，步骤2在URL中使用"""
        from apps.api_testing.models import (
            ApiRequest,
            ApiCollection,
            ApiProject,
            TestSuite,
            TestSuiteRequest,
        )
        from apps.api_testing.utils import execute_test_suite
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user = User.objects.first()
        if not user:
            user = User.objects.create_user(username="testrunner", password="pass")

        # 创建项目和集合
        project = ApiProject.objects.create(
            name="测试项目", project_type="HTTP", status="IN_PROGRESS", owner=user
        )
        collection = ApiCollection.objects.create(name="测试集合", project=project)

        # 步骤1: 登录 → 提取 accessToken
        step1 = ApiRequest.objects.create(
            name="登录",
            collection=collection,
            method="POST",
            url="http://example.com/login",
            headers=[{"key": "Content-Type", "value": "application/json", "enabled": True}],
            body={"type": "json", "data": {"username": "admin", "password": "123"}},
            variable_extractions=[
                {"variable": "token", "source": "body", "json_path": "$.data.accessToken"}
            ],
            created_by=user,
        )

        # 步骤2: 获取用户 → URL 中使用 {{token}}
        step2 = ApiRequest.objects.create(
            name="获取用户",
            collection=collection,
            method="GET",
            url="http://example.com/users/1",
            headers=[
                {"key": "Content-Type", "value": "application/json", "enabled": True},
                {"key": "Authorization", "value": "Bearer {{token}}", "enabled": True},
            ],
            assertions=[],
            created_by=user,
        )

        suite = TestSuite.objects.create(
            name="变量传递测试", project=project, created_by=user
        )
        TestSuiteRequest.objects.create(
            test_suite=suite, request=step1, order=1
        )
        TestSuiteRequest.objects.create(
            test_suite=suite, request=step2, order=2
        )

        # Mock 响应
        login_response = self._make_response(
            body={"code": 0, "data": {"accessToken": "extracted_token_999"}}
        )
        user_response = self._make_response(body={"code": 0, "data": {"id": 1, "name": "test"}})

        mock_request.side_effect = [login_response, user_response]

        result = execute_test_suite(suite, None, user)

        self.assertTrue(result["success"])
        # 验证步骤2的请求头中 token 被正确替换
        second_call_headers = mock_request.call_args_list[1][1]["headers"]
        self.assertEqual(second_call_headers["Authorization"], "Bearer extracted_token_999")

    @patch("apps.api_testing.utils.http_client.request")
    def test_step1_extracts_variable_step2_uses_it_in_body(self, mock_request):
        """步骤1提取变量，步骤2在请求体中使用"""
        from apps.api_testing.models import (
            ApiRequest,
            ApiCollection,
            ApiProject,
            TestSuite,
            TestSuiteRequest,
        )
        from apps.api_testing.utils import execute_test_suite
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.first() or User.objects.create_user(
            username="testrunner2", password="pass"
        )

        project = ApiProject.objects.create(
            name="Body测试", project_type="HTTP", status="IN_PROGRESS", owner=user
        )
        collection = ApiCollection.objects.create(name="集合", project=project)

        step1 = ApiRequest.objects.create(
            name="创建用户",
            collection=collection,
            method="POST",
            url="http://example.com/users",
            headers=[{"key": "Content-Type", "value": "application/json", "enabled": True}],
            body={"type": "json", "data": {"name": "test"}},
            variable_extractions=[
                {"variable": "newUserId", "source": "body", "json_path": "$.data"}
            ],
            created_by=user,
        )

        step2 = ApiRequest.objects.create(
            name="修改用户",
            collection=collection,
            method="PUT",
            url="http://example.com/users",
            headers=[{"key": "Content-Type", "value": "application/json", "enabled": True}],
            body={"type": "json", "data": {"id": "{{newUserId}}", "name": "updated"}},
            created_by=user,
        )

        suite = TestSuite.objects.create(
            name="Body变量传递", project=project, created_by=user
        )
        TestSuiteRequest.objects.create(test_suite=suite, request=step1, order=1)
        TestSuiteRequest.objects.create(test_suite=suite, request=step2, order=2)

        create_response = self._make_response(body={"code": 0, "data": 42})
        update_response = self._make_response(body={"code": 0, "data": True})

        mock_request.side_effect = [create_response, update_response]

        result = execute_test_suite(suite, None, user)

        self.assertTrue(result["success"])
        # 验证步骤2的请求体中 userId 被正确替换
        second_call_body = mock_request.call_args_list[1][1]["json"]
        self.assertEqual(second_call_body["id"], "42")

    @patch("apps.api_testing.utils.http_client.request")
    def test_three_step_chain(self, mock_request):
        """三步链式传递：登录→创建→查询，变量依次传递"""
        from apps.api_testing.models import (
            ApiRequest,
            ApiCollection,
            ApiProject,
            TestSuite,
            TestSuiteRequest,
        )
        from apps.api_testing.utils import execute_test_suite
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.first() or User.objects.create_user(
            username="testrunner3", password="pass"
        )

        project = ApiProject.objects.create(
            name="三步链", project_type="HTTP", status="IN_PROGRESS", owner=user
        )
        collection = ApiCollection.objects.create(name="集合", project=project)

        step1 = ApiRequest.objects.create(
            name="登录",
            collection=collection,
            method="POST",
            url="http://example.com/login",
            headers=[{"key": "Content-Type", "value": "application/json", "enabled": True}],
            body={"type": "json", "data": {"username": "admin", "password": "123"}},
            variable_extractions=[
                {"variable": "authToken", "source": "body", "json_path": "$.data.token"}
            ],
            created_by=user,
        )

        step2 = ApiRequest.objects.create(
            name="创建",
            collection=collection,
            method="POST",
            url="http://example.com/items",
            headers=[
                {"key": "Content-Type", "value": "application/json", "enabled": True},
                {"key": "Authorization", "value": "Bearer {{authToken}}", "enabled": True},
            ],
            body={"type": "json", "data": {"name": "item1"}},
            variable_extractions=[
                {"variable": "itemId", "source": "body", "json_path": "$.data.id"}
            ],
            created_by=user,
        )

        step3 = ApiRequest.objects.create(
            name="查询",
            collection=collection,
            method="GET",
            url="http://example.com/items/{{itemId}}",
            headers=[
                {"key": "Authorization", "value": "Bearer {{authToken}}", "enabled": True},
            ],
            created_by=user,
        )

        suite = TestSuite.objects.create(
            name="三步链测试", project=project, created_by=user
        )
        TestSuiteRequest.objects.create(test_suite=suite, request=step1, order=1)
        TestSuiteRequest.objects.create(test_suite=suite, request=step2, order=2)
        TestSuiteRequest.objects.create(test_suite=suite, request=step3, order=3)

        resp1 = self._make_response(body={"data": {"token": "my_token"}})
        resp2 = self._make_response(body={"data": {"id": 77}})
        resp3 = self._make_response(body={"data": {"id": 77, "name": "item1"}})

        mock_request.side_effect = [resp1, resp2, resp3]

        result = execute_test_suite(suite, None, user)

        self.assertTrue(result["success"])
        # 步骤3的 URL 应包含提取的 itemId
        third_call_url = mock_request.call_args_list[2][1]["url"]
        self.assertIn("77", third_call_url)
        # 步骤3的 Auth 头应包含步骤1提取的 token
        third_call_headers = mock_request.call_args_list[2][1]["headers"]
        self.assertEqual(third_call_headers["Authorization"], "Bearer my_token")
