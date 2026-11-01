![Baihua](assets/images/logo.png)

# binder-organization.github.io

## Binder Official Website

[![Author: ChepleBob](https://img.shields.io/badge/Author-ChepleBob-00B4D8)](https://github.com/ChepleBob30)
[![License: Apache v2](https://img.shields.io/badge/License-Apache%20v2-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

English | [简体中文](README_zh-CN.md)

---

## Table of Contents

- [Changelog](#changelog)
- [Overview](#overview)
- [How to Publish an Article](#how-to-publish-an-article)
- [License](#license)
- [Closing](#closing)

---

## Changelog

### Added

- Brand-new article page `article.html`;
- Article publishing tools `article_convertor.py` and `build_article_index.py`;
- Automated article index workflow.

### Changed

- Updated several images;
- Improved layouts on the home, products, and docs pages.

### Fixed

- Layout issues on narrow viewports in Firefox.

---

## Overview

This website serves as the official Binder platform, handling both promotion and announcements.

---

## How to Publish an Article

### Publishing Workflow

1. Create separate Chinese and English Markdown files, for example `zh-cn.md` and `en.md`. Both can start with YAML front matter:

```markdown
---
title: Binder feature release
author: Jane Doe
date: 2026-11-01
slug: binder_news_20261101
---

Write the article body in Markdown.
```

Set localized `title` and `author` in each file. `date` is required article-wide metadata and belongs only in the Chinese file; `slug` is optional and defaults to the Chinese filename. `header` and `footer` are optional. The converter asks for missing title, author, or date in interactive mode, and reports missing values in non-interactive mode. The date also supplies the displayed publication time in both languages.
2. Run `python3 tools/article_convertor.py --zh-cn zh-cn.md --en en.md`. `--zhcn` is also accepted as a short alias. The converter writes the website JSON file to `assets/articles/` and updates the article index.
3. Review the generated JSON and preview locally. Article Markdown supports headings, paragraphs, bold, italics, inline and fenced code, links, blockquotes, ordered and unordered lists, and horizontal rules. Raw HTML is displayed as text. Images are not supported yet.
4. Fork the official repository and open a PR containing the generated article JSON and updated `assets/articles/index.json`. Do not include the Markdown source files.
5. Once reviewed and merged, GitHub Actions updates the index and deploys the article page.

### Guidelines

Your PR must meet the following requirements to be approved:
- The article must include both Chinese and English versions.
- The article must not contain formatting errors (e.g. broken lines, stray symbols).
- The article must not plagiarize existing content on the website.
- The article content should be related to Binder.
- The submission timestamp should match the actual publication date.
- The article must not impersonate another person.
- The article must be distributed under the `CC BY` license.
- The submission must not include unrelated files (e.g. `__pycache__`, `AGENTS.md`, etc.).
- Submissions must follow safe and open principles; exploiting vulnerabilities is strictly prohibited.
- Changes must be limited to the `assets/articles` directory; other parts of the repository must not be modified.
- Any other behaviour detrimental to article distribution.

Don't worry — you are free to express your opinions. We will not reject a merge just because of criticism.

---

## License

[Apache v2](../../LICENSE), Copyright 2026 ChepleBob.

---

## Closing

- If you like this project, please share it with others. You can also open an issue to help us improve.
- You are also welcome to join our organization [Binder](https://github.com/binder-organization).
