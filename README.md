# Paper_Interaction

把一篇论文拆解成一个交互式学习网站。一次一篇，拆到**真正读懂**为止——不是摘要。

在线阅读：**https://lafloraison.github.io/reader/paper-interaction/**

## 这个项目在做什么

> 原文有的，卡片里都有；原文没讲清楚的，卡片里讲清楚；读者缺的知识、素养与经验，补足并训练。
> 卡片只是一种形式，目的是减少读者长篇学习的认知负担。

四条判据：

1. **全量覆盖** — 论文里每一个论断、每一张图表、每一个公式都有对应卡片，没有"略过"。
2. **澄清** — 论文没讲清的（设计动机、符号来源、失效边界、数字对不对）卡片必须讲清；论文的沉默本身也是题目。
3. **补足与训练** — 缺失的前置知识与领域框架，由**拓展小节**从零补齐；补完必须练（习题），不是读过就算。
4. **卡片是形式，不是目的** — 切卡边界画在"读者的注意力单元"处，不画在长度处。不设卡片数上限。

读者设定：**数学成熟、要求严谨，但没读过这篇论文、可能也没学过这个话题**。

## 站点长什么样

每张教学卡一律 **是什么 → 例子 → 习题** 三段：

- **是什么** — 定义盒（正式定义 + 白话重述）→ 动机 → 直觉积木 → 公式
- **例子** — ≥2 个由小到大的实例，全部数字先用 Python 算过再写
- **习题** — 覆盖理解 / 应用 / 迁移三层；选择题每个错误选项都指出"选它的人错在哪"；数值题带答案/容差/提示/解答

七章跟随论文本身：Title · Pre-knowledge · Abstract · Introduction · Method · Experiments · Conclusion，另附 Wrap-up 与引用附录。**图表公式在其所属章节就地讲解**，可以对着 PDF 同步读。

**拓展小节**是项目的复利资产：通用性强的话题（线性代数、图论、决策树家族、GNN 谱系、评测协议、科研素养……）写在 `shared/kp-library/`，**一篇论文写一次、后续论文直接编译复用**。每个小节自带跳过测验。

## 结构

```
CLAUDE.md         项目宪法（教学法铁律 + 技术铁律 + 工作流）
index.html        大厅：论文列表（按拆解日期）+ 全站检索 + 通用说明 + 知识点目录
sites/            成品：每篇论文一个自包含交互站（双击离线可开，零外部请求）
content/{slug}/   论文的卡片数据（JSON）——站点是这些数据的编译产物
shared/           core.js 交互引擎 · 知识点登记表 · 审卡 rubric · 拓展库 kp-library/
templates/        外壳模板（站点 + 大厅）
tools/            build_site.py 渲染器 · build_lobby.py 大厅 · validate.py 校验 · deploy_pages.py 发布
decomposition/    拆解蓝图与审卡记录留档
AI-tutoring/      教学法来源：Kestin et al. 2025 哈佛 AI 家教 RCT + 完整提示词
```

站点是**构建产物**，不手工编辑：改 `content/{slug}/cards/c*.json`，跑 `python tools/build_site.py {slug}`。

## 常用命令

```bash
python tools/build_site.py   feng-2026-knowledge-hgnn   # 由卡片数据编译站点
python tools/validate.py     feng-2026-knowledge-hgnn   # 数据层 + 渲染层双重校验
python tools/build_lobby.py                             # 重新生成大厅与检索索引
python tools/deploy_pages.py                            # 镜像到 GitHub Pages 用户站（不自动推送）
python tools/new_paper.py    {slug} "论文标题"           # 铺好一篇新论文的骨架
```

## 技术约束

零外部 CDN（公式用内嵌 KaTeX 本地渲染）· 单 HTML 自包含 · 无 IIFE · 产物业务区 0 反引号 · 每篇站点离线可开。

## 已经拆过的论文

| 论文 | 拆解日期 | 卡片 |
|---|---|---|
| Knowledge-Embedded Hypergraph Neural Networks (TPAMI 2026) | 2026-10-08 | 140 |
| End-to-End Game-Focused Learning of Adversary Behavior in Security Games (AAAI-20) | 2026-09-30 | 66 |

## 教学法

基于 Kestin et al. 2025（Scientific Reports）验证有效的教学实践：认知负荷管理、一次一步、主动学习、脚手架、准确性、针对性反馈、自定步调。视觉风格参考 brilliant.org：浅色、一屏一概念、explain → interact → check。
