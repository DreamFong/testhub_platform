import json
from argparse import ArgumentParser
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.management.base import BaseCommand, CommandError

from apps.ui_automation.services.ragflow_scenario_runner import (
    ScenarioRunResult,
    run_candidate_scenario,
)

User = get_user_model()


class Command(BaseCommand):
    help = "运行 RAGFlow 生成 UI 场景到 TestHub UI 自动化导入执行的契约校验链路"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--candidate-json", required=True, help="本地 UI candidate JSON 文件路径")
        parser.add_argument("--username", required=True, help="用于导入和执行 UI 场景的本地用户名")
        parser.add_argument("--execute", action="store_true", help="导入后执行第一个测试套件")
        parser.add_argument(
            "--engine",
            choices=("playwright", "selenium"),
            default="playwright",
            help="执行引擎，默认 playwright",
        )
        parser.add_argument(
            "--browser",
            choices=("chrome", "firefox", "safari"),
            default="chrome",
            help="浏览器类型，默认 chrome",
        )
        parser.add_argument("--headless", action="store_true", help="是否使用无头模式执行")
        parser.add_argument("--normalized-output", help="保存归一化后 JSON 的路径")
        parser.add_argument("--report-output", help="保存归一化和执行报告的路径")

    def handle(self, *args: Any, **options: Any) -> None:
        user = self._get_user(options["username"])
        candidate = self._load_candidate(options["candidate_json"])

        try:
            result = run_candidate_scenario(
                candidate,
                user=user,
                execute=options["execute"],
                engine=options["engine"],
                browser=options["browser"],
                headless=options["headless"],
            )
        except Exception as exc:
            raise CommandError(f"执行 UI 场景链路时发生未预期错误: {exc}") from exc

        output_error: CommandError | None = None
        try:
            self._write_outputs(result, options)
        except CommandError as exc:
            output_error = exc

        if not result.success:
            self._write_failure(result)
            if output_error:
                self.stderr.write(self.style.WARNING(str(output_error)))
            raise CommandError(result.error or "RAGFlow UI 场景链路执行失败")

        self._write_success(result)
        if output_error:
            raise output_error

    def _get_user(self, username: str) -> AbstractBaseUser:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(f"用户不存在: {username}") from exc

    def _load_candidate(self, candidate_json: str) -> dict[str, Any]:
        try:
            payload = json.loads(Path(candidate_json).read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise CommandError(f"candidate 文件不存在: {candidate_json}") from exc
        except JSONDecodeError as exc:
            raise CommandError(f"candidate JSON 解析失败: {exc}") from exc
        except OSError as exc:
            raise CommandError(f"读取 candidate 文件失败: {exc}") from exc

        if not isinstance(payload, dict):
            raise CommandError("candidate 顶层必须是 JSON 对象")
        return payload

    def _write_outputs(self, result: ScenarioRunResult, options: dict[str, Any]) -> None:
        normalized_output = options.get("normalized_output")
        if normalized_output:
            try:
                Path(normalized_output).write_text(
                    json.dumps(result.normalized, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            except OSError as exc:
                raise CommandError(f"写入 normalized 输出失败: {exc}") from exc

        report_output = options.get("report_output")
        if report_output:
            report = {
                "success": result.success,
                "changes": result.report.changes,
                "schema_errors": [
                    {"path": error.path, "message": error.message}
                    for error in result.schema_errors
                ],
                "import_result": result.import_result,
                "execution_result": result.execution_result,
                "error": result.error,
            }
            try:
                Path(report_output).write_text(
                    json.dumps(report, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            except OSError as exc:
                raise CommandError(f"写入 report 输出失败: {exc}") from exc

    def _write_failure(self, result: ScenarioRunResult) -> None:
        for error in result.schema_errors:
            self.stderr.write(self.style.ERROR(f"schema 错误 {error.path}: {error.message}"))
        if result.import_result:
            self.stderr.write(self.style.ERROR(f"导入结果: {result.import_result}"))
        if result.execution_result:
            self.stderr.write(self.style.ERROR(f"执行结果: {result.execution_result}"))

    def _write_success(self, result: ScenarioRunResult) -> None:
        self.stdout.write(self.style.SUCCESS("RAGFlow UI 场景链路执行成功"))
        if result.report.changes:
            self.stdout.write(f"归一化修正数: {len(result.report.changes)}")
        if result.import_result:
            self.stdout.write(f"导入结果: {result.import_result}")
        if result.execution_result:
            self.stdout.write(f"执行结果: {result.execution_result}")
