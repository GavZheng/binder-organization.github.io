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

1. Write your article locally using any method you prefer.
2. Run `python3 tools/article_convertor.py` and follow the prompts to convert your article to JSON.
   - Note: after conversion you need to fork this repository and open a PR. We recommend running a local HTTP server to preview the article before submitting.
3. Place your article under the `assets/articles` directory and submit a PR.
4. Once reviewed and merged, GitHub Actions will automatically rebuild the index and deploy.
5. Your article will then appear on the official website's article page.

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
