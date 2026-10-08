# -*- coding: utf-8 -*-
"""批12 修复: c48 / c49 / c50"""
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


# ================= c48 =================
rep('<p class="lz">读到这里，你已经会自己验算了。本卡把我们全程复核出的实据汇总成一张账——<b>大部分结论经得起复算，但有十来处数字对不上</b>。全部证据可自行回表核对。</p>',
    '<p class="lz">本卡只有一个主题：<b>把全篇的数字逐格复核一遍，把对不上的账列出来</b>。先备好缩写（后文全靠它们）：<b>RD / DD</b>＝第 34 卡的两个型号（规则驱动 / 双驱）；<b>HGNN</b>＝超图网络基础款；<b>GBDT</b>＝梯度提升树（纯特征基线）；<b>Δ</b>＝差值；<b>|E|、|V|</b>＝边数与顶点数（第 8 卡记号）。<b>大部分结论经得起复算，但有十来处数字对不上</b>——每条都给了可复算的算式。文末附一条定位注（与最像的前人工作 BGNN 的界线），不属于本卡的审计主题。</p>', "c48-open-zh")
rep('<p class="len">By now you can verify for yourself. This card gathers every finding from our audit — <b>most conclusions survive recomputation, but a dozen figures do not balance</b>. Each item is checkable against the tables.</p>',
    '<p class="len">This card has one theme: <b>recompute the paper cell by cell and list the entries that do not balance</b>. Abbreviations first (used throughout): <b>RD / DD</b> = card 34\'s two models (Rule-Driven / Dual-Driven); <b>HGNN</b> = the basic hypergraph network; <b>GBDT</b> = gradient-boosted trees (feature-only baseline); <b>Δ</b> = difference; <b>|E|, |V|</b> = edge and vertex counts (card 8\'s notation). <b>Most conclusions survive recomputation; a dozen figures do not</b> — each item ships with a recomputable arithmetic. A positioning footnote (the line against the nearest predecessor, BGNN) closes the card; it is not part of the audit proper.</p>', "c48-open-en")
rep('<span class="lz">正文写"1.9 和 1.7"；表 V 最后一行是 <b>RD 1.7 / DD 1.5</b>（我们按十行名次复算：17/10 = 1.7、15/10 = 1.5，表对、正文错）</span>',
    '<span class="lz">正文写"RD/DD 平均排名 1.9 和 1.7"；表 V 最后一行印的是 <b>1.7 / 1.5</b>。自行复算：把 RD 在十个数据集里各排第几名列出相加 = 17，17 ÷ 10 = 1.7；DD 合计 15，15 ÷ 10 = 1.5——<b>表对、正文错</b></span>', "c48-row1-zh")
rep('<span class="len">Text says "1.9 and 1.7"; Table V\'s last row reads <b>RD 1.7 / DD 1.5</b> (we recomputed ranks: 17/10 = 1.7, 15/10 = 1.5 — the table is right, the text is not)</span>',
    '<span class="len">Text says RD/DD average ranks are "1.9 and 1.7"; Table V\'s last row prints <b>1.7 / 1.5</b>. Recompute yourself: list RD\'s rank in each of the ten datasets, sum = 17, 17 ÷ 10 = 1.7; DD sums to 15 → 1.5 — <b>the table is right, the text wrong</b></span>', "c48-row1-en")
rep('<span class="lz">5.86 可复算（DD 列均值 87.648 − GBDT 均值 81.792 = 5.856 ✓）；<b>2.28 无出处</b>——最近的候选是 DD−HGNN = 2.12、RD−HGNN = 2.07</span>',
    '<span class="lz">"5.86"可复算：DD 十格求和 ÷ 10 = 87.648、GBDT 十格求和 ÷ 10 = 81.792，87.648 − 81.792 = 5.856 ✓；<b>"2.28"无出处</b>——最接近的组合是 DD−HGNN = 2.12、RD−HGNN = 2.07，都对不上 2.28</span>', "c48-row2-zh")
