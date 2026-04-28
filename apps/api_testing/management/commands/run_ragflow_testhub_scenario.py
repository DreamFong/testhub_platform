import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.api_testing.services.ragflow_scenario_runner import (
    generate_candidate_from_ragflow,
    run_candidate_scenario,
)

User = get_user_model()


class Command(BaseCommand):
    help = "运行 RAGFlow 生成场景到 TestHub 导入执行的契约校验链路"

    def add_arguments(self, parser):
        source_group = parser.add_mutually_exclusive_group(required=True)
        source_group.add_argument(
            "--candidate-json",
            help="本地 RAGFlow 候选 JSON 文件路径",
        )
        source_group.add_argument(
            "--agent-id",
            help="RAGFlow Agent ID，用于在线生成候选 JSON",
        )
        parser.add_argument(
            "--username",
            required=True,
            help="用于导入和执行 TestHub 场景的本地用户名",
        )
        parser.add_argument(
            "--question",
            default="请生成一个最小可执行的接口自动化测试场景，只输出 TestHub JSON。",
            help="传给 RAGFlow Agent 的用户问题",
        )
        parser.add_argument(
            "--ragflow-api",
            default=os.environ.get("RAGFLOW_API", ""),
            help="RAGFlow API base URL，也可使用 RAGFLOW_API 环境变量",
        )
        parser.add_argument(
            "--ragflow-key-env",
            default="RAGFLOW_KEY",
            help="存放 RAGFlow API Key 的环境变量名，默认 RAGFLOW_KEY",
        )
        parser.add_argument(
            "--ragflow-user-id",
            default="testhub-ragflow-runner",
            help="RAGFlow session 使用的 user_id",
        )
        parser.add_argument(
            "--env-var",
            action="append",
            default=[],
            help="写入 TestHub environment.variables 的键值，例如 baseUrl=http://example.test，可重复传入",
        )
        parser.add_argument(
            "--no-execute",
            action="store_true",
            help="只导入不执行测试套件",
        )
        parser.add_argument(
            "--normalized-output",
            help="保存归一化后 JSON 的路径",
        )
        parser.add_argument(
            "--report-output",
            help="保存归一化和执行报告的路径",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        user = self._get_user(options["username"])
        environment_variables = self._parse_environment_variables(options["env_var"])
        candidate = self._load_candidate(options)

        result = run_candidate_scenario(
            candidate,
            user=user,
            environment_variables=environment_variables,
            execute=not options["no_execute"],
        )
        self._write_outputs(result, options)

        if not result.success:
            self._write_failure(result)
            raise CommandError(result.error or "RAGFlow 场景链路执行失败")

        self._write_success(result)

    def _get_user(self, username: str) -> AbstractBaseUser:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(f"用户不存在: {username}") from exc

    def _parse_environment_variables(self, values: list[str]) -> dict[str, str]:
        variables: dict[str, str] = {}
        for value in values:
            if "=" not in value:
                raise CommandError(f"--env-var 必须是 key=value 格式: {value}")
            key, item_value = value.split("=", 1)
            if not key:
                raise CommandError("--env-var 的 key 不能为空")
            variables[key] = item_value
        return variables

    def _load_candidate(self, options: dict[str, Any]) -> dict[str, Any]:
        candidate_json = options.get("candidate_json")
        if candidate_json:
            return json.loads(Path(candidate_json).read_text(encoding="utf-8"))

        api_base_url = options.get("ragflow_api")
        if not api_base_url:
            raise CommandError("使用 --agent-id 时必须提供 --ragflow-api 或 RAGFLOW_API")
        self._validate_api_base_url(api_base_url)

        api_key_env = options["ragflow_key_env"]
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise CommandError(f"环境变量 {api_key_env} 未设置")

        return generate_candidate_from_ragflow(
            api_base_url=api_base_url,
            api_key=api_key,
            agent_id=options["agent_id"],
            question=options["question"],
            user_id=options["ragflow_user_id"],
        )

    def _validate_api_base_url(self, api_base_url: str) -> None:
        parsed = urlparse(api_base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise CommandError("--ragflow-api 必须是有效的 http(s) URL")

    def _write_outputs(self, result: Any, options: dict[str, Any]) -> None:
        normalized_output = options.get("normalized_output")
        if normalized_output:
            Path(normalized_output).write_text(
                json.dumps(result.normalized, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        report_output = options.get("report_output")
        if report_output:
            report = {
                "success": result.success,
                "changes": result.report.changes,
                "schema_errors": [
                    {"path": error.path, "message": error.message}
                    for error in result.schema_errors
                ],
                "import_result": self._summarize_import_result(result.import_result),
                "execution_result": self._summarize_execution_result(result.execution_result),
                "error": result.error,
            }
            Path(report_output).write_text(
                json.dumps(report, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def _write_failure(self, result: Any) -> None:
        for error in result.schema_errors:
            self.stderr.write(self.style.ERROR(f"schema 错误 {error.path}: {error.message}"))
        if result.import_result:
            self.stderr.write(
                self.style.ERROR(
                    f"导入结果: {self._summarize_import_result(result.import_result)}"
                )
            )
        if result.execution_result:
            self.stderr.write(
                self.style.ERROR(
                    f"执行结果: {self._summarize_execution_result(result.execution_result)}"
                )
            )

    def _write_success(self, result: Any) -> None:
        self.stdout.write(self.style.SUCCESS("RAGFlow 场景链路执行成功"))
        if result.report.changes:
            self.stdout.write(f"归一化修正数: {len(result.report.changes)}")
        if result.import_result:
            self.stdout.write(
                f"导入结果: {self._summarize_import_result(result.import_result)}"
            )
        if result.execution_result:
            self.stdout.write(
                f"执行结果: {self._summarize_execution_result(result.execution_result)}"
            )

    def _summarize_import_result(self, result: dict[str, Any] | None) -> dict[str, Any] | None:
        if not result:
            return None
        keys = ("success", "project_id", "environment_id", "collection_ids", "suite_ids", "error")
        return {key: result[key] for key in keys if key in result}

    def _summarize_execution_result(self, result: dict[str, Any] | None) -> dict[str, Any] | None:
        if not result:
            return None
        return {
            key: result[key]
            for key in (
                "success",
                "execution_id",
                "passed_count",
                "failed_count",
                "total_count",
                "error",
            )
            if key in result
        }
