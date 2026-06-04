#!/usr/bin/env python3
"""Check whether a generated SRS PDF has an extractable text layer."""

from __future__ import annotations

import argparse
import re
import sys
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
    error: str | None = None,
) -> str:
    text_length = len(text.strip())
    text_extractable = error is None and text_length >= min_text_length
    title_results = [(title, title in text) for title in required_titles]
    fr_matches = re.findall(fr_regex, text) if text else []
    term_results = [(term, term in text) for term in key_terms]
    cjk_ok = has_cjk(text) if text else False

    missing_titles = [title for title, ok in title_results if not ok]
    missing_terms = [term for term, ok in term_results if not ok]

    if error or not text_extractable or not cjk_ok:
        result = "fail"
        gate = "fail"
        reason = error or "PDF 文本层不可提取、文本过短或中文文本无法识别。"
    elif required_titles and missing_titles:
        result = "conditional pass"
        gate = "conditional pass"
        reason = "PDF 文本层可提取，但部分必需标题未检出。"
    elif not fr_matches:
        result = "conditional pass"
        gate = "conditional pass"
        reason = "PDF 文本层可提取，但未检出 FR 编号。"
    elif missing_terms:
        result = "conditional pass"
        gate = "conditional pass"
        reason = "PDF 文本层可提取，但部分关键规则术语未检出。"
    else:
        result = "pass"
        gate = "pass"
        reason = "PDF 文本层可提取，标题、FR 编号和关键术语检查通过。"

    lines = [
        "# PDF 文本层检查报告",
        "",
        "## 1. 基本信息",
        "",
        "```text",
        f"pdf_file: {pdf_path}",
        f"report_file: {report_path}",
        f"page_count: {page_count}",
        f"extraction_engine: {extraction_engine}",
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
        f"recommended_gate_impact: {gate}",
        "```",
        "",
        "## 3. 标题检查",
        "",
        "| 标题 | 是否检出 |",
        "|---|---|",
    ]
    for title, ok in title_results:
        lines.append(f"| {title} | {'是' if ok else '否'} |")

    lines.extend(["", "## 4. FR 编号检查", "", f"正则：`{fr_regex}`", "", "检出结果：", ""])
    if fr_matches:
        for match in sorted(set(fr_matches)):
            lines.append(f"- {match}")
    else:
        lines.append("- 未检出")

    lines.extend(["", "## 5. 关键术语检查", "", "| 术语 | 是否检出 |", "|---|---|"])
    for term, ok in term_results:
        lines.append(f"| {term} | {'是' if ok else '否'} |")

    lines.extend(["", "## 6. 问题记录", "", "| 问题 | 影响 | 处理建议 |", "|---|---|---|"])
    if error:
        lines.append(f"| {error} | high | 修复 PDF 生成或依赖后重试 |")
    if not text_extractable and not error:
        lines.append("| 文本层不可提取或文本长度过短 | high | 重新生成 PDF |")
    if not cjk_ok and text:
        lines.append("| 未识别到中文文本 | high | 检查字体和文本层 |")
    for title in missing_titles:
        lines.append(f"| 标题未检出：{title} | medium | 检查 Markdown 标题或 PDF 转换 |")
    if not fr_matches:
        lines.append("| FR 编号未检出 | medium | 检查 FR 编号格式 |")
    for term in missing_terms:
        lines.append(f"| 关键术语未检出：{term} | medium | 检查正文是否包含该规则 |")
    if not (error or not text_extractable or not cjk_ok or missing_titles or not fr_matches or missing_terms):
        lines.append("| 无 | low | 无需处理 |")

    lines.extend(["", "## 7. 结论", "", "```text", f"result: {result}", f"reason: {reason}", "```", ""])

    report = "\n".join(lines)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check PDF text layer quality.")
    parser.add_argument("--pdf", required=True, help="Input PDF file")
    parser.add_argument("--report", required=True, help="Output Markdown report")
    parser.add_argument("--required-title", action="append", default=[], help="Required title text, can repeat")
    parser.add_argument("--fr-regex", default=r"FR-[A-Za-z0-9]+-\d{3}", help="Regex for FR numbers")
    parser.add_argument("--key-term", action="append", default=[], help="Key term that must appear in extracted text, can repeat")
    parser.add_argument("--min-text-length", type=int, default=100, help="Minimum extracted text length")
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
        error=error,
    )

    print(f"PDF text check result: {result}")
    print(f"Report written: {report_path}")
    if result == "fail":
        return 2
    if result == "conditional pass" and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
