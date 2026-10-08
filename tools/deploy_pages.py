# -*- coding: utf-8 -*-
"""deploy_pages.py —— 把 Paper_Interaction 发布到 GitHub Pages 用户站

用法: python tools/deploy_pages.py [--no-cache-bump]

做三件事：
  1. 把 index.html + sites/ 镜像到 <用户站>/reader/paper-interaction/
  2. 在用户站 index.html 的 PROJECTS 数组里插入/更新本项目的条目
  3. 提升 sw.js 的 CACHE_NAME 版本号 —— 用户站的 Service Worker 是缓存优先，
     不 bump 的话访客会一直看到旧的 index.html

只改文件，不执行 git。推送请另行确认。
"""
import json
import re
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
HUB = Path("D:/MainSpace/lafloraison.github.io")
MIRROR_NAME = "paper-interaction"
MIRROR = HUB / "reader" / MIRROR_NAME

ENTRY = """  {
    id:'paper-interaction',
    icon:'📄',
    name:'Paper Interaction',
    title:'论文拆解 · 交互式学习',
    desc:'把一篇论文拆到真正读懂为止——不是摘要。原文里每一个论断、每一张图表、每一个公式都有对应卡片；论文没讲清的地方卡片讲清；读者缺的前置知识，由可跳过、可复用的拓展小节从零补齐。每张卡都是「定义 → 例子 → 习题」三段，习题按理解/应用/迁移三层设，每个错误选项都指出选它的人错在哪。',
    gradient:'linear-gradient(135deg,#1a6bff,#16a34a)',
    glow:'rgba(26,107,255,0.25)',
    color:'#1a6bff',
    link:'reader/paper-interaction/',
    github:'https://github.com/LaFloraison/Paper_Interaction',
    stats:{lessons:2,generated:2,label:'篇论文'}
  }"""


def mirror_files():
    if not HUB.exists():
        print("找不到用户站目录:", HUB)
        return False
    if MIRROR.exists():
        shutil.rmtree(MIRROR)
    (MIRROR / "sites").mkdir(parents=True)
    shutil.copy2(ROOT / "index.html", MIRROR / "index.html")
    n = 0
    # 论文对照栏现在是文本（~60KB），默认随镜像走；--no-paper 可剥掉
    strip = "--no-paper" in sys.argv
    for f in sorted((ROOT / "sites").glob("*.html")):
        dest = MIRROR / "sites" / f.name
        if strip:
            html = f.read_text(encoding="utf-8")
            i = html.find("<!--PI-PAGES-START-->")
            j = html.find("<!--PI-PAGES-END-->")
            if i >= 0 and j > i:
                html = html[:i] + html[j + len("<!--PI-PAGES-END-->"):]
                dest.write_text(html, encoding="utf-8")
                print("  %s：已剥掉论文对照栏" % f.name)
            else:
                shutil.copy2(f, dest)
        else:
            shutil.copy2(f, dest)
        n += 1
    size = sum(f.stat().st_size for f in MIRROR.rglob("*") if f.is_file())
    print("镜像到 reader/%s/ ：index.html + %d 个站点，共 %.1f MB"
          % (MIRROR_NAME, n, size / 1048576))
    return True


def patch_projects():
    """插入或更新 PROJECTS 里的本项目条目；已存在则整段替换，并清理重复项。"""
    p = HUB / "index.html"
    s = p.read_text(encoding="utf-8")
    start = s.find("var PROJECTS = [")
    end = s.find("\n];", start)
    if start < 0 or end < 0:
        print("在用户站 index.html 里找不到 PROJECTS 数组")
        return False
    pat = re.compile(r"\{\s*\n\s*id:'paper-interaction'")
    spans = []
    for m in pat.finditer(s[start:end]):
        a = start + m.start()
        b = s.find("\n  }", a)
        if b < 0:
            continue
        spans.append((a, b + len("\n  }")))
    if spans:
        for a, b in reversed(spans[1:]):
            tail = s[b:]
            s = s[:a] + (tail[1:] if tail.startswith(",") else tail)
        a, b = spans[0]
        s = s[:a] + ENTRY + s[b:]
        p.write_text(s, encoding="utf-8")
        print("PROJECTS 条已更新（清理重复 %d 处）" % max(0, len(spans) - 1))
        return True
    s = s[:end] + ",\n" + ENTRY + s[end:]
    p.write_text(s, encoding="utf-8")
    print("PROJECTS 条已插入")
    return True


def bump_cache():
    p = HUB / "sw.js"
    s = p.read_text(encoding="utf-8")
    m = re.search(r"var CACHE_NAME = '([a-z\-]+)-v(\d+)'", s)
    if not m:
        print("在 sw.js 里找不到 CACHE_NAME")
        return False
    new = "%s-v%d" % (m.group(1), int(m.group(2)) + 1)
    p.write_text(s.replace(m.group(0), "var CACHE_NAME = '" + new + "'"), encoding="utf-8")
    print("sw.js 缓存版本 ->", new)
    return True


def main():
    ok = mirror_files()
    ok = patch_projects() and ok
    if "--no-cache-bump" not in sys.argv:
        ok = bump_cache() and ok
    print("完成（未执行 git）" if ok else "有步骤失败，请检查")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
