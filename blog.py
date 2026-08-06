#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mdblog - 极简静态博客生成器。纯标准库，零依赖。"""
import re, sys, shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATE_FILE = BASE_DIR / "template.html"
OUTPUT_DIR = BASE_DIR / "site"
SITE_TITLE = "我的博客"
SITE_DESCRIPTION = "用 mdblog 生成的极简静态博客"

def parse_front_matter(text):
    meta = {}; body = text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if m:
        raw_meta, body = m.group(1), m.group(2)
        for line in raw_meta.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip().strip('"')
    return meta, body

def inline(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text

def convert_markdown(text):
    lines = text.splitlines(); html, i = [], 0
    list_stack = []; in_code = False; code_buf = []
    def close_list(level):
        while list_stack and list_stack[-1] >= level:
            html.append("</ul>"); list_stack.pop()
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if not in_code:
                close_list(1); in_code, code_buf = True, []
            else:
                in_code = False
                html.append("<pre><code>" + "\n".join(code_buf) + "</code></pre>")
            i += 1; continue
        if in_code:
            code_buf.append(line); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1)); close_list(1)
            html.append(f"<h{level}>{inline(m.group(2))}</h{level}>"); i += 1; continue
        if line.startswith(">"):
            close_list(1)
            html.append(f"<blockquote>{inline(line.lstrip('>').strip())}</blockquote>")
            i += 1; continue
        m = re.match(r"^(\s*)[-*+]\s+(.*)$", line)
        if m:
            indent = len(m.group(1)) // 2
            if not list_stack or list_stack[-1] < indent:
                html.append("<ul>"); list_stack.append(indent)
            elif list_stack[-1] > indent:
                close_list(indent + 1); html.append("<ul>"); list_stack.append(indent)
            html.append(f"<li>{inline(m.group(2))}</li>"); i += 1; continue
        close_list(1)
        if not line.strip():
            i += 1; continue
        para = [line]
        while (i + 1 < len(lines) and lines[i + 1].strip()
               and not lines[i + 1].startswith(("#", ">", "-", "*", "```"))):
            i += 1; para.append(lines[i])
        html.append(f"<p>{inline(' '.join(para))}</p>")
        i += 1
    close_list(1)
    if in_code:
        html.append("<pre><code>" + "\n".join(code_buf) + "</code></pre>")
    return "\n".join(html)

def render_page(title, content_html, extra=""):
    t = TEMPLATE_FILE.read_text(encoding="utf-8")
    return (t.replace("{{TITLE}}", title).replace("{{SITE_TITLE}}", SITE_TITLE)
             .replace("{{SITE_DESCRIPTION}}", SITE_DESCRIPTION)
             .replace("{{CONTENT}}", content_html).replace("{{EXTRA}}", extra)
             .replace("{{YEAR}}", str(datetime.now().year)))

def build():
    if OUTPUT_DIR.exists(): shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    posts = []
    for md in sorted(CONTENT_DIR.glob("*.md")):
        meta, body = parse_front_matter(md.read_text(encoding="utf-8"))
        slug = md.stem; title = meta.get("title", slug)
        date = meta.get("date", ""); tags = meta.get("tags", "")
        html_body = convert_markdown(body)
        extra = f'<p class="meta">{date} · {tags}</p>' if (date or tags) else ""
        (OUTPUT_DIR / f"{slug}.html").write_text(render_page(title, html_body, extra), encoding="utf-8")
        posts.append((date, title, slug, tags))
    posts.sort(reverse=True)
    items = "".join(f'<li><a href="{slug}.html">{title}</a><span class="meta">{date} · {tags}</span></li>'
                    for date, title, slug, tags in posts)
    (OUTPUT_DIR / "index.html").write_text(render_page("首页", f"<ul class='posts'>{items}</ul>"), encoding="utf-8")
    print(f"生成完成：{len(posts)} 篇文章")

def clean():
    if OUTPUT_DIR.exists(): shutil.rmtree(OUTPUT_DIR)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    (build if cmd == "build" else clean)()
