# -*- coding: utf-8 -*-
"""批8 修复 part2: c34"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = "sites/feng-2026-knowledge-hgnn.html"
s = open(p, encoding="utf-8").read()
done = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND:", tag); return
    s = s.replace(o, n, 1); done.append(tag)


# ① 例 2 开头补 Table V 单位口径 + ② CC-Cora 两数 + ⑥ 破误解
rep('<b>例 2（论文实测的选型规律——Table V 真实数字）：</b>看"DD 减 RD"在十数据集上的符号：图数据集上全是负的——Cora 上 RD 88.64、DD 87.22（<b>DD 反而低 1.42</b>）、Github、Amazon-P、Amazon-C 同样 RD 略胜；超图数据集上全是正的——CA-Cora 上 DD 79.75、RD 79.36（<b>DD 高 0.39</b>）、CC-Cora 上 DD 更是高出 <b>1.76</b>。规律一句话：<b>结构越复杂（超边的世界），双驱越占便宜；关系越简单（两两边就够），单驱反而更利落。</b>',
    '<b>例 2（论文实测的选型规律——Table V 真实数字）：</b>先交代口径：Table V 是论文在十数据集上的<b>分类准确率对照表（单位 %，越大越好）</b>；下面比较的是 DD 减 RD 的差值。图数据集上差值全为负——Cora：RD 88.64、DD 87.22（<b>DD 反而低 1.42</b>），Github、Amazon-P、Amazon-C 同样 RD 略胜；超图数据集上全为正——CA-Cora：DD 79.75、RD 79.36（<b>DD 高 0.39</b>），CC-Cora：DD 76.06、RD 74.30（<b>高 1.76</b>）。<br><b>顺手破一个直觉误解：很多人以为“多喂一路结构信息只会更好”——Cora 却显示 DD 反而低 1.42。</b>规律一句话：<b>结构越复杂（超边的世界），双驱越占便宜；关系越简单（两两成对就够），单驱反而更利落。</b>', "c34-ex2-zh")
rep('<b>Example 2 (the paper\'s selection pattern — real Table V numbers):</b> watch the sign of "DD − RD" across the ten datasets: negative on every graph dataset — on Cora, RD 88.64 vs DD 87.22 (<b>DD lower by 1.42</b>), with Github, Amazon-P, Amazon-C likewise slightly favoring RD; positive on every hypergraph dataset — CA-Cora: DD 79.75 vs RD 79.36 (<b>DD higher by 0.39</b>), CC-Cora\'s gap reaching <b>1.76</b>. One line: <b>the richer the structure (hyperedges), the more the dual-drive pays; the simpler the relations (pairwise suffices), the leaner single-drive wins.</b>',
    '<b>Example 2 (the paper\'s selection pattern — real Table V numbers):</b> the convention first: Table V is the paper\'s <b>classification-accuracy comparison across ten datasets (unit %, higher is better)</b>; what follows compares DD minus RD. On graph datasets every gap is negative — Cora: RD 88.64 vs DD 87.22 (<b>DD lower by 1.42</b>), with Github, Amazon-P, Amazon-C likewise favoring RD; on hypergraph datasets all positive — CA-Cora: DD 79.75 vs RD 79.36 (<b>higher by 0.39</b>), CC-Cora: DD 76.06 vs RD 74.30 (<b>higher by 1.76</b>).<br><b>One intuition worth breaking here: many assume “an extra structural stream can only help” — Cora shows DD lower by 1.42.</b> One line: <b>the richer the structure (hyperedges), the more the dual-drive pays; the simpler the relations (pairwise suffices), the leaner single-drive wins.</b>', "c34-ex2-en")

# ③ 是什么段补 HGNN/H/Z 白话
rep("备料车间全部完工：规则账 X<sub>r</sub>（5 格）与融合账 Z（10 格）都造好了；打分机器（HGNN，第 22 卡）和超图结构 H 一直没变。剩下的只是<b>装料选择</b>——喂哪一本给机器。",
    "备料车间全部完工：规则账 X<sub>r</sub>（5 格）与融合账 Z（10 格，第 33 卡）都造好了；那台打分机器（第 22 卡的 HGNN：顺着超图反复平均、再分类的机器）和它脚下的关系网（编组表 H：谁在哪个组）一直没变。剩下的只是<b>装料选择</b>——喂哪一本给机器。", "c34-gloss-zh")
rep("The prep floor is finished: rule ledger X<sub>r</sub> (5 slots) and fused ledger Z (10 slots) both built; the scoring machine (HGNN, card 22) and the hypergraph H never changed.",
    "The prep floor is finished: rule ledger X<sub>r</sub> (5 slots) and fused ledger Z (10 slots, card 33) both built; the scoring machine (card 22's HGNN: averages along the hypergraph, then classifies) and the relation web under it (the roster H: who sits in which group) never changed.", "c34-gloss-en")

# ④⑤ 数值题换题 + 去泄题 hint
rep('data-answer="5" data-tol="0.01" data-hint="DD 的料比 RD 的料多出“另一半”——想想 10 格与 5 格差在哪里（第 33 卡的 Z 配方）。" data-sol="DD 输入 10 格、RD 输入 5 格 → 多出 5 格（正是被结构加权过的那一份 X̃r）。"',
    'data-answer="-0.46" data-tol="0.02" data-hint="翻到 Table V 原图，找 Amazon-C 那一行：按“DD 减 RD”的差口径相减（注意符号）。" data-sol="91.57 − 92.03 = −0.46：图数据集上 DD 又输给了 RD——与 Cora 的 −1.42 同一方向，且这回两数都印在你眼前的表里。"', "c34-quiz-attrs")
rep('<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：DD-HGNN 的输入比 RD-HGNN 多几格？</span><span class="len">Numeric: how many slots does DD-HGNN\'s input hold beyond RD-HGNN\'s?</span></p>',
    '<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：用 Table V，"DD 减 RD"在 Amazon-C 上的差值是多少个百分点（两位小数，含符号）？</span><span class="len">Numeric: from Table V, what is "DD minus RD" on Amazon-C, in points (two decimals, sign included)?</span></p>', "c34-quiz-q")

open(p, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
