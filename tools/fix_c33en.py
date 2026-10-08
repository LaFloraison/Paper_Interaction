# -*- coding: utf-8 -*-
"""批8 c33 EN 侧同步"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = "sites/feng-2026-knowledge-hgnn.html"
s = open(p, encoding="utf-8").read()
done = []


def rep(o, n, tag):
    global s
    if o not in s:
        print("!! NOT FOUND:", tag); return
    s = s.replace(o, n, 1); done.append(tag)


rep('<p class="len">Two ledgers now sit on the desk: the <b>structural ledger</b> X<sub>s</sub> (one number per vertex — membership counts, card 25) and the <b>rule ledger</b> X<sub>r</sub> (five numbers per vertex — the content×position lists, card 32). They must bind into one feature set Z for the scoring machine.</p>',
    '<p class="len">Two ledgers now sit on the desk, both kept one page per “person” (a person is a vertex; the “groups” it joins — hyperedges embracing a crowd at once — were introduced at card 24): the <b>structural ledger</b> holds 1 number each (how many groups joined); the <b>rule ledger</b> holds 5 each (how five rules scored).</p>', "c33-open-en")

rep('<b><span class="hl">The binding recipe, two steps: (1) let the structural number multiply into every slot of the rule ledger (⊙, slot-wise), giving a "structure-weighted" copy X̃<sub>r</sub>; (2) staple the weighted copy and the original side by side (‖) into a 10-slot Z.</span></b>',
    '<b><span class="hl">The binding recipe, two steps: (1) multiply the structural score into every slot of the rule ledger, giving an “amplified or damped” copy; (2) staple the copy beside the original into one double-length feature.</span></b> (The two moves are written ⊙ and ‖ in the formula below.)', "c33-bold-en")

rep('The paper\'s own analogy: this resembles positional encoding in Transformers — extra information (the structural weight) is <b>injected into every slot</b> rather than bolted on the end.',
    'The paper\'s own analogy: this resembles a common trick elsewhere — a tag <b>seeps into every slot</b> rather than being bolted on at the end. (The trick\'s proper name is positional encoding; all you need here is “seeps into every slot”.)', "c33-transformer-en")

rep('structural X<sub>s</sub>(A) = σ(2) ≈ <b>0.8808</b> (he joins 2 groups — card 25\'s walkthrough);',
    'structural X<sub>s</sub> (vertex A): he joins 2 groups — card 25\'s way squeezes the count into 0–1 (the squeeze is called σ: 0 groups → 0.5, 2 groups → 0.88, larger counts nearer 1) — so X<sub>s</sub> = <b>0.8808</b>;', "c33-sigma-en")

rep('<b>Example 2 (a marginal vertex, damped):</b> suppose a vertex\'s structural ledger reads X<sub>s</sub> = 0.5 (isolated, no groups) and its rule ledger [1.125, 0, 0, 0, 0] →',
    '<b>Example 2 (another vertex — isolated, damped):</b> this is a different vertex with no groups; by σ\'s rule its structural score is exactly <b>0.5</b> (the midpoint, meaning “no information”); its rule ledger [1.125, 0, 0, 0, 0] (one unsettled entry) →', "c33-ex2-en")

open(p, "w", encoding="utf-8").write(s)
print("applied:", len(done))
for d in done:
    print(" -", d)
