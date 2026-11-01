![Baihua](assets/images/logo.png)

# binder-organization.github.io

## 必达的官方网站

[![作者: ChepleBob](https://img.shields.io/badge/作者-ChepleBob-00B4D8)](https://github.com/ChepleBob30)
[![许可证: Apache v2](https://img.shields.io/badge/许可证-Apache%20v2-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

[English](README.md) | 简体中文

---

## 目录

- [更新说明](#更新说明)
- [总览](#总览)
- [如何发表文章](#如何发表文章)
- [许可证](#许可证)
- [尾声](#尾声)

---

## 更新说明

### 添加

- 全新文章页面`article.html`；
- 文章发布工具`article_convertor.py`与`build_article_index.py`；
- 自动处理文章索引工作流。

### 更改

- 更新了一些图片；
- 改进了主页、产品、文档页面的布局。

### 修复

- 在firefox上，窄布局可能会出现布局问题。

---

## 总览

本网站为必达官方平台，承担宣传与通知两大职责。

---

## 如何发表文章

### 发表流程

1. 分别创建中文和英文 Markdown 文件，例如`zh-cn.md`和`en.md`。两份文件都可以在开头写 YAML Front Matter：

```markdown
---
title: 必达新功能发布
author: 张三
date: 2026-11-01
slug: binder_news_20261101
---

正文使用 Markdown 编写。
```

`title`和`author`按语言分别填写；`date`为必填文章级字段，仅放在中文文件中；`slug`可选，默认取中文文件名。`header`和`footer`可选。缺少标题、作者或日期时，转换器会交互询问；在非交互环境运行时会报告缺少项。日期同时用于生成中英文显示时间。

2. 运行`python3 tools/article_convertor.py --zh-cn zh-cn.md --en en.md`。也支持`--zhcn`作为`--zh-cn`的简写。转换器会在`assets/articles/`生成网站使用的 JSON 文件，并更新文章索引。
3. 检查生成的 JSON，并在本地预览。Markdown 正文支持标题、段落、粗体、斜体、行内代码、代码块、链接、引用、无序和有序列表及分隔线；原始 HTML 会作为普通文本显示。图片暂不支持。
4. Fork 官网并提出 PR，提交生成的文章 JSON 和更新后的`assets/articles/index.json`。不要把 Markdown 源文件加入 PR。
5. 审核通过后，由 GitHub Actions 自动更新索引并部署，文章随后会出现在官网文章页面。

### 注意事项

在pr审核过程中，你的申请需遵守以下规定才能通过：
- 文章必须包含中英双语版本。
- 文章不得出现排版错乱（例如换行错误，出现不明符号）的问题。
- 文章不得抄袭官网已有内容。
- 文章内容应与必达有关。
- 文章的提交时间应与现实时间相符。
- 文章不得冒用他人名称来发布。
- 文章需以`CC BY`许可分发。
- 提交中不得包含无关文件（例如__pycache__目录，AGENTS.md等）。
- 提交应保持安全、公开的原则，严禁使用小手段试图卡出漏洞。
- 提交只能作用于assets/articles目录，不得修改其他部分。
- 其他不利于文章传播的行为。
无需担心，你可以畅所欲言，我们不会因为批评就拒绝合并。

---

## 许可证

[Apache v2](../../LICENSE), Copyright 2026 ChepleBob.

---

## 尾声

- 如果你喜欢此项目，请推荐给更多的人，也可以提交issue来帮助我们改进项目。
- 你还可以试试加入我们的组织[必达](https://github.com/binder-organization)。
