# -*- coding: utf-8 -*-
"""audit_card_order.py — 列出站点每张卡顶层块的呈现顺序，检查
"是什么 → 例子 → 习题" 铁律是否被遵守。
用法: python tools/audit_card_order.py sites/<slug>.html
顶层块识别: card-inner 内恰好 4 空格缩进的元素（机器生成格式保证）。
"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

path = sys.argv[1]
html = open(path, encoding="utf-8").read()

# 卡片切分
cards = re.split(r'(?=<section class="card")', html)
headers = re.compile(
    r'<section class="card"[^>]*data-c="(-?\d+)"[^>]*data-title-en="([^"]*)"')

TOP = re.compile(
    r'^    <(p class="lz"|span class="tex-display"|div class="([a-z0-9 -]+?)"|details class="faq"|h3)(?=[ >])',
    re.M)

def snippet(s, n=52):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return (s[:n] + "…") if len(s) > n else s

for chunk in cards:
    if not chunk.startswith('<section class="card"'):
        continue
    m = headers.match(chunk)
    if not m:
        continue
    cid, ten = m.group(1), m.group(2)
    # 只取 card-inner 到 section 结束
    body = chunk
    seq = []
    for mt in TOP.finditer(body):
        kind = mt.group(1)
        line_end = body.find("\n", mt.start())
        line = body[mt.start():line_end]
        if kind.startswith('p class="lz"'):
            txt = line[len('<p class="lz">'):]
            seq.append('P「' + snippet(txt, 46) + '」')
        elif kind.startswith('span class="tex-display"'):
            mm = re.search(r'data-tex="([^"]{0,40})', line)
            seq.append('TEX ' + (mm.group(1) if mm else ""))
        elif kind.startswith('details'):
            seq.append('FAQ')
        elif kind.startswith('h3'):
            seq.append('H3「' + snippet(line[4:], 24) + '」')
        else:
            cls = mt.group(2) or "?"
            tag = {"callout": "CALLOUT", "callout warn": "WARN",
                   "quiz": "QUIZ", "quiz quiz-num": "QUIZ#",
                   "lab-panel": "LAB", "stepper": "STEP"}.get(cls, cls.upper())
            seq.append(tag)
    print(f'c{cid:>3} | {ten[:44]:<44} | ' + " → ".join(seq))
