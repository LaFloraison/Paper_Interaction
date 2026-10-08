# -*- coding: utf-8 -*-
"""批3 修复 part 3: 清除旧英文残留 + c12 data-kp + c13 选项文字/callout"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
applied = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND (" + tag + ")")
        return
    s = s.replace(o, n, 1)
    applied.append(tag)


# --- c12: 删除旧英文段 (boosting/gradient 旧版) ---
rep('<p class="len">This relay is called <b>boosting</b>; "gradient" means each new tree fits the steepest error-descent direction (one link to what you may know: gradient descent takes small steps in <b>parameters</b>, gradient boosting adds a small <b>tree</b> — both rely on small steps to stay safe; card 13 has the full recap).</p>\n',
    "", "c12-del-old-en-1")

# --- c12: 删除旧英文例2 段 ---
rep('<p class="len"><b>Example 2 (keep relaying):</b> still short by 80 − 52.5 = 27.5. Tree h₂ learns "+27": f₂ = 52.5 + 0.1 × 27 = 52.5 + 2.7 = <b>55.2</b>. Each tree moves 2.7 — that is ε\'s discount: slow, but every step is double-checked by ten trees. At this pace, if every tree corrected 27, after 10 trees: 52.5 + 10 × 2.7 = <b>79.5 ≈ 80</b>, arrived. (In real training the residual shrinks, and later trees\' opinions shrink with it.)</p>\n',
    "", "c12-del-old-en-2")

# --- c12: 移除 a 卡上的 data-kp (真正执行) ---
rep('<section class="card" data-c="12" data-kp="kp-gbdt" data-title-zh="一般理论 · 梯度提升决策树 GBDT（论文之外）"',
    '<section class="card" data-c="12" data-title-zh="一般理论 · 梯度提升决策树 GBDT（论文之外）"', "c12-del-datakp")

# --- c13: 删除旧英文加粗定义段 ---
rep('<p class="len"><b><span class="hl">The paper\'s usage = treat the trained GBDT as a rule mine: pre-train → get T = {T₁,…,T_K} → one rule per inner node → feed the TDR-Encoder (the raw material for Eqs. 4–8).</span></b></p>\n',
    "", "c13-del-old-en-bold")

# --- c13: Q3 正确选项文字 (中英) 去残差 ---
rep('<span class="lz">第一棵树的根先摘走最大的残差，与目标绑定最紧</span><span class="len">The first tree\'s root takes the biggest residual, binding most tightly to the target</span>',
    '<span class="lz">第一棵树的根先摘走上一轮没算对的最大误差，与目标绑定最紧</span><span class="len">The first tree\'s root takes the biggest remaining error, binding most tightly to the target</span>', "c13-q3-opt")

# --- c13: Q3 错误项解析软点 ---
rep("正确！第一轮要纠的误差最大，第一棵树的根一刀切走最大的一块——根规则与目标绑定最紧。",
    "正确！第一轮要纠的误差最大，第一棵树的根一刀切走上一轮没算对的最大一块——根规则与目标绑定最紧。", "c13-q3-expl")

# --- c13: 回顾 callout "上一卡" ---
rep("记住这个对照，式 (2) 的 ε 就是两种\"小步\"共用的时间表。",
    "记住这个对照，上一卡式 (2) 里的 ε，就是两种\"小步\"共用的时间表。", "c13-callout-zh")
rep("Eq. (2)'s ε is the timetable both \"small steps\" share.",
    "the last card's Eq. (2) ε is the timetable both \"small steps\" share.", "c13-callout-en")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(applied))
for a in applied:
    print(" -", a)