rep('<span class="len">5.86 recomputes (DD mean 87.648 − GBDT 81.792 = 5.856 ✓); <b>2.28 has no source</b> — nearest candidates are DD−HGNN = 2.12 and RD−HGNN = 2.07</span>',
    '<span class="len">"5.86" recomputes (DD\'s ten cells / 10 = 87.648; GBDT\'s / 10 = 81.792; 87.648 − 81.792 = 5.856 ✓); <b>"2.28" has no source</b> — the nearest combinations are DD−HGNN = 2.12 and RD−HGNN = 2.07</span>', "c48-row2-en")
rep('<span class="lz">Github 行符合 2|E|/|V|（2×144,501/37,700 = 7.67 ≈ 7.7 ✓）；Amazon 两行符合 |E|/|V|（31.13 ≈ 31.1 ✓）；<b>Cora 行两者都不符</b>（2.75 / 5.49 vs 表值 3.9）</span>',
    '<span class="lz">"平均顶点度"该按"2×边数 ÷ 顶点数"算（每条边两个端点）。Github 行符合：2×144,501 ÷ 37,700 = 7.67 ≈ 7.7 ✓；Amazon-P 行却符合"边数 ÷ 顶点数"：238,163 ÷ 7,650 = 31.13 ≈ 31.1 ✓；<b>Cora 行两个口径都不是</b>（7,440÷2,708 = 2.75；2×÷ = 5.49；表印 3.9）</span>', "c48-row8-zh")
rep('<span class="len">Github matches 2|E|/|V| (7.67 ≈ 7.7 ✓); the Amazon rows match |E|/|V| (31.13 ≈ 31.1 ✓); <b>Cora matches neither</b> (2.75 / 5.49 vs printed 3.9)</span>',
    '<span class="len">"Average vertex degree" should read 2|E|/|V| (two endpoints per edge). Github matches: 2×144,501 ÷ 37,700 = 7.67 ≈ 7.7 ✓; Amazon-P instead matches |E|/|V|: 238,163 ÷ 7,650 = 31.13 ≈ 31.1 ✓; <b>Cora matches neither</b> (7,440÷2,708 = 2.75; ×2 = 5.49; printed 3.9)</span>', "c48-row8-en")
rep('这十笔没有一笔推翻论文的<b>主要结论</b>（"知识嵌入有效"在十数据集、多设定、多底座上都有无例外的证据），但每一笔都提醒：<b>论文里的数字和你自己算出来的，可能差一点点</b>——不验算是读不出这些的。这正是本站从第 20 卡起一路让你亲手复算的原因。',
    '分层看这十笔：<b>第 9 类（划分差 1 个样本）确实轻微，属取整误差；但第 1/4/7 类是方向性矛盾</b>——峰值在 50 还是 150、−0.09 被印成 +0.00，这些改变的是读者对"模型在哪最好、赢没赢"的判断。十笔没有一笔推翻<b>主要结论</b>（知识嵌入在十数据集、多设定、多底座上无例外地有效），但每笔都提醒：<b>论文数字和你的复算可能差一点点——不验算读不出来</b>。', "c48-callout-zh")
rep('Not one of these ten overturns the paper\'s <b>main conclusion</b> (knowledge embedding pays across ten datasets, several settings, several backbones — no exceptions there). Each still reminds you: <b>a paper\'s figures and your own arithmetic can disagree by a hair</b> — invisible unless you verify. Which is why this site has had you recompute by hand since card 20.',
    'Split them by weight: <b>item 9 (a one-sample rounding gap) is minor; items 1/4/7 are directional conflicts</b> — peak at 50 versus 150, −0.09 printed as +0.00 reshape a reader\'s judgment of where a model peaks and whether it wins. None of the ten overturns the <b>main conclusion</b> (knowledge embedding pays without exception across ten datasets, several settings, several backbones), yet each reminds you: <b>paper figures and your own arithmetic can disagree by a hair — invisible unless you verify</b>.', "c48-callout-en")
