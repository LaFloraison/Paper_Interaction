# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

b = "decomposition/feng-2026-knowledge-hgnn/blueprint.md"
t = open(b, encoding="utf-8").read()

pairs = [
    ("| c10 | a 卡 (k-pre) | kp-decision-tree 一般理论：20 问游戏/内部节点/深度 | 待审",
     "| c10 | a 卡 (k-pre) | kp-decision-tree 一般理论：20 问游戏/内部节点/深度 | 批3/R1 FAIL→修（sol深度笔误/属性白话/例2补深度走查）→待重审"),
    ("| c11 | b 卡 (k-pre, data-kp) | 本文 O_in 内部节点集、d(o) 深度、规则 r_o | 待审",
     "| c11 | b 卡 (k-pre, data-kp) | 本文 O_in 内部节点集、d(o) 深度、规则 r_o | 批3/R2 PASS（修：树结构半句/重训调和/例2前向压缩）"),
    ("| c12 | a 卡 (k-pre, data-kp) | kp-gbdt 一般理论：函数空间逐步纠错（式 2 一般形态） | 批3/R3 待审",
     "| c12 | a 卡 (k-pre) | kp-gbdt 一般理论：函数空间逐步纠错（式 2 一般形态） | 批3/R3 FAIL→修（术语拆段/残差注释/计数歧义/坏干扰项）→待重审；data-kp 移至 c13"),
    ("| c13 | b 卡 (k-pre, data-kp) | 本文 GBDT 预训练→产树 T={T1..TK} 当“规则提取器” | 批3/R4 待审",
     "| c13 | b 卡 (k-pre, data-kp) | 本文 GBDT 预训练→产树 T={T1..TK} 当“规则提取器” | 批3/R4 FAIL→修（定义去行话/2^4-1推导/换数值题/RD·DD交代）→待重审；承接 kp-gbdt 锚点"),
]
for o, n in pairs:
    if o in t:
        t = t.replace(o, n, 1)
        print("ok:", o[:24])
    else:
        print("MISS:", o[:40])
open(b, "w", encoding="utf-8").write(t)
