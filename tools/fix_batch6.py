# -*- coding: utf-8 -*-
"""批6 修复: c25/c26/c27/c28"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
done = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND:", tag)
        return
    s = s.replace(o, n, 1)
    done.append(tag)


# ===== c25 =====
rep('<tr><td>ρ</td>', '<tr><td>ρ</td>', "c25-noop") if '<tr><td>ρ</td>' in s else None
rep('w、b = 两个可调旋钮；σ = 把任意数压到 0–1。<b>整式一句话：存档第 v 个数 = 压一压（v 的参加条数）。</b>',
    'w = 放大倍数的旋钮（把条数乘几；乘 2 就是翻倍）；b = 整体偏移的旋钮（此处 = 0，即不挪动）；σ = 把任意数压到 0–1。<b>整式一句话：存档第 v 个数 = 压一压（v 的参加条数）。</b>', "c25-wb-zh")
rep('w, b = two tunable knobs; σ = squashing anything into 0–1.',
    'w = a magnification knob (times the count; ×2 doubles it); b = a shift knob (here 0, i.e. no shift); σ = squashing anything into 0–1.', "c25-wb-en")
rep('存档 = [0.9975, 0.8808, 0.9820, 0.9820, 0.5]。</p>',
    '存档 = [0.9975, 0.8808, 0.9820, 0.9820, 0.5]。本例 b 恒为 0，未展示 b≠0 时的偏移效果。</p>', "c25-ex-decl-zh")
rep('Archive = [0.9975, 0.8808, 0.9820, 0.9820, 0.5].</p>',
    'Archive = [0.9975, 0.8808, 0.9820, 0.9820, 0.5]. This example keeps b = 0 throughout; the shift when b ≠ 0 is not shown.</p>', "c25-ex-decl-en")
rep('会计干的活——数参加几个组、压成 0–1 的一个数', '会计干的活——数它参加几个组（即几条超边）、压成 0–1 的一个数', "c25-gloss")

# ===== c26 =====
rep('论文的原文就一句：∑<sub>e∈E</sub> π(H)[v, π(e)] = ∑<sub>e∈E</sub> H[v, e]，说的正是这件事。',
    '论文的原文就一句：∑<sub>e∈E</sub> π(H)[v, π(e)] = ∑<sub>e∈E</sub> H[v, e]。顺手译一下这两个记号：∑<sub>e∈E</sub> 就是“把 E 里所有超边挨个加起来”；π(e) 指“第 e 列搬家后落在第几个位置”。整句读作：换列后沿行相加 = 换列前沿行相加。', "c26-sigma-zh")
rep('The paper\'s line — ∑<sub>e∈E</sub> π(H)[v, π(e)] = ∑<sub>e∈E</sub> H[v, e] — says exactly this.',
    'The paper\'s line — ∑<sub>e∈E</sub> π(H)[v, π(e)] = ∑<sub>e∈E</sub> H[v, e] — says exactly this. Two symbols translated: ∑<sub>e∈E</sub> means "add up over all hyperedges in E"; π(e) means "where column e lands after the move". Read the whole line as: row-sum after the swap = row-sum before the swap.', "c26-sigma-en")
rep('你可能想起用矩阵/转置来做排列——但本证明只用两件事：加法不挑顺序（换列 = 换相加顺序）；② ρ 逐顶点、只吃一个数（与列无关）。两块一接，性质成立。',
    '你可能想着“排列不就是矩阵/转置的活儿吗”——但本证明的地基只有两件事：① 加法不挑顺序（换列 = 换相加顺序）；② ρ 逐顶点、只吃一个数（与列无关）。矩阵记号只是这两块地基的一种写法，不是独立的地基。', "c26-q1a")

# ===== c27 =====
rep('备料车间的第二条流水线，是查规则的学究。他手里有一队已经训练好的树（第 12、13 卡的"接力纠错树队"：每棵树都在补前一棵的漏）。但学究<b>不拿树去预测</b>——他只要每棵树在分叉处问过的那些问题。',
    '备料车间的第二条流水线，交给一位查规则的研究者。他手里有一队已经训练好的树（第 12、13 卡的"接力纠错树队"：每棵树都在补前一棵的漏），但他<b>从不拿树去预测</b>——他只要每棵树在分叉处问过的那些问题。', "c27-motif")
rep('The prep floor\'s second line is the rule-reading scholar. In his hands sits a team of trained trees (cards 12–13\'s "relay of error-correcting trees": each patching the previous one\'s leaks). Yet the scholar <b>never predicts with them</b> — he only wants the questions asked at each branching point.',
    'The prep floor\'s second line belongs to a rule-reading researcher. In his hands sits a team of trained trees (cards 12–13\'s "relay of error-correcting trees": each patching the previous one\'s leaks), yet he <b>never predicts with them</b> — he only wants the questions asked at each branching point.', "c27-motif-en")
rep('论文给这两条记录各起了一个代号：内容映射叫 μ<sub>c</sub>，位置映射叫 μ<sub>p</sub>（正式公式在第 29、30 卡，本卡只需认得这两个代号）。',
    '论文给这两条记录各起了一个代号：管"内容"的叫 μ<sub>c</sub>，管"位置"的叫 μ<sub>p</sub>——"映射"听着玄，其实就是"一张登记表"：把内容登记成对/不对、把位置登记成层级权重（正式公式在第 29、30 卡，本卡只需认得这两个代号）。', "c27-mu-gloss")
rep('The paper codenames the two records: μ<sub>c</sub> for content mapping, μ<sub>p</sub> for position mapping (equations at cards 29–30; here you only need the codenames).',
    'The paper codenames the two records: μ<sub>c</sub> for content, μ<sub>p</sub> for position — "mapping" sounds grand but is just a registry: content logged as satisfied/not, position logged as a layer weight (equations at cards 29–30; here the codenames suffice).', "c27-mu-gloss-en")
rep('学究逐棵抄录，账本共 <b>2 + 3 = 5</b> 条规则。叶子上的 A / B / C 标签一律不抄。',
    '研究者逐棵抄录，顺手把每条规则的<b>位置</b>也登记上：T₁ 两条分别在第 1、2 层，T₂ 三条分别在第 1、2、2 层。账本共 <b>2 + 3 = 5</b> 条规则——每条都带"内容 + 位置"两份记录。叶子上的 A / B / C 标签一律不抄。', "c27-ex1-pos-zh")
rep('The scholar copies tree by tree: <b>2 + 3 = 5</b> rules. Leaf labels A / B / C are never copied.',
    'The researcher copies tree by tree, logging each rule\'s <b>position</b> as he goes: T₁\'s two rules sit at layers 1 and 2; T₂\'s three at layers 1, 2, 2. The ledger holds <b>2 + 3 = 5</b> rules — every entry carrying both "content" and "position". Leaf labels A / B / C are never copied.', "c27-ex1-pos-en")
rep('顶点甲的数值 x = (1, 3, 4)：', '先说一个词：顶点 = 图里的一个样本；x = (1, 3, 4) 表示它的三个特征分别是 x₁ = 1、x₂ = 3、x₃ = 4。顶点甲的数值 x = (1, 3, 4)：', "c27-vertex-zh")
rep('Vertex A\'s values x = (1, 3, 4):', 'One term first: a vertex = one sample in the graph; x = (1, 3, 4) means its three features are x₁ = 1, x₂ = 3, x₃ = 4. Vertex A\'s values x = (1, 3, 4):', "c27-vertex-en")

# ===== c28 =====
rep('图 2 是学究的"记账流程图"：', '图 2 是一张"记账流程图"：', "c28-mood")
rep('It answers: what do those two records (content + position) look like in practice, and how are they bound?</p>',
    'It answers: what do those two records (content + position) look like in practice, and how are they bound?</p>\n    <p class="dim"><span class="lz">本卡的"研究者"即第 27 卡那位查规则的学究。</span><span class="len">The "researcher" here is card 27\'s rule-reading scholar.</span></p>', "c28-noop")
rep('中间两条流水线分别记录每条规则的内容和位置', '中间两条登记线分别记录每条规则的内容和位置', "c28-wording")
rep('μ<sub>p</sub> 面版画着一条从左上到右下缓降的曲线（横轴 = 深度），以及三个半径依次变小的点，标着 d(o) = 1、2、3。',
    'μ<sub>p</sub> 面版画着一条从左上到右下缓降的曲线（横轴 = 深度），以及三个半径依次变小的点，标着 d(o) = 1、2、3——d(o) 就是"这个提问点在第几层"的层号（根 = 第 1 层）。', "c28-do-gloss-zh")
rep('the μ<sub>p</sub> panel shows a gently descending curve (horizontal axis = depth) and three dots shrinking in radius, labeled d(o) = 1, 2, 3.',
    'the μ<sub>p</sub> panel shows a gently descending curve (horizontal axis = depth) and three dots shrinking in radius, labeled d(o) = 1, 2, 3 — d(o) is simply "which layer this question node sits on" (root = layer 1).', "c28-do-gloss-en")
rep('每个提问点旁边标着问题原文（"x₂ ≥ 2"、"x₁ ≥ 1"、"x₃ ≥ 5"、"x₁ ≥ 2"、"x₂ ≥ 1"），底部一排 A / B / C 叶子。',
    '每个提问点旁边标着问题原文——T₁ 的 2 个（"x₂ ≥ 2"、"x₁ ≥ 1"）与 T₂ 的 3 个（"x₃ ≥ 5"、"x₁ ≥ 2"、"x₂ ≥ 1"）——底部一排 A / B / C 叶子。', "c28-walk1-count-zh")
rep('each question node tagged with its question ("x₂ ≥ 2", "x₁ ≥ 1", "x₃ ≥ 5", "x₁ ≥ 2", "x₂ ≥ 1"), and a row of A / B / C leaves at bottom.',
    'each question node tagged with its question — T₁\'s two ("x₂ ≥ 2", "x₁ ≥ 1") and T₂\'s three ("x₃ ≥ 5", "x₁ ≥ 2", "x₂ ≥ 1") — with a row of A / B / C leaves at bottom.', "c28-walk1-count-en")
rep('两摞竖方块，分别标 1st Layer、2nd Layer——表示"多条记录叠起来"，一摞对着一棵树收来的那批规则。每格方块就是一个数（= 内容记录 × 位置权重，第 31 卡逐格算）。',
    '两摞竖方块，分别标 1st Layer、2nd Layer——这是本流水线自己的"整理层"：第 1 层叠 T₁ 收来的那批规则、第 2 层叠 T₂ 的，虚线箭头再把两层并成一摞更长的条（论文式 (8) 的"逐树编码、再拼接"）。注意：这里 Layer 指<b>流水线的整理层</b>，不是下游网络的层数，也不是树的深度——树的深度已经由 μ<sub>p</sub> 权重登记过了。每格方块就是一个数（= 内容记录 × 位置权重，第 31 卡逐格算）。', "c28-layer-fix-zh")
rep('two stacks of bars labeled 1st Layer, 2nd Layer — "records stacked", one stack per tree\'s rule batch. Each bar is one number (= content record × position weight; computed bar by bar at card 31).',
    'two stacks of bars labeled 1st Layer, 2nd Layer — the pipeline\'s own "filing layers": layer 1 stacks T₁\'s rule batch, layer 2 stacks T₂\'s, and dashed arrows merge the two into one longer bar (Eq. (8)\'s "encode per tree, then concatenate"). Note: "Layer" here means the <b>pipeline\'s filing layer</b> — not a downstream network layer, not tree depth (tree depth is already logged via μ<sub>p</sub> weights). Each bar is one number (= content record × position weight; computed bar by bar at card 31).', "c28-layer-fix-en")
rep('data-hint="照图 2 的规模先把已有的提问点数出来，再按题目加一棵。"',
    'data-hint="现有两棵树一共收了 5 条规则（走查 3），题目又说 T₂ 是 3 条——先算出 T₁ 的条数，再求和。"', "c28-hint")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
