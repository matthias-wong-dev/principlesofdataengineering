#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
import shutil
import struct
import subprocess
import time
import zlib
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
DOCS_DIR = PROJECT_ROOT / "content" / "docs"
TITLE = "Principles of Data Engineering"
AUTHOR = "Matthias Wong"
DEFAULT_OUTPUTS = {
    "pdf": ROOT / "book.md",
    "epub": ROOT / "book-epub.md",
    "kdp": ROOT / "book-kdp.md",
}
DEFAULT_ARTIFACTS = {
    "pdf": ROOT / f"{TITLE}.pdf",
    "epub": ROOT / f"{TITLE}.epub",
    "kdp": ROOT / f"{TITLE} - KDP Interior.pdf",
}
EPUB_ASSETS_DIR = ROOT / "epub-assets"
PDF_SAFE_REPLACEMENTS: dict[str, str] = {}
BOOK_URL = "https://principlesofdataengineering.org"
BOOK_DOMAIN = "principlesofdataengineering.org"
AVAILABILITY_NOTE = (
    f"The book is available on [{BOOK_DOMAIN}]({BOOK_URL}).\n\n"
    "Downloadable PDF and EPUB editions are available for offline reading. "
    "The online version is canonical and may be updated over time."
)


@dataclass
class Page:
    path: Path
    title: str
    weight: int
    body: str
    is_section: bool
    url: str | None
    lede: str | None


FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
KEY_VALUE_RE = re.compile(r'^([A-Za-z0-9_]+):\s*(.*)$')
NOTE_START_RE = re.compile(r"^> \[!NOTE\]\s*$")
NOTE_LINE_RE = re.compile(r"^>\s?(.*)$")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HTML_DIV_RE = re.compile(r"\n?<div\b[^>]*>\s*(.*?)\s*</div>\n?", re.DOTALL | re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
SVG_BLOCK_RE = re.compile(r"<svg\b.*?</svg>", re.DOTALL | re.IGNORECASE)
HUGO_RELREF_RE = re.compile(
    r"{{\s*[<%]\s*(?:relref|ref)\s+['\"]?([^'\"\s>]+)['\"]?\s*[>%]\s*}}"
)
HUGO_SHORTCODE_INLINE_RE = re.compile(r"{{\s*[<%]\s*/?[\w-]+.*?[>%]\s*}}")
MARKDOWN_SITE_LINK_RE = re.compile(r"(\[[^\]]+\]\()(/docs/[^)#\s]+)(#[^)]+)?(\))")
FENCED_CODE_RE = re.compile(
    r"(^```[ \t]*([A-Za-z0-9_-]+)?[^\n]*\n)(.*?)(^```[ \t]*$)",
    re.DOTALL | re.MULTILINE,
)
SQL_KEYWORDS = {
    "all",
    "and",
    "apply",
    "as",
    "between",
    "by",
    "case",
    "cast",
    "coalesce",
    "convert",
    "cross",
    "distinct",
    "else",
    "end",
    "exists",
    "from",
    "full",
    "group",
    "having",
    "in",
    "inner",
    "is",
    "join",
    "left",
    "not",
    "null",
    "on",
    "or",
    "order",
    "outer",
    "over",
    "partition",
    "right",
    "select",
    "then",
    "union",
    "when",
    "where",
    "with",
}
DAX_KEYWORDS = {
    "all",
    "allexcept",
    "allselected",
    "and",
    "average",
    "averagex",
    "blank",
    "calculate",
    "calculatetable",
    "countrows",
    "crossfilter",
    "distinctcount",
    "divide",
    "false",
    "filter",
    "hasonevalue",
    "if",
    "isfiltered",
    "isinscope",
    "keepfilters",
    "max",
    "min",
    "not",
    "or",
    "related",
    "relatedtable",
    "removefilters",
    "return",
    "selectcolumns",
    "selectedvalue",
    "sum",
    "summarize",
    "summarizecolumns",
    "sumx",
    "switch",
    "treatas",
    "true",
    "userelationship",
    "userprincipalname",
    "values",
    "var",
}
CODE_KEYWORDS = {
    "sql": SQL_KEYWORDS,
    "dax": DAX_KEYWORDS,
}


class DiagramRenderer:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled and shutil.which("qlmanage") is not None
        self.index = 0
        if self.enabled:
            EPUB_ASSETS_DIR.mkdir(exist_ok=True)
            for asset in EPUB_ASSETS_DIR.glob("diagram-*"):
                if asset.is_file():
                    asset.unlink()

    def render(self, svg: str) -> str:
        if not self.enabled:
            return raw_html_block(svg)

        self.index += 1
        stem = f"diagram-{self.index:03d}"
        svg_path = EPUB_ASSETS_DIR / f"{stem}.svg"
        png_path = EPUB_ASSETS_DIR / f"{stem}.png"
        svg_path.write_text(svg_for_thumbnail(svg))

        try:
            if png_path.exists():
                png_path.unlink()
            subprocess.run(
                ["qlmanage", "-t", "-s", "1600", "-o", str(EPUB_ASSETS_DIR), str(svg_path)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            candidates: list[Path] = []
            for _ in range(20):
                candidates = sorted(EPUB_ASSETS_DIR.glob(f"{svg_path.name}*.png"))
                if candidates:
                    break
                time.sleep(0.1)
            if not candidates:
                svg_path.unlink(missing_ok=True)
                return raw_html_block(svg)
            candidates[0].replace(png_path)
            crop_png_whitespace(png_path)
            svg_path.unlink(missing_ok=True)
            return f"\n\n![](book/epub-assets/{png_path.name})\n\n"
        except (OSError, subprocess.CalledProcessError):
            svg_path.unlink(missing_ok=True)
            return raw_html_block(svg)


def svg_for_thumbnail(svg: str) -> str:
    view_box_match = re.search(
        r'viewBox="([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)"',
        svg,
    )
    if not view_box_match:
        return svg

    min_x, min_y, width, height = (float(value) for value in view_box_match.groups())
    if height <= width:
        return svg

    svg = re.sub(r'(<svg\b[^>]*?)\sstyle="[^"]*"', r"\1", svg, count=1, flags=re.IGNORECASE)
    svg = re.sub(r"<svg\b", '<svg overflow="visible"', svg, count=1, flags=re.IGNORECASE)

    square = format_svg_number(height)
    view_box_match = re.search(
        r'viewBox="([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)"',
        svg,
    )
    view_box = f'viewBox="{format_svg_number(min_x)} {format_svg_number(min_y)} {square} {square}"'
    svg = svg[: view_box_match.start()] + view_box + svg[view_box_match.end() :]
    if re.search(r'\bwidth="[+-]?\d+(?:\.\d+)?"', svg):
        svg = re.sub(r'\bwidth="[+-]?\d+(?:\.\d+)?"', f'width="{square}"', svg, count=1)
    return svg


def format_svg_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:g}"


def png_chunks(data: bytes) -> list[tuple[bytes, bytes]]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("not a PNG")

    chunks: list[tuple[bytes, bytes]] = []
    offset = 8
    while offset < len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        kind = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        chunks.append((kind, chunk_data))
        offset += length + 12
        if kind == b"IEND":
            break
    return chunks


def paeth_predictor(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    distances = (
        abs(estimate - left),
        abs(estimate - above),
        abs(estimate - upper_left),
    )
    if distances[0] <= distances[1] and distances[0] <= distances[2]:
        return left
    if distances[1] <= distances[2]:
        return above
    return upper_left


def unfilter_png_scanlines(raw: bytes, width: int, height: int, channels: int) -> bytearray:
    stride = width * channels
    out = bytearray(height * stride)
    raw_offset = 0

    for y in range(height):
        filter_type = raw[raw_offset]
        raw_offset += 1
        row = bytearray(raw[raw_offset : raw_offset + stride])
        raw_offset += stride
        previous = out[(y - 1) * stride : y * stride] if y else bytearray(stride)

        for x in range(stride):
            left = row[x - channels] if x >= channels else 0
            above = previous[x]
            upper_left = previous[x - channels] if x >= channels else 0
            if filter_type == 1:
                row[x] = (row[x] + left) & 0xFF
            elif filter_type == 2:
                row[x] = (row[x] + above) & 0xFF
            elif filter_type == 3:
                row[x] = (row[x] + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                row[x] = (row[x] + paeth_predictor(left, above, upper_left)) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter: {filter_type}")

        out[y * stride : (y + 1) * stride] = row

    return out


def encode_png(width: int, height: int, channels: int, pixels: bytes) -> bytes:
    color_type = 6 if channels == 4 else 2
    rows = []
    stride = width * channels
    for y in range(height):
        rows.append(b"\x00" + pixels[y * stride : (y + 1) * stride])

    def chunk(kind: bytes, chunk_data: bytes) -> bytes:
        checksum = zlib.crc32(kind + chunk_data) & 0xFFFFFFFF
        return struct.pack(">I", len(chunk_data)) + kind + chunk_data + struct.pack(">I", checksum)

    header = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(
        b"IDAT", zlib.compress(b"".join(rows), level=9)
    ) + chunk(b"IEND", b"")


def crop_png_whitespace(path: Path, padding: int = 24, threshold: int = 245) -> None:
    data = path.read_bytes()
    chunks = png_chunks(data)
    ihdr = next(chunk_data for kind, chunk_data in chunks if kind == b"IHDR")
    width, height, bit_depth, color_type, _, _, _ = struct.unpack(">IIBBBBB", ihdr)
    if bit_depth != 8 or color_type not in {2, 6}:
        return

    channels = 4 if color_type == 6 else 3
    compressed = b"".join(chunk_data for kind, chunk_data in chunks if kind == b"IDAT")
    pixels = unfilter_png_scanlines(zlib.decompress(compressed), width, height, channels)
    stride = width * channels

    left = width
    top = height
    right = -1
    bottom = -1
    for y in range(height):
        row_offset = y * stride
        for x in range(width):
            offset = row_offset + x * channels
            red, green, blue = pixels[offset : offset + 3]
            alpha = pixels[offset + 3] if channels == 4 else 255
            if alpha > 0 and (red < threshold or green < threshold or blue < threshold):
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    if right < left or bottom < top:
        return

    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(width - 1, right + padding)
    bottom = min(height - 1, bottom + padding)
    cropped_width = right - left + 1
    cropped_height = bottom - top + 1

    cropped = bytearray(cropped_width * cropped_height * channels)
    for y in range(cropped_height):
        src = ((top + y) * width + left) * channels
        dst = y * cropped_width * channels
        cropped[dst : dst + cropped_width * channels] = pixels[src : src + cropped_width * channels]

    path.write_bytes(encode_png(cropped_width, cropped_height, channels, bytes(cropped)))


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text

    front_matter = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        kv = KEY_VALUE_RE.match(line)
        if not kv:
            continue
        key, value = kv.groups()
        value = value.strip().strip('"').strip("'")
        front_matter[key] = value

    return front_matter, text[match.end() :]


def load_page(path: Path) -> Page:
    front_matter, body = parse_front_matter(path.read_text())
    title = front_matter.get("title", path.stem.replace("-", " ").title())
    weight = int(front_matter.get("weight", "9999"))
    is_section = path.name == "_index.md"
    return Page(
        path=path,
        title=title,
        weight=weight,
        body=body,
        is_section=is_section,
        url=front_matter.get("url"),
        lede=front_matter.get("lede"),
    )


def section_pages() -> list[tuple[Page, list[Page]]]:
    sections = []
    for section_dir in sorted(p for p in DOCS_DIR.iterdir() if p.is_dir()):
        index_path = section_dir / "_index.md"
        if not index_path.exists():
            continue

        section = load_page(index_path)
        children = []
        for child_path in sorted(section_dir.glob("*.md")):
            if child_path.name == "_index.md":
                continue
            children.append(load_page(child_path))

        children.sort(key=lambda page: (page.weight, page.title.lower(), page.path.name))
        sections.append((section, children))

    sections.sort(key=lambda item: (item[0].weight, item[0].title.lower(), item[0].path.parent.name))
    return sections


def normalize_whitespace(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]

    out: list[str] = []
    blank = False
    for line in lines:
        if line.strip():
            out.append(line)
            blank = False
        else:
            if not blank:
                out.append("")
            blank = True

    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()

    return "\n".join(out)


def normalize_site_url(url: str | None) -> str:
    if not url:
        return ""

    normalized = url.strip().split("#", 1)[0].split("?", 1)[0]
    if not normalized:
        return ""
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    if not normalized.endswith("/"):
        normalized += "/"
    return normalized


def slugify_anchor(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def page_anchor(page: Page) -> str:
    if page.url:
        return slugify_anchor(normalize_site_url(page.url).strip("/"))

    relative = page.path.relative_to(DOCS_DIR)
    if relative.name == "_index.md":
        return slugify_anchor("docs/" + str(relative.parent))
    return slugify_anchor("docs/" + str(relative.with_suffix("")))


def build_link_map(sections: list[tuple[Page, list[Page]]]) -> dict[str, str]:
    links: dict[str, str] = {}
    for section, children in sections:
        pages = [section, *children]
        for page in pages:
            url = normalize_site_url(page.url)
            if url:
                links[url] = page_anchor(page)
    return links


def strip_leading_title_heading(text: str, title: str) -> str:
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)

    if lines:
        heading = lines[0].strip().lstrip("#").strip()
        if heading.lower() == title.lower():
            lines.pop(0)
            while lines and not lines[0].strip():
                lines.pop(0)

    return "\n".join(lines)


def convert_note_blocks(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        if NOTE_START_RE.match(lines[i]):
            note_lines: list[str] = []
            i += 1
            while i < len(lines):
                note_match = NOTE_LINE_RE.match(lines[i])
                if not note_match:
                    break
                note_lines.append(note_match.group(1))
                i += 1

            cleaned = [line for line in note_lines if line is not None]
            while cleaned and not cleaned[0].strip():
                cleaned.pop(0)
            while cleaned and not cleaned[-1].strip():
                cleaned.pop()

            label = "Note"
            body_lines = cleaned
            if body_lines and re.fullmatch(r"\*\*(.+?)\*\*", body_lines[0].strip()):
                label = re.fullmatch(r"\*\*(.+?)\*\*", body_lines[0].strip()).group(1)
                body_lines = body_lines[1:]
                while body_lines and not body_lines[0].strip():
                    body_lines.pop(0)

            out.append(f"> **{label}.**")
            if body_lines:
                out.append(">")
                for body_line in body_lines:
                    out.append("> " + body_line if body_line else ">")
            continue

        out.append(lines[i])
        i += 1

    return "\n".join(out)


def rewrite_caption_div(match: re.Match[str]) -> str:
    caption = HTML_TAG_RE.sub("", match.group(1))
    caption = html.unescape(" ".join(caption.split()))
    if not caption:
        return "\n\n"
    return f"\n\n*{caption}*\n\n"


def strip_hugo_markup(text: str) -> str:
    text = HUGO_RELREF_RE.sub(lambda match: match.group(1), text)
    text = HTML_COMMENT_RE.sub("", text)
    text = HTML_DIV_RE.sub(rewrite_caption_div, text)
    return HUGO_SHORTCODE_INLINE_RE.sub("", text)


def raw_html_block(svg: str) -> str:
    return f"\n\n```{{=html}}\n{svg.strip()}\n```\n\n"


def highlight_code_segment(text: str, keywords: set[str], target: str) -> str:
    out: list[str] = []
    pos = 0
    for match in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]*\b", text):
        word = match.group(0)
        out.append(escape_code_text(text[pos : match.start()], target))
        if word.lower() in keywords:
            if target == "epub":
                out.append(f'<span class="kw">{html.escape(word)}</span>')
            else:
                out.append(r"\textcolor{codeKeyword}{" + word + "}")
        else:
            out.append(escape_code_text(word, target))
        pos = match.end()

    out.append(escape_code_text(text[pos:], target))
    return "".join(out)


def escape_code_text(text: str, target: str) -> str:
    if target == "epub":
        return html.escape(text)

    return (
        text.replace("\\", r"\textbackslash{}")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def highlighted_code_text(code: str, keywords: set[str], target: str) -> str:
    protected = re.compile(r"('(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|\[[^\]]*\])")
    parts: list[str] = []
    pos = 0

    for match in protected.finditer(code):
        parts.append(highlight_code_segment(code[pos : match.start()], keywords, target))
        parts.append(escape_code_text(match.group(0), target))
        pos = match.end()

    parts.append(highlight_code_segment(code[pos:], keywords, target))
    return "".join(parts)


def highlighted_dax_code(code: str, target: str) -> str:
    parts: list[str] = []
    found_measure_name = False

    for line in code.splitlines(keepends=True):
        if not found_measure_name and line.strip() and "=" in line:
            lhs, separator, rhs = line.partition("=")
            parts.append(escape_code_text(lhs + separator, target))
            parts.append(highlighted_code_text(rhs, DAX_KEYWORDS, target))
            found_measure_name = True
        else:
            parts.append(highlighted_code_text(line, DAX_KEYWORDS, target))

    highlighted = "".join(parts)
    return wrap_highlighted_code(highlighted, "dax", target)


def wrap_highlighted_code(highlighted: str, language: str, target: str) -> str:
    if target == "epub":
        return (
            f'\n\n<div class="pode-code pode-code-{language}">'
            f"<pre><code>{highlighted}</code></pre></div>\n\n"
        )

    return f"\n\n\\begin{{podecode}}\n{highlighted}\n\\end{{podecode}}\n\n"


def highlighted_code(code: str, language: str, target: str) -> str:
    if language == "dax":
        return highlighted_dax_code(code, target)

    highlighted = highlighted_code_text(code, CODE_KEYWORDS[language], target)
    return wrap_highlighted_code(highlighted, language, target)

def highlight_code_blocks(text: str, target: str) -> str:
    def replace_block(match: re.Match[str]) -> str:
        opener, language, code, closer = match.groups()
        normalized = (language or "").lower()
        if target in {"pdf", "kdp", "epub"} and normalized in CODE_KEYWORDS:
            return highlighted_code(code.rstrip("\n"), normalized, target)
        return opener + code + closer

    return FENCED_CODE_RE.sub(replace_block, text)


def wrap_svg_blocks_for_epub(text: str, diagrams: DiagramRenderer) -> str:
    def replace_svg(match: re.Match[str]) -> str:
        svg = match.group(0).strip()
        return diagrams.render(svg)

    return SVG_BLOCK_RE.sub(replace_svg, text)


def rewrite_internal_links(text: str, link_map: dict[str, str]) -> str:
    def replace_link(match: re.Match[str]) -> str:
        prefix, url, fragment, suffix = match.groups()
        anchor = link_map.get(normalize_site_url(url))
        if not anchor:
            return match.group(0)
        return f"{prefix}#{anchor}{fragment or ''}{suffix}"

    return MARKDOWN_SITE_LINK_RE.sub(replace_link, text)


def clean_body(
    page: Page,
    target: str,
    link_map: dict[str, str],
    diagrams: DiagramRenderer,
) -> str:
    text = page.body.replace("\r\n", "\n")
    text = strip_hugo_markup(text)
    if target in {"epub", "pdf", "kdp"}:
        text = wrap_svg_blocks_for_epub(text, diagrams)
    if target in {"epub", "pdf", "kdp"}:
        text = rewrite_internal_links(text, link_map)
        text = highlight_code_blocks(text, target)
    text = convert_note_blocks(text)
    text = strip_leading_title_heading(text, page.title)
    text = normalize_whitespace(text)
    if target in {"pdf", "kdp"}:
        for src, dst in PDF_SAFE_REPLACEMENTS.items():
            text = text.replace(src, dst)
    return text


def clean_title(title: str, target: str) -> str:
    if target not in {"pdf", "kdp"}:
        return title

    for src, dst in PDF_SAFE_REPLACEMENTS.items():
        title = title.replace(src, dst)
    return title


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def render_heading(page: Page, target: str) -> str:
    title = clean_title(page.title, target)
    if target in {"epub", "pdf", "kdp"}:
        return f"# {title} {{#{page_anchor(page)}}}"
    return f"# {title}"


def render_section_break(page: Page, target: str) -> str:
    if target == "epub":
        return render_heading(page, target)

    title = latex_escape(clean_title(page.title, target))
    anchor = page_anchor(page)
    return "\n".join(
        [
            r"\thispagestyle{empty}",
            r"\phantomsection",
            f"\\hypertarget{{{anchor}}}{{}}",
            f"\\addcontentsline{{toc}}{{part}}{{{title}}}",
            r"\vspace*{0.34\textheight}",
            r"\begin{center}",
            f"{{\\Huge\\bfseries {title}}}",
            r"\end{center}",
            r"\cleardoublepage",
        ]
    )


def render_chapter(
    page: Page,
    target: str,
    link_map: dict[str, str],
    diagrams: DiagramRenderer,
) -> str:
    body = clean_body(page, target, link_map, diagrams)
    heading = render_heading(page, target)
    if page.lede:
        lede = f"*{page.lede.strip()}*"
        return f"{heading}\n\n{lede}\n\n{body}" if body else f"{heading}\n\n{lede}"
    if body:
        return f"{heading}\n\n{body}"
    return heading


def render_pdf_front_matter() -> str:
    return render_print_front_matter()


def render_print_front_matter() -> str:
    return "\n".join(
        [
            "---",
            f'title: "{TITLE}"',
            f'author: "{AUTHOR}"',
            'documentclass: book',
            'classoption:',
            "  - openright",
            "  - 10pt",
            "geometry: paperwidth=7in,paperheight=10in,inner=0.7in,outer=0.55in,top=0.65in,bottom=0.75in",
            "fontsize: 10pt",
            "linestretch: 1.08",
            "toc: true",
            "toc-depth: 3",
            "numbersections: false",
            "links-as-notes: false",
            "---",
            "",
            "\\frontmatter",
            "",
            "\\thispagestyle{empty}",
            "",
            "\\vspace*{0.25\\textheight}",
            "",
            "\\begin{center}",
            "",
            f"{{\\Huge\\bfseries {TITLE}\\\\}}",
            "",
            "\\vspace{1.5cm}",
            "",
            f"{{\\Large {AUTHOR}}}",
            "",
            "\\end{center}",
            "",
            "\\cleardoublepage",
            "",
            "\\thispagestyle{empty}",
            "",
            "\\vspace*{0.35\\textheight}",
            "",
            "\\noindent "
            f"The book is available on \\href{{{BOOK_URL}}}{{{BOOK_DOMAIN}}}.",
            "",
            "\\vspace{1em}",
            "",
            "\\noindent Downloadable PDF and EPUB editions are available for offline reading. "
            "The online version is canonical and may be updated over time.",
            "",
            "\\cleardoublepage",
            "",
            "\\tableofcontents",
            "",
            "\\cleardoublepage",
            "",
            "\\mainmatter",
        ]
    )


def render_kdp_front_matter() -> str:
    return render_print_front_matter()


def render_epub_front_matter() -> str:
    return "\n".join(
        [
            "---",
            f'title: "{TITLE}"',
            f'author: "{AUTHOR}"',
            "language: en-AU",
            "toc: true",
            "toc-depth: 3",
            "numbersections: false",
            "links-as-notes: false",
            "css: book/epub.css",
            "---",
            "",
            AVAILABILITY_NOTE,
        ]
    )


def render_front_matter(target: str) -> str:
    if target == "epub":
        return render_epub_front_matter()
    if target == "kdp":
        return render_kdp_front_matter()
    return render_pdf_front_matter()


def build_book(target: str) -> str:
    sections = section_pages()
    link_map = build_link_map(sections)
    diagrams = DiagramRenderer(enabled=target in {"epub", "pdf", "kdp"})
    chunks: list[str] = [render_front_matter(target)]

    for section, children in sections:
        if section.title.lower() != "about":
            chunks.append(render_section_break(section, target))

        for child in children:
            chunks.append(render_chapter(child, target, link_map, diagrams))
            if target in {"pdf", "kdp"}:
                chunks.append(r"\cleardoublepage")

    while chunks and chunks[-1] in {r"\newpage", r"\cleardoublepage"}:
        chunks.pop()

    return "\n\n".join(chunks) + "\n"


def pandoc_command(target: str, source: Path, artifact: Path) -> list[str]:
    command = [
        "pandoc",
        str(source),
        "-o",
        str(artifact),
        "--resource-path",
        f"{PROJECT_ROOT}:{ROOT}",
    ]
    if target in {"pdf", "kdp"}:
        command.extend(
            [
                "-f",
                "markdown-smart",
                "--pdf-engine=xelatex",
                "--syntax-highlighting=none",
                "--template",
                str(ROOT / "template.tex"),
            ]
        )
    else:
        command.extend(["--toc", "--toc-depth=3"])
    return command


def build_artifact(target: str, source: Path, artifact: Path) -> None:
    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc was not found on PATH.")
    if target in {"pdf", "kdp"} and shutil.which("xelatex") is None:
        raise SystemExit("xelatex was not found on PATH; install a TeX distribution to build PDF.")

    artifact.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(pandoc_command(target, source, artifact), check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concatenate Hugo book chapters into a Pandoc-friendly Markdown manuscript."
    )
    parser.add_argument(
        "--target",
        choices=sorted(DEFAULT_OUTPUTS),
        default="pdf",
        help="Output target. Use kdp for a 6x9 print interior PDF manuscript. Default: pdf",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output Markdown file. Defaults to book/book.md, book/book-epub.md, or book/book-kdp.md.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Also run Pandoc to build the final PDF or EPUB artifact.",
    )
    parser.add_argument(
        "--artifact-output",
        type=Path,
        default=None,
        help="Final PDF/EPUB path when --build is used. Defaults to the target's artifact path.",
    )
    args = parser.parse_args()

    output = args.output or DEFAULT_OUTPUTS[args.target]
    book = build_book(args.target)
    output.write_text(book)
    print(f"Wrote {output}")

    if args.build:
        artifact = args.artifact_output or DEFAULT_ARTIFACTS[args.target]
        build_artifact(args.target, output, artifact)
        print(f"Wrote {artifact}")


if __name__ == "__main__":
    main()
