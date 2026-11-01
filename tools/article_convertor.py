#!/usr/bin/env python3
"""Convert bilingual Markdown articles with YAML-style front matter to site JSON.

Usage: python3 tools/article_convertor.py --zh-cn zh-cn.md --en en.md
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SUPPORTED_VERSION = "v2"
ARTICLE_DIR_NAME = "assets/articles"
FRONT_MATTER_KEYS = {"title", "author", "date", "slug", "header", "footer"}


def read_markdown(path):
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text
    lines = text.splitlines()
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError(f"{path}: front matter begins with --- but has no closing ---")
    metadata = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{number}: expected key: value in front matter")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key not in FRONT_MATTER_KEYS:
            raise ValueError(f"{path}:{number}: unsupported front matter key {key!r}")
        if key in metadata:
            raise ValueError(f"{path}:{number}: duplicate front matter key {key!r}")
        # Scalars may be plain, single-quoted, or JSON-style double-quoted strings.
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{number}: invalid quoted string: {error}")
        elif len(value) >= 2 and value[0] == value[-1] == "'":
            value = value[1:-1].replace("''", "'")
        if not isinstance(value, str):
            raise ValueError(f"{path}:{number}: front matter values must be strings")
        metadata[key] = value
    return metadata, "\n".join(lines[end + 1:]).lstrip("\n")


def ask_missing(label, value, default=None):
    if value:
        return value
    if not sys.stdin.isatty():
        raise ValueError(f"Missing required metadata: {label}")
    suffix = f" [{default}]" if default else ""
    answer = input(f"{label}{suffix}: ").strip()
    return answer or (default or "")


def valid_date(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def safe_slug(value):
    return bool(value) and all(char in "abcdefghijklmnopqrstuvwxyz0123456789_-" for char in value)


def build_article(args, article_dir):
    zh_path, en_path = Path(args.zh_cn), Path(args.en)
    zh_meta, zh_body = read_markdown(zh_path)
    en_meta, en_body = read_markdown(en_path)

    # date and slug are article-wide and belong in the Chinese file only.
    for key in ("date", "slug"):
        if key in en_meta:
            raise ValueError(f"{en_path}: {key} is article-wide metadata; put it in {zh_path}")
    post_date = ask_missing("Publication date YYYY-MM-DD (zh-CN front matter)", zh_meta.get("date"), date.today().isoformat())
    if not valid_date(post_date):
        raise ValueError(f"Invalid publication date {post_date!r}; expected YYYY-MM-DD")

    slug = zh_meta.get("slug") or zh_path.stem
    if not safe_slug(slug):
        raise ValueError("Slug may contain only lowercase ASCII letters, digits, underscores, and hyphens")
    target = article_dir / f"{slug}.json"
    if target.exists():
        raise ValueError(f"Output already exists: {target}")

    fields = {name: {} for name in ("author", "post_time", "title", "header", "content", "footer")}
    for language, label, metadata, body in (
        ("zh-CN", "zh-CN", zh_meta, zh_body),
        ("en-US", "en-US", en_meta, en_body),
    ):
        for field in ("title", "author"):
            value = ask_missing(f"{label} {field}", metadata.get(field))
            if not value:
                raise ValueError(f"{label} {field} cannot be empty")
            fields[field][language] = [value]
        fields["post_time"][language] = [post_date if language == "en-US" else post_date.replace("-", ".")]
        for field in ("header", "footer"):
            if metadata.get(field):
                fields[field][language] = [metadata[field]]
        if not body.strip():
            raise ValueError(f"{label} Markdown body is empty")
        fields["content"][language] = [body.strip()]

    result = {"info": [SUPPORTED_VERSION, post_date], "content_format": "markdown"}
    result.update(fields)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Written: {target}")
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name("build_article_index.py"))],
        check=True,
    )
    print("The website renders Markdown in article bodies. Include the article JSON and updated index.json in your PR.")


def main():
    parser = argparse.ArgumentParser(description="Convert bilingual Markdown articles to website JSON")
    parser.add_argument("--zh-cn", "--zhcn", dest="zh_cn", required=True, help="Chinese Markdown file")
    parser.add_argument("--en", required=True, help="English Markdown file")
    args = parser.parse_args()
    try:
        root = Path(__file__).resolve().parent.parent
        article_dir = root / ARTICLE_DIR_NAME
        build_article(args, article_dir)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
