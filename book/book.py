#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
DOCS_DIR = PROJECT_ROOT / "content" / "docs"
DEFAULT_OUTPUTS = {
    "pdf": ROOT / "book.md",
    "epub": ROOT / "book-epub.md",
}
PDF_SAFE_REPLACEMENTS = {
    "\u00a9": "(c)",
    "\u2013": "--",
    "\u2014": "---",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u2264": "<=",
    "\u2265": ">=",
}


@dataclass
class Page:
    path: Path
    title: str
    weight: int
    body: str
    is_section: bool
    url: str | None


TITLE = "Principles of Data Engineering"
AUTHOR = "Matthias Wong"


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


def wrap_svg_blocks_for_epub(text: str) -> str:
    def replace_svg(match: re.Match[str]) -> str:
        svg = match.group(0).strip()
        return f"\n\n```{{=html}}\n{svg}\n```\n\n"

    return SVG_BLOCK_RE.sub(replace_svg, text)


def rewrite_internal_links(text: str, link_map: dict[str, str]) -> str:
    def replace_link(match: re.Match[str]) -> str:
        prefix, url, fragment, suffix = match.groups()
        anchor = link_map.get(normalize_site_url(url))
        if not anchor:
            return match.group(0)
        return f"{prefix}#{anchor}{fragment or ''}{suffix}"

    return MARKDOWN_SITE_LINK_RE.sub(replace_link, text)


def clean_body(page: Page, target: str, link_map: dict[str, str]) -> str:
    text = page.body.replace("\r\n", "\n")
    text = strip_hugo_markup(text)
    if target == "epub":
        text = wrap_svg_blocks_for_epub(text)
        text = rewrite_internal_links(text, link_map)
    text = convert_note_blocks(text)
    text = strip_leading_title_heading(text, page.title)
    text = normalize_whitespace(text)
    if target == "pdf":
        for src, dst in PDF_SAFE_REPLACEMENTS.items():
            text = text.replace(src, dst)
    return text


def clean_title(title: str, target: str) -> str:
    if target != "pdf":
        return title

    for src, dst in PDF_SAFE_REPLACEMENTS.items():
        title = title.replace(src, dst)
    return title


def render_heading(page: Page, target: str) -> str:
    title = clean_title(page.title, target)
    if target == "epub":
        return f"# {title} {{#{page_anchor(page)}}}"
    return f"# {title}"


def render_chapter(page: Page, target: str, link_map: dict[str, str]) -> str:
    body = clean_body(page, target, link_map)
    heading = render_heading(page, target)
    if body:
        return f"{heading}\n\n{body}"
    return heading


def render_pdf_front_matter() -> str:
    return "\n".join(
        [
            "---",
            f'title: "{TITLE}"',
            f'author: "{AUTHOR}"',
            'documentclass: book',
            'classoption:',
            "  - oneside",
            "  - openany",
            "  - 11pt",
            "geometry: margin=1in",
            "fontsize: 11pt",
            "linestretch: 1.15",
            "toc: true",
            "toc-depth: 3",
            "numbersections: false",
            "links-as-notes: false",
            "header-includes:",
            "  - |",
            "    \\usepackage{microtype}",
            "  - |",
            "    \\usepackage{setspace}",
            "  - |",
            "    \\usepackage{titlesec}",
            "  - |",
            "    \\usepackage{fancyhdr}",
            "  - |",
            "    \\pagestyle{fancy}",
            "  - |",
            "    \\fancyhf{}",
            "  - |",
            "    \\fancyfoot[C]{\\thepage}",
            "  - |",
            "    \\renewcommand{\\headrulewidth}{0pt}",
            "  - |",
            "    \\titleformat{\\chapter}[display]{\\normalfont\\bfseries\\Huge}{}{0pt}{\\Huge}",
            "  - |",
            "    \\titlespacing*{\\chapter}{0pt}{0pt}{24pt}",
            "---",
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
            "\\newpage",
            "",
            "\\tableofcontents",
            "",
            "\\newpage",
        ]
    )


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
        ]
    )


def render_front_matter(target: str) -> str:
    if target == "epub":
        return render_epub_front_matter()
    return render_pdf_front_matter()


def build_book(target: str) -> str:
    sections = section_pages()
    link_map = build_link_map(sections)
    chunks: list[str] = [render_front_matter(target)]

    for section, children in sections:
        if section.title.lower() != "about":
            chunks.append(render_heading(section, target))
            if target == "pdf":
                chunks.append(r"\newpage")

        for child in children:
            chunks.append(render_chapter(child, target, link_map))
            if target == "pdf":
                chunks.append(r"\newpage")

    while chunks and chunks[-1] == r"\newpage":
        chunks.pop()

    return "\n\n".join(chunks) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concatenate Hugo book chapters into a Pandoc-friendly Markdown manuscript."
    )
    parser.add_argument(
        "--target",
        choices=sorted(DEFAULT_OUTPUTS),
        default="pdf",
        help="Output target. Use epub for a Hugo-free EPUB manuscript. Default: pdf",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output Markdown file. Defaults to book/book.md for pdf or book/book-epub.md for epub.",
    )
    args = parser.parse_args()

    output = args.output or DEFAULT_OUTPUTS[args.target]
    book = build_book(args.target)
    output.write_text(book)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
