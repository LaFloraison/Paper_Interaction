# -*- coding: utf-8 -*-
"""批10 修复: c41 打磨 / c42 打磨 / c43 打磨 / c44 硬伤"""
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


# ===== c41 =====
rep('① <b>± 后面的数</b>是五次不同随机种子的波动（第 20 卡的规矩）——两方法之差若小于波动，就不该当真；',
    '① <b>± 后面的数</b>是"重复实验的晃动幅度"：同一设置用五个随机起点各跑一遍（像考试前掷五次骰子定座位），五次成绩的高低差就是 ±——两方法之差若小于晃动，就不该当真；', "c41-seed-zh")
rep('(1) the number after <b>±</b> is the spread over five random seeds (card 20\'s rule) — a gap smaller than the spread should not be taken seriously;',
    '(1) the number after <b>±</b> is the run-to-run wobble: the same setup repeated from five random starting points (like dice-decided seating across five exams); a gap smaller than the wobble should not be taken seriously;', "c41-seed-en")
rep('平均排名：MLP 5.8、GCN 3.9、GBDT 5.1、HGNN 3.3、TLF 6.1、<b>RD 1.7、DD 1.5</b>——本文两个型号分列第一、第二。我们复算了这张排名表：RD 十行名次之和 = 17（均值 1.7 ✓）、DD = 15（1.5 ✓）。',
    '平均排名：MLP 5.8、GCN 3.9、GBDT 5.1、HGNN 3.3、TLF 6.1、<b>RD 1.7、DD 1.5</b>——本文两个型号分列第一、第二。（顺带示范"加粗"这条读表工具：Cora 行里 RD 88.64 就是加粗的——它是该行最优；下划线标次优。）我们复算了这张排名表：把 RD 在十个数据集里各自排第几列出来相加除以 10，得 17/10 = 1.7 ✓、15/10 = 1.5 ✓。', "c41-rank-zh")
rep('average ranks: MLP 5.8, GCN 3.9, GBDT 5.1, HGNN 3.3, TLF 6.1, <b>RD 1.7, DD 1.5</b> — the paper\'s two models place first and second. We recomputed this rank table: RD\'s ten ranks sum to 17 (mean 1.7 ✓), DD to 15 (1.5 ✓).',
    'average ranks: MLP 5.8, GCN 3.9, GBDT 5.1, HGNN 3.3, TLF 6.1, <b>RD 1.7, DD 1.5</b> — the paper\'s two models place first and second. (Demonstrating tool (2) while at it: in the Cora row, RD 88.64 is the bolded best; the underline marks runner-up.) We recomputed the rank row by listing each method\'s rank in every dataset, summing and dividing by ten: 17/10 = 1.7 ✓, 15/10 = 1.5 ✓.', "c41-rank-en")
rep('复算 DD 列十行均值 87.648 减 GBDT 均值 81.792 = <b>5.86 ✓</b>（口径 = DD 对 GBDT）。',
    '复算"平均增益"：把 DD 列十格逐一相加除以 10 得均值 87.648、GBDT 列同样处理得 81.792，两者相减 = <b>5.86 ✓</b>（口径 = DD 对 GBDT）。', "c41-gain-zh")
rep('DD\'s column mean 87.648 minus GBDT\'s 81.792 = <b>5.86 ✓</b> (DD-versus-GBDT convention).',
    'the "average gain": sum DD\'s ten cells and divide by ten (mean 87.648), likewise GBDT (81.792), subtract = <b>5.86 ✓</b> (DD-versus-GBDT convention).', "c41-gain-en")

# ===== c42 =====
rep('方法分四族：纯特征派（MLP、GBDT）、结构派（GCN、HGNN）、树网混合（TLF）、本文（RD-HGNN、DD-HGNN）。',
    '方法分四族（列名逐一对号）：纯特征派 <b>MLP</b>（多层感知机）与 <b>GBDT</b>（梯度提升树，第 12 卡）、结构派 <b>GCN</b>（经典图卷积网）与 <b>HGNN</b>（超图卷积，第 22 卡）、树网混合 <b>TLF</b>、本文 <b>RD</b>（规则驱动）与 <b>DD</b>（双驱）——后两个即第 34 卡两个型号。', "c42-roles-zh")
