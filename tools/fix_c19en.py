# -*- coding: utf-8 -*-
"""c19: 三处 EN 机械同步（重跑，前次因异常未写盘）"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
done = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND:", tag)
        return
    s = s.replace(o, n, 1)
    done.append(tag)


# 1. 例2 EN 术语铺垫
rep("the TDR-Encoder's GBDT pre-trains on a \"predefined task\" — if that pre-training peeked",
    "the GBDT from the prereq cards (cards 12–13, the relay team of error-correcting trees) pre-trains on a \"predefined task\" (a prediction task fixed in advance); the resulting rules are encoded into a vector by the TDR-Encoder (the protagonist of the method part, detailed in card 27) — this is the paper's \"knowledge embedding\" — if that pre-training peeked",
    "c19-en-ex2")

# 2. 例1 EN 补自检两行
rep("but 406 splits into transductive 244 + inductive 162; during training",
    "but 406 splits into transductive 244 + inductive 162 (two self-checks: 1,625 + 677 + 406 = 2,708 ✓; 244 + 162 = 406 ✓); during training",
    "c19-en-checks")

# 3. production EN 补 162 括注
rep("and 20% V<sub>i</sub> (inductive: these points are hidden from training <b>together with their edges</b>",
    "and 20% V<sub>i</sub> (inductive: these points — 20% of the tests, 162 papers on Cora — are hidden from training <b>together with their edges</b>",
    "c19-en-paren")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
