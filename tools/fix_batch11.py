# -*- coding: utf-8 -*-
"""批11 修复: c45 打磨 / c46 硬伤 / c47 打磨"""
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


# ===== c45 打磨 =====
rep('第 17 卡许过的愿在这里兑现：<b>过平滑的代价到底多大？</b>表 VIII 只拧一个旋钮——打分机器叠几层（2 / 4 / 6 / 8 层），看普通 HGNN、RD-HGNN、DD-HGNN 三列的准确率怎么塌。',
    '第 17 卡许过的愿在这里兑现：<b>过平滑的代价到底多大？</b>表 VIII 只拧一个旋钮——打分机器（第 22 卡那台"沿超边平均再分类"的机器）叠几层（2 / 4 / 6 / 8 层），看三个型号的准确率怎么塌：普通 HGNN（超图网络基础款）、RD-HGNN（规则账驱动版）、DD-HGNN（双驱版，第 34 卡）。', "c45-gloss-zh")
rep('Card 17\'s promise comes due here: <b>how costly is over-smoothing, really?</b> Table VIII twists one knob — how many layers the scoring machine stacks (2 / 4 / 6 / 8) — and watches plain HGNN, RD-HGNN and DD-HGNN collapse.',
    'Card 17\'s promise comes due here: <b>how costly is over-smoothing, really?</b> Table VIII twists one knob — how many layers the scoring machine (card 22\'s "average along hyperedges, then classify") stacks (2 / 4 / 6 / 8) — watching three models: plain HGNN (the basic hypergraph net), RD-HGNN (rule-ledger driven), DD-HGNN (the dual-drive, card 34).', "c45-gloss-en")
rep('<b><span class="hl">读数前记牢第 22 卡的机制：每多一层 = 多一轮"沿超边平均"。层数就是平均次数——平均越多，顶点特征越趋同（过平滑），个性越薄。</span></b>',
    '<b><span class="hl">读数前记牢第 22 卡的机制：每多一层 = 多一轮"沿超边平均"（超边＝一次把一圈顶点圈进来的"群连接"，第 22 卡讲过）。层数就是平均次数——平均越多，顶点特征越趋同（过平滑），个性越薄。</span></b>', "c45-hyperedge-zh")
rep('<b><span class="hl">Recall card 22\'s mechanism before reading: every extra layer = one more round of "averaging along hyperedges". Layers are averaging rounds — more rounds homogenize vertices (over-smoothing), thinning their individuality.</span></b>',
    '<b><span class="hl">Recall card 22\'s mechanism before reading: every extra layer = one more round of "averaging along hyperedges" (a hyperedge is a group link sweeping a whole circle of vertices at once — card 22). Layers are averaging rounds — more rounds homogenize vertices (over-smoothing), thinning their individuality.</span></b>', "c45-hyperedge-en")
rep('<b>走查 2（三列并排比"谁耐叠"）：</b>DD：',
    '<b>走查 2（三列并排比"谁耐叠"）：</b>DD（结构账＝"参加几条超边"那份账，第 24 卡）：', "c45-account-zh")

# ===== c46 硬伤 + 打磨 =====
rep('六种不同的超图网络——GCN（把超图退化当图算）、HGNN（论文的默认底座）、HGNN+（增强版 HGNN）、HNHN（超图-超边双通道）、LightHGNN（轻量蒸馏版）、AllSetTransformer（基于集合注意力）——每种都跑三行（Production / Transductive / Inductive）。',
    '六种不同的超图网络——GCN（把超图退化当图算）、HGNN（论文的默认底座）、HGNN+（增强版 HGNN）、HNHN（超图-超边双通道）、LightHGNN（"蒸馏"压缩出来的轻量版：把大模型的知识榨进小模型，具体见下文）、AllSetTransformer（基于集合注意力）——每种都跑三行：<b>Production（直推+归纳合并）、Transductive（见过人、缺答案）、Inductive（全新点）</b>（三设定的定义见第 39 卡）。', "c46-settings-zh")
rep('six different scoring machines — GCN (a hypergraph flattened to a graph), HGNN (the paper\'s default), HGNN+ (enhanced HGNN), HNHN (a vertex-edge dual channel model), LightHGNN (a lightweight distilled one), AllSetTransformer (set attention) — each run in three settings (Production / Transductive / Inductive).',
    'six scoring machines — GCN (a hypergraph flattened to a graph), HGNN (the paper\'s default), HGNN+ (enhanced HGNN), HNHN (a vertex-edge dual channel model), LightHGNN (a lightweight one squeezed out by distillation — see below), AllSetTransformer (set attention) — each run in three settings: <b>Production (transductive + inductive merged), Transductive (faces seen, answers unseen), Inductive (brand-new points)</b> (definitions at card 39).', "c46-settings-en")
