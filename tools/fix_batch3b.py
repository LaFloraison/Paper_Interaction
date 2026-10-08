# -*- coding: utf-8 -*-
"""批3 修复 part 2: c12 / c13 审卡意见落地"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
applied = []


def rep(o, n, tag=""):
    global s
    if o not in s:
        print("!! NOT FOUND (" + tag + "): " + o[:70])
        return
    s = s.replace(o, n, 1)
    applied.append(tag)


# ========== c12 ==========
# 1. 拆段落: boosting / 梯度 分开; 删"已学过+第13卡"错误指路
rep("这个\"接力\"有个学名叫<b>提升（boosting）</b>；\"梯度\"指每棵新树拟合的方向是当前误差下降最快的方向（补一句给你已学过的：梯度下降是拧<b>参数</b>的小步，梯度提升是加一棵<b>树</b>的小步——都靠\"小步走\"防跑偏，站点第 13 卡有梯度下降的完整回顾）。</p>",
    "这个\"接力\"有个学名叫<b>提升（boosting）</b>——一队小树，后一棵专补前一棵的漏。</p>"
    "<p class=\"len\">This relay has a proper name: <b>boosting</b> — a team of small trees, each patching the previous one's leaks.</p>"
    "<p class=\"lz\">那\"梯度\"呢？它指每棵新树瞄准的方向：<b>当前误差下降最快的方向</b>。想象蒙着眼下山，每一步都朝最陡的坡迈——树就是那一步。</p>"
    "<p class=\"len\">And the \"gradient\"? It is the direction each new tree aims at: <b>the steepest error-descent direction</b>. Picture descending a hill blindfolded, each step on the steepest slope — a tree is one such step.</p>", "c12-terms-split")

# 2. 残差 first-use gloss + 例2 拆段 + 计数歧义修复 + 把关比喻
rep("<p class=\"lz\"><b>例 2（继续接力）：</b>还差 80 − 52.5 = 27.5。第二棵树 h₂ 学出意见\"+27\"：f₂ = 52.5 + 0.1 × 27 = 52.5 + 2.7 = <b>55.2</b>。每棵只挪 2.7——这就是 ε 打折的味道：慢，但每一步都被 10 棵树各自把关。照这个节奏，若每棵都纠 27，10 棵后 52.5 + 10 × 2.7 = <b>79.5 ≈ 80</b>，基本到位。（真实训练里，残差会越剩越少，新树的意见也随之变小。）</p>",
    "<p class=\"lz\"><b>例 2（继续接力）：</b>还差 80 − 52.5 = 27.5（这个\"还差的量\"学名叫<b>残差</b>——后面习题还会见到它）。第二棵树 h₂ 学出意见\"+27\"：f₂ = 52.5 + 0.1 × 27 = 52.5 + 2.7 = <b>55.2</b>。每棵只挪 2.7——这就是 ε 打折的味道：答案不再押在某一棵大树上，而是由许多小树各出一小票慢慢凑。</p>"
    "<p class=\"len\"><b>Example 2 (keep relaying):</b> still short by 80 − 52.5 = 27.5 (that \"still-short amount\" is called the <b>residual</b> — you will meet it again in the exercises). Tree h₂ learns \"+27\": f₂ = 52.5 + 0.1 × 27 = 52.5 + 2.7 = <b>55.2</b>. Each tree moves just 2.7 — that is ε's discount: the answer no longer rests on one big tree, but accumulates small votes from many small ones.</p>"
    "<p class=\"lz\">照这个节奏，若接下来每棵树的意见都还是 27（现实中残差会越剩越少、意见越来越小），再接力 10 棵：52.5 + 10 × 2.7 = <b>79.5 ≈ 80</b>，基本到位。</p>"
    "<p class=\"len\">At this pace, if every coming tree kept saying 27 (in reality the residual shrinks and opinions shrink with it), ten more relays give 52.5 + 10 × 2.7 = <b>79.5 ≈ 80</b> — arrived.</p>", "c12-ex2")

# 3. 误解块 Table VII -> 实验篇
rep("本文 Table VII 里 RD-HGNN 从 50 棵的 75.70 掉到 200 棵的 71.49，就是接力过头的样子。",
    "后面实验篇会看到：树从 50 棵加到 200 棵，准确率掉 4 个多点——接力过头的样子。", "c12-mis-zh")
rep("in the paper's Table VII, RD-HGNN falls from 75.70 at 50 trees to 71.49 at 200: a relay run too long.",
    "the experiment part will show accuracy dropping by more than 4 points as trees grow from 50 to 200 — a relay run too long.", "c12-mis-en")

# 4. 错别字
rep("这正式论文式 (2) 的一般形态。", "这正是论文式 (2) 的模样。", "c12-typo1")
rep("为什么用小学习率 ε = 0.1，而不是让每棵树的的意见一次到位（ε = 1）？",
    "为什么用小学习率 ε = 0.1，而不是让每棵树的意见一次到位（ε = 1）？", "c12-typo2")
rep("why a small learning rate ε = 0.1 rather than taking each tree's opinion at full value (ε = 1)?",
    "why a small learning rate ε = 0.1 rather than taking each tree's opinion at full value (ε = 1)?", "c12-typo2-en")

# 5. Q3 坏干扰项 A 换成真实误解
rep("<button class=\"opt\" data-expl=\"每棵树小步走、后面还有几百棵把关——接力慢是故意的。一次到位反而把前几棵的偏差全信了。\"><span class=\"lz\">ε=1 太慢，收敛不动</span><span class=\"len\">ε = 1 would be too slow to converge</span></button>",
    "<button class=\"opt\" data-expl=\"ε 不是无关的调参数字——它决定每棵树的意见被打几折：0.1 是小步慢走，1 是全信单棵。全信单棵，恰恰是接力最怕的事。\"><span class=\"lz\">ε 只是训练前随便定的数字，不影响学得好坏</span><span class=\"len\">ε is just an arbitrary number that does not affect learning</span></button>", "c12-q3a")

# ========== c13 ==========
# 1. 加粗定义句去行话
rep("<b><span class=\"hl\">本文的用法 = 把\"训好的 GBDT\"当规则矿：预训练 → 得到 T = {T₁,…,T_K} → 每个内部节点一条规则 → 交给 TDR-Encoder 编码（式 4–8 的原料）。</span></b></p>",
    "<b><span class=\"hl\">本文的用法 = 把训好的 GBDT 当\"规则矿\"：先在预设任务上训练，然后丢掉它的预测，只把每棵树里每个判断分叉点上的判断条件收走，一条就是一条规则。</span></b></p>"
    "<p class=\"len\"><b><span class=\"hl\">The paper's usage = treat the trained GBDT as a rule mine: train it on a preset task, throw the predictions away, and keep only the yes/no conditions at every branching point of every tree — each condition is one rule.</span></b></p>"
    "<p class=\"lz\">收来的规则稍后交给一个叫 TDR-Encoder 的部件去编码（第 27 卡细讲）；论文的式 (4)–(8) 写的全是这件事。上一卡式 (2) 里的树，到这里就变身为\"规则集装箱\"。</p>"
    "<p class=\"len\">The collected rules later go to a component called the TDR-Encoder for encoding (card 27); the paper's Eqs. (4)–(8) are all about this. The trees of Eq. (2) from the last card thus become \"rule containers\".</p>", "c13-def")

# 2. 例1: 2^4-1 推导 + 60×15 乘出来
rep("这意味着规则矿里最多 60 × (最多 2⁴−1 = 15 个内部节点) 条规则，而根上的规则是第一轮纠错摘下的\"最大果子\"——与预测目标关系最强。挖矿完成后，这 60 棵树的预测结果被丢掉，只留下规则骨架。",
    "深度 4 的满树能有多少个分叉点？逐层数：第 1 层 1 个、第 2 层 2 个、第 3 层 4 个、第 4 层 8 个，共 1+2+4+8 = 15 个（写作 2⁴−1）。所以规则矿最多装 60 × 15 = <b>900</b> 条规则。根上的规则是第一轮纠错摘下的\"最大果子\"——与预测目标关系最强；挖矿完成后，预测结果丢掉，只留规则骨架。",
    "c13-ex1-zh")
rep("The mine can hold up to 60 × (at most 2⁴−1 = 15 inner nodes) rules, and root-side rules are the \"biggest fruit\" picked by the first corrections — most related to the target. After mining, the 60 trees' predictions are discarded, leaving the rule skeleton.",
    "How many branching points can a depth-4 full tree hold? Count layer by layer: 1, then 2, 4, 8 — total 1+2+4+8 = 15 (written 2⁴−1). So the mine holds at most 60 × 15 = <b>900</b> rules. Root-side rules are the \"biggest fruit\" picked by the first corrections — most related to the target; after mining, predictions are discarded, leaving the rule skeleton.",
    "c13-ex1-en")

# 3. 例2: RD/DD 交代 + CC-Cora 标注
rep("<b>例 2（树的数量多少才好——Table VII 真实数字）：</b>CC-Cora 上把树从 5 棵加到 200 棵：RD-HGNN 从 72.97 一路涨到 50 棵的 <b>75.70</b>（+2.73，规则越多矿越富），随后回落：100 棵 75.31、150 棵 74.44、200 棵 <b>71.49</b>（从峰值跌 4.21——接力过头的代价）。而 DD-HGNN 全程 73.46–75.77，极差仅 2.31——两路知识互补，一路变差另一路托底。</p>",
    "<b>例 2（树的数量多少才好——Table VII 真实数字）：</b>先认两个名字：RD-HGNN 与 DD-HGNN 是论文的两个最终型号（各吃一路知识，第 34 卡正式讲）——这里只需看数字的形状。在 CC-Cora（Cora 引文家族的另一个数据集）上把树从 5 棵加到 200 棵：RD-HGNN 从 72.97 一路涨到 50 棵的 <b>75.70</b>（+2.73，规则越多矿越富），随后回落：100 棵 75.31、150 棵 74.44、200 棵 <b>71.49</b>（从峰值跌 4.21——接力过头的代价）。而 DD-HGNN 全程 73.46–75.77，极差仅 2.31——两路知识互补，一路变差另一路托底。</p>",
    "c13-ex2-zh")
rep("<b>Example 2 (how many trees — real Table VII numbers):</b> on CC-Cora, growing trees from 5 to 200:",
    "<b>Example 2 (how many trees — real Table VII numbers):</b> first, two names: RD-HGNN and DD-HGNN are the paper's two final models (each feeds on one stream of knowledge, card 34) — here just watch the shapes. On CC-Cora (another dataset in the Cora citation family), growing trees from 5 to 200:", "c13-ex2-en")

# 4. Q1 A 解析去"稀疏词袋"
rep("本文的顶点特征是稀疏词袋（1,433 维），GBDT 在表格上确实强——但“当矿”的决定性理由是可读性 + 靠根规则的相关性。",
    "GBDT 在表格数据上确实强——但“当矿”的决定性理由是可读性 + 靠根规则的相关性，预测准不准是另一回事。", "c13-q1a")

# 5. Q3 正确项去"残差"生词
rep("正确！第一轮残差最大，第一棵树的根一刀切走最大误差——根规则绑定目标最紧。μp 给浅层大权重（第 30 卡）就是在兑现这一点。",
    "正确！第一轮要纠的误差最大，第一棵树的根一刀切走最大的一块——根规则与目标绑定最紧。后面给浅层规则更大权重的设计（第 30 卡）就是在兑现这一点。", "c13-q3b")

# 6. 数值题换成未在例子中直接给结果的题
rep('<div class="quiz quiz-num" data-answer="75.7" data-tol="0.11" data-hint="读 Table VII 的 RD-HGNN 列——50 棵那一行的数字（例 2 刚走过）。" data-sol="RD-HGNN 在 50 棵时达到峰值 75.70（5 棵时仅 72.97），随后 100/150/200 棵回落到 75.31/74.44/71.49。">',
    '<div class="quiz quiz-num" data-answer="0.87" data-tol="0.05" data-hint="翻开第 44 卡的 Table VII 原图，读 RD-HGNN 列：100 棵与 150 棵两行相减。" data-sol="75.31 − 74.44 = 0.87。50 棵之后每加 50 棵都在倒退——这就是接力过头的坡度：100→150 棵掉 0.87，150→200 棵掉 2.95。">', "c13-quiz-attrs")
rep('<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：Table VII 中 RD-HGNN 的峰值准确率出现在 50 棵树，是多少（百分数，保留一位小数）？</span><span class="len">Numeric: in Table VII, RD-HGNN peaks at 50 trees — what is that accuracy (one decimal)?</span></p>',
    '<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：查 Table VII，RD-HGNN 从 100 棵到 150 棵掉了多少个百分点（两位小数）？</span><span class="len">Numeric: from Table VII, how many points does RD-HGNN drop from 100 to 150 trees (two decimals)?</span></p>', "c13-quiz-q")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(applied))
for a in applied:
    print(" -", a)