rep('论文主动区分了与 <b>BGNN</b>（Boost-then-Convolve，2020，本文表 V 里 TLF 的同族）的差别：BGNN 把 GBDT 当<b>预处理器</b>——把异质的表格特征翻译成同质的表示后交给图网络，<b>GBDT 学到的规则本身并没有与结构信息融合</b>；本文的 TDR-Encoder 显式编码规则的<b>内容与位置</b>，再经 MDK-Fusion 与结构账深度融合。',
    '附注（定位，非审计）：论文区分了与 <b>BGNN</b>（2020 年的一项前人工作，把树和网络拼在一起）的差别——BGNN 把树队当"<b>翻译机</b>"：先把五花八门的表格特征翻成统一样式交给图网络，<b>但树学到的规则本身没有和结构信息融合</b>；本文则把每条规则的<b>内容（问什么）与位置（第几层）</b>显式编码，再与结构账深度融合。', "c48-bgnn-zh")
rep('The paper draws its line against <b>BGNN</b> (Boost-then-Convolve, 2020 — kin of Table V\'s TLF): BGNN uses GBDT as a <b>preprocessor</b>, translating heterogeneous tabular features into a homogeneous representation for the graph network, <b>without ever fusing the learned rules with structure</b>; this paper\'s TDR-Encoder encodes each rule\'s <b>content and position</b> and deeply fuses them with the structural ledger via MDK-Fusion.',
    'A positioning footnote (not part of the audit): the paper distinguishes itself from <b>BGNN</b> (a 2020 predecessor that bolts trees onto networks) — BGNN uses the tree team as a <b>translator</b>, turning motley tabular features into one uniform style for the graph network, <b>without ever fusing the learned rules with structure</b>; this paper encodes each rule\'s <b>content (what is asked) and position (which layer)</b> and deeply fuses them with the structural ledger.', "c48-bgnn-en")
rep('data-expl="这些多半是笔误，不必当真"',
    'data-expl="分层看：第 9 类（划分差 1 个样本）确实轻微、可归为取整；但第 1/4/7 类是方向性矛盾（峰值 50 vs 150、−0.09 印成 +0.00）——它们改的是读者对"在哪最好、赢没赢"的判断，不能一概归为笔误。"', "c48-q2-expl")

# ================= c49 =================
rep('<p class="lz">上一卡算的是"数字对不对"；本卡问的是"论文没说的部分"——这些问题不是挑刺，而是你把方法真正用起来时会撞上的墙。</p>',
    '<p class="lz">批判卡之一问了"数字对不对"；本卡问"论文没说的部分"。先备缩写：<b>GBDT</b>＝梯度提升树（第 12 卡那队接力小树）；<b>TDR</b>＝本文"规则矿"那台机器；<b>μ<sub>c</sub></b>＝规则内容登记；<b>超边</b>＝一次圈住一群点的"群连接"；<b>KNN</b>＝"找最近 k 个邻居"的规则。这些问题不是挑刺——是你把方法用起来时会撞上的墙。</p>', "c49-open-zh")
rep('<p class="len">The last card checked the figures; this one asks what the paper never says — not nitpicking, but the walls you will hit when you actually deploy it.</p>',
    '<p class="len">One critique card checked the figures; this one asks what the paper never says. Abbreviations first: <b>GBDT</b> = gradient-boosted trees (card 12\'s relay); <b>TDR</b> = this paper\'s rule mine; <b>μ<sub>c</sub></b> = the rule-content registry; <b>hyperedge</b> = a group link embracing a crowd at once; <b>KNN</b> = "find the nearest k neighbors". Not nitpicking — the walls you hit when you deploy.</p>', "c49-open-en")
rep('<span class="lz">论文只说 TDR 在"预定义任务"上预训练，但<b>没说这任务和最终分类任务什么关系</b>。若它就是最终任务本身，等于用（可能含测试集的）标签训练规则矿——需要论文明确"预训练只用训练集标签"才能排除疑虑。原文未交代。</span>',
    '<span class="lz">规则矿（TDR）靠一队 GBDT 树预训练出来，论文只说它在"预定义任务"上训练——<b>却没说这任务和最终分类任务是什么关系</b>。若两者是同一个任务，等于用可能含测试集的标签训练了规则矿，成绩就有"偷看"成分。原文没写"预训练只用训练集标签"，读者无法排除。</span>', "c49-q1-zh")
