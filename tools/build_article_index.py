#!/usr/bin/env python3
# Article manifest generator.
#
# Purpose: Scans all article JSON files under assets/articles and writes the
#          manifest assets/articles/index.json (content: {"files": [...]}).
# Usage:   python3 tools/build_article_index.py [--verbose]
#          With --verbose, prints the loader version and publish date for each article.
# Trigger: The GitHub Action (.github/workflows/articles-index.yml) runs this script
#          automatically when assets/articles changes; can also be run manually.

import argparse
import json
import sys
from pathlib import Path

repositoryRoot = Path(__file__).resolve().parent.parent
articleDirectory = repositoryRoot / "assets" / "articles"
manifestFileName = "index.json"


def readArticleFile(articlePath):
    """Read the sorting info from an article: filename and exact publish date from info[1]."""
    with articlePath.open(encoding="utf-8") as articleFile:
        rawJson = json.load(articleFile)

    if not isinstance(rawJson, dict):
        raise ValueError("top-level is not a JSON object")

    informationFields = rawJson.get("info")
    if not isinstance(informationFields, list) or len(informationFields) < 2:
        raise ValueError('missing info field (expected ["v1" or "v2", "2026-08-30"])')

    loaderVersion = informationFields[0]
    postDate = informationFields[1]
    if not isinstance(loaderVersion, str) or not loaderVersion:
        raise ValueError("info first element must be a loader version string")
    if not isinstance(postDate, str) or not postDate:
        raise ValueError("info second element must be a language-free publish date string")

    return {"fileName": articlePath.name, "loaderVersion": loaderVersion, "postDate": postDate}


def collectArticles(verbose):
    """Scan the directory, return sorted manifest entries; collect problems into a list."""
    if not articleDirectory.is_dir():
        print("Article directory not found: " + str(articleDirectory), file=sys.stderr)
        return [], ["Article directory not found"]

    articleEntries = []
    problems = []
    for articlePath in sorted(articleDirectory.glob("*.json")):
        if articlePath.name == manifestFileName:
            continue
        try:
            articleEntries.append(readArticleFile(articlePath))
        except (json.JSONDecodeError, ValueError) as error:
            problems.append(articlePath.name + ": " + str(error))

    # Sort by filename ascending, then by date descending (stable sort).
    # Result: newest first; same-day articles sorted by name.
    articleEntries.sort(key=lambda entry: entry["fileName"])
    articleEntries.sort(key=lambda entry: entry["postDate"], reverse=True)

    if verbose:
        for entry in articleEntries:
            print(
                "  " + entry["fileName"]
                + "  版本=" + entry["loaderVersion"]
                + "  发表时间=" + entry["postDate"]
            )
    return articleEntries, problems


def writeManifest(articleEntries):
    """Write the manifest file; skip writing if content is unchanged."""
    manifestPath = articleDirectory / manifestFileName
    manifestText = json.dumps(
        {"files": [entry["fileName"] for entry in articleEntries]},
        ensure_ascii=False,
        indent=2,
    ) + "\n"

    if manifestPath.is_file() and manifestPath.read_text(encoding="utf-8") == manifestText:
        print("Manifest is up to date: " + str(manifestPath))
        return False

    with manifestPath.open("w", encoding="utf-8") as manifestFile:
        manifestFile.write(manifestText)
    print("Manifest written: " + str(manifestPath) + " (" + str(len(articleEntries)) + " articles)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate the article manifest file")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print loader version and publish date for each article",
    )
    arguments = parser.parse_args()

    articleEntries, problems = collectArticles(arguments.verbose)
    for problem in problems:
        print("Problem with article file: " + problem, file=sys.stderr)

    writeManifest(articleEntries)

    if problems:
        print(str(len(problems)) + " article file(s) failed validation", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
