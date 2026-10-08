# -*- coding: utf-8 -*-
"""批7 修复: c29 (T1/T2 铺垫) + c30 (打磨) + c31 (符号顺序/位置分来历/hint)"""
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


# ===== c29 =====
rep('<p class="lz"><b>例 1（把 5 条规则逐个打勾）：</b>顶点甲 x = (1, 3, 4)，逐条问：',
    '<p class="lz">先认两个名字：本文的树队里有好几棵"规则树"（第 11 卡那种一串提问的树，第 27 卡讲过从它们身上收规则）；本卡用<b>两棵</b>演示——T₁ 装前两条规则（x₂ ≥ 2、x₁ ≥ 1），T₂ 装后三条（x₃ ≥ 5、x₁ ≥ 2、x₂ ≥ 1）。另外，记法 x₂ 指特征串里的第 2 个数。</p>'
    '<p class="lz"><b>例 1（把 5 条规则逐个打勾）：</b>顶点甲 x = (1, 3, 4)，逐条问：', "c29-trees-gloss-zh")
rep('<p class="len">Example 1 (tick five rules one by one):</b>', '<p class="len">Two names first: the paper\'s team holds several "rule trees" (card 11\'s question-chains; rules were harvested from them at card 27); this card demos with <b>two</b> — T₁ carries the first two rules (x₂ ≥ 2, x₁ ≥ 1), T₂ the last three (x₃ ≥ 5, x₁ ≥ 2, x₂ ≥ 1). Also, the notation x₂ means the 2nd number in the feature string.</p>'
    '<p class="len"><b>Example 1 (tick five rules one by one):</b>', "c29-trees-gloss-en")
rep('登记结果：T₁ 的两条 = 【0, 0】；T₂ 的三条 = 【1, 1, 0】。',
    '登记结果：T₁ 的两条 = 【0, 0】（两个问题都被它解释清楚）；T₂ 的三条 = 【1, 1, 0】。', "c29-ex1-split")
rep('这两个顶点的"被规则覆盖画像"完全不同，这正是"特征知识"的原料。',
    '两个顶点的"被规则覆盖画像"（特征知识——某顶点被哪些规则管住、哪些管不住的整体画像）完全不同，这正是它的原料。', "c29-featurek-zh")
rep('the two vertices\' "rule-coverage portraits" differ completely; this is the raw material of feature knowledge.',
    'the two vertices\' "rule-coverage portraits" differ completely — feature knowledge (the whole picture of which rules do and do not cover a vertex) in raw form.', "c29-featurek-en")

# ===== c30 打磨 =====
rep('规律很朴素：纠错接力里先问的问题摘走最大的误差（第 13 卡），所以<b>越靠根（层号越小）的规则，分量越大</b>。',
    '规律很朴素：纠错接力（第 12、13 卡：一队小树轮流补误差）里先问的问题摘走最大的误差，所以<b><span class="hl">越靠根（层号越小）的规则，分量越大</span></b>。', "c30-bold")
rep('论文把 α、β 用"网格搜索"在 {6, 7, 8, 9, 10} 里逐个数据集试出',
    '论文把 α、β 用"网格搜索"（就是把组合挨个试）在 {6, 7, 8, 9, 10} 里逐个数据集试出', "c30-grid-zh")
rep('The paper grid-searches α, β over {6, 7, 8, 9, 10} per dataset',
    'The paper grid-searches α, β over {6, 7, 8, 9, 10} (i.e., tries the combinations one by one) per dataset', "c30-grid-en")

# ===== c31 =====
rep('<h2><span class="lz">式 (7)：内容分 × 位置分 = 一条规则的得分</span><span class="len">Eq. (7): content × position = one rule\'s score</span></h2>',
    '<h2><span class="lz">式 (7)：位置分 × 内容分 = 一条规则的得分</span><span class="len">Eq. (7): position × content = one rule\'s score</span></h2>', "c31-title")
rep('<b><span class="hl">每条规则的得分 = 内容分 × 位置分；一棵树所有规则的得分按顺序排成的一列，就是这棵树对某个顶点的"编码"——位数等于这棵树的提问点个数。</span></b>',
    '<b><span class="hl">每条规则的得分 = 位置分 × 内容分；一棵树所有规则的得分按顺序排成的一列，就是这棵树对某个顶点的"编码"——位数等于这棵树的提问点个数。</span></b>', "c31-bold")
rep('现在把同一棵树的所有规则<b>逐条算分、排成一列</b>——这就是式 (7)。',
    '现在把同一棵树的所有规则<b>逐条算分、排成一列</b>——这就是式 (7)；下面先说清三样东西各叫什么，再让公式出场。', "c31-lead")
rep('<p class="formula-note"><span class="lz">逐符号：φ<sub>r</sub><sup>i</sup> = 第 i 棵树的编码函数；x = 顶点特征串；T<sub>i</sub> = 第 i 棵树；每个括号项 = "第 k 个提问点的位置分 × 内容分"；上标 ⊤ 只是"立成一列"的排版记号；|O<sub>in</sub>| = 这棵树的提问点个数（第 11 卡数过）。<b>整式一句话：把每对（位置, 内容）乘起来、排成一列。</b></span><span class="len">Symbol by symbol: φ<sub>r</sub><sup>i</sup> = tree i\'s encoding function; x = the vertex\'s features; T<sub>i</sub> = the i-th tree; each bracket term = "position of question k × content of question k"; the ⊤ superscript just means "stack into a column"; |O<sub>in</sub>| = the tree\'s question count (counted at card 11). <b>The whole line in a breath: multiply each (position, content) pair and line them up.</b></span></p>',
    '<p class="formula-note"><span class="lz">逐符号（一份一个）：φ<sub>r</sub><sup>i</sup> = "第 i 棵树的编码函数"——把顶点翻译成这棵树那一列得分的机器；T<sub>i</sub> = 第 i 棵树；x = 顶点特征串；|O<sub>in</sub>| = 这棵树的提问点个数（第 11 卡数过）；上标 ⊤ 只是"立成一列"的排版记号，不是计算。<b>整式一句话：把每对（位置分, 内容分）乘起来、排成一列。</b></span><span class="len">Symbol by symbol (one per line of thought): φ<sub>r</sub><sup>i</sup> = "tree i\'s encoding function" — the machine translating a vertex into that tree\'s column of scores; T<sub>i</sub> = the i-th tree; x = the vertex\'s features; |O<sub>in</sub>| = the tree\'s question count (counted at card 11); the ⊤ superscript merely means "stack into a column", not a computation. <b>The whole line in a breath: multiply each (position, content) pair and line them up.</b></span></p>', "c31-symbols")