rep('<span class="len">The TDR pre-trains on a "predefined task", yet the paper <b>never says how that task relates to the final one</b>. If it is the final task, the rule mine trains on labels (possibly including tests) — only an explicit "pre-training sees training labels only" would settle it. The paper stays silent.</span>',
    '<span class="len">The rule mine (TDR) is pre-trained on a team of GBDTs, on a "predefined task" — yet the paper <b>never says how that task relates to the final classification task</b>. If they are one and the same, the mine trained on labels possibly including the test set, tainting every score. The paper never writes "pre-training sees training labels only", so the doubt cannot be closed.</span>', "c49-q1-en")
rep('<span class="lz">图数据集要用 KNN 在特征空间造超边（第 37 卡），k 取 5–20 全靠经验；Heloc/ModelNet40 的超图更是为本文现造。<b>换一个 k，结论还稳吗？</b>论文没有 k 的敏感性实验。</span>',
    '<span class="lz">没有现成超边的数据集（Cora、Github 等普通图），论文用"最近邻居"规则现造超边：每个点找特征空间里最近的 k 个同伴，圈成一条超边。k 取 5 到 20 全凭经验（第 37 卡）。<b>把 k 换一换，结论还稳吗？</b>论文没做这个敏感性实验——k 是人为选的关键旋钮，却没有对应的"拧一拧"验收。</span>', "c49-q4-zh")
rep('<span class="len">Graph datasets get KNN-built hyperedges (card 37) with k chosen by rule of thumb (5–20); Heloc/ModelNet40\'s hypergraphs are purpose-built here. <b>Would another k move the conclusions?</b> No k-sensitivity study appears.</span>',
    '<span class="len">Datasets lacking ready hyperedges (plain graphs like Cora, Github) get hyperedges built on the spot: each point grabs its k nearest neighbors in feature space into one group. k ranges 5–20 by rule of thumb (card 37). <b>Would another k move the conclusions?</b> No such sensitivity study appears — a human-chosen key knob with no acceptance test.</span>', "c49-q4-en")
rep('<span class="lz">Z 的维度 = 2 × 各树提问点数之和（第 32/33 卡）。树数 190、深度 7（表 IV 的 Github）时，维度可以极大；论文没有报告各数据集的 Cr 实际取值，也没讨论维度控制（剪枝、共享规则）。</span>',
    '<span class="lz">知识账每个顶点一格长度 = 2 ×（各树提问点总数）：一条规则记"内容 + 位置"两个数（第 31/33 卡），树越多、问得越深，账就越长。表 IV 的 Github 配了 190 棵树、深度 7——账长可能上千格，而这会直接吃显存和训练时间，<b>方法可能根本跑不动</b>。论文既没报告各数据集的实际账长，也没讨论怎么控制它（剪枝、共享规则）。</span>', "c49-q5-zh")
rep('<span class="len">Z\'s width = 2 × the summed question-node count (cards 32/33). With 190 trees at depth 7 (Table IV\'s Github) it can balloon; the paper reports neither the actual Cr per dataset nor any width control (pruning, shared rules).</span>',
    '<span class="len">Each vertex\'s knowledge-ledger length = 2 × (the summed question count): every rule records two numbers, "content + position" (cards 31/33) — more trees and deeper questions mean a longer ledger. Table IV\'s Github runs 190 trees at depth 7, so the length can reach into the thousands, which eats VRAM and training time — <b>the method may simply not run</b>. The paper reports neither the actual ledger lengths nor any control (pruning, shared rules).</span>', "c49-q5-en")
