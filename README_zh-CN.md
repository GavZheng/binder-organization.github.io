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

1. 在本地用你习惯的方式写好一篇文章。
2. 调用`python3 tools/article_convertor.py`，按照提示将文章转换为json格式。
  - 请注意，完成转换后，你需要fork官网并提出pr。我们建议你自己在本地开一个网站服务器来预览文章显示效果。
3. 将你的文章放置在assets/articles目录下，提出pr。
4. 审核通过后，由github actions自动重新处理索引并部署。
5. 之后，你就可以在官网的文章页面看到你的文章。

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
