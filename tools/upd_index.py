# -*- coding: utf-8 -*-
"""更新大厅 index.html：新增 Paper #2 卡片、6 个知识点行、按 slug 的进度总数"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = "index.html"
s = open(p, encoding="utf-8").read()
n = 0


def rep(o, nn, tag):
    global s, n
    if o not in s:
        print("!! NOT FOUND:", tag); return
    s = s.replace(o, nn, 1); n += 1; print("ok", tag)


# 1) Paper #2 卡片：插在 Paper #1 卡片之后、hint 之前
card2 = '''    <a class="papercard" href="sites/feng-2026-knowledge-hgnn.html">
      <span class="pc-kicker">Paper #2 · TPAMI 2026</span>
      <div class="pc-title">Knowledge-Embedded Hypergraph Neural Networks</div>
      <div class="pc-en">Feng, Zhang, Du, Ying, Wu, Gao · Tsinghua × Xi'an Jiaotong × Shanghai U × Shenzhen U</div>
      <div class="pc-meta">52 cards · bilingual 中/EN · ~2–3 h · prerequisites from zero · 3 figures + 10 tables each on their own card</div>
      <div class="pc-line"><b>In one sentence:</b> conventional hypergraph networks only smooth features along relations — this paper prepends a knowledge-embedding stage (a structural ledger from hyperedge counts, a rule ledger from GBDT questions) and fuses them, gaining 7.3 points on Cora.</div>
      <div class="pc-prog"><div class="pc-bar"><div class="pc-fill" id="fill-feng-2026-knowledge-hgnn"></div></div><span id="txt-feng-2026-knowledge-hgnn">Not started</span></div>
    </a>
'''
rep('    <div class="hint">📄 <b>Next paper:</b>', card2 + '    <div class="hint">📄 <b>Next paper:</b>', "papercard2")

# 2) 六个新知识点行：插在 perrault 最后一行之后（kp-opt-gradient 行后）
kp_rows = '''      <tr><td class="kpid">kp-hypergraph</td><td><a href="sites/feng-2026-knowledge-hgnn.html#kp-hypergraph">Hypergraph &amp; incidence matrix</a></td><td>Paper #2</td><td>A hyperedge joins any number of vertices; H is the 0/1 roster, row sums = vertex degrees</td></tr>
      <tr><td class="kpid">kp-decision-tree</td><td><a href="sites/feng-2026-knowledge-hgnn.html#kp-decision-tree">Decision tree</a></td><td>Paper #2</td><td>A question flowchart; inner nodes ask (rules), leaves conclude; depth counts layers from the root</td></tr>
      <tr><td class="kpid">kp-gbdt</td><td><a href="sites/feng-2026-knowledge-hgnn.html#kp-gbdt">Gradient boosted decision trees</a></td><td>Paper #2</td><td>A relay of small trees each patching the previous residual; here mined for rules, not predictions</td></tr>
      <tr><td class="kpid">kp-permutation-invariance</td><td><a href="sites/feng-2026-knowledge-hgnn.html#kp-permutation-invariance">Permutation invariance</a></td><td>Paper #2</td><td>Sum/max/average ignore order; hypergraph encoders must be column-exchange invariant</td></tr>
      <tr><td class="kpid">kp-over-smoothing</td><td><a href="sites/feng-2026-knowledge-hgnn.html#kp-over-smoothing">Over-smoothing &amp; over-squashing</a></td><td>Paper #2</td><td>Repeated neighbor averaging homogenizes features; 8-layer HGNN collapses 73.41 → 30.22</td></tr>
      <tr><td class="kpid">kp-transductive-inductive</td><td><a href="sites/feng-2026-knowledge-hgnn.html#kp-transductive-inductive">Transductive vs inductive</a></td><td>Paper #2</td><td>Faces seen with answers withheld vs brand-new points; production = both exam formats merged</td></tr>
'''
anchor = '<tr><td class="kpid">kp-opt-gradient</td>'
i = s.find(anchor)
j = s.find('\n', s.find('</tr>', i))
rep(s[i:j+1], s[i:j+1] + '\n' + kp_rows.rstrip('\n'), "kp-rows")

# 3) 进度 JS：按 slug 记总数
rep("  var slugs = ['perrault-2020-game-focused'];\n  var total = 54, i, raw, st, pct;",
    "  var totals = { 'perrault-2020-game-focused': 66, 'feng-2026-knowledge-hgnn': 52 };\n  var slugs = ['perrault-2020-game-focused', 'feng-2026-knowledge-hgnn'];\n  var i, raw, st, pct, total;",
    "js-totals")
rep("  for (i = 0; i < slugs.length; i++) {\n    try { raw = localStorage.getItem('pi-progress-' + slugs[i]); } catch (e) { raw = null; }",
    "  for (i = 0; i < slugs.length; i++) {\n    total = totals[slugs[i]];\n    try { raw = localStorage.getItem('pi-progress-' + slugs[i]); } catch (e) { raw = null; }",
    "js-loop")

open(p, "w", encoding="utf-8").write(s)
print("applied:", n)
