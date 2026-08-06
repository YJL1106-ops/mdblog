# 📝 mdblog — 极简静态博客生成器

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个 **零依赖** 的静态博客生成器，仅用 Python 标准库实现。
写 Markdown → 一条命令生成静态网站 → GitHub Actions 自动部署到 Pages。

## ✨ 特性

- 🚫 **零依赖**：纯标准库，无需 pip install
- 📝 **Markdown 渲染**：标题 / 列表 / 代码块 / 引用 / 链接 / 粗体斜体
- 🏷️ **Front-matter**：支持标题、日期、标签等元信息
- 🏠 **自动首页**：按日期倒序生成文章列表
- 🎨 **响应式模板**：内置简洁现代的主题
- ⚡ **一键部署**：内置 GitHub Actions + Pages 工作流

## 🚀 快速开始

```bash
git clone https://github.com/YJL1106-ops/mdblog.git
cd mdblog
python blog.py build
python -m http.server 8000 --directory site
# 浏览器打开 http://localhost:8000
```

## 📁 目录结构

```
mdblog/
├── blog.py            # 生成器主程序（零依赖）
├── template.html      # 页面模板
├── content/           # 文章目录（Markdown）
└── .github/workflows/ # GitHub Actions 自动部署
```

## ✍️ 写文章

在 `content/` 下新建 `.md` 文件，头部加元信息：

```markdown
---
title: 我的文章标题
date: 2025-01-26
tags: 技术, 随笔
---

这里是正文，支持 **Markdown** 语法。
```

## 📄 License

MIT
