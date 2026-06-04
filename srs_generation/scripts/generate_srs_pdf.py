#!/usr/bin/env python3
"""Generate a text-layer PDF from a Markdown SRS document.

The script prefers reportlab when available. If reportlab is not installed, it
falls back to a minimal built-in PDF writer that emits real text drawing
operators with a CID font, so the output still has an extractable text layer.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import textwrap
from pathlib import Path

DEFAULT_FONT = "STSong-Light"
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT_MARGIN = 54
TOP_MARGIN = 54
BOTTOM_MARGIN = 54
LINE_HEIGHT = 16


def markdown_to_plain_lines(markdown_text: str, title: str | None = None) -> list[str]:
    lines: list[str] = []
    in_code = False
    if title:
        lines.append(title)
        lines.append("")

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            continue

        if in_code:
            lines.append(line)
            continue

        if not stripped:
            lines.append("")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            prefix = "" if level == 1 else "  " * min(level - 1, 3)
            lines.append(f"{prefix}{text}")
            lines.append("")
            continue

        if re.match(r"^\s*[-*+]\s+", line):
            item = re.sub(r"^\s*[-*+]\s+", "", line).strip()
            lines.append(f"• {strip_inline_markdown(item)}")
            continue

        if re.match(r"^\s*\d+[.)]\s+", line):
            lines.append(strip_inline_markdown(stripped))
            continue

        if stripped == "---":
            lines.append("")
            continue

        if stripped.startswith("|"):
            cleaned = " ".join(part.strip() for part in stripped.strip("|").split("|"))
            if cleaned and not set(cleaned.replace(" ", "")) <= {"-", ":"}:
                lines.append(cleaned)
            continue

        lines.extend(wrap_text(strip_inline_markdown(stripped)))

    return lines


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def wrap_text(text: str, width: int = 46) -> list[str]:
    if len(text) <= width:
        return [text]
    chunks: list[str] = []
    current = ""
    for char in text:
        current += char
        if len(current) >= width:
            chunks.append(current)
            current = ""
    if current:
        chunks.append(current)
    return chunks


def try_reportlab(input_path: Path, output_path: Path, title: str | None, author: str | None, subject: str | None, font_name: str) -> bool:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer
    except Exception:
        return False

    def register_font(name: str) -> str:
        try:
            pdfmetrics.registerFont(UnicodeCIDFont(name))
            return name
        except Exception:
            return "Helvetica"

    def inline_markdown_to_html(text: str) -> str:
        escaped = html.escape(text)
        escaped = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", escaped)
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
        return escaped

    resolved_font = register_font(font_name)
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("SrsTitle", parent=base["Title"], fontName=resolved_font, fontSize=22, leading=28, spaceAfter=18, alignment=TA_LEFT),
        "h1": ParagraphStyle("SrsHeading1", parent=base["Heading1"], fontName=resolved_font, fontSize=18, leading=24, spaceBefore=14, spaceAfter=8, keepWithNext=True),
        "h2": ParagraphStyle("SrsHeading2", parent=base["Heading2"], fontName=resolved_font, fontSize=15, leading=20, spaceBefore=12, spaceAfter=6, keepWithNext=True),
        "h3": ParagraphStyle("SrsHeading3", parent=base["Heading3"], fontName=resolved_font, fontSize=13, leading=18, spaceBefore=10, spaceAfter=5, keepWithNext=True),
        "body": ParagraphStyle("SrsBody", parent=base["BodyText"], fontName=resolved_font, fontSize=10.5, leading=16, spaceAfter=6),
        "bullet": ParagraphStyle("SrsBullet", parent=base["BodyText"], fontName=resolved_font, fontSize=10.5, leading=16, leftIndent=16, firstLineIndent=-10, spaceAfter=4),
        "code": ParagraphStyle("SrsCode", parent=base["Code"], fontName="Courier", fontSize=8.5, leading=11, backColor=colors.whitesmoke, borderColor=colors.lightgrey, borderWidth=0.5, borderPadding=5, spaceAfter=8),
    }

    story: list = []
    markdown_text = input_path.read_text(encoding="utf-8")
    if title:
        story.append(Paragraph(inline_markdown_to_html(title), styles["title"]))

    for line in markdown_to_plain_lines(markdown_text, None):
        if not line:
            story.append(Spacer(1, 0.12 * cm))
        elif line.startswith("  "):
            story.append(Paragraph(inline_markdown_to_html(line.strip()), styles["h2"]))
        elif line.startswith("• "):
            story.append(Paragraph(inline_markdown_to_html(line), styles["bullet"]))
        else:
            story.append(Paragraph(inline_markdown_to_html(line), styles["body"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=1.8 * cm, leftMargin=1.8 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm, title=title or input_path.stem, author=author or "Skill A", subject=subject or "Source-to-SRS generated document")
    doc.build(story)
    return True


def pdf_hex_text(text: str) -> str:
    return text.encode("utf-16-be").hex().upper()


def pdf_escape_literal(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_page_stream(lines: list[str]) -> bytes:
    content = ["BT", "/F1 11 Tf", f"1 0 0 1 {LEFT_MARGIN} {PAGE_HEIGHT - TOP_MARGIN} Tm", f"{LINE_HEIGHT} TL"]
    for line in lines:
        safe = line if line else " "
        content.append(f"<{pdf_hex_text(safe)}> Tj")
        content.append("T*")
    content.append("ET")
    return "\n".join(content).encode("ascii")


def chunk_pages(lines: list[str]) -> list[list[str]]:
    max_lines = int((PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN) / LINE_HEIGHT)
    pages: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if len(current) >= max_lines:
            pages.append(current)
            current = []
        current.append(line)
    if current:
        pages.append(current)
    return pages or [[""]]


def write_builtin_pdf(input_path: Path, output_path: Path, title: str | None, author: str | None, subject: str | None) -> None:
    markdown_text = input_path.read_text(encoding="utf-8")
    lines = markdown_to_plain_lines(markdown_text, title)
    pages = chunk_pages(lines)

    objects: list[bytes] = []

    def add(obj: str | bytes) -> int:
        data = obj.encode("utf-8") if isinstance(obj, str) else obj
        objects.append(data)
        return len(objects)

    catalog_id = add("<< /Type /Catalog /Pages 2 0 R >>")
    pages_id = add(b"")
    font_id = add(
        "<< /Type /Font /Subtype /Type0 /BaseFont /STSong-Light /Encoding /UniGB-UCS2-H "
        "/DescendantFonts [4 0 R] >>"
    )
    descendant_font_id = add(
        "<< /Type /Font /Subtype /CIDFontType0 /BaseFont /STSong-Light "
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (GB1) /Supplement 2 >> "
        "/FontDescriptor 5 0 R >>"
    )
    font_descriptor_id = add("<< /Type /FontDescriptor /FontName /STSong-Light /Flags 4 /Ascent 880 /Descent -120 /CapHeight 700 /StemV 80 >>")

    page_ids: list[int] = []
    for page_lines in pages:
        stream = build_page_stream(page_lines)
        stream_id = add(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
        page_id = add(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {stream_id} 0 R >>"
        )
        page_ids.append(page_id)

    objects[pages_id - 1] = f"<< /Type /Pages /Kids [{' '.join(f'{pid} 0 R' for pid in page_ids)}] /Count {len(page_ids)} >>".encode("utf-8")

    info_id = add(
        "<< "
        f"/Title ({pdf_escape_literal(title or input_path.stem)}) "
        f"/Author ({pdf_escape_literal(author or 'Skill A')}) "
        f"/Subject ({pdf_escape_literal(subject or 'Source-to-SRS generated document')}) "
        "/Producer (Skill A built-in PDF writer) "
        ">>"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as pdf:
        pdf.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for index, obj in enumerate(objects, start=1):
            offsets.append(pdf.tell())
            pdf.write(f"{index} 0 obj\n".encode("ascii"))
            pdf.write(obj)
            pdf.write(b"\nendobj\n")
        xref_offset = pdf.tell()
        pdf.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        pdf.write(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            pdf.write(f"{offset:010d} 00000 n \n".encode("ascii"))
        pdf.write(
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R /Info {info_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
        )


def generate_pdf(input_path: Path, output_path: Path, title: str | None, author: str | None, subject: str | None, font_name: str, force_builtin: bool) -> str:
    if not input_path.exists():
        raise FileNotFoundError(f"Markdown input not found: {input_path}")

    if not force_builtin and try_reportlab(input_path, output_path, title, author, subject, font_name):
        return "reportlab"

    write_builtin_pdf(input_path, output_path, title, author, subject)
    return "builtin"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a text-layer PDF from Markdown.")
    parser.add_argument("--input", required=True, help="Input Markdown file path")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    parser.add_argument("--title", help="PDF title")
    parser.add_argument("--author", default="Skill A", help="PDF author metadata")
    parser.add_argument("--subject", default="Source-to-SRS generated document", help="PDF subject metadata")
    parser.add_argument("--font", default=DEFAULT_FONT, help="ReportLab CID font name, default STSong-Light")
    parser.add_argument("--force-builtin", action="store_true", help="Use the built-in PDF writer even if reportlab is installed")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        engine = generate_pdf(
            input_path=Path(args.input),
            output_path=Path(args.output),
            title=args.title,
            author=args.author,
            subject=args.subject,
            font_name=args.font,
            force_builtin=args.force_builtin,
        )
    except Exception as exc:
        print(f"PDF generation failed: {exc}", file=sys.stderr)
        return 2

    print(f"PDF generated: {args.output}")
    print(f"PDF engine: {engine}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