rep('The methods fall into four camps: feature-only (MLP, GBDT), structure-only (GCN, HGNN), tree-net hybrid (TLF), and this paper (RD-HGNN, DD-HGNN).',
    'Four camps, column by column: feature-only <b>MLP</b> (multilayer perceptron) and <b>GBDT</b> (gradient-boosted trees, card 12); structure-only <b>GCN</b> (classic graph convolution) and <b>HGNN</b> (hypergraph convolution, card 22); the tree-net hybrid <b>TLF</b>; and this paper\'s <b>RD</b> (Rule-Driven) with <b>DD</b> (Dual-Driven) — card 34\'s two models.', "c42-roles-en")
rep('Production：RD <b>88.25</b>、HGNN 81.91 → ΔHGNN = 6.34；',
    'Production：RD <b>88.25</b>、DD 86.48——取大者 RD（88.25 > 86.48，这就是 Δ 规则"取 max"的落地步骤）、HGNN 81.91 → ΔHGNN = 88.25 − 81.91 = 6.34；', "c42-walk1-zh")
rep('Production: RD <b>88.25</b>, HGNN 81.91 → ΔHGNN = 6.34;',
    'Production: RD <b>88.25</b>, DD 86.48 — take the larger, RD (88.25 > 86.48: the "max" rule in action), vs HGNN 81.91 → ΔHGNN = 88.25 − 81.91 = 6.34;', "c42-walk1-en")
rep('我们把 Production 十行复算：ΔGBDT 均值 5.94、ΔHGNN 均值 2.72——<b>两个都不完全对得上</b>（差 0.2–0.4）。',
    '我们把 Production 十行的 Δ 列逐行相加再平均（十个数据集的行值见原图）：得 ΔGBDT 均值约 5.9、ΔHGNN 均值约 2.7——<b>与表底印的 6.31 / 2.53 都不完全对得上</b>（差 0.2–0.4）。', "c42-footer-zh")
rep('we recomputed the ten Production lines: ΔGBDT mean 5.94, ΔHGNN mean 2.72 — <b>neither matches exactly</b> (off by 0.2–0.4).',
    'we summed the ten Production Δ cells and averaged (row values in the original table): ΔGBDT ≈ 5.9, ΔHGNN ≈ 2.7 — <b>neither matches the printed 6.31 / 2.53 exactly</b> (off by 0.2–0.4).', "c42-footer-en")

# ===== c43 =====
rep('它们回答同一类问题：<b>把某个因素从很小调到很大，成绩会怎么动？</b>三个子图的横轴分别是 α（1→10）、β（1→10）、噪声比例（0→80%）。',
    '这种"拧掉或拧动一个因素、看成绩怎么动"的做法叫<b>消融</b>。三个子图回答同一类问题：<b>把某个因素从很小调到很大，成绩会怎么动？</b>横轴分别是 α（1→10）、β（1→10）、噪声比例（0→80%）。', "c43-ablation-zh")
rep('All three answer one kind of question: <b>sweep a factor from tiny to huge — how do scores move?</b> The x-axes are α (1→10), β (1→10), and noise ratio (0→80%).',
    'Twisting or removing one factor and watching the scores is called an <b>ablation</b>. The three panels answer one kind of question: <b>sweep a factor from tiny to huge — how do scores move?</b> The x-axes are α (1→10), β (1→10), and noise ratio (0→80%).', "c43-ablation-en")
rep('<b>走查 2（中格 (b)：β 一拧，红线跳水）：</b>β 从 10 减到 1，<b>红线（RD）明显下坠</b>——β = 1 时它掉到五成上下；而黑线（DD）基本守住 76 一线。两线在低 β 区张开约 20–25 个点（正文说"约 10 个百分点"，图上按横轴刻度估算更大——这类"读图约值"与正文数不一致时，以你自己量的为准并记账，第 48 卡）。',
    '<b>走查 2（中格 (b)：β 从高（10）往低（1）拧，红线跳水）：</b><b>红线（RD）明显下坠</b>——β = 1 时它掉到约 52；而黑线（DD）基本守住 76 一线。两线在低 β 区张开约 24 个点。顺带记账：正文说"DD 在低 β 时比 RD 高约 10 个百分点"，按图上刻度读出的差距更大——这类"正文数字 vs 读图约值"的出入记入第 48 卡（本卡读数均为近似读图，误差以横轴小格为准）。', "c43-walk2-zh")
