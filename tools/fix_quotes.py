# -*- coding: utf-8 -*-
"""把 data-expl/hint/sol 属性值内的曲引号按出现顺序规范成 “…” 交替对"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def canon(m):
    val = m.group(2)
    out = []
    open_next = True
    for ch in val:
        if ch in "“”":
            out.append("“" if open_next else "”")
            open_next = not open_next
        else:
            out.append(ch)
    return 'data-' + m.group(1) + '="' + ''.join(out) + '"'


s2, n = re.subn(r'data-(expl|hint|sol)="([^"]*)"', canon, s)
open(path, "w", encoding="utf-8").write(s2)

vals = re.findall(r'data-(?:expl|hint|sol)="([^"]*)"', s2)
wrong = 0
for v in vals:
    seq = [c for c in v if c in "“”"]
    exp = ["“" if k % 2 == 0 else "”" for k in range(len(seq))]
    if seq != exp:
        wrong += 1
print("canonicalized attrs:", n, "| remaining wrong:", wrong)