rep('<span class="lz">表 VI 里 Github 的三行本文型号都没能超过 HGNN（Production Δ = −0.09，归纳行 Δ 为负）。论文承认"图数据集上 RD 略胜"的规律，但对 Github 这个例外<b>没有个案分析</b>——是数据太简单、还是超边构造没造好？读者无从判断。</span>',
    '<span class="lz">在 Github 数据集上，本文三个型号都没赢过基础款 HGNN：直推行差 <b>约输 0.09 个百分点</b>（表 VI，印成 +0.00），归纳行也是负的。零基础读法：这是"方法在自家规律之外的例外"。论文承认"图数据集上 RD 略胜"的规律，却对 Github 这个反常<b>没有一句个案分析</b>——是数据太简单、还是超边没造好？读者无从判断。</span>', "c49-q6-zh")
rep('<span class="len">On Github none of the three paper models beats HGNN (Production Δ = −0.09; inductive Δ negative). The paper names the "RD edges out on graph data" trend but offers <b>no case analysis for Github</b> — too-simple data, or badly built hyperedges? The reader cannot tell.</span>',
    '<span class="len">On Github none of the three paper models beats the basic HGNN: the production line trails by <b>about 0.09 points</b> (Table VI prints +0.00), and the inductive line is negative too — an exception to the paper\'s own rule. The paper names the "RD edges out on graph data" trend yet offers <b>no case analysis for Github</b> — too-simple data, or badly built hyperedges? The reader cannot tell.</span>', "c49-q6-en")
rep('<span class="lz">其中第 2 条（μ<sub>c</sub> 软化）与第 4 条（k 敏感性）是现成的、一两周可做的消融实验；第 1 条（预训练任务的泄漏边界）则是复现这篇论文时<b>必须先向作者问清楚</b>的一条。读到好论文的尽头，就是能开出这样的清单。</span>',
    '<span class="lz">其中第 2 条（把"满足/不满足"从 0/1 换成保留距离的连续值）与第 4 条（换 k 再跑）是现成的、一两周可做的对照实验；第 1 条（预训练的标签边界）是复现这篇论文<b>必须先向作者问清楚</b>的一条。读到好论文的尽头，就是能开出这样的清单。</span>', "c49-close-zh")
rep('<span class="len">Items 2 (softened μ<sub>c</sub>) and 4 (k-sensitivity) are ready-made ablations doable in a week or two; item 1 (the pre-training leakage boundary) is something you <b>must ask the authors</b> before reproducing. Reaching the end of a good paper means holding exactly such a list.</span>',
    '<span class="len">Item 2 (swap the 0/1 content bit for a continuous distance-preserving value) and item 4 (rerun with other k) are ready-made controlled experiments doable in a week or two; item 1 (the pre-training label boundary) is what you <b>must ask the authors</b> before reproducing. Reaching the end of a good paper means holding exactly such a list.</span>', "c49-close-en")
rep('data-expl="第 1 条是唯一可能动摇结论的：若规则矿的预训练偷看了测试标签，表 V/VI 的成绩就有泄漏成分；而论文恰好没写清这一句。其余五条（粒度、开销、k、维度、个案）影响的是"好不好用"，不动摇"有效"这一主张。"',
    'data-expl="第 1 条是唯一可能动摇结论的：若规则矿的预训练偷看了测试标签，表 V/VI 的成绩就有泄漏成分；而论文恰好没写清这一句。其余五条（粒度、开销、k、维度、个案）影响的是"好不好用"，不动摇"有效"这一主张。"', "c49-noop")

# ================= c50 =================
rep('<span class="lz">“Cora 是哪篇论文里的 Cora？”</span>',
    '<span class="lz">“Cora 是哪篇论文里的 Cora？”</span>', "c50-noop")
rep('data-expl="这是本站最想让你养成的反条件反射——凡遇数字先问口径，再问数值。"><span class="lz">"Cora 是哪篇论文里的 Cora？"</span>',
    'data-expl="问出处只解决"数据是哪一版"——还差一层：同一个数据集、同一对方法，换张表数字就从 6.83 变成 7.30，所以更硬的一问是"和谁比、在哪张表、哪个设定"。"</span>', "c50-q7-expl") if False else None
open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
