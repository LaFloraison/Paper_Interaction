# -*- coding: utf-8 -*-
"""批4 修复: c14 打磨 / c15 答案键 / c16 例2 / c17 / c18"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
applied = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND (" + tag + "): " + o[:60])
        return
    s = s.replace(o, n, 1)
    applied.append(tag)


# ===== c14 =====
rep("顺序一变答案就变，不不变。", "顺序一变答案就变，就不是“不变”了。", "c14-typo")
rep("the order changed, the answer changed, not invariant.",
    "the order changed, so the answer changed — not invariant.", "c14-typo-en")
rep("结账小票是 sums 的主场，体育比赛“第几棒”是反例的主场。",
    "结账小票是“求和”的主场，体育比赛“第几棒”是反例的主场。", "c14-sums")
rep("Receipt totals live in the sum world; relay \"which leg did I run\" lives in the counter-example world.",
    "Receipt totals live in the summing world; relay \"which leg did I run\" lives in the counter-example world.", "c14-sums-en")
rep("论文的 HOI-Encoder 用的正是加法汇总。",
    "论文里“数人脉”的那位主角（HOI-Encoder，第 24 卡登场）用的正是加法汇总。", "c14-hoi")
rep("The paper's HOI-Encoder lives on exactly this summing aggregation.",
    "The paper's people-counting protagonist (the HOI-Encoder, arriving at card 24) lives on exactly this summing aggregation.", "c14-hoi-en")
rep("这就是 Deep Sets 等集合网络用“先求和再变换”的原因，也是本文 HOI-Encoder 对超边求和的原因。",
    "很多处理“一堆东西”的模型都这么做——本文那位数人脉的主角对超边用的也是加法。", "c14-deepsets")
rep("This is why set networks like Deep Sets sum-then-transform, and why the paper's HOI-Encoder sums over hyperedges.",
    "Plenty of models that handle \"a bunch of things\" do exactly this — and the paper's people-counting protagonist sums over hyperedges too.", "c14-deepsets-en")
rep("数值题：订单\"3 个苹果、2 个梨\"，苹果 2 元、梨 3 元。总价多少？若把订单倒过来写（2 梨 3 苹果），总价又是多少？",
    "数值题：订单倒过来写成\"2 个梨、3 个苹果\"（梨 3 元、苹果 2 元），新写法的总价是多少？", "c14-quiz-zh")
rep("Numeric: an order of 3 apples and 2 pears, apples 2 yuan, pears 3 yuan. The total? And if the order is written reversed (2 pears, 3 apples)?",
    "Numeric: the order is written reversed as \"2 pears, 3 apples\" (pears 3 yuan, apples 2 yuan). What is the total in this new writing?", "c14-quiz-en")

# ===== c15 =====
rep('<div class="quiz quiz-num" data-answer="3" data-tol="0.01" data-hint="行和 = 每行 1 的个数。列对调不改任何一行的成员构成——每行的 1 还是那么多。" data-sol="v1：只属于围棋 → 行 [1,0,0] → 行和 1；对调后 [0,0,1] 仍只有一个 1。四行行和 = 1,2,2,1，与第 8 卡完全一致——这正是“不变”的含义。">',
    '<div class="quiz quiz-num" data-answer="1" data-tol="0.01" data-hint="行和 = 每行 1 的个数。列倒序不改任何一行的成员构成——每行的 1 还是那么多。" data-sol="v1：只属于围棋 → 行 [1,0,0] → 行和 1；倒序后 [0,0,1] 仍只有一个 1。四行行和 = 1,2,2,1，与第 8 卡完全一致——这正是“不变”的含义。">', "c15-answerkey")
rep("数值题：第 8 卡的 H 里 v1 行为 [1,0,0]。把三条超边的列整个倒序排列后，v1 的新行和是多少？",
    "数值题：第 8 卡的 H 里 v1 行为 [1,0,0]。把三条超边的列整个倒序排列后，v1 的新行和是多少？（先写出倒序后的行，再数 1 的个数）", "c15-quiz-zh")
rep("φ 必须列交换不变——H 的列随便怎么调换",
    "φ（论文给结构编码器起的名字）必须列交换不变——H 的列随便怎么调换", "c15-phi")
rep("φ must be column-exchange invariant",
    "φ (the paper's name for the structural encoder) must be column-exchange invariant", "c15-phi-en")
rep('<button class="opt" data-correct="1" data-expl="正确！“第 1 列的行和”“第 2 列的行和”把列的身份写进了输出——列一换，输出就变。不变性要求输出只依赖“行的成员构成”。"><span class="lz">给每个顶点输出“第 1 列的行和”</span><span class="len">Outputting for each vertex "the row sum of column 1"</span></button>',
    '<button class="opt" data-correct="1" data-expl="正确！“第 1 组里有多少人”把组的编号写进了输出——登记顺序一换，“第 1 组”就指另一群人，输出跟着变。不变性要求输出只依赖“每个顶点自己的成员构成”。"><span class="lz">给每个顶点输出“第 1 条超边圈住了几个人”</span><span class="len">Outputting for each vertex "how many people the first hyperedge embraces"</span></button>', "c15-q3")

# ===== c16 =====
rep("<b><span class=\"hl\">过平滑 = 邻居间反复互相平均，把各自独有的特征抹到趋同——信息是共享了，个性也丢了。</span></b>它是\"图上的平均\"这类操作的固有代价，不是 bug。",
    "<b><span class=\"hl\">过平滑 = 邻居间反复互相平均，把各自独有的特征（描述每个人的那些数值）抹到趋同——信息是共享了，个性也丢了。</span></b>它是\"图上的平均\"这类操作的固有代价，不是 bug。", "c16-features")
rep("single average often helps; the harm is <b>many rounds without stopping</b>",
    "A single average often helps; the harm is <b>many rounds without stopping</b>", "c16-mis-en-cap")
rep("<p class=\"lz\"><b>例 2（一条链上的慢性趋同）：</b>四个顶点排成链（第 9 卡沙盒的原型），只有 v1 拿着 10、其余全 0。第 1 轮：10 漏给邻居一点（沙盒实测 5.00、3.54、0、0）；第 2、3 轮：沿链继续渗；多轮之后四个值挤成一团。链越长渗得越慢，但方向只有一个：<b>全部一样</b>。</p>",
    "<p class=\"lz\"><b>例 2（两间包厢的分界）：</b>四个人分两组：包厢 A = {甲, 乙}，特征 [8, 0]；包厢 B = {丙, 丁}，特征 [2, 0]。规则仍是\"同组互相平均\"，一轮：甲、乙都变 (8+0)÷2 = <b>4</b>；丙、丁都变 (2+0)÷2 = <b>1</b>。注意：包厢内差异归零了，但 A 组 4、B 组 1——<b>两组之间差 3，一轮平均抹不掉</b>，因为没有连线把他们连起来。平滑只抹\"有连线的人之间\"的差异。</p>", "c16-ex2-zh")
rep("<p class=\"len\"><b>Example 2 (slow convergence along a chain):</b> four vertices in a chain (the card-9 sandbox prototype), only v1 holding 10. Round 1: some leaks to neighbors (sandbox measured 5.00, 3.54, 0, 0); rounds 2–3: it seeps along the chain; after many rounds the four values crowd together. Longer chains leak slower — but the direction is singular: <b>all the same</b>.</p>",
    "<p class=\"len\"><b>Example 2 (two rooms, two fates):</b> four people in two groups: room A = {A1, A2} with features [8, 0]; room B = {B1, B2} with features [2, 0]. The rule is still \"group-mates average together\"; after one round A1, A2 both become (8+0)÷2 = <b>4</b>, and B1, B2 both become (2+0)÷2 = <b>1</b>. Notice: within-room differences hit zero, yet room A sits at 4 and room B at 1 — <b>the gap of 3 survives one round</b>, because no line joins the rooms. Smoothing only erases differences between connected people.</p>", "c16-ex2-en")
rep("超边/边还是那些。变的只是顶点身上的值。",
    "连线一条没动——原来谁挨着谁，现在还是谁挨着谁。变的只是每个人身上的值。", "c16-q1c")
rep("The connections between vertices one bit — hyperedges/edges unchanged; only vertex values move.",
    "Not a single connection moves — who neighbors whom stays exactly as it was; only the values on each person change.", "c16-q1c-en")
rep("趋同抹掉的是“谁与谁不同”——而图任务恰恰靠“不同”来分类。个性没了，分类就抓瞎。",
    "趋同抹掉的是“谁与谁不同”——而要分辨“谁是谁”，靠的恰恰是“不同”。个性没了，分辨就抓瞎。", "c16-q1b")
rep("Over-smoothing erases… the differences between vertices (individuality)?</p>",
    "Over-smoothing erases… the differences between vertices (individuality)?</p>", "c16-q1b-en-noop")
rep("删特征只会更糟——模型可用信息更少了，平不平滑它都更瞎。",
    "删特征只会更糟——手里的信息更少了，平不平滑都更瞎。", "c16-q3c")

# ===== c17 =====
rep("标准 HGNN 里，特征每过一层就被\"按度数归一化\"地平均一次——数值稳了，但论文指出两笔账：一笔是<b>过平滑</b>（多轮平均后顶点特征同质化）；另一笔是<b>特征压缩</b>（邻居暴增时信息挤进固定大小的向量，有判别力的信号被挤丢）。",
    "标准 HGNN（第 22 卡正式认识它）里，特征每过一层就被\"按度数归一化\"地平均一次——数值稳了，但论文指出两笔账：一笔是<b>过平滑</b>（多轮平均后顶点特征同质化，上一卡刚讲过）；另一笔是<b>特征压缩</b>（邻居暴增时信息挤进固定大小的向量，有判别力的信号被挤丢）。", "c17-hgnn-gloss")
rep("而 DD-HGNN（两份档案都在）同范围只从 76.06 降到 <b>49.53</b>：不是免疫，但两路未平滑知识托了底。",
    "而本文的双路型号 DD-HGNN（第 34 卡正式讲，两份档案都在）同范围只从 76.06 降到 <b>49.53</b>（落差 26.53，约为 HGNN 落差 43.19 的六成）：不是免疫，但两路未平滑知识托了底。</p>"
    "<p class=\"len\">…EN…</p>", "c17-dd-gloss-zh")
rep("<b>例 1（一个被冲走的数字）：</b>v1 参加 6 条超边。标准 HGNN 第一层就把它除以 √6（归一化），第二层再被邻居平均稀释——三轮之后，\"6\"这个数在 v1 的特征向量里已经不对了。",
    "<b>例 1（一个被冲走的数字）：</b>v1 参加 6 条超边。标准 HGNN 第一层就把它除以 √6：6 ÷ 2.449 ≈ <b>2.45</b>——这一步是刻意把\"参加 6 条\"和\"参加 36 条\"的顶点拉到同一个尺度，代价是原始计数从此失真。第二层起，邻居平均再把这点残迹混进别人的值里，混完就无法还原——\"6\"再也读不出来了。", "c17-ex1-zh")
rep("<b>Example 1 (a washed-away number):</b> v1 joins 6 hyperedges. A standard HGNN divides by √6 in the very first layer (normalization), then neighbor-averaging dilutes it further — after three rounds, the \"6\" is no longer readable in v1's features.",
    "<b>Example 1 (a washed-away number):</b> v1 joins 6 hyperedges. A standard HGNN divides by √6 in the very first layer: 6 ÷ 2.449 ≈ <b>2.45</b> — deliberately pulling \"joins 6\" and \"joins 36\" vertices onto one scale, at the price of distorting the raw count. From layer two on, neighbor-averaging blends the trace into other vertices' values, unrecoverable — the \"6\" is gone for good.", "c17-ex1-en")
rep("而 HOI-Encoder 的存档方式：直接把 6（或它的平滑函数值）放进一份<b>不参与平滑</b>的向量。",
    "而 HOI-Encoder 的存档方式：直接把 6（或它经一层变换后的值）放进一份<b>不参与平滑</b>的向量。", "c17-ex1-fix2")
rep("（40 类任务随机猜是 2.5，等于几乎全废）",
    "（40 类任务随机猜的底线是 2.5——30.22 只剩原来的四成）", "c17-ex2-fix")
rep("(a 40-class task has a 2.5 random floor — nearly destroyed)",
    "(a 40-class task has a 2.5 random floor — 30.22 is barely four-tenths of where it started)", "c17-ex2-fix-en")
rep('<div class="quiz quiz-num" data-answer="43.19" data-tol="0.06" data-hint="读第 45 卡 Table VIII：普通 HGNN 2 层与 8 层两行相减。" data-sol="73.41 − 30.22 = 43.19——8 层时 40 类任务只剩 30.22（随机底线 2.5），过平滑随层数累积的直接实测。">',
    '<div class="quiz quiz-num" data-answer="7.91" data-tol="0.05" data-hint="读第 45 卡 Table VIII 的 HGNN 列：4 层与 6 层两行相减（例 2 用的是 2 层与 8 层，这题换两行）。" data-sol="51.10 − 43.19 = 7.91——每加两层损失都在加剧（2→4 层已掉 22.31）。">', "c17-quiz-attrs")
rep('<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：Table VIII 里普通 HGNN 从 2 层到 8 层掉了多少个百分点（两位小数）？</span><span class="len">Numeric: from Table VIII, how many points does plain HGNN drop from 2 to 8 layers (two decimals)?</span></p>',
    '<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：Table VIII 里普通 HGNN 从 4 层到 6 层掉了多少个百分点（两位小数）？</span><span class="len">Numeric: from Table VIII, how many points does plain HGNN drop from 4 to 6 layers (two decimals)?</span></p>', "c17-quiz-q")
rep("更隐蔽的一笔：结构性信息本身。",
    "更隐蔽的一笔（本卡的主角）：结构性信息本身。", "c17-focus")
rep("它的近亲叫<b>特征压缩（over-squashing）</b>",
    "它的近亲叫<b>特征压缩（over-squashing）</b>", "c17-noop")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(applied))
for a in applied:
    print(" -", a)
