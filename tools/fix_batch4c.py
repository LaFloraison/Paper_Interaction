# -*- coding: utf-8 -*-
"""批4 修复 part 3: c18"""
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


# 动机 3 句并 2 句
rep("两个学生备考。甲拿到历年考卷<b>练过题干</b>（但没答案）；乙只复习讲义，从没见过真题。上考场，两人面对的难度其实不同。",
    "两个学生备考：甲拿到历年考卷<b>练过题干</b>（但没答案），乙只复习讲义、从没见过真题。上考场，两人面对的难度其实不同。", "c18-motif-zh")
rep("Two students prepare. Student A has drilled the <b>questions</b> of past papers (never the answers); B has only read lecture notes, never a real exam. On test day they face genuinely different difficulties.",
    "Two students prepare: A has drilled the <b>questions</b> of past papers (never the answers), while B has only read lecture notes, never a real exam. On test day they face genuinely different difficulties.", "c18-motif-en")

# 半监督 白话
rep("半监督学习的经典场景：100 个学生只有 20 个有成绩单（标签贵）",
    "半监督学习（只有一小部分数据带答案）的经典场景：100 个学生只有 20 个有成绩单（成绩单要花钱、花时间）", "c18-semi-zh")
rep("The classic semi-supervised setup: 100 students, only 20 with transcripts (labels are expensive)",
    "The classic semi-supervised setup (only a small slice of the data carries answers): 100 students, only 20 with transcripts (transcripts cost money and time)", "c18-semi-en")

# 特征 白话挂靠
rep("直推设定里测试点的<b>标签</b>始终锁着，看到的只是特征和关系——正如同卷面没答案时读题是合法的。",
    "直推设定里测试点的<b>标签</b>始终锁着，看到的只是特征和关系（比如他们选了什么课、和谁同组）——正如同卷面没答案时读题是合法的。", "c18-feature-zh")
rep("In the transductive setting the test points' <b>labels</b> stay locked; only features and relations are visible — like reading an exam paper whose answers are missing.",
    "In the transductive setting the test points' <b>labels</b> stay locked; only features and relations are visible (which courses they take, who shares their group) — like reading an exam paper whose answers are missing.", "c18-feature-en")

# Q1 正确项解析 删"（图都连在一起）" + production 指路
rep("对！直推：测试点特征已在训练视野里（图都连在一起）；归纳：测试点训练时不存在。论文的 production 设定两种各占一部分。",
    "对！直推：测试点的特征训练时就在你眼前（认识这个人）；归纳：测试点训练时根本不存在。论文的 production 设定（下一卡细讲）两种各占一部分。", "c18-q1a")

# easier 混语
rep("直觉上直推 easier：毕竟你研究过他们选课的口味。",
    "直觉上直推更轻松：毕竟你研究过他们选课的口味。", "c18-easier")
rep("Intuitively transductive is easier — you have studied their course tastes.",
    "Intuitively the transductive side feels easier — you have studied their course tastes.", "c18-easier-en")

# 例2 升级：两份成绩单
rep("<p class=\"lz\"><b>例 2（数字版）：</b>100 名学生、20 份标签：直推测试 = 80 人（见过特征没见过标签）；归纳测试 = 50 名新生（连特征都是训练后出现的）。直觉上直推更轻松：毕竟你研究过他们选课的口味。论文两种都考——还把它们打包成一个\"production 设定\"。</p>",
    "<p class=\"lz\"><b>例 2（两份成绩单）：</b>同一套规律、两场考试分开记分：直推考场坐 80 个\"认识但没成绩单\"的老面孔，归纳考场坐 50 个明天才转来的全新学生。同一班人马，直推可能猜得更准（毕竟研究过他们选课的口味），归纳才是硬功夫——外推到完全没见过的人。两场分数<b>分开报告</b>，不能混在一张榜上。</p>", "c18-ex2-zh")
rep("<p class=\"len\"><b>Example 2 (with numbers):</b> 100 students, 20 labels: transductive = 80 (features seen, labels unseen); inductive = 50 newcomers (features appear only after training). Intuitively the transductive side feels easier — you have studied their course tastes. The paper tests both — and bundles them into one \"production setting\".</p>",
    "<p class=\"len\"><b>Example 2 (two report cards):</b> one rule-set, two exams scored separately: the transductive hall seats 80 familiar faces without transcripts; the inductive hall seats 50 brand-new students transferring in tomorrow. The same crew may guess the transductive hall more accurately (their course tastes were studied), but induction is the real test — extrapolating to people never seen. The two scores are <b>reported separately</b>, never merged into one board.</p>", "c18-ex2-en")

# 数值题换数字
rep('<div class="quiz quiz-num" data-answer="80" data-tol="0.01" data-hint="100 个学生里，20 个有标签、80 个没有——直推测试的正是“认识但没答案”的那批。" data-sol="直推测试集 = 80 人（特征可见、标签锁定）；归纳测试集是后来的 50 名新生。两批人互不重叠。">',
    '<div class="quiz quiz-num" data-answer="175" data-tol="0.01" data-hint="没有成绩单的那批人正是直推测试集——用总人数减去有成绩单的人数。" data-sol="240 − 65 = 175 人（特征可见、标签锁定）。对比本卡例子的 100−20=80：规则不变，数字换人。">', "c18-quiz-attrs")
rep('<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：100 名学生、20 份成绩单。直推测试集有多大？</span><span class="len">Numeric: 100 students, 20 transcripts. How big is the transductive test set?</span></p>',
    '<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：年级里 240 名学生，只有 65 份成绩单。直推测试集有多大？</span><span class="len">Numeric: a grade has 240 students, only 65 with transcripts. How big is the transductive test set?</span></p>', "c18-quiz-q")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(applied))
for a in applied:
    print(" -", a)
