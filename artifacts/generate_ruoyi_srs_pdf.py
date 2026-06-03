from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR / "ruoyi-user-management-srs-v2-regenerated-aligned.md"
OUTPUT = BASE_DIR / "ruoyi-user-management-srs-v2-regenerated-aligned.pdf"

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="DocTitleCn",
    parent=styles["Title"],
    fontName="STSong-Light",
    fontSize=18,
    leading=24,
    alignment=TA_CENTER,
    spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="Heading1Cn",
    parent=styles["Heading1"],
    fontName="STSong-Light",
    fontSize=15,
    leading=20,
    spaceBefore=16,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Heading2Cn",
    parent=styles["Heading2"],
    fontName="STSong-Light",
    fontSize=13,
    leading=18,
    spaceBefore=12,
    spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Heading3Cn",
    parent=styles["Heading3"],
    fontName="STSong-Light",
    fontSize=11.5,
    leading=16,
    spaceBefore=8,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="BodyCn",
    parent=styles["BodyText"],
    fontName="STSong-Light",
    fontSize=10,
    leading=15,
    alignment=TA_LEFT,
    firstLineIndent=0,
    spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="MetaCn",
    parent=styles["BodyText"],
    fontName="STSong-Light",
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#444444"),
    spaceAfter=4,
))


def escape_text(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("`", "")
    )


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows = []
    idx = start
    while idx < len(lines) and lines[idx].strip().startswith("|"):
        raw = lines[idx].strip().strip("|")
        cells = [cell.strip() for cell in raw.split("|")]
        if not all(re.fullmatch(r"[-: ]+", cell or "") for cell in cells):
            rows.append(cells)
        idx += 1
    return rows, idx


def table_widths(column_count: int) -> list[float]:
    available = A4[0] - 4 * cm
    if column_count == 2:
        return [available * 0.25, available * 0.75]
    if column_count == 3:
        return [available * 0.18, available * 0.18, available * 0.64]
    return [available / column_count] * column_count


def add_table(story: list, rows: list[list[str]]) -> None:
    if not rows:
        return
    col_count = max(len(row) for row in rows)
    normalized = [row + [""] * (col_count - len(row)) for row in rows]
    data = [
        [Paragraph(escape_text(cell), styles["BodyCn"]) for cell in row]
        for row in normalized
    ]
    table = Table(data, colWidths=table_widths(col_count), repeatRows=1)
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "STSong-Light"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F4F7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D5DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.append(Spacer(1, 8))


def add_paragraph(story: list, text: str, style_name: str = "BodyCn") -> None:
    story.append(Paragraph(escape_text(text), styles[style_name]))


def build_story(markdown_text: str) -> list:
    lines = markdown_text.splitlines()
    story = []
    paragraph_buffer: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            add_paragraph(story, " ".join(paragraph_buffer).strip())
            paragraph_buffer = []

    idx = 0
    while idx < len(lines):
        line = lines[idx].rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            idx += 1
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            rows, idx = parse_table(lines, idx)
            add_table(story, rows)
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            add_paragraph(story, stripped[2:].strip(), "DocTitleCn")
            idx += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            add_paragraph(story, stripped[3:].strip(), "Heading1Cn")
            idx += 1
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            add_paragraph(story, stripped[4:].strip(), "Heading2Cn")
            idx += 1
            continue

        if stripped.startswith("#### "):
            flush_paragraph()
            add_paragraph(story, stripped[5:].strip(), "Heading3Cn")
            idx += 1
            continue

        if stripped.startswith("---"):
            flush_paragraph()
            idx += 1
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            add_paragraph(story, "• " + stripped[2:].strip())
            idx += 1
            continue

        if re.match(r"^\d+\.\s", stripped):
            flush_paragraph()
            add_paragraph(story, stripped)
            idx += 1
            continue

        if ":" in stripped and len(stripped) < 100 and not stripped.endswith("。"):
            flush_paragraph()
            add_paragraph(story, stripped, "MetaCn")
            idx += 1
            continue

        paragraph_buffer.append(stripped)
        idx += 1

    flush_paragraph()
    return story


def main() -> None:
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="RuoYi-Vue-Pro 用户管理模块 Software Requirements Specification",
        author="TestHub SRS Reproduction",
    )
    story = build_story(SOURCE.read_text(encoding="utf-8"))
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    main()
