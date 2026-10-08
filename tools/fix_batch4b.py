# -*- coding: utf-8 -*-
"""批4 修复 part 2: 清占位符 + 剩余未命中项"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
applied = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND (" + tag + "): " + o[:60])
        return
    s = s.replace(o, n, 1)
    applied.append(tag)


# --- c17: 修占位符 + 双 </p> → 正式 EN 句 ---
rep("</p><p class=\"len\">…EN…</p></p>\n",
    "", "c17-placeholder-remove")
rep("DD-HGNN (both archives on board) falls only 76.06 → <b>49.53</b> over the same range: not immune, but the two un-smoothed streams hold the floor.</p>",
    "The paper's dual-stream model DD-HGNN (properly introduced at card 34, both archives on board) falls only 76.06 → <b>49.53</b> over the same range — a 26.53 drop, about six-tenths of HGNN's 43.19: not immune, but the two un-smoothed streams hold the floor.</p>", "c17-dd-gloss-en")

# --- c17: 平滑函数值 ---
rep("直接把 6（或它的平滑函数值）放进一份<b>不参与平滑</b>的向量。",
    "直接把 6（或它经一层变换后的值）放进一份<b>不参与平滑</b>的向量。", "c17-ex1-fix2")
rep("put the 6 (or its smoothed value) into a vector that <b>never participates in smoothing</b>",
    "put the 6 (or its value after one transform) into a vector that <b>never participates in smoothing</b>", "c17-ex1-fix2-en")

# --- c14: 剩余 ---
rep("order changed, answer changed, not invariant.",
    "the order changed and so did the answer — not invariant.", "c14-typo-en")
o = s.find("的主场，体育比赛")
seg = s[max(0, o - 40):o]
print("c14-sums context:", repr(seg))
rep("结账小票是\"求和\"的主场", "结账小票是“求和”的主场", "c14-sums-try1")
rep("结账小票是 sums 的主场", "结账小票是“求和”的主场", "c14-sums-try2")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(applied))
for a in applied:
    print(" -", a)
