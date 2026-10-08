# -*- coding: utf-8 -*-
"""批间质检: 检查 data-expl/hint/sol 属性值内的裸引号 + quiz 结构"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
lines = s.split("\n")
bad = 0
for i, ln in enumerate(lines, 1):
    if "data-expl" in ln or "data-hint" in ln or "data-sol" in ln:
        for m in re.finditer(r'(data-(?:expl|hint|sol)=)"', ln):
            start = m.end()
            j = start
            depth_ok = True
            # value runs to the next quote that is followed by tag-ish chars
            while j < len(ln):
                if ln[j] == '"':
                    rest = ln[j + 1: j + 3]
                    if rest.startswith(">") or rest.startswith(" ") or rest.startswith("/"):
                        break
                j += 1
            val = ln[start:j]
            if '"' in val:
                bad += 1
                print("LINE", i, "BROKEN ATTR:", val[:110].replace("\n", " "))
print("broken attrs:", bad)
print("hidden stubs:", s.count('style="display:none"></div>'))
print("quiz divs:", len(re.findall(r'<div class="quiz', s)))
