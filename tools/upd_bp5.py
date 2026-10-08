# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

b = "decomposition/feng-2026-knowledge-hgnn/blueprint.md"
t = open(b, encoding="utf-8").read()

recs = [
    ("| c21 | 精讲 (k-math) | 两步框架 K=φ(D), Y=HGNN(ψ(K),H)；为何不止一层 Θ | 待审",
     "| c21 | 精讲 (k-math) | 两步框架 K=φ(D), Y=HGNN(ψ(K),H)；为何不止一层 Θ | 批5/R1 FAIL(行话墙/步数矛盾)→整卡重写→待复审"),
    ("| c22 | 公式(1) (k-math) | HGNN 平滑层逐符号 + 2 顶点算例 | 待审",
     "| c22 | 公式(1) (k-math) | HGNN 平滑层逐符号 + 2 顶点算例 | 批5/R2 FAIL(公式先行/术语裸奔)→整卡重写(三块积木)→待复审"),
    ("| c23 | 图1 (k-fig) | 框架全景走查（KE-Phase→MDK-Fusion→iHGNN） | 待审",
     "| c23 | 图1 (k-fig) | 框架全景走查（KE-Phase→MDK-Fusion→iHGNN） | 批5/R3 FAIL(术语堆叠/hint泄题)→整卡重写(文字版总览)→待复审"),
    ("| c24 | 精讲 (k-math) | HOI-Encoder：数超边=记人脉 | 待审",
     "| c24 | 精讲 (k-math) | HOI-Encoder：数超边=记人脉 | 批5/R4 FAIL(σ不自足/答案抄例)→整卡重写(σ就地演示)→待复审"),
]
for o, n in recs:
    if o in t:
        t = t.replace(o, n, 1)
        print("ok:", o[:14])
    else:
        print("MISS:", o[:30])

lesson = u"""
## 8. 方法篇写作硬约束（批5 四卡全 FAIL 后定，批 6+ 必须遵守）

审读门四卡全部倒在同四类问题上，逐条立规：
1. **加粗定义句零行话**：允许出现的最多是一个自造的日常比喻（如"备料机器"）；KE-Phase / Θ / ρ / X_s 等一律放展开段。
2. **公式永远在符号表之后**：先"三块积木"式纯白话推演，再公式，再逐符号白话表；表内每行必须有"一句话白话"列。
3. **每个符号首现就地白话，或显式发放"本卡无需计算"许可**（如"公式仅供对照，不必计算；例 1 替你算完"）。
4. **数值题三不**：hint 不得含答案数字或中间量；answer 不得与本卡例子中已印出的数字重合；题干只问一件事。
5. **跨卡引用必须就地重述**（"第 9 卡沙盒"→ 用一行重述场景），引用外部代号（TDR/HOI/RD/DD）必须半句白话 + 卡号指路。
"""
if u"## 8. 方法篇写作硬约束" not in t:
    t = t.rstrip() + u"\n" + lesson
open(b, "w", encoding="utf-8").write(t)
print("blueprint updated")
