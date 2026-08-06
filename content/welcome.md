---
title: 欢迎来到我的博客
date: 2025-01-26
tags: 随笔
---

# 欢迎！👋

你好呀，这里是 **mdblog** 生成的第一篇文章。

## 这个博客是怎么来的？

它完全由 **Cherry Studio + MCP** 自动搭建：

1. 用 `cherry/filesystem` 在本地写好代码
2. 用 `cherry/python` 测试生成器
3. 用 GitHub API 自动创建仓库并推送
4. 配置好 GitHub Actions，以后每次提交自动部署

> 写 Markdown 就是写作的全部，剩下的交给工具。

## 怎么开始写文章？

在 `content/` 目录新建一个 `.md` 文件，加上 front-matter：

```markdown
---
title: 我的新文章
date: 2025-01-26
tags: 技术
---

正文用 Markdown 写就行。
```

然后运行 `python blog.py build`，一切搞定 ✨
