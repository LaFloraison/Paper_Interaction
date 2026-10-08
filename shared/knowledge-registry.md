# 全项目知识点登记表 (Knowledge Registry)

> 规则：新论文遇到已登记知识点 → 默认链接复用不重讲；确需重讲必须在卡内写明理由。
> 双卡制（2026-10-01 起）：每个知识点两卡——a 一般理论（论文之外的定义/例子/习题）+ b 在本文中（论文如何实例化，持 data-kp 锚点）。登记表锚点一律指向 b 卡。
> 锚点格式：`sites/{slug}.html#kp-{id}`（站点加载时自动跳转到对应卡）。
> 状态：● 已讲（完整一卡）｜↻ 重讲（新版或有新视角，卡内说明理由）｜＋ 深化（更高阶版本）

| id | 知识点 (EN) | 知识点 (中) | 首讲论文 | 状态 | 备注 |
|----|-------------|------------|---------|------|------|
| kp-expected-utility | Expected utility | 期望效用 | perrault-2020-game-focused | ● | 概率加权收益；(1−p)·q·\|u_d\| 三因子结构 |
| kp-mixed-strategy | Mixed strategy & coverage probability | 混合策略与覆盖概率 | perrault-2020-game-focused | ● | 长期频率视角；Σp≤资源预算 |
| kp-stackelberg-game | Stackelberg game & commitment | Stackelberg 博弈与承诺 | perrault-2020-game-focused | ● | 先手承诺的价值；leader-follower |
| kp-softmax-qr | Softmax / Quantal Response | Softmax 与量化响应 | perrault-2020-game-focused | ● | λ 旋钮：随机性↔理性；有限理性=信息源 |
| kp-suqr | SUQR (Subjective Utility QR) | 主观效用量化响应 | perrault-2020-game-focused | ● | exp(w·p_i+φ(y_i))；可分解性是反演前提 |
| kp-loss-function | Loss function | 损失函数 | perrault-2020-game-focused | ● | "错得有多离谱"的量化 |
| kp-cross-entropy | Cross-entropy | 交叉熵 | perrault-2020-game-focused | ● | 分布匹配损失；与 KL 的关系 |
| kp-gradient-descent | Gradient descent | 梯度下降 | perrault-2020-game-focused | ● | 下坡一步；学习率；局部极小 |
| kp-mle | Maximum likelihood estimation | 最大似然估计 | perrault-2020-game-focused | ● | 让观测最可能的参数；硬币例子 |
| kp-decision-focused-learning | Decision-focused learning / end-to-end predict-then-optimize | 决策聚焦学习 | perrault-2020-game-focused | ● | 损失=下游决策质量；Bengio97→Donti17→Wilder19→本文 |
| kp-counterfactual-estimation | Counterfactual estimation (strategic setting) | 反事实估计 | perrault-2020-game-focused | ● | 只见对历史覆盖的回应；分解性反演 φ̂ |
| kp-opt-gradient | Differentiating through optimization (local QP) | 穿优化器求导（局部 QP） | perrault-2020-game-focused | ● | 定理4；严格局部最优+泰勒碗+OptNet 导数 |
| kp-deu | Defender expected utility (DEU) | 防守方期望效用 | perrault-2020-game-focused | ● | Σ(1−p_i)q_i u_d(i)；攻击转移效应 |
| kp-hypergraph | Hypergraph & incidence matrix | 超图与关联矩阵 | feng-2026-knowledge-hgnn | ● | 超边一次圈一群点；H 行=顶点、列=超边；行和=顶点度 |
| kp-decision-tree | Decision tree | 决策树 | feng-2026-knowledge-hgnn | ● | 提问流程图；内部节点=规则、叶子=结论；深度自根数起 |
| kp-gbdt | Gradient boosted decision trees | 梯度提升决策树 | feng-2026-knowledge-hgnn | ● | 接力纠错树队；本文当"规则矿"用（只取提问点） |
| kp-permutation-invariance | Permutation invariance | 置换不变性 | feng-2026-knowledge-hgnn | ● | 求和/最大/平均不看顺序；结构编码器须列交换不变 |
| kp-over-smoothing | Over-smoothing & over-squashing | 过平滑与特征压缩 | feng-2026-knowledge-hgnn | ● | 反复邻居平均→特征趋同；8 层 HGNN 73.41→30.22 |
| kp-transductive-inductive | Transductive vs inductive | 直推与归纳设定 | feng-2026-knowledge-hgnn | ● | 见过人缺答案 vs 全新点；production=两者合并 |

## 登记协议

1. 拆解新论文时先读本表；蓝图里为每个预备/正文知识点标注：`复用#kp-xxx` / `新增 kp-xxx` / `重讲 kp-xxx（理由）`
2. 新增知识点在站点内卡片打 `data-kp="kp-xxx"`，登记表加行
3. 复用知识点时，卡内放"快速回顾框"（3 句话内）+ 正式链接，不展开完整教学
4. 每篇论文完成后更新本表与 `index.html` 知识点目录页