rep('<b>Walk 2 (middle panel (b): twist β, the red line dives):</b> dropping β 10→1, <b>red (RD) plunges</b> — near five-tens at β = 1 — while black (DD) holds around 76. The two pull apart by roughly 20–25 points at low β (the text says "about 10 percentage points"; estimating from the axis the gap looks larger — when read-off values clash with the text, trust your own measurement and keep the account; card 48).',
    '<b>Walk 2 (middle panel (b): twist β from high (10) down to 1 — the red line dives):</b> <b>red (RD) plunges</b> — about 52 at β = 1 — while black (DD) holds near 76. At low β the two pull apart by roughly 24 points. An account to keep: the text says "DD beats RD by about 10 percentage points at low β", while the axis reads a wider gap — such text-versus-read-off gaps go to card 48 (all readings here are approximate, measured in axis ticks).', "c43-walk2-en")
rep('ε 是均值 0、波动 0.5 的正态噪声',
    'ε 是"钟形抖动"式的随机噪声（正态噪声：多数时候抖得小、偶尔很大；均值 0、波动幅度 0.5）', "c43-noise-zh")
rep('ε normal noise, mean 0, spread 0.5',
    'ε bell-shaped jitter (normal noise: mostly small, occasionally large; mean 0, spread 0.5)', "c43-noise-en")

# ===== c44 =====
rep('表 VII 只变一个量：树队的棵数（5、10、50、100、150、200），看它如何影响 GBDT 基线与本文两个型号的准确率——回答"规则账该多长"。',
    '表 VII 只变一个量：树队的棵数（5、10、50、100、150、200），看它如何影响 GBDT 基线（第 12 卡的树队本身，不带任何图结构）与本文两个型号（RD = 规则驱动、DD = 双驱，第 34 卡）的准确率——回答"规则账该多长"。', "c44-terms-zh")
rep('Table VII varies one quantity only: the number of trees (5, 10, 50, 100, 150, 200), tracking its effect on the GBDT baseline and the two models — answering "how long should the rule ledger be".',
    'Table VII varies one quantity only: the number of trees (5, 10, 50, 100, 150, 200), tracking its effect on the GBDT baseline (card 12\'s tree team, no graph structure attached) and the two models (RD = Rule-Driven, DD = Dual-Driven, card 34) — answering "how long should the rule ledger be".', "c44-terms-en")
rep('数据集固定为 CC-Cora（消融实验的常驻考场），六行 × 三列，加粗标每行最优。',
    '数据集固定为 CC-Cora（消融——"拧动一个因素看成绩怎么动"的对照实验——的常驻考场），六行 × 三列，加粗标每行最优。', "c44-ablation-zh")
rep('The dataset is CC-Cora (the ablation\'s standing venue); six rows × three columns, bold marks each row\'s best.',
    'The dataset is CC-Cora (the standing venue for ablations — controlled runs that twist one factor and watch the score); six rows × three columns, bold marks each row\'s best.', "c44-ablation-en")
rep('① 5 → 50 棵，+2.73——规则矿越挖越富，规则账从短变长，知识越来越全；② 50 → 200 棵，−4.21——开始"接力过头"（第 12 卡的坑）：后面的树在纠缠训练集的巧合，规则账里掺进了噪声规则。',
    '① 5 → 50 棵：75.70 − 72.97 = <b>+2.73</b>——规则矿越挖越富，规则账从短变长，知识越来越全；② 50 → 200 棵：71.49 − 75.70 = <b>−4.21</b>——开始"接力过头"（第 12 卡的坑）：后面的树在纠缠训练集的巧合，规则账里掺进了噪声规则。', "c44-walk1-zh")
rep('(1) 5 → 50, +2.73 — a richer mine yields a fuller ledger; (2) 50 → 200, −4.21 — the relay runs too long (card 12\'s pit): later trees chase training-set coincidences, and noise rules enter the ledger.',
    '(1) 5 → 50 trees: 75.70 − 72.97 = <b>+2.73</b> — a richer mine yields a fuller ledger; (2) 50 → 200: 71.49 − 75.70 = <b>−4.21</b> — the relay runs too long (card 12\'s pit): later trees chase training-set coincidences, and noise rules enter the ledger.', "c44-walk1-en")
