# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = "sites/feng-2026-knowledge-hgnn.html"
s = open(p, encoding="utf-8").read()
i = s.find("孤零零的箭")
print("context:", repr(s[i - 20:i + 20]))
old = s[i:i + 12]
new = "孤零零的箭头。"
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
print("fixed:", repr(old), "->", repr(new))
