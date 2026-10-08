# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = "decomposition/feng-2026-knowledge-hgnn/cards/c30.html"
s = open(p, encoding="utf-8").read()

o1 = 'data-answer="0.75" data-tol="0.01" data-hint="把层号代进 μp 的除法：α 在分子、d+β 在分母。题目给的旋钮是 α=6、β=6。" data-sol="μ<sub>p</sub>(2) = 6 ÷ (2 + 6) = 6 ÷ 8 = 0.75。注意：这是 Amazon-P 的旋钮组合（例 2），与例 1 的 CC-Cora 组合不同。"'
n1 = 'data-answer="0.6667" data-tol="0.005" data-hint="把层号代进 μp 的除法：α 在分子、d+β 在分母。题目给的旋钮是 α=6、β=6。" data-sol="μ<sub>p</sub>(3) = 6 ÷ (3 + 6) = 6 ÷ 9 ≈ 0.6667。同一组旋钮下，层号越大分量越小——0 层 1.0、3 层约 0.67，缓降形状一目了然。"'
assert o1 in s
s = s.replace(o1, n1, 1)

o2 = '<span class="lz">数值题：某数据集的 α = 6、β = 6。第 2 层的规则分量是多少？</span>'
n2 = '<span class="lz">数值题：某数据集的 α = 6、β = 6。第 3 层的规则分量是多少（保留四位小数）？</span>'
assert o2 in s
s = s.replace(o2, n2, 1)

o3 = '<span class="len">Numeric: a dataset uses α = 6, β = 6. What is the weight of a layer-2 rule?</span>'
n3 = '<span class="len">Numeric: a dataset uses α = 6, β = 6. What is the weight of a layer-3 rule (four decimals)?</span>'
assert o3 in s
s = s.replace(o3, n3, 1)

open(p, "w", encoding="utf-8").write(s)
print("c30 quiz fixed; 6/9 =", round(6 / 9, 4))
