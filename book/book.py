#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "content" / "docs"
DEFAULT_OUTPUT = ROOT / "book.md"
LATEX_SAFE_REPLACEMENTS = {
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


FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
KEY_VALUE_RE = re.compile(r'^([A-Za-z0-9_]+):\s*(.*)$')
NOTE_START_RE = re.compile(r"^> \[!NOTE\]\s*$")
NOTE_LINE_RE = re.compile(r"^>\s?(.*)$")


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
    return Page(path=path, title=title, weight=weight, body=body, is_section=is_section)


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


def clean_body(page: Page) -> str:
    text = page.body.replace("\r\n", "\n")
    text = convert_note_blocks(text)
    text = strip_leading_title_heading(text, page.title)
    text = normalize_whitespace(text)
    for src, dst in LATEX_SAFE_REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text


def render_section_title(section: Page) -> str:
    title = section.title
    for src, dst in LATEX_SAFE_REPLACEMENTS.items():
        title = title.replace(src, dst)
    return f"# {title}"


def render_chapter(page: Page) -> str:
    body = clean_body(page)
    title = page.title
    for src, dst in LATEX_SAFE_REPLACEMENTS.items():
        title = title.replace(src, dst)
    if body:
        return f"# {title}\n\n{body}"
    return f"# {title}"


def build_book() -> str:
    chunks: list[str] = []

    for section, children in section_pages():
        chunks.append(render_section_title(section))
        chunks.append(r"\newpage")

        for child in children:
            chunks.append(render_chapter(child))
            chunks.append(r"\newpage")

    while chunks and chunks[-1] == r"\newpage":
        chunks.pop()

    return "\n\n".join(chunks) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concatenate Hugo book chapters into a Pandoc-friendly Markdown manuscript."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output Markdown file. Default: {DEFAULT_OUTPUT}",
    )
    args = parser.parse_args()

    book = build_book()
    args.output.write_text(book)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
