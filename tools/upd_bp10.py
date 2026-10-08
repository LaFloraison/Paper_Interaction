# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

b = "decomposition/feng-2026-knowledge-hgnn/blueprint.md"
t = open(b, encoding="utf-8").read()

r = [
    ("| c41 | Table V (k-fig) | 主结果 transductive；平均排名 RD 1.7 / DD 1.5（复算验证） | 待审",
     "| c41 | Table V (k-fig) | 主结果 transductive；平均排名 RD 1.7 / DD 1.5（复算验证） | 批10/R1 PASS（打磨：种子白话/复算口径/加粗示范）"),
    ("| c42 | Table VI (k-fig) | production；7.30 的出处行；Δ 列=max(RD,DD)−基线 | 待审",
     "| c42 | Table VI (k-fig) | production；7.30 的出处行；Δ 列=max(RD,DD)−基线 | 批10/R2 PASS（打磨：四族列名对号/max 规则落地/footer 口径）"),
    ("| c43 | 图3 (k-fig) | 消融三联：α 不敏感/β 低值 RD 崩/噪声鲁棒 | 待审",
     "| c43 | 图3 (k-fig) | 消融三联：α 不敏感/β 低值 RD 崩/噪声鲁棒 | 批10/R3 PASS（打磨：消融白话/正态噪声白话/β 方向与端点值）"),
    ("| c44 | Table VII (k-fig) | 树数消融；正文“DD 峰在 150”与表不符（峰在 50） | 待审",
     "| c44 | Table VII (k-fig) | 树数消融；正文“DD 峰在 150”与表不符（峰在 50，已回原文核实） | 批10/R4 FAIL(三列只走两列/差值无算式/术语裸用)→修→待复审"),
]
for o, n in r:
    if o in t:
        t = t.replace(o, n, 1)
        print("ok:", o[:14])
    else:
        print("MISS:", o[:32])

lesson = u"""
## 9. 展品卡（图/表）写作补充约束（批 9-10 后定）
1. **表的每一列都要走查，或显式声明省略**（批 10 c44 教训：三列只走两列 = B4 硬伤）。
2. **差值必须给算式**（"+2.73" 要写成 "75.70 − 72.97 = +2.73"）。
3. **列名/行名中的术语首现即白话**（学习率/隐层维度/基线/消融/重复实验波动/四族方法名）。
4. **答案与例子的隔离**：读数题的答案数字（及其两端读数）不得在走查中印出——端点可留白交给习题（c43/c44 的"下一题请你亲手量"式脚手架效果好）。
5. **对论文正文的指控性断言必须先回原文逐字核实**，并在卡内注明"已回原文核对"。
"""
if u"## 9. 展品卡（图/表）写作补充约束" not in t:
    t = t.rstrip() + u"\n" + lesson
open(b, "w", encoding="utf-8").write(t)
print("blueprint updated")
