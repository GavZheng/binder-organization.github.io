#!/usr/bin/env python3
"""Website article converter.

Interactively asks for article fields in the terminal and produces a standard
article JSON file under assets/articles/.

Usage:
    python3 tools/article_convertor.py

The tool locates the assets/articles directory by walking up from the current
working directory, so it can be invoked from anywhere inside the repository.
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

SUPPORTED_VERSION = "v1"
ARTICLE_DIR_NAME = "assets/articles"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class LanguageText:
    """Ordered list of (language_code, [elements]) pairs."""

    def __init__(self):
        self._entries = []

    def push_language(self, language_code, elements):
        if elements:
            self._entries.append((language_code, list(elements)))

    def entries(self):
        return list(self._entries)

    def is_empty(self):
        return len(self._entries) == 0

    def last_language(self):
        return self._entries[-1] if self._entries else None


class ArticleBody:
    """All user-provided fields (except info)."""

    def __init__(self):
        self.author = LanguageText()
        self.post_time = LanguageText()
        self.title = LanguageText()
        self.header = LanguageText()
        self.content = LanguageText()
        self.footer = LanguageText()

    def field_pairs(self):
        """Yield (name, LanguageText) in JSON key order."""
        return [
            ("author", self.author),
            ("post_time", self.post_time),
            ("title", self.title),
            ("header", self.header),
            ("content", self.content),
            ("footer", self.footer),
        ]


# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------

def read_line(prompt=""):
    """Print *prompt*, read one line, strip whitespace.  Raises EOFError on
    end-of-input so callers can bail instead of spinning forever."""
    print(prompt, end="", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("input ended")
    return line.rstrip("\n").rstrip("\r")


def today_date():
    """Return YYYY-MM-DD for today, or empty string on failure."""
    try:
        return date.today().isoformat()
    except Exception:
        return ""


def is_valid_date(text):
    """Check YYYY-MM-DD format and plausible ranges."""
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        return False
    try:
        year, month, day = int(text[:4]), int(text[5:7]), int(text[8:10])
    except ValueError:
        return False
    return year > 2000 and 1 <= month <= 12 and 1 <= day <= 31


def is_valid_file_name(name, article_dir):
    """Only lowercase ASCII letters, digits, underscores, hyphens; must not
    collide with an existing article file."""
    stem = name.removesuffix(".json")
    if not stem:
        return False
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_-")
    if not all(c in allowed for c in stem):
        return False
    if (article_dir / f"{stem}.json").exists():
        return False
    return True


def discover_article_dir():
    """Walk up from cwd looking for assets/articles/."""
    candidate = Path.cwd()
    while True:
        target = candidate / ARTICLE_DIR_NAME
        if target.is_dir():
            return target
        parent = candidate.parent
        if parent == candidate:
            return None
        candidate = parent


# ---------------------------------------------------------------------------
# JSON serialisation (hand-rolled to avoid extra dependencies)
# ---------------------------------------------------------------------------

def json_escape(text):
    """Escape a string for inclusion in a JSON double-quoted value."""
    out = []
    for ch in text:
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 0x20:
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(ch)
    return "".join(out)


def json_array(elements, element_indent="      ", closing_indent="    "):
    """Render a list of strings as a pretty-printed JSON array."""
    lines = ["[\n"]
    for i, elem in enumerate(elements):
        comma = "," if i + 1 < len(elements) else ""
        lines.append(f'{element_indent}"{json_escape(elem)}"{comma}\n')
    lines.append(f"{closing_indent}]")
    return "".join(lines)


def json_language_map(lang_text):
    """Render a LanguageText as {"zh-CN": [...], "en-US": [...]}."""
    parts = []
    for code, elements in lang_text.entries():
        parts.append(f'    "{json_escape(code)}": {json_array(elements)}')
    return "{\n" + ",\n".join(parts) + "\n  }"


def assemble_article_json(info, body):
    """Produce the full article JSON string."""
    entries = [f'  "info": ["{json_escape(info["version"])}", "{json_escape(info["date"])}"]']
    for field_name, field in body.field_pairs():
        if field.is_empty():
            continue
        entries.append(f'  "{field_name}": {json_language_map(field)}')
    return "{\n" + ",\n".join(entries) + "\n}\n"


# ---------------------------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------------------------

SENTENCE_ENDS = set("。！？；.!?;")
FULLWIDTH_SPACES = {"\u3000", " "}


def split_long_text(text):
    """Split a long line at sentence boundaries.

    Chinese punctuation (。！？；) always triggers a split.
    Western punctuation (. ! ? ;) only splits when followed by whitespace
    so that dates like ``2026.8.30`` are not cut apart.
    Fragments shorter than 8 characters are merged back into the previous
    sentence (without adding a space when the previous sentence ends with
    a Chinese full-width mark).
    """
    sentences = []
    current = []
    chars = list(text)
    pos = 0
    while pos < len(chars):
        ch = chars[pos]
        current.append(ch)
        do_split = False
        if ch in ("。", "！", "？", "；"):
            do_split = True
        elif ch in (".", "!", "?", ";"):
            nxt = chars[pos + 1] if pos + 1 < len(chars) else ""
            if nxt in FULLWIDTH_SPACES:
                do_split = True
        if do_split:
            sentences.append("".join(current).strip())
            current = []
        pos += 1
    tail = "".join(current).strip()
    if tail:
        sentences.append(tail)

    merged = []
    for sentence in sentences:
        if len(sentence) < 8 and merged:
            prev = merged[-1]
            if not prev or prev[-1] in ("。", "！", "？", "；"):
                merged[-1] = prev + sentence
            else:
                merged[-1] = prev + " " + sentence
        else:
            merged.append(sentence)
    return merged


def split_into_elements(lines):
    """Apply the paragraph-to-elements rules."""
    elements = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        term_count = sum(1 for ch in stripped if ch in SENTENCE_ENDS)
        if len(stripped) > 40 and term_count >= 2:
            elements.extend(split_long_text(stripped))
        else:
            elements.append(stripped)
    return elements


# ---------------------------------------------------------------------------
# Interactive prompts
# ---------------------------------------------------------------------------

def ask_file_name(article_dir):
    """Ask for a filename; default is a date-time stamp."""
    try:
        import subprocess
        suggested = subprocess.check_output(
            ["date", "+article_%Y%m%d_%H%M%S"], text=True
        ).strip()
    except Exception:
        suggested = "article_new"

    while True:
        entered = read_line(
            f"\nArticle file name (lowercase letters, digits, underscore, "
            f"hyphen; press Enter to use {suggested}, q to quit): "
        )
        if entered.lower() == "q":
            sys.exit("Aborted by user.")
        name = entered if entered else suggested
        stem = name.removesuffix(".json")
        if is_valid_file_name(stem, article_dir):
            return stem
        print("  Invalid name: only lowercase ASCII letters, digits, "
              "underscore, hyphen allowed; must not overwrite an existing article.")


def ask_article_info():
    """Ask for the publication date; version is always v1."""
    default = today_date()
    if is_valid_date(default):
        entered = read_line(
            f"Publication date (press Enter for today {default}): "
        )
        post_date = entered if entered else default
    else:
        post_date = read_line("Publication date (YYYY-MM-DD): ")

    while not is_valid_date(post_date):
        print("  Bad date format, expected something like 2026-08-30.")
        post_date = read_line("Publication date (YYYY-MM-DD): ")

    return {"version": SUPPORTED_VERSION, "date": post_date}


def ask_language_text(field_name, hint):
    """Ask for a multilingual field.  Each language is collected line-by-line.

    A line containing only ``#`` ends the current language block.
    A line containing only ``=`` copies the previous language's content.
    """
    collected = LanguageText()
    print()
    print(f"  [{field_name}]  {hint}")

    for lang_code in ("zh-CN", "en-US"):
        reuse = ""
        prev = collected.last_language()
        if prev:
            reuse = f", type = to reuse {prev[0]}"
        print(f"  {lang_code} (enter lines, single # to finish{reuse}):")

        lines = []
        while True:
            line = read_line("    > ")
            if line == "#":
                break
            if line == "=" and prev:
                collected.push_language(lang_code, prev[1])
                break
            if line:
                lines.append(line)
        else:
            # stdin closed
            pass

        if lines and not (line == "=" and prev):
            collected.push_language(lang_code, split_into_elements(lines))

    if collected.is_empty():
        print("    (both languages empty — field will be omitted)")
    return collected


def collect_article_body():
    """Interactively collect all article fields."""
    body = ArticleBody()
    body.author = ask_language_text("author", "Author, displayed below the title")
    body.post_time = ask_language_text("post_time", "Display publication time, next to author")
    body.title = ask_language_text("title", "Title, shown at the top of the page")
    body.header = ask_language_text("header", "Placed at the top-left of the article")
    body.content = ask_language_text("content", "Body text, displayed in the middle")
    body.footer = ask_language_text("footer", "Placed below the body, bottom-right")
    return body


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("Website article converter — interactively produces an article JSON file.")
    print("Splitting rule: each line is one element; lines longer than 40 chars with")
    print("two or more sentence-ending marks are automatically split at those marks.")
    print()

    article_dir = discover_article_dir()
    if article_dir is None:
        sys.exit("Cannot find assets/articles/ — please run from inside the repository.")

    print(f"Article directory: {article_dir}")

    file_name = ask_file_name(article_dir)
    info = ask_article_info()
    body = collect_article_body()

    json_text = assemble_article_json(info, body)

    print("\n──── Generated JSON ────")
    print(json_text)

    confirm = read_line("Write to disk? (y to confirm, anything else to abort): ")
    if confirm.lower() != "y":
        print("Aborted.  You can copy the JSON above manually.")
        return

    target = article_dir / f"{file_name}.json"
    target.write_text(json_text, encoding="utf-8")
    print(f"Written: {target}")
    print("Next step: run  python3 tools/build_article_index.py  to update the manifest,")
    print("or push to GitHub and let the articles-index.yml workflow do it automatically.")


if __name__ == "__main__":
    main()
