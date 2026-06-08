#!/usr/bin/env python3
"""Generate a readable text-layer PDF from a Markdown SRS document."""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_FONT = "auto"
FALLBACK_CID_FONT = "STSong-Light"
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT_MARGIN = 54
TOP_MARGIN = 54
BOTTOM_MARGIN = 54
LINE_HEIGHT = 16

CJK_FONT_FILE_CANDIDATES = [
    (
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ),
    (
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ),
]


@dataclass(frozen=True)
class MarkdownBlock:
    kind: str
    text: str
    level: int = 0


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def markdown_has_top_heading(markdown_text: str) -> bool:
    for raw_line in markdown_text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        return bool(re.match(r"^#\s+.+$", stripped))
    return False


def parse_markdown_blocks(markdown_text: str) -> list[MarkdownBlock]:
    blocks: list[MarkdownBlock] = []
    paragraph_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines if line.strip())
            if text:
                blocks.append(MarkdownBlock("paragraph", strip_inline_markdown(text)))
            paragraph_lines.clear()

    def flush_code() -> None:
        if code_lines:
            blocks.append(MarkdownBlock("code", "\n".join(code_lines).rstrip()))
            code_lines.clear()

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            blocks.append(
                MarkdownBlock(
                    "heading",
                    strip_inline_markdown(heading.group(2).strip()),
                    level,
                )
            )
            continue

        if stripped == "---":
            flush_paragraph()
            continue

        if re.match(r"^\s*[-*+]\s+", line):
            flush_paragraph()
            item = re.sub(r"^\s*[-*+]\s+", "", line).strip()
            blocks.append(MarkdownBlock("bullet", strip_inline_markdown(item)))
            continue

        if re.match(r"^\s*\d+[.)]\s+", line):
            flush_paragraph()
            blocks.append(MarkdownBlock("numbered", strip_inline_markdown(stripped)))
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            cleaned = " ".join(part.strip() for part in stripped.strip("|").split("|"))
            if cleaned and not set(cleaned.replace(" ", "")) <= {"-", ":"}:
                blocks.append(MarkdownBlock("paragraph", strip_inline_markdown(cleaned)))
            continue

        paragraph_lines.append(stripped)

    flush_paragraph()
    flush_code()
    return blocks


def markdown_to_plain_lines(markdown_text: str, title: str | None = None) -> list[str]:
    lines: list[str] = []
    if title and not markdown_has_top_heading(markdown_text):
        lines.append(title)
        lines.append("")

    for block in parse_markdown_blocks(markdown_text):
        if block.kind == "heading":
            prefix = "" if block.level == 1 else "  " * min(block.level - 1, 3)
            lines.append(f"{prefix}{block.text}")
            lines.append("")
        elif block.kind == "bullet":
            lines.append(f"• {block.text}")
        elif block.kind == "code":
            lines.extend(block.text.splitlines())
            lines.append("")
        else:
            lines.extend(wrap_text(block.text))
    return lines


def split_long_token(token: str, width: int) -> list[str]:
    if len(token) <= width:
        return [token]
    if re.match(r"^[A-Za-z0-9_:/?.&=#%+.-]+$", token):
        return [token]
    return [token[index : index + width] for index in range(0, len(token), width)]


def wrap_text(text: str, width: int = 46) -> list[str]:
    if len(text) <= width:
        return [text]

    chunks: list[str] = []
    current = ""
    for token in re.split(r"(\s+)", text):
        if not token:
            continue
        if token.isspace():
            if current and not current.endswith(" "):
                current += " "
            continue
        for piece in split_long_token(token, width):
            candidate = f"{current}{piece}" if not current or current.endswith(" ") else f"{current} {piece}"
            if current and len(candidate) > width:
                chunks.append(current.rstrip())
                current = piece
            else:
                current = candidate
    if current.strip():
        chunks.append(current.rstrip())
    return chunks


