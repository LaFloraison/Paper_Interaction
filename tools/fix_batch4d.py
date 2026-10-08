# -*- coding: utf-8 -*-
"""批4 修复 part 4: c15/c16/c17/c18/c19 复审意见"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P = "sites/feng-2026-knowledge-hgnn.html"
s = open(P, encoding="utf-8").read()
applied = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND (" + tag + "): " + o[:70])
        return
    s = s.replace(o, n, 1)
    applied.append(tag)


# ===== c15: EN 题干补引导 =====
rep("After reversing the order of all three columns, what is v1's new row sum?</span>",
    "After reversing the order of all three columns, what is v1's new row sum? (First write the reversed row, then count the 1s)</span>", "c15-en-stem")

# ===== c16: 两处错字 =====
rep("A A single average often helps", "A single average often helps", "c16-A A")
rep("连接一条没动——连线一条没动——", "连线一条没动——", "c16-dup")

# ===== c17: sol 措辞 + 丢掉的 </p> + EN 同步 =====
rep("51.10 − 43.19 = 7.91——每加两层损失都在加剧（2→4 层已掉 22.31）。",
    "51.10 − 43.19 = 7.91——每往深处加两层，都还在失血（2→4 层已掉 22.31，6→8 层还要再掉 12.97）。", "c17-sol-wording")
rep("托了底。    <p class=\"len\">", "托了底。</p>\n    <p class=\"len\">", "c17-p-fix")
rep("In a standard HGNN, features get degree-normalized averaging once per layer",
    "In a standard HGNN (properly met at card 22), features get degree-normalized averaging once per layer", "c17-en-sync1")
rep("over-smoothing</b> (features homogenize over rounds)",
    "over-smoothing</b> (features homogenize over rounds — the last card's topic)", "c17-en-sync2")
rep("And a subtler one: structural information itself.",
    "And a subtler one (this card's protagonist): structural information itself.", "c17-en-sync3")
rep("（邻居暴增时信息挤进固定大小的向量，有判别力的信号被挤丢）。",
    "（邻居暴增时信息挤进固定大小的向量，有判别力的信号被挤丢——本卡不展开，方法篇的讨论卡会回收它）。", "c17-squash-ptr")
rep("(when neighbors explode, discriminative signals get crushed out of fixed-size vectors)",
    "(when neighbors explode, discriminative signals get crushed out of fixed-size vectors — not expanded here; the discussion card picks it up)", "c17-squash-ptr-en")

# ===== c18: 新顶点 → 新成员 =====
rep("因为线上系统每天都会遇到“训练时不存在”的新顶点——归纳成绩差的上不了线。production = 直推 + 归纳合并考，正是这个现实。",
    "因为线上系统每天都会遇到“训练时不存在”的新成员——归纳成绩差的上不了线。production = 直推 + 归纳合并考，正是这个现实。", "c18-xind成员")

# ===== c19: 硬伤清单 =====
rep("训练时把这三个点连<b>图都不给看</b>，用子图 G_sub 训练，考时才放进大图）。",
    "训练时把这些点（那 20%，Cora 上共 162 篇）连<b>图都不给看</b>，用子图 G_sub 训练，考时才放进大图）。", "c19-three-points")
rep("正文宣称 80/20，表格实测另有说法（第 48 批判卡揭晓）。",
    "正文宣称 80/20，表格实测另有说法（第 48 批判卡揭晓）。", "c19-noop")
rep("<b>例 1（Cora 的完整切分走查，Table II/III 转录）：</b>",
    "<b>例 1（Cora 的完整切分走查，转录自论文的两张结果表 Table II/III）：</b>", "c19-tbl-gloss")
rep("production 卷：同样的 1,625/677 不动，406 再切成直推 244 + 归纳 162；训练阶段 162 个点及其连边 entirely 隐去，只能用 2,546 个点拼出的子图。</p>",
    "production 卷：同样的 1,625/677 不动，406 再切成直推 244 + 归纳 162（自检两行：1,625 + 677 + 406 = 2,708 ✓；244 + 162 = 406 ✓）。训练阶段把 162 篇及其连边完全隐去：2,708 − 162 = <b>2,546</b>，只能用剩下 2,546 篇拼出的子图。</p>", "c19-ex1-arith")
rep("during training the 162 and their edges are entirely hidden, leaving a sub-graph of 2,546 nodes.</p>",
    "during training the 162 and their edges are fully hidden: 2,708 − 162 = <b>2,546</b>, leaving a sub-graph of 2,546 nodes.</p>", "c19-ex1-arith-en")
rep("论文用两套设定考所有方法。<b>Transductive（传统卷）</b>",
    "论文用两套设定考所有方法（设定 = 考法，模型还是同一个）。<b>Transductive（传统卷）</b>", "c19-setting-gloss")
rep("The paper tests everything under two settings. <b>Transductive (the classic paper)</b>",
    "The paper tests everything under two settings (a setting is an exam format — the model stays the same). <b>Transductive (the classic paper)</b>", "c19-setting-gloss-en")
rep('<div class="quiz quiz-num" data-answer="244" data-tol="0.01" data-hint="Cora 的 406 个测试点切成“直推 + 归纳”两部分——第 17 卡例 1 刚走过切法。" data-sol="406 = 244（直推，训练时可见）+ 162（归纳，训练时隐去）。production 报告的 Cora 成绩 = 两种测试合并的 406 点上的表现。">',
    '<div class="quiz quiz-num" data-answer="244" data-tol="0.01" data-hint="Cora 的 406 个测试点切成“直推 + 归纳”两部分——本卡例 1 刚走过这道切法题。" data-sol="406 = 244（直推，训练时可见）+ 162（归纳，训练时隐去）。production 报告的 Cora 成绩 = 两种测试合并的 406 点上的表现。">', "c19-hint")
rep("例 2（为什么在乎这个差别）：</b>TDR-Encoder 的 GBDT 在\"预定义任务\"上预训练",
    "例 2（为什么在乎这个差别）：</b>预备篇讲过的 GBDT（第 12、13 卡的接力纠错树队）会在一个\"预定义任务\"（提前定好的预测任务）上预训练，产出的规则由 TDR-Encoder（方法篇的主角，第 27 卡细讲）编成向量——这就是论文说的\"知识嵌入\"", "c19-ex2-gloss")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(applied))
for a in applied:
    print(" -", a)
