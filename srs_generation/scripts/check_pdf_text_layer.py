#!/usr/bin/env python3
"""Check text-layer and readability quality for a generated SRS PDF."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception:  # pragma: no cover
        PdfReader = None  # type: ignore


DEFAULT_REQUIRED_TITLES = [
    "文档概述",
    "模块范围",
    "功能需求",
    "字段与输入规则",
    "业务规则",
    "异常处理规则",
    "验收标准",
]

DEFAULT_ABNORMAL_SPACING_PATTERNS = [
    r"R\s+u\s+o\s+Y\s+i\s*-\s*V\s+u\s+e\s*-\s*P\s+r\s+o",
    r"C\s+o\s+n\s+t\s+r\s+o\s+l\s+l\s+e\s+r",
    r"S\s+e\s+r\s+v\s+i\s+c\s+e",
    r"M\s+a\s+p\s+p\s+e\s+r",
    r"F\s+R\s*-\s*U\s+S\s+E\s+R\s*-\s*\d\s+\d\s+\d",
    r"s\s+y\s+s\s+t\s+e\s+m\s*:\s*u\s+s\s+e\s+r\s*:\s*[a-z]",
]


@dataclass(frozen=True)
class CheckResult:
    result: str
    gate: str
    reason: str


def extract_text_with_pypdf(pdf_path: Path) -> tuple[str, int]:
    if PdfReader is None:
        raise RuntimeError("pypdf or PyPDF2 is not available")
    reader = PdfReader(str(pdf_path))
    chunks: list[str] = []
    for page in reader.pages:
        try:
            chunks.append(page.extract_text() or "")
        except Exception:
            chunks.append("")
    return "\n".join(chunks), len(reader.pages)


def decode_hex_pdf_text(hex_text: str) -> str:
    try:
        raw = bytes.fromhex(hex_text)
    except ValueError:
        return ""
    for encoding in ("utf-16-be", "utf-8", "latin-1"):
        try:
            return raw.decode(encoding)
        except Exception:
            continue
    return ""


def extract_text_builtin(pdf_path: Path) -> tuple[str, int]:
    data = pdf_path.read_bytes()
    text = data.decode("latin-1", errors="ignore")
    chunks: list[str] = []

    for match in re.finditer(r"<([0-9A-Fa-f]{4,})>\s*Tj", text):
        decoded = decode_hex_pdf_text(match.group(1))
        if decoded:
            chunks.append(decoded)

    for match in re.finditer(r"\((.*?)\)\s*Tj", text, re.DOTALL):
        literal = match.group(1).replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\")
        if literal:
            chunks.append(literal)

    page_count = max(1, len(re.findall(r"/Type\s*/Page\b", text)))
    return "\n".join(chunks), page_count


def extract_text(pdf_path: Path) -> tuple[str, int, str]:
    try:
        text, page_count = extract_text_with_pypdf(pdf_path)
        if text.strip():
            return text, page_count, "pypdf"
    except Exception:
        pass
    text, page_count = extract_text_builtin(pdf_path)
    return text, page_count, "builtin"


def has_cjk(text: str) -> bool:
    return bool(re.search(r"[一-鿿]", text))


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def count_title_occurrences(text: str, title: str) -> int:
    if not title:
        return 0
    title_pattern = re.compile(
        rf"^\s*(?:#+\s*)?(?:\d+(?:\.\d+)*[.、]?\s*)?{re.escape(title)}\s*$",
        re.MULTILINE,
    )
    return len(title_pattern.findall(text))


def find_abnormal_spacing(text: str) -> list[str]:
    findings: list[str] = []
    normalized = normalize_spaces(text)
    for pattern in DEFAULT_ABNORMAL_SPACING_PATTERNS:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if match:
            findings.append(match.group(0))
    return sorted(set(findings))


def classify_text_layer_gate(
    error: str | None,
    text_extractable: bool,
    cjk_ok: bool,
    missing_titles: list[str],
    fr_matches: list[str],
    missing_terms: list[str],
    abnormal_spacing: list[str],
) -> CheckResult:
    if error or not text_extractable or not cjk_ok:
        return CheckResult(
            "fail",
            "fail",
            error or "PDF 文本层不可提取、文本过短或中文文本无法识别。",
        )
    if abnormal_spacing:
        return CheckResult(
            "fail",
            "fail",
            "提取文本中存在英文异常拆字，可能影响知识库检索。",
        )
    if missing_titles:
        return CheckResult(
            "conditional pass",
            "conditional pass",
            "PDF 文本层可提取，但部分必需标题未检出。",
        )
    if not fr_matches:
        return CheckResult(
            "conditional pass",
            "conditional pass",
            "PDF 文本层可提取，但未检出 FR 编号。",
        )
    if missing_terms:
        return CheckResult(
            "conditional pass",
            "conditional pass",
            "PDF 文本层可提取，但部分关键规则术语未检出。",
        )
    return CheckResult(
        "pass",
        "pass",
        "PDF 文本层可提取，标题、FR 编号、关键术语和英文术语检查通过。",
    )


def classify_readability_gate(
    duplicate_titles: list[str],
    abnormal_spacing: list[str],
    manual_readability: str,
) -> CheckResult:
    if duplicate_titles:
        return CheckResult(
            "fail",
            "fail",
            "检测到标题重复，PDF 可读性不合格。",
        )
    if abnormal_spacing:
        return CheckResult(
            "fail",
            "fail",
            "检测到英文异常拆字，PDF 可读性不合格。",
        )
    if manual_readability == "fail":
        return CheckResult(
            "fail",
            "fail",
            "人工可读性检查未通过。",
        )
    if manual_readability == "pass":
        return CheckResult(
            "pass",
            "pass",
            "自动检查通过，人工可读性检查通过。",
        )
    return CheckResult(
        "conditional pass",
        "conditional pass",
        "自动可读性检查通过，但页边距、标题层级和整体风格仍需人工确认。",
    )


def combine_gate(text_gate: str, readability_gate: str) -> str:
    if "fail" in {text_gate, readability_gate}:
        return "fail"
    if "conditional pass" in {text_gate, readability_gate}:
        return "conditional pass"
    return "pass"


def build_report(
    pdf_path: Path,
    report_path: Path,
    text: str,
    page_count: int,
    extraction_engine: str,
    required_titles: list[str],
    fr_regex: str,
    key_terms: list[str],
    min_text_length: int,
    manual_readability: str,
    error: str | None = None,
) -> str:
    text_length = len(text.strip())
    text_extractable = error is None and text_length >= min_text_length
    title_results = [
        (title, (count := count_title_occurrences(text, title)) > 0, count)
        for title in required_titles
    ]
    fr_matches = re.findall(fr_regex, text) if text else []
    term_results = [(term, term in text) for term in key_terms]
    cjk_ok = has_cjk(text) if text else False
    abnormal_spacing = find_abnormal_spacing(text) if text else []

    missing_titles = [title for title, ok, _ in title_results if not ok]
    duplicate_titles = [title for title, ok, count in title_results if ok and count > 1]
    missing_terms = [term for term, ok in term_results if not ok]

    text_layer = classify_text_layer_gate(
        error=error,
        text_extractable=text_extractable,
        cjk_ok=cjk_ok,
        missing_titles=missing_titles,
        fr_matches=fr_matches,
        missing_terms=missing_terms,
        abnormal_spacing=abnormal_spacing,
    )
    readability = classify_readability_gate(
        duplicate_titles=duplicate_titles,
        abnormal_spacing=abnormal_spacing,
        manual_readability=manual_readability,
    )
    result = combine_gate(text_layer.gate, readability.gate)
    allowed_to_enter_skill_b = result == "pass"
    has_acceptance = any(term in text for term in ["验收标准", "Acceptance Criteria"])
    has_field_rules = any(term in text for term in ["字段", "必填", "唯一", "长度", "格式"])
    has_exception_rules = any(term in text for term in ["异常", "错误", "不存在", "重复", "失败"])

    lines = [
        "# PDF 质量检查报告",
        "",
        "## 1. 基本信息",
        "",
        "```text",
        f"pdf_file: {pdf_path}",
        f"report_file: {report_path}",
        f"page_count: {page_count}",
        f"extraction_engine: {extraction_engine}",
        "reference_pdf: docs/ruoyi-user-management-srs-v2.pdf",
        "```",
        "",
        "## 2. 检查摘要",
        "",
        "```text",
        f"pdf_generated: {str(pdf_path.exists()).lower()}",
        f"text_extractable: {str(text_extractable).lower()}",
        f"extracted_text_length: {text_length}",
        f"has_chinese_text: {str(cjk_ok).lower()}",
        f"has_title_structure: {str(not missing_titles).lower()}",
        f"has_fr_numbers: {str(bool(fr_matches)).lower()}",
        f"has_key_field_rules: {str(has_field_rules).lower()}",
        f"has_key_exception_rules: {str(has_exception_rules).lower()}",
        f"has_acceptance_criteria: {str(has_acceptance).lower()}",
        f"has_duplicate_title: {str(bool(duplicate_titles)).lower()}",
        f"has_abnormal_english_spacing: {str(bool(abnormal_spacing)).lower()}",
        f"pdf_text_layer_gate: {text_layer.gate}",
        f"pdf_readability_gate: {readability.gate}",
        f"recommended_gate_impact: {result}",
        "```",
        "",
        "## 3. 文本层 gate",
        "",
        "| 检查项 | 结果 | 备注 |",
        "|---|---|---|",
        f"| PDF 文件存在 | {'是' if pdf_path.exists() else '否'} |  |",
        f"| PDF 文本可提取 | {'是' if text_extractable else '否'} | 文本长度：{text_length} |",
        f"| 中文文本可识别 | {'是' if cjk_ok else '否'} |  |",
        f"| 标题可检出 | {'是' if not missing_titles else '否'} | 缺失：{', '.join(missing_titles) if missing_titles else '无'} |",
        f"| FR 编号可检出 | {'是' if fr_matches else '否'} | 数量：{len(set(fr_matches))} |",
        f"| 字段规则可检出 | {'是' if has_field_rules else '否'} |  |",
        f"| 异常处理可检出 | {'是' if has_exception_rules else '否'} |  |",
        f"| 验收标准可检出 | {'是' if has_acceptance else '否'} |  |",
        f"| 关键英文术语提取正常 | {'否' if abnormal_spacing else '是'} | {', '.join(abnormal_spacing) if abnormal_spacing else '无异常拆字'} |",
        "",
        "## 4. 标题检查",
        "",
        "| 标题 | 是否检出 | 是否重复 | 备注 |",
        "|---|---|---|---|",
    ]
    for title, ok, count in title_results:
        lines.append(f"| {title} | {'是' if ok else '否'} | {'是' if count > 1 else '否'} | 出现 {count} 次 |")

    lines.extend(["", "## 5. FR 编号检查", "", f"正则：`{fr_regex}`", "", "检出结果：", ""])
    if fr_matches:
        for match in sorted(set(fr_matches)):
            lines.append(f"- {match}")
    else:
        lines.append("- 未检出")

    lines.extend(["", "## 6. 关键术语检查", "", "| 术语 | 是否检出 |", "|---|---|"])
    for term, ok in term_results:
        lines.append(f"| {term} | {'是' if ok else '否'} |")

    lines.extend(
        [
            "",
            "## 7. 可读性 gate",
            "",
            "| 检查项 | 结果 | 检查方式 | 备注 |",
            "|---|---|---|---|",
            f"| 标题不重复 | {'否' if duplicate_titles else '是'} | 自动 | {', '.join(duplicate_titles) if duplicate_titles else '无重复标题'} |",
            f"| 中英文混排正常 | {'否' if abnormal_spacing else '是'} | 自动 + 人工 | {', '.join(abnormal_spacing) if abnormal_spacing else '未发现异常拆字'} |",
            f"| 英文术语没有异常拆字 | {'否' if abnormal_spacing else '是'} | 自动 |  |",
            "| 标题层级清晰 | 待人工确认 | 人工 | 自动脚本不判断视觉层级 |",
            "| 正文段落连续可读 | 待人工确认 | 人工 | 自动脚本不判断段落视觉效果 |",
            "| 页边距、行距、段落间距正常 | 待人工确认 | 人工 | 自动脚本不判断版式舒适度 |",
            "| 页面无明显截断、溢出、乱码 | 待人工确认 | 人工 | 自动脚本不判断页面截图 |",
            "| 整体风格简洁正式，接近原始 SRS v2 | 待人工确认 | 人工 | 需人工对照 reference_pdf |",
        ]
    )

    lines.extend(["", "## 8. 自动发现的问题", "", "| 问题 | 影响 | 处理建议 |", "|---|---|---|"])
    issues: list[tuple[str, str, str]] = []
    if error:
        issues.append((error, "high", "修复 PDF 生成或依赖后重试"))
    if not text_extractable and not error:
        issues.append(("文本层不可提取或文本长度过短", "high", "重新生成 PDF"))
    if not cjk_ok and text:
        issues.append(("未识别到中文文本", "high", "检查字体和文本层"))
    for title in missing_titles:
        issues.append((f"标题未检出：{title}", "medium", "检查 Markdown 标题或 PDF 转换"))
    for title in duplicate_titles:
        issues.append((f"标题重复：{title}", "high", "修复 PDF 标题渲染策略"))
    if not fr_matches:
        issues.append(("FR 编号未检出", "medium", "检查 FR 编号格式"))
    for term in missing_terms:
        issues.append((f"关键术语未检出：{term}", "medium", "检查正文是否包含该规则"))
    for finding in abnormal_spacing:
        issues.append((f"英文异常拆字：{finding}", "high", "修复 PDF 字体和文本渲染方式"))
    if not issues:
        issues.append(("无自动发现问题", "low", "人工确认可读性后可进入下一步"))
    for issue, impact, suggestion in issues:
        lines.append(f"| {issue} | {impact} | {suggestion} |")

    lines.extend(
        [
            "",
            "## 9. 人工可读性确认",
            "",
            "```text",
            f"manual_readability_checked: {str(manual_readability in {'pass', 'fail'}).lower()}",
            f"manual_readability_result: {manual_readability}",
            "manual_reviewer: ",
            "manual_checked_at: ",
            "manual_notes: ",
            "```",
            "",
            "建议人工至少检查：",
            "",
            "- 首页标题和文档概述页",
            "- 一个功能需求页",
            "- 字段规则相关页面",
            "- 异常处理或验收标准相关页面",
            "",
            "## 10. 结论",
            "",
            "```text",
            f"pdf_text_layer_gate: {text_layer.gate}",
            f"pdf_text_layer_reason: {text_layer.reason}",
            f"pdf_readability_gate: {readability.gate}",
            f"pdf_readability_reason: {readability.reason}",
            f"result: {result}",
            f"allowed_to_enter_skill_b: {str(allowed_to_enter_skill_b).lower()}",
            "```",
            "",
        ]
    )

    report = "\n".join(lines)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check PDF text layer and readability quality.")
    parser.add_argument("--pdf", required=True, help="Input PDF file")
    parser.add_argument("--report", required=True, help="Output Markdown report")
    parser.add_argument("--required-title", action="append", default=[], help="Required title text, can repeat")
    parser.add_argument("--fr-regex", default=r"FR-[A-Za-z0-9]+-\d{3}", help="Regex for FR numbers")
    parser.add_argument("--key-term", action="append", default=[], help="Key term that must appear in extracted text, can repeat")
    parser.add_argument("--min-text-length", type=int, default=100, help="Minimum extracted text length")
    parser.add_argument(
        "--manual-readability",
        choices=["pending", "pass", "fail"],
        default="pending",
        help="Manual readability review result",
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero for conditional pass")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf)
    report_path = Path(args.report)
    required_titles = args.required_title or DEFAULT_REQUIRED_TITLES

    text = ""
    page_count = 0
    extraction_engine = "none"
    error = None
    if not pdf_path.exists():
        error = f"PDF 文件不存在：{pdf_path}"
    else:
        try:
            text, page_count, extraction_engine = extract_text(pdf_path)
        except Exception as exc:
            error = f"PDF 文本提取失败：{exc}"

    result = build_report(
        pdf_path=pdf_path,
        report_path=report_path,
        text=text,
        page_count=page_count,
        extraction_engine=extraction_engine,
        required_titles=required_titles,
        fr_regex=args.fr_regex,
        key_terms=args.key_term,
        min_text_length=args.min_text_length,
        manual_readability=args.manual_readability,
        error=error,
    )

    print(f"PDF quality check result: {result}")
    print(f"Report written: {report_path}")
    if result == "fail":
        return 2
    if result == "conditional pass" and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
