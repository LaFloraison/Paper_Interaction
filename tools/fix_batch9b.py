# -*- coding: utf-8 -*-
"""批9 修复: c40"""
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


# 定义句去行话 + 白话盒
rep('<b><span class="hl">表 IV 是复现实验的钥匙：每个数据集一行，记着训练用的全部可调项——学习率、树队的棵数、隐层维度、树的最大深度，以及位置公式的两个旋钮 α、β。</span></b>表 I/II/III 描述"考什么、怎么切"，这张表描述"怎么练"。',
    '<b><span class="hl">表 IV 是每个数据集一行的"训练配方卡"：把训练时要拧的每一个旋钮都记下来，照着一行就能把实验原样重跑。</span></b>表 I/II/III 描述"考什么、怎么切"，这张表描述"怎么练"。</p>'
    '<p class="lz">配方里的旋钮逐一向白话（不认识的先看这里）：<b>学习率</b>=每次修正模型时"一步迈多大"（太大容易跳过头、太小走得慢）；<b>树数</b>=接力纠错树队有几棵（第 12 卡）；<b>隐层维度</b>=模型内部"加工站"同时并行处理几个特征（一层里排多少个格子）；<b>最大深度</b>=每棵树最多问到第几层（第 10 卡）；<b>α、β</b>=位置公式 μ<sub>p</sub>(o) = α ÷ (d(o) + β) 的两个旋钮（α 整体抬高或压低权重曲线、β 决定衰减多快，第 30 卡）。', "c40-bold-zh")
rep('<b><span class="hl">Table IV is the reproducibility key: one row per dataset recording every tunable in training — learning rate, number of trees, hidden width, tree depth, and the position formula\'s two knobs α, β.</span></b>',
    '<b><span class="hl">Table IV is a "training recipe card" per dataset: every knob turned during training is written down, so one row re-runs the experiment as-is.</span></b></p>'
    '<p class="len">The knobs in plain words (start here if they are new): <b>learning rate</b> = how big a step each correction takes (too big overshoots, too small crawls); <b>number of trees</b> = how many relay trees (card 12); <b>hidden width</b> = how many features the model\'s inner "processing station" handles in parallel (slots per layer); <b>max depth</b> = how deep each tree may ask (card 10); <b>α, β</b> = the two knobs of μ<sub>p</sub>(o) = α ÷ (d(o) + β) (α raises or lowers the weight curve; β sets the decay speed — card 30).', "c40-bold-en")

# 补两列纵向走查 + 修正“不重样”
rep('最后看 α、β：每一行都不重样（10/6、9/8、6/6、6/10……）——这两只旋钮是逐数据集网格搜索出来的（第 30 卡提过），因为树的深度分布各数据集不同。',
    '再把剩下两列也竖着读一遍：<b>学习率</b>在 0.1 到 0.6 之间浮动（Tencent 最小 0.1、Cora 最大 0.6）；<b>最大深度</b>从 3（多数数据集）到 7（Github）——深树用于关系更缠绕的数据。最后看 α、β 这对组合：十行里九种都不同（10/6、9/8、6/6、6/10……），只有 Github、CC-Cora、Heloc 三家恰好都落在 9/8 上——这两只旋钮是逐数据集网格搜索（把候选值两两配成表、挨个试一遍挑最好）出来的，因为各数据集的树形深浅不同。', "c40-walk2-zh")
rep('Finally α, β: no two rows repeat (10/6, 9/8, 6/6, 6/10 …) — the two knobs came from per-dataset grid search (noted at card 30), because tree-depth profiles differ across datasets.',
    'Now read the last two columns vertically too: <b>learning rate</b> floats between 0.1 and 0.6 (Tencent lowest, Cora highest); <b>max depth</b> ranges from 3 (most datasets) to 7 (Github) — deeper trees for more tangled relations. Finally the α, β pair: nine of ten rows differ (10/6, 9/8, 6/6, 6/10 …); only Github, CC-Cora and Heloc happen to share 9/8 — the pair came from per-dataset grid search (pair the candidates up on a table and try them one by one), because tree-depth profiles differ across datasets.', "c40-walk2-en")

# 走查 1 补公式就地
rep('学习率 0.4；树 140 棵；隐层 128 维；最大深度 3；<b>α = 9、β = 8</b>——正是第 30 卡例 1 用过的那组！回看那张小表：第 0 层权重 9÷8 = 1.125、第 2 层 9÷10 = 0.9——你当时算的数就是从这一行取的。',
    '学习率 0.4；树 140 棵；隐层 128 维；最大深度 3；<b>α = 9、β = 8</b>。把 α、β 代进上面那条公式（层号 d 从 0 起）：第 0 层权重 = 9 ÷ (0+8) = 1.125、第 2 层 = 9 ÷ (2+8) = 0.9——正是第 30 卡例 1 算过的那两个数！', "c40-walk1-zh")
rep('learning rate 0.4; 140 trees; 128 hidden units; max depth 3; <b>α = 9, β = 8</b> — card 30\'s Example 1 exactly! Look back at that little table: layer 0 weighs 9÷8 = 1.125, layer 2 weighs 0.9 — the numbers you computed came from this row.',
    'learning rate 0.4; 140 trees; 128 hidden units; max depth 3; <b>α = 9, β = 8</b>. Feed α, β into the formula above (layer d from 0): layer 0 weighs 9 ÷ (0+8) = 1.125, layer 2 weighs 9 ÷ (2+8) = 0.9 — exactly card 30\'s Example 1 numbers!', "c40-walk1-en")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