def try_reportlab(
    input_path: Path,
    output_path: Path,
    title: str | None,
    author: str | None,
    subject: str | None,
    font_name: str,
) -> bool:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer
    except Exception:
        return False

    def is_registered(name: str) -> bool:
        try:
            pdfmetrics.getFont(name)
            return True
        except KeyError:
            return False

    def register_ttf(name: str, path: Path) -> bool:
        try:
            if not is_registered(name):
                pdfmetrics.registerFont(TTFont(name, str(path)))
            return True
        except Exception:
            return False

    def register_font_pair(requested_font: str) -> tuple[str, str]:
        if requested_font and requested_font != "auto":
            requested_path = Path(requested_font).expanduser()
            if requested_path.exists() and register_ttf("SkillACJKRegular", requested_path):
                return "SkillACJKRegular", "SkillACJKRegular"
            try:
                pdfmetrics.registerFont(UnicodeCIDFont(requested_font))
                return requested_font, requested_font
            except Exception:
                pass

        for regular, bold in CJK_FONT_FILE_CANDIDATES:
            regular_path = Path(regular)
            bold_path = Path(bold)
            if regular_path.exists() and bold_path.exists():
                regular_ok = register_ttf("SkillACJKRegular", regular_path)
                bold_ok = register_ttf("SkillACJKBold", bold_path)
                if regular_ok and bold_ok:
                    return "SkillACJKRegular", "SkillACJKBold"

        try:
            pdfmetrics.registerFont(UnicodeCIDFont(FALLBACK_CID_FONT))
        except Exception:
            pass
        return FALLBACK_CID_FONT, FALLBACK_CID_FONT

    regular_font, bold_font = register_font_pair(font_name)

    def inline_markdown_to_html(text: str) -> str:
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        escaped = html.escape(text)
        escaped = re.sub(
            r"`([^`]+)`",
            r"<font name='Courier'>\1</font>",
            escaped,
        )
        escaped = re.sub(
            r"\*\*([^*]+)\*\*",
            lambda match: f"<font name='{bold_font}'>{match.group(1)}</font>",
            escaped,
        )
        return escaped

    base = getSampleStyleSheet()
    styles = {
        "h1": ParagraphStyle(
            "SrsHeading1",
            parent=base["Title"],
            fontName=bold_font,
            fontSize=20,
            leading=28,
            spaceBefore=4,
            spaceAfter=16,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "SrsHeading2",
            parent=base["Heading1"],
            fontName=bold_font,
            fontSize=15,
            leading=22,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "SrsHeading3",
            parent=base["Heading2"],
            fontName=bold_font,
            fontSize=12.5,
            leading=18,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h4": ParagraphStyle(
            "SrsHeading4",
            parent=base["Heading3"],
            fontName=bold_font,
            fontSize=11.5,
            leading=17,
            spaceBefore=8,
            spaceAfter=5,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "SrsBody",
            parent=base["BodyText"],
            fontName=regular_font,
            fontSize=10.5,
            leading=16.5,
            spaceAfter=7,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "SrsBullet",
            parent=base["BodyText"],
            fontName=regular_font,
            fontSize=10.5,
            leading=16.5,
            leftIndent=16,
            firstLineIndent=-10,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "SrsCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            backColor=colors.whitesmoke,
            borderColor=colors.lightgrey,
            borderWidth=0.5,
            borderPadding=5,
            spaceBefore=4,
            spaceAfter=8,
        ),
    }

    story: list = []
    markdown_text = input_path.read_text(encoding="utf-8")
    blocks = parse_markdown_blocks(markdown_text)
    has_document_title = any(block.kind == "heading" and block.level == 1 for block in blocks)

    if title and not has_document_title:
        story.append(Paragraph(inline_markdown_to_html(title), styles["h1"]))
        story.append(Spacer(1, 0.1 * cm))

    for block in blocks:
        if block.kind == "heading":
            style_name = f"h{min(block.level, 4)}"
            story.append(Paragraph(inline_markdown_to_html(block.text), styles[style_name]))
        elif block.kind == "bullet":
            story.append(Paragraph(inline_markdown_to_html(block.text), styles["bullet"], bulletText="•"))
        elif block.kind == "numbered":
            story.append(Paragraph(inline_markdown_to_html(block.text), styles["body"]))
        elif block.kind == "code":
            story.append(Preformatted(block.text, styles["code"]))
        else:
            story.append(Paragraph(inline_markdown_to_html(block.text), styles["body"]))

    if not story:
        story.append(Paragraph(" ", styles["body"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.9 * cm,
        leftMargin=1.9 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title=title or input_path.stem,
        author=author or "Skill A",
        subject=subject or "Source-to-SRS generated document",
    )
    doc.build(story)
    return True


def pdf_hex_text(text: str) -> str:
    return text.encode("utf-16-be").hex().upper()


def pdf_escape_literal(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_page_stream(lines: list[str]) -> bytes:
    content = [
        "BT",
        "/F1 11 Tf",
        f"1 0 0 1 {LEFT_MARGIN} {PAGE_HEIGHT - TOP_MARGIN} Tm",
        f"{LINE_HEIGHT} TL",
    ]
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


def write_builtin_pdf(
    input_path: Path,
    output_path: Path,
    title: str | None,
    author: str | None,
    subject: str | None,
) -> None:
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
        "<< /Type /Font /Subtype /Type0 /BaseFont /STSong-Light "
        "/Encoding /UniGB-UCS2-H /DescendantFonts [4 0 R] >>"
    )
    add(
        "<< /Type /Font /Subtype /CIDFontType0 /BaseFont /STSong-Light "
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (GB1) /Supplement 2 >> "
        "/FontDescriptor 5 0 R >>"
    )
    add(
        "<< /Type /FontDescriptor /FontName /STSong-Light /Flags 4 "
        "/Ascent 880 /Descent -120 /CapHeight 700 /StemV 80 >>"
    )

    page_ids: list[int] = []
    for page_lines in pages:
        stream = build_page_stream(page_lines)
        stream_id = add(
            b"<< /Length "
            + str(len(stream)).encode("ascii")
            + b" >>\nstream\n"
            + stream
            + b"\nendstream"
        )
        page_id = add(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {stream_id} 0 R >>"
        )
        page_ids.append(page_id)

    objects[pages_id - 1] = (
        f"<< /Type /Pages /Kids [{' '.join(f'{pid} 0 R' for pid in page_ids)}] "
        f"/Count {len(page_ids)} >>"
    ).encode("utf-8")

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


def generate_pdf(
    input_path: Path,
    output_path: Path,
    title: str | None,
    author: str | None,
    subject: str | None,
    font_name: str,
    force_builtin: bool,
) -> str:
    if not input_path.exists():
        raise FileNotFoundError(f"Markdown input not found: {input_path}")

    if not force_builtin and try_reportlab(input_path, output_path, title, author, subject, font_name):
        return "reportlab"

    write_builtin_pdf(input_path, output_path, title, author, subject)
    return "builtin"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a readable text-layer PDF from Markdown.")
    parser.add_argument("--input", required=True, help="Input Markdown file path")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    parser.add_argument("--title", help="PDF title metadata; Markdown controls visible title")
    parser.add_argument("--author", default="Skill A", help="PDF author metadata")
    parser.add_argument("--subject", default="Source-to-SRS generated document", help="PDF subject metadata")
    parser.add_argument(
        "--font",
        default=DEFAULT_FONT,
        help="Font file path, CID font name, or 'auto' for mixed Chinese/English font selection",
    )
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