rep('反面是 <b>HGNN 的 Production 行增益最小（+2.35）</b>（它本来就是这套系里结构保留较好的一款），说明"提升空间取决于底座缺什么"。',
    '反面是 <b>HGNN（六个底座里增益最小的一族：三行 +2.35 / +1.09 / +6.29——走查 1 说的"全表最小 +1.09"正是它的 Transductive 行）</b>：HGNN 本来就是这套系里结构保留较好的一款，"仓库里不缺货"，提升空间自然小——<b>提升幅度取决于底座缺什么</b>。', "c46-minfix-zh")
rep('The other extreme: <b>HGNN\'s Production row gains least (+2.35)</b> (already structure-preserving), showing that headroom depends on what a backbone lacks.',
    'The other extreme: <b>HGNN — the least-gaining family (rows +2.35 / +1.09 / +6.29; walk 1\'s "+1.09 minimum" is exactly its Transductive row)</b>. Already structure-preserving, its warehouse has little missing, so headroom is small — <b>gains track what a backbone lacks</b>.', "c46-minfix-en")
rep('复算一例：其归纳行 Origin 65.46、插账后最好 73.82，73.82 − 65.46 = <b>8.35 ✓</b>。',
    '复算一例：其归纳行 Origin 65.46、插账后最好 73.82，73.82 − 65.46 = <b>8.36</b>——表里印 +8.35（印值来自更精确的原始数据，四舍五入差 0.01，属正常）。', "c46-arithmetic-zh")
rep('recompute one: inductive Origin 65.46, plugged-in best 73.82: 73.82 − 65.46 = <b>8.35 ✓</b>.',
    'recompute one: inductive Origin 65.46, plugged-in best 73.82: 73.82 − 65.46 = <b>8.36</b> — the table prints +8.35 (its value comes from more precise raw data; a 0.01 rounding difference, nothing unusual).', "c46-arithmetic-en")
rep('为什么偏偏是"轻量版"受益最多？回到第 24/32 卡的道理：LightHGNN 靠蒸馏把大模型压小，<b>它被压掉的信息</b>恰恰包括结构细节与任务规则——而知识账正是这两样的"备份"，插回去等于把蒸馏时丢掉的部分捞回来。',
    '为什么偏偏是"轻量版"受益最多？道理在第 24/32 卡：LightHGNN 被蒸馏压缩，<b>压掉的信息</b>恰恰包括结构细节与任务规则。', "c46-split-zh")
rep('Why the lightweight one? Cards 24/32: LightHGNN is distilled small, and <b>what distillation squeezed out</b> includes exactly structural detail and task rules — the ledgers are backups of both, so plugging them in recovers the loss.',
    'Why the lightweight one? Cards 24/32: LightHGNN is distilled small, and <b>what distillation squeezed out</b> includes exactly structural detail and task rules.', "c46-split-en")
rep('（它本来就是这套系里结构保留较好的一款），说明"提升空间取决于底座缺什么"。</p>' if False else '（它本来就是这套系里结构保留较好的一款），说明"提升空间取决于底座缺什么"。',
    '（它本来就是这套系里结构保留较好的一款），说明"提升空间取决于底座缺什么"。', "c46-noop")

# ===== c47 打磨 =====
rep('六个超图数据集（转导设定），八行方法按"演进代际"排列。',
    '六个超图数据集（转导设定＝测试点训练时"见过人、缺答案"，第 38 卡），八行方法按"演进代际"排列。', "c47-trans-zh")
rep('six hypergraph datasets (transductive), eight method rows in evolutionary order.',
    'six hypergraph datasets (transductive: test points seen during training, answers withheld — card 38), eight method rows in evolutionary order.', "c47-trans-en")
rep('两个新混血型号由此登场：<b>RD-GNN = 知识账 + 普通 GNN</b>、<b>DD-GNN = 融合账 + 普通 GNN</b>（字母 G 从 HGNN 退成 GNN）。',
    '两个新"混血"型号由此登场（混血＝把知识账那一路信息和图结构那一路拼在一起打分）：<b>RD-GNN = 知识账 + 普通 GNN</b>、<b>DD-GNN = 融合账 + 普通 GNN</b>（字母 G 从 HGNN 退成 GNN——机器降级了）。', "c47-hybrid-zh")
rep('Two hybrids debut: <b>RD-GNN = rule ledger + plain GNN</b>, <b>DD-GNN = fused ledger + plain GNN</b> (the H drops out of HGNN).',
    'Two "hybrids" debut (hybrid = scoring with ledger information and graph structure glued together): <b>RD-GNN = rule ledger + plain GNN</b>, <b>DD-GNN = fused ledger + plain GNN</b> (the H drops out of HGNN — the machine got demoted).', "c47-hybrid-en")
rep('<b>The key read: even with the hypergraph machine downgraded to a plain GNN (the two hybrid rows), scores clearly beat the structure camp</b> — the ledgers do not depend on the hypergraph carrier.',
    '<b>The key read: even with the hypergraph machine downgraded to a plain GNN (the two hybrid rows), scores clearly beat the structure camp</b> — the ledgers do not depend on the hypergraph carrier.</p>\n    <p class="len"><b>A misconception worth naming here: you might assume the ledgers only work on hypergraph machines. Table X exists precisely to disprove it.</b>', "c47-mis-en")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