rep('T₁ 的两条规则在 0、1 层，位置分 = 1.125、1.0；内容分 = 0、0（第 29 卡例 1）→ 逐位乘：',
    '先说位置分的来历（沿用第 30 卡的除法）：CC-Cora 参数 α=9、β=8，第 0 层 9÷8 = 1.125、第 1 层 9÷9 = 1.0。顶点甲 x = (1, 3, 4) 过 T₁：x₂ ≥ 2？3 ≥ 2 满足 → 0；x₁ ≥ 1？1 ≥ 1 满足 → 0。位置分 = 1.125、1.0，内容分 = 0、0 → 逐位乘：', "c31-ex1-rederive-zh")
rep('T₁\'s two rules sit at layers 0 and 1, positions 1.125 and 1.0; contents 0 and 0 (card 29\'s Example 1) → multiply slot by slot:',
    'First, where the positions come from (card 30\'s division): CC-Cora uses α = 9, β = 8, so layer 0 gives 9÷8 = 1.125 and layer 1 gives 9÷9 = 1.0. Vertex A x = (1, 3, 4) through T₁: x₂ ≥ 2? 3 ≥ 2 satisfied → 0; x₁ ≥ 1? 1 ≥ 1 satisfied → 0. Positions 1.125, 1.0; contents 0, 0 → slot by slot:', "c31-ex1-rederive-en")
rep('<b>例 1 续（T₂ 三位）：</b>T₂ 的三条在 0、1、1 层，位置分 = 1.125、1.0、1.0；内容分 = 1、1、0 → 逐位乘：',
    '<b>例 1 续（T₂ 三位）：</b>T₂ 的三条在 0、1、1 层，位置分 = 1.125、1.0、1.0；内容分逐条问：x₃ ≥ 5？4 ≥ 5 不满足 → 1；x₁ ≥ 2？1 ≥ 2 不满足 → 1；x₂ ≥ 1？3 ≥ 1 满足 → 0 → 逐位乘：', "c31-ex1-cont-zh")
rep('<b>Example 1, continued (T₂\'s three slots):</b> T₂\'s three rules sit at layers 0, 1, 1 with positions 1.125, 1.0, 1.0; contents 1, 1, 0 → slot by slot:',
    '<b>Example 1, continued (T₂\'s three slots):</b> T₂\'s three rules sit at layers 0, 1, 1 with positions 1.125, 1.0, 1.0; contents asked one by one: x₃ ≥ 5? 4 ≥ 5 missed → 1; x₁ ≥ 2? 1 ≥ 2 missed → 1; x₂ ≥ 1? 3 ≥ 1 satisfied → 0 → slot by slot:', "c31-ex1-cont-en")
rep('对！乘法的语义是"闸门"：满足（0）就彻底关掉这格的悬账、不满足（1）就放位置分全额通过。加法做不到这种"一票否决"——满足反而加分会把"解释得越清楚、得分越高"搞反。',
    '对！乘法的语义是"闸门"：满足（0）就彻底关掉这格的悬账、不满足（1）就放位置分全额通过。加法做不到这种"一票否决"——满足反而加分会把"解释得越清楚、得分越高"搞反。', "c31-q3-noop")
rep('网络的可训练性不取决于这一步——μc/μp 是固定登记，不参与训练；设计动机是语义，不是梯度。',
    '网络的可训练性不取决于这一步——内容分与位置分都是固定的登记规则，不参与训练；设计动机是语义，不是梯度。', "c31-q3c")
# 数值题题干与 hint 重写（不抄题）
rep('<div class="quiz quiz-num" data-answer="4" data-tol="0.01" data-hint="一列的位数对着"这棵树的提问点个数"——不用算乘积，数提问点。" data-sol="4 位。式 (7) 的输出位数 = 该树的提问点个数 |O<sub>in</sub>|——每个提问点独占一格。">',
    '<div class="quiz quiz-num" data-answer="4" data-tol="0.01" data-hint="式 (7) 的每一格对着树的哪个部位？先数一数这棵树有几个这样的部位。" data-sol="4 位。式 (7) 的输出位数 = 该树的提问点个数 |O<sub>in</sub>|——根 1 个 + 其下 3 个，共 4 格。">', "c31-quiz-attrs")
rep('<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：某树有 4 个提问点。式 (7) 对单个顶点输出几位（几个数）？</span><span class="len">Numeric: a tree has 4 question nodes. How many entries does Eq. (7) output for one vertex?</span></p>',
    '<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：某树的结构是"根问一个问题，其下还有 3 个提问点"。式 (7) 对单个顶点输出几位（几个数）？</span><span class="len">Numeric: a tree has a root question with 3 further question nodes below it. How many entries does Eq. (7) output for one vertex?</span></p>', "c31-quiz-q")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
