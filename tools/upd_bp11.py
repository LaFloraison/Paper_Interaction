# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

b = "decomposition/feng-2026-knowledge-hgnn/blueprint.md"
t = open(b, encoding="utf-8").read()
r = [
    ("| c45 | Table VIII (k-fig) | 层数消融；8 层 HGNN 崩至 30.22, DD 49.53 最稳 | 待审",
     "| c45 | Table VIII (k-fig) | 层数消融；8 层 HGNN 崩至 30.22, DD 49.53 最稳 | 批11/R1 PASS（打磨：超边/型号名/结构账白话）"),
    ("| c46 | Table IX (k-fig) | 换底座：GCN/HGNN+/HNHN/LightHGNN/AllSet 全涨 | 待审",
     "| c46 | Table IX (k-fig) | 换底座：GCN/HGNN+/HNHN/LightHGNN/AllSet 全涨 | 批11/R2 FAIL(最小增益矛盾/8.35✓应为8.36)→修→待复审"),
    ("| c47 | Table X (k-fig) | KE-GNN 跨界；Δ_GCN 六数据集全验证 | 待审",
     "| c47 | Table X (k-fig) | KE-GNN 跨界；Δ_GCN 六数据集全验证 | 批11/R3 PASS（打磨：转导/混血白话 + 显式误解框）"),
]
for o, n in r:
    if o in t:
        t = t.replace(o, n, 1)
        print("ok:", o[:12])
    else:
        print("MISS:", o[:30])
open(b, "w", encoding="utf-8").write(t)
print("recorded")
