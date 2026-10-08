# -*- coding: utf-8 -*-
"""批5 复审意见落地: c24 数值题硬伤 + c21/c22 打磨"""
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


# ===== c24: 数值题三处修正 =====
rep('data-answer="0.9526" data-tol="0.002" data-hint="先数这个顶点参加几条超边，代入 ρ(x)=σ(2x)，再用 σ 的算法 1÷(1+e⁻ˣ) 压到 0–1——把你答案的前四位小数填进来。" data-sol="参加 3 条 → σ(2×3) = σ(6) = 1 ÷ (1 + e⁻⁶) = 1 ÷ 1.002479 ≈ 0.9526。注意 ρ 里的 2 是旋钮 w——行和先乘 2 再进 σ。"',
    'data-answer="0.9526" data-tol="0.002" data-hint="先数这个顶点参加几条超边，代入本题的 ρ(x)=σ(x)，再用 σ 的算法 1÷(1+e⁻ˣ) 压到 0–1——把答案的前四位小数填进来。" data-sol="参加 3 条 → σ(1×3) = σ(3) = 1 ÷ (1 + e⁻³) = 1 ÷ 1.049787 ≈ <b>0.9526</b>。本题 w=1（本文惯例是 w=2，见例 1、例 2）——旋钮不同，同一个行和会得到不同的显著性。"',
    "c24-quiz-fix")

# ===== c24: 例 1 拆句 + Q3 平滑白话 =====
rep("<b>第二步压一压：</b>ρ(x) = σ(2x)，而 σ 的算法是 σ(x) = 1 ÷ (1 + e<sup>−x</sup>)（e ≈ 2.718，计算器上有这个键）。逐个算：",
    "<b>第二步压一压：</b>ρ(x) = σ(2x)，而 σ 的算法是 σ(x) = 1 ÷ (1 + e<sup>−x</sup>)（e ≈ 2.718，计算器上有这个键）。<br>逐个算：", "c24-ex1-split")
rep("而机器中间的特征扛不过",
    "而打分机器中间算出来的那些特征（顺着关系反复平均后的数值）扛不过", "c24-q3-gloss")
rep("while the machine's intermediate features do not",
    "while the scoring machine's own intermediate features (values repeatedly averaged along relations) do not", "c24-q3-gloss-en")

# ===== c22: 积木③ 措辞 + 公式下移到符号表后 =====
rep("<b>③ 归一化</b>——每个顶点收下自己各条超边送回的\"组平均值\"后，整体除以 √(自己参加的超边条数)（人脉广的顶点不该因为票多而吵翻天）。</p>",
    "<b>③ 归一化</b>——每个顶点收下自己各条超边送回的\"组平均值\"后除以 √(自己参加的超边条数)；这个除法在\"送去\"和\"收回\"时各做一次（人脉广的顶点不该因为票多而吵翻天）。</p>", "c22-block3")
rep("<b>(3) Normalize</b> — each vertex collects the group averages sent back and divides the total by √(how many hyperedges it joined) (well-connected vertices must not drown everyone with extra votes).</p>",
    "<b>(3) Normalize</b> — each vertex collects the group averages sent back and divides by √(how many hyperedges it joined), applied once on the send leg and once on the return leg (well-connected vertices must not drown everyone with extra votes).</p>", "c22-block3-en")

# 公式块下移：先删除原位置，再插到符号表之后
formula = '''    <span class="tex-display" data-tex="X^{l+1} = \\sigma\\!\\left(D_v^{-1/2}\\, H\\, W\\, D_e^{-1}\\, H^{\\top}\\, D_v^{-1/2}\\, X^{l}\\, \\Theta\\right)"></span>
    <p class="formula-note"><span class="lz">读法（从右往左）：X<sup>l</sup> 是第 l 层的特征表 → 乘 Θ（机器自己学的旋钮）→ 经过归一化与收集的连乘（= 上面三块积木）→ 最后套 σ（把数值折一下，增加表达力的"弯折"）。别被连乘吓到：它按顺序执行，就是"收集→平均→归一化"。</span><span class="len">Reading (right to left): X<sup>l</sup> is the layer-l feature table → times Θ (the machine's learned knobs) → through the chain of collect-and-average matrices (= the three blocks above) → wrapped in σ (a bend that adds expressiveness). Do not fear the chain: executed in order, it is simply "collect → average → normalize".</span></p>
'''
if formula in s:
    s = s.replace(formula, "", 1)
    # 插到符号表结束 </table> 之后
    anchor = '<td><span class="lz">最后一步</span><span class="len">The final touch</span></td></tr>\n    </table>\n'
    if anchor in s:
        s = s.replace(anchor, anchor + formula, 1)
        done.append("c22-formula-move")
    else:
        print("!! anchor for formula move not found")
else:
    print("!! formula block not found verbatim")

# ===== c21: 数值题换非例子数字 + 段落拆分 =====
rep('data-answer="2" data-tol="0.01" data-hint="备料机器的台数对着“有几种数据”——回看例 2 的走查。" data-sol="两种数据（原始标签 X、编组表 H）→ 两台备料机器。若只喂一种，就只剩一台——DD 与 RD 的分家正是“两本账 or 一本账”。"',
    'data-answer="3" data-tol="0.01" data-hint="备料机器的台数对着“数据有几路”——原来的路数再加新路数。" data-sol="2 + 1 = 3 台（原文的数据两路 + 新增一路）。只多装一台、多订一列，两步骨架纹丝不动——这正是下一题要考的“可扩展”的具体数字。"',
    "c21-quiz")
rep('<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：本文实例化里装了几台备料机器（编码器）？</span><span class="len">Numeric: how many prep machines (encoders) does the paper\'s instantiation install?</span></p>',
    '<p class="quiz-q"><span class="ex-tag">APPLY</span><span class="lz">数值题：某医院照搬论文配方（原有两路数据），再加一路"化验单数据"，总共要装几台备料机器？</span><span class="len">Numeric: a hospital copies the paper\'s recipe (its two data streams) and adds one more stream of lab reports. How many prep machines in total?</span></p>',
    "c21-quiz-q")
rep('<p class="lz">配方里的两样东西值得多说一句：<b>备料的机器</b>按"有几种数据"配置——喂几路数据，就放几台（论文叫它 encoder，编码器："把原始资料翻译成数字的机器"）；<b>加工</b>那一步内部又劈成两小段：先把几串数字合成一份（论文叫 fusion，融合："把几份成绩单订成一份"），再进打分机器打分。合成发生在第二步<b>内部</b>，不是独立的第三步。</p>',
    '<p class="lz"><b>备料的机器</b>按"有几种数据"配置——喂几路数据，就放几台（论文叫它 encoder，编码器："把原始资料翻译成数字的机器"）。</p>'
    '<p class="lz">再说<b>加工</b>那一步：它内部又劈成两小段——先把几串数字合成一份（论文叫 fusion，融合："把几份成绩单订成一份"），再进打分机器打分。注意：合成发生在第二步<b>内部</b>，不是独立的第三步。</p>',
    "c21-split")

open(P, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
