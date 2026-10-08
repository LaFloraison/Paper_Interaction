# -*- coding: utf-8 -*-
"""批3 修复: c10 / c11 / c12 / c13 审卡意见落地"""
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


# ========== c10 ==========
rep("所以“第 2 层的节点”是根的两步之后——本卡例 1 的两问树最大深度只有 1。",
    "所以“第 2 层的节点”是根的两步之后——例 1 的问题节点最深在第 1 层，叶子落在第 2 层。", "c10-sol")

rep("每个内部节点问一个特征问题（这条问题就是一条规则），顺着答案走到叶子，叶子上的就是结论。",
    "每个内部节点问一个关于某项属性的具体问题（如“直径多大？”“是不是黄色？”——这条问题就是一条规则），顺着答案走到叶子，叶子上的就是结论。", "c10-def-zh")

rep("each inner node asks one question about a feature (that question is a rule)",
    "each inner node asks one concrete question about an attribute (like “how wide?” “is it yellow?” — that question is a rule)", "c10-def-en")

rep("申请人乙：收入 8 万 → 第一问就“否”（8 &lt; 10）→ 拒绝。同一条规则对不同的人，答案各自走进不同的叶子。</p>",
    "申请人乙：收入 8 万 → 第一问就“否”（8 &lt; 10）→ 拒绝。顺带数深度：收入问题在第 0 层，逾期问题在第 1 层，叶子结论在第 2 层——最狠的问题站最浅层。</p>", "c10-ex2-depth-zh")

rep("Applicant B: income 80k → first \"no\" (80 &lt; 100) → rejected. One rule, different people, different leaves.</p>",
    "Applicant B: income 80k → first \"no\" (80 &lt; 100) → rejected. Count depths along the way: the income question sits at layer 0, the overdue question at layer 1, the leaves at layer 2 — the fiercest question stands shallowest.</p>", "c10-ex2-depth-en")

rep("这叫过拟合，后面 Table VII 会亲眼看到树太多反而变差。",
    "这叫过拟合，后面实验篇会亲眼看到树太多反而变差。", "c10-mis-zh")
rep("overfitting; Table VII will show more trees hurting.",
    "overfitting; the experiment part will show more trees hurting.", "c10-mis-en")

rep("照片是像素海——没有现成的“问题”可问，得先提取特征才轮得到树。这正是本文让它先“预训练”的原因。",
    "照片是几百万个小色块——没有现成的“问题”可问，得先提炼出属性才轮得到提问。这正是本文后面要先训练出一队树的原因。", "c10-q3a-zh")
rep("Photos are oceans of pixels — no ready-made \"questions\" to ask; features must be extracted before any questioning. This is exactly why the paper pre-trains first.",
    "Photos are millions of color dots — no ready-made \"questions\" to ask; attributes must be distilled before any questioning. This is why the paper trains its team of trees first.", "c10-q3a-en")

rep("逐问筛选天然适合树。本文的 Heloc 信贷数据集正是这种形状。",
    "逐问筛选天然适合树。本文实验里就有这样一份信贷数据集。", "c10-q3b-zh")
rep("question-by-question filtering is a tree's home turf. The paper's Heloc credit dataset is exactly this shape.",
    "question-by-question filtering is a tree's home turf. The paper's experiments include exactly such a credit dataset.", "c10-q3b-en")

rep("硬拆成“温度&gt;25？”的问题串会很笨拙——时间序列另有更顺手的工具。",
    "硬拆成“温度&gt;25？”的问题串会很笨拙——这类连绵曲线另有更顺手的工具。", "c10-q3c-zh")
rep("forcing it into \"temp &gt; 25?\" questions is clumsy — time series have better tools.",
    "forcing it into \"temp &gt; 25?\" questions is clumsy — smooth curves have better tools.", "c10-q3c-en")

# ========== c11 ==========
rep("T₁ 的内部节点：根 x₂ ≥ 2（深度 0）、下层 x₁ ≥ 1（深度 1）。",
    "T₁ 一共就两个问题：根 x₂ ≥ 2（深度 0）——它的“满足”枝直接连一片叶子，“不满足”枝才进入下层的问题 x₁ ≥ 1（深度 1，其两个出口都是叶子）。", "c11-struct-zh")
rep("T₁'s inner nodes: root x₂ ≥ 2 (depth 0), below it x₁ ≥ 1 (depth 1).",
    "T₁ has exactly two questions: root x₂ ≥ 2 (depth 0) — its \"yes\" branch runs straight to a leaf, its \"no\" branch enters the lower question x₁ ≥ 1 (depth 1, both exits are leaves).", "c11-struct-en")

rep("这个 0/1 记录正是后面 μc 要的东西。",
    "这个“满足/不满足”的 0/1 记录，正是后面给规则编码时要用的原料（第 29 卡）。", "c11-muc-zh")
rep("the satisfied/not-satisfied record of the two rules — exactly what μc will consume.",
    "the satisfied/not-satisfied 0/1 record of the two rules — the raw material the later rule encoding consumes (card 29).", "c11-muc-en")

rep("记住这个 5——后面“每棵树一位、每位乘权重”的编码向量正好 5 维，再翻倍拼接成 10 维。",
    "记住这个 5——后面给每条规则分配一个数位时，向量正好 5 维（第 31 卡）。", "c11-five-zh")
rep("Remember this 5 — the \"one slot per rule, weighted\" encoding will be exactly 5-dimensional, then doubled to 10 by concatenation.",
    "Remember this 5 — when each rule later gets its own slot, the vector is exactly 5-dimensional (card 31).", "c11-five-en")

rep("叶子只是当时那个任务的答案，换个任务就作废。",
    "叶子只是当时那个任务的答案，换个任务就作废（换任务时 GBDT 会重新训出新树，但“只留问题不留答案”的原则不变）。", "c11-retrain-zh")
rep("leaves are answers to that one old task, void on a new one.",
    "leaves are answers to that one old task, void on a new one (a new task means retraining fresh trees, but the keep-questions-drop-answers principle never changes).", "c11-retrain-en")

rep("深度 d(o) 从根 = 0 数起——叶子结论一律不要。</span></b></p>",
    "深度 d(o) 从根（树最顶上的起点节点）= 0 数起——叶子结论一律不要。</span></b></p>", "c11-root-zh")
rep("depth d(o) counts from the root = 0 — leaf conclusions are discarded.</span></b></p>",
    "depth d(o) counts from the root (the tree's topmost starting node) = 0 — leaf conclusions are discarded.</span></b></p>", "c11-root-en")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(applied))
for a in applied:
    print(" -", a)
