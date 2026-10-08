# -*- coding: utf-8 -*-
"""把重写的 c21-c24 替换回站点"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()

pairs = [
    ("<!-- ============ c21 框架总览 ============ -->", "<!-- ============ c22 公式(1) ============ -->", "c21"),
    ("<!-- ============ c22 公式(1) ============ -->", "<!-- ============ c23 图1 ============ -->", "c22"),
    ("<!-- ============ c23 图1 ============ -->", "<!-- ============ c24 HOI 精讲 ============ -->", "c23"),
    ("<!-- ============ c24 HOI 精讲 ============ -->", "<!-- NEXT-CARD -->", "c24"),
]

for start_mark, end_mark, name in pairs:
    i = s.find(start_mark)
    j = s.find(end_mark, i + 1)
    assert i > 0 and j > i, name
    new_block = open("decomposition/feng-2026-knowledge-hgnn/cards/" + name + ".html", encoding="utf-8").read()
    s = s[:i] + new_block + "\n" + s[j:]
    print("replaced", name, "old", j - i, "-> new", len(new_block))

open(P, "w", encoding="utf-8").write(s)
print("done")
