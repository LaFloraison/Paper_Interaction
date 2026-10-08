# -*- coding: utf-8 -*-
"""批9 修复: c37/c38/c39/c40"""
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


# ================= c37 =================
rep('四份是普通图（Cora、Github、Amazon-P、Amazon-C），六份是真超图（CA-Cora、DBLP-Conf、CC-Cora、Tencent、ModelNet40、Heloc）。',
    '其中有普通图也有超图——先把两个词钉死：<b>普通图 = 一条边只连两个点的关系网；超图 = 允许一条边一次圈住任意多个点的关系网（第 7 卡的老朋友）。</b>', "c37-hyper-gloss-zh")
rep('Four are ordinary graphs (Cora, Github, Amazon-P, Amazon-C); six are true hypergraphs (CA-Cora, DBLP-Conf, CC-Cora, Tencent, ModelNet40, Heloc).',
    'Some are ordinary graphs, some hypergraphs — two words pinned first: <b>an ordinary graph = each edge joins exactly two vertices; a hypergraph = one edge may embrace any number of vertices at once (card 7\'s old friend).</b>', "c37-hyper-gloss-en")
rep('1,433 个词（特征，每篇论文的词袋表示）', '1,433 个词（特征——"词袋表示"就是把每篇论文记成"出现过哪些词、各几次"，像一张词频清单）', "c37-bagofwords-zh")
rep('1,433 words (features, each paper as a bag of words)', '1,433 words (features — a "bag of words" records each paper as "which words appear and how often", like a frequency list)', "c37-bagofwords-en")
rep('后者用少得多的关系装下同样的团结构', '后者用少得多的关系装下同样的"团"（一群互相有关联的对象）', "c37-cluster-zh")
rep('far fewer relations carry the same crowds', 'far fewer relations carry the same "clusters" (groups of mutually related objects)', "c37-cluster-en")
rep('<span class="lz">论文表 I 原图（Feng et al., TPAMI 2026）。前十行是图数据集，后六行是超图数据集。</span>',
    '<span class="lz">论文表 I 原图（Feng et al., TPAMI 2026）。前四行是图数据集，后六行是超图数据集（Type 列写着 Graph / Hypergraph）。</span>', "c37-caption-fix")
rep('<div class="quiz quiz-num" data-answer="6" data-tol="0.01" data-hint="数一数表里 Type 列写着 Hypergraph 的行有几行。" data-sol="六行：CA-Cora、DBLP-Conf、CC-Cora、Tencent、ModelNet40、Heloc。其余四行（Cora、Github、Amazon-P、Amazon-C）是普通图。">',
    '<div class="quiz quiz-num" data-answer="4005" data-tol="0.5" data-hint="翻到表 I 原图：找 Github 行，再往右找到 #Features 那一列。" data-sol="4,005 个特征（Github 的词袋维度）。顺带自检：Github 的测试集人数 5,655 与顶点数 37,700 也在同一行——读表时要横着把一行读全。">', "c37-quiz")
rep('<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：表 I 里超图（Hypergraph）数据集有几个？</span><span class="len">Numeric: how many hypergraph datasets does Table I list?</span></p>',
    '<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：表 I 里 Github 的特征数（#Features）是多少？</span><span class="len">Numeric: what is Github\'s #Features in Table I?</span></p>', "c37-quiz-q")
rep('点云转表格后，用 KNN 在特征空间现建超边（Heloc 同理）',
    '点云（3D 物体表面的一堆点的坐标）转成表格后，用 KNN（"找最近的 K 个邻居"的简单规则）在特征空间里现建超边（Heloc 同理）', "c37-knn-zh")
rep('After tabularizing the point cloud, KNN builds hyperedges in feature space (same for Heloc)',
    'After tabularizing the point cloud (a 3D surface given as a cloud of point coordinates), KNN ("find the nearest K neighbors") builds hyperedges in feature space (same for Heloc).', "c37-knn-en")
rep('20 × 982.2 = 19,644 人次，摊给 4,057 人 ≈ 4.84，与表里的"平均顶点度 4.8"吻合（超图两列互相印证）。',
    '20 × 982.2 = 19,644 人次，摊给 4,057 人 ≈ 4.84，与表里的"平均顶点度 4.8"吻合（超图两列互相印证）。<br>顺手做一次诚实的交叉检查：同一个恒等式套到 Cora 行却不成立——7,440 × 2 = 14,880 ≠ 2,708 × 3.9 ≈ 10,561。<b>这说明不同数据集的度数口径或数据版本可能有别，读表时不能假设所有行同规矩</b>；这笔账记入第 48 批判卡。', "c37-identity-zh")
rep('matching the table\'s vertex degree 4.8 (the hypergraph\'s two columns cross-confirm).',
    'matching the table\'s vertex degree 4.8 (the hypergraph\'s two columns cross-confirm).<br>One honest cross-check: the same identity fails on the Cora row — 7,440 × 2 = 14,880 ≠ 2,708 × 3.9 ≈ 10,561. <b>Rows may follow different degree conventions or data versions; never assume one rule for the whole table</b> — the account goes to card 48.', "c37-identity-en")

# ================= c38 =================
rep('另外第 16 卡的老约定在这里沿用：全图 G 仍然参与消息传递。',
    '另外沿用第 16 卡的老约定：<b>整张图（所有点加所有连接，记作 G）在训练时全部送进模型</b>参与"沿关系传递信息"（即每一层的平均）；不是只放训练那 60%。', "c38-gloss-zh")
rep('Card 16\'s old convention also holds: the full graph G keeps participating in message passing.',
    'Card 16\'s old convention also holds: <b>the entire graph (all points and links, written G) is fed to the model during training</b> and joins "information passing along links" (the per-layer averaging) — not merely the 60% training slice.', "c38-gloss-en")
rep('第 18 卡的"传统卷"（transductive）落到实处，就是表 II：',
    '第 18 卡的"传统卷"（transductive，中译"直推"：见过人、不见答案）落到实处，就是表 II：', "c38-trans-gloss")
rep('Card 18\'s "classic exam" (transductive) lands in Table II:',
    'Card 18\'s "classic exam" (transductive: faces seen, answers unseen) lands in Table II:', "c38-trans-gloss-en")
rep('Cora 行：#V = 2,708、#C = 7、训练 1,625、验证 677、测试 406。',
    'Cora 行：#V = 2,708、#C = 7、训练 1,625、验证 677、测试 406；Github 行：训练 22,620、验证 9,425、测试 <b>5,655</b>（稍后习题会用到这一行）。', "c38-github-zh")
rep('Cora: #V = 2,708, #C = 7, training 1,625, validation 677, testing 406.',
    'Cora: #V = 2,708, #C = 7, training 1,625, validation 677, testing 406; Github: training 22,620, validation 9,425, testing <b>5,655</b> (the exercises will use this row).', "c38-github-en")
rep('训练集没有答案——它只用来最后打分，用它挑模型就等于考前偷看试卷。',
    '测试集才是"不带答案、最后打分"的那份；训练与验证都带答案，差别在分工（一个学参数、一个做选择）。', "c38-q1a")
rep('The test set carries no answers — it only scores at the end; picking a model with it is peeking at the exam.',
    'The test set is the answerless one, used only for the final score; training and validation both carry answers and differ in role (one learns parameters, one selects the model).', "c38-q1a-en")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
