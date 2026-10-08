# -*- coding: utf-8 -*-
"""批8 修复 part3: c35 打磨 + c36 替换"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
done = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND:", tag); return
    s = s.replace(o, n, 1); done.append(tag)


# ===== c35 =====
rep('<p class="len">The team is fixed as card 27\'s two trees: T₁ asks x₂ ≥ 2 (layer 0), x₁ ≥ 1 (layer 1); T₂ asks x₃ ≥ 5 (layer 0), x₁ ≥ 2 (layer 1), x₂ ≥ 1 (layer 1). <b>Predict before you touch</b> — at each change, guess which slots will move.</p>',
    '<p class="len">The team is fixed as card 27\'s two trees: T₁ asks x₂ ≥ 2 (layer 0), x₁ ≥ 1 (layer 1); T₂ asks x₃ ≥ 5 (layer 0), x₁ ≥ 2 (layer 1), x₂ ≥ 1 (layer 1).</p>\n    <p class="len"><b><span class="hl">Every rule earns two scores that multiply into its ledger slot: the content score (missed → 1, satisfied → 0) × the position score (α ÷ (its layer + β)).</span></b> The panel\'s bottom line “Cr = 5, dim(Z) = 10” reads: five rules in total, ten slots in the final feature. <b>Predict before you touch</b> — at each change, guess which slots will move.</p>', "c35-formula-en")
rep('树队固定为第 27 卡那两棵：T₁ 问 x₂ ≥ 2（第 0 层）、x₁ ≥ 1（第 1 层）；T₂ 问 x₃ ≥ 5（第 0 层）、x₁ ≥ 2（第 1 层）、x₂ ≥ 1（第 1 层）。<b>先预测再动手</b>——每改一次滑块，先猜猜哪几格会变。</p>',
    '树队固定为第 27 卡那两棵：T₁ 问 x₂ ≥ 2（第 0 层）、x₁ ≥ 1（第 1 层）；T₂ 问 x₃ ≥ 5（第 0 层）、x₁ ≥ 2（第 1 层）、x₂ ≥ 1（第 1 层）。</p>\n    <p class="lz"><b><span class="hl">每条规则得两个分，相乘就是账里那一格：内容分（不满足记 1、满足记 0）× 位置分（总幅度 α ÷（所在层 + 缓冲 β））。</span></b>面板底部那行“Cr = 5、Z 的维数 = 10”读作：规则共 5 条、最终特征共 10 格。<b>先预测再动手</b>——每改一次滑块，先猜猜哪几格会变。</p>', "c35-formula-zh")
rep('三个滑块给顶点设定特征 (x₁, x₂, x₃)', '三个滑块给每个对象（顶点）设定特征 (x₁, x₂, x₃)', "c35-vertex-zh")
rep('three sliders set the vertex\'s features (x₁, x₂, x₃)', 'three sliders set each object\'s (vertex\'s) features (x₁, x₂, x₃)', "c35-vertex-en")
rep('对照上方账本：T₁ 两格（0、0，两条都被满足）；T₂ 三格（1.125、1.0、0）。与第 31 卡例 1 的数字逐一对上——面板和笔算应当一字不差。',
    '对照下方账本：T₁ 两格（0、0，两条都被满足）；T₂ 三格（1.125、1.0、0）。与这里给出的数字逐一对上——面板和笔算应当一字不差。', "c35-task1-zh")
rep('Check the panel: T₁\'s two slots (0, 0 — both satisfied); T₂\'s three (1.125, 1.0, 0). Match them against card 31\'s Example 1 — the panel and your hand work should agree digit for digit.',
    'Check the panel: T₁\'s two slots (0, 0 — both satisfied); T₂\'s three (1.125, 1.0, 0). Match them against the numbers given right here — panel and hand work should agree digit for digit.', "c35-task1-en")
rep('观察深层格子（第 1 层的三格）：分母变小，位置分集体变大——规则的"轻重差"被拉开了。',
    '观察第 1 层三条规则的<b>位置分</b>（面板上每条规则旁标着 μp=…）：分母变小，三个位置分一起变大——账本里被满足的格子仍是 0，动的只是"位置分"这一栏。', "c35-task3-zh")
rep('Watch the deeper slots (layer-1\'s three): smaller denominator lifts all positions — the weight spread widens.',
    'Watch the <b>position scores</b> of the three layer-1 rules (each rule chip shows μp=…): a smaller denominator lifts all three — satisfied slots stay 0; only the "position" column moves.', "c35-task3-en")

# ===== c36 替换 =====
i = s.find('<!-- ============ c36 ')
j = s.find('<!-- NEXT-CARD -->', i)
assert i > 0 and j > i
new36 = open("decomposition/feng-2026-knowledge-hgnn/cards/c36.html", encoding="utf-8").read()
s = s[:i] + new36 + "\n" + s[j:]
done.append("c36-replaced")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