rep('<b>走查 2（DD 列 + 一处正文与表格的出入）：</b>DD 逐行 73.46 → 74.98 → <b>75.77</b>（50 棵）→ 74.98 → 75.28 → 75.13（200 棵）。',
    '<b>走查 2（GBDT 基线列：只升不回头）：</b>基线逐行 68.94 → 70.36 → 71.74 → <b>71.69</b> → 70.74 → 70.76。读法：它 50 棵后基本走平再微跌（峰值 71.74），<b>全表最高的那格才 71.7</b>——本文两型号的 73–76 整体高出它一个身位，说明增益来自"知识嵌入"这一步，而树数只是两支队伍共同踩着的底板。这也解释了为什么论文把基线画在表里：它划出"不嵌入知识"的天花板。</p>'
    '<p class="lz"><b>走查 3（DD 列——黑线 + 一处正文与表格的出入）：</b>DD（图上画作黑线）逐行 73.46 → 74.98 → <b>75.77</b>（50 棵）→ 74.98 → 75.28 → 75.13（200 棵）。', "c44-walk3-zh")
rep('<b>Walk 2 (the DD column + one text-table mismatch):</b> DD row by row 73.46 → 74.98 → <b>75.77</b> (50 trees) → 74.98 → 75.28 → 75.13 (200).',
    '<b>Walk 2 (the GBDT baseline column — rises, then flattens):</b> row by row 68.94 → 70.36 → 71.74 → <b>71.69</b> → 70.74 → 70.76. Reading: it levels off after 50 trees (peak 71.74), and <b>the table\'s best baseline cell is only 71.7</b> — both models sit a full step above (73–76), so the gain comes from the knowledge-embedding stage while tree count merely sets the floor both sides stand on. That is why the baseline is drawn in: it marks the ceiling without knowledge embedding.</p>'
    '<p class="len"><b>Walk 3 (the DD column — the black line — plus one text-table mismatch):</b> DD row by row 73.46 → 74.98 → <b>75.77</b> (50 trees) → 74.98 → 75.28 → 75.13 (200).', "c44-walk3-en")
rep('① 黑线六个数的起落很小（最大与最小差多少，下一题请你亲手量）',
    '① 黑线（DD）六个数的起落很小：75.77 − 73.46 = 2.31 起落（这个数下一题会让你亲手算）', "c44-walk2-zh") if False else None
rep('② <b>这里有一处不一致</b>：正文说"DD 的性能持续上升、在 150 棵达到峰值"——表里 DD 的峰值其实在 <b>50 棵（75.77）</b>，150 棵是 75.28，低于 50 棵。同一段还说"RD 在 200 棵跌 5 个点"，实际跌幅是 4.21（≈4.2 个点）。',
    '② <b>这里有一处不一致（我们已回原文逐字核对，确实如此）</b>：正文原句说 DD"持续上升、在 150 棵达到峰值"——表里 DD 的峰值其实在 <b>50 棵（75.77）</b>，150 棵是 75.28，低于 50 棵。同一段还说"RD 在 200 棵跌 5 个点"，实际跌幅是 4.21（≈4.2 个点）。', "c44-mismatch-zh")
rep('(2) <b>one inconsistency</b>: the text says "DD keeps improving, peaking at 150 trees" — the table\'s DD peak is in fact at <b>50 trees (75.77)</b>, with 150 at 75.28, below it. The same passage also says "RD drops 5 points at 200 trees", while the actual fall is 4.21 (≈4.2).',
    '(2) <b>one inconsistency (verified word-for-word against the source)</b>: the text says DD "keeps improving, peaking at 150 trees" — the table\'s DD peak is in fact at <b>50 trees (75.77)</b>, with 150 at 75.28, below it. The same passage says "RD drops 5 points at 200 trees" while the actual fall is 4.21 (≈4.2).', "c44-mismatch-en")
rep('数值题：表 VII 里 DD-HGNN 列的极差（最大减最小）是多少？', '数值题：表 VII 里 DD（双驱，黑线）那一列的极差（最大减最小）是多少？', "c44-quiz-q-zh")
rep('Numeric: what is the range (max minus min) of Table VII\'s DD-HGNN column?', 'Numeric: what is the range (max minus min) of Table VII\'s DD column (the black line)?', "c44-quiz-q-en")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
