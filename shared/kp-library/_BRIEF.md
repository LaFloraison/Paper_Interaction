# 拓展库写作规范（子代理必读）

你要为一个「论文 → 交互式学习网站」项目写**一个**可复用拓展小节。产物是 JSON 卡片文件，由 Python 编译器编译成英文单语交互页面。

## 1 先读范本（强制）

- `shared/kp-library/graph-theory/section.json`
- `shared/kp-library/graph-theory/c1.json`（教学卡：定义盒 → 动机 → 直觉 → 公式 → 例子 → 习题）
- `shared/kp-library/graph-theory/c5.json`（公式密集型教学卡）
- `shared/kp-library/graph-theory/c6.json`（`kind:"check"` 的跳过测验卡）
- `shared/card-quality-rubric.md`（质量门槛）

范本的**深度、语气、单卡长度（渲染后约 900–1400 词）就是标准**。不要压缩。

## 2 产物文件

```
shared/kp-library/<key>/section.json
shared/kp-library/<key>/c1.json ... cN.json
```

`section.json`：
```json
{ "key": "...", "name": "...", "title": "...",
  "blurb": "2–3 句：本节讲什么、为什么对这篇论文重要",
  "skip_hint": "一句话：会做什么就可以跳过本节" }
```

## 3 卡片 JSON 结构

```json
{ "kind": "extension",
  "title": "...",
  "what":    [ <blocks> ],
  "example": [ <blocks> ],
  "quiz":    [ <quiz items> ],
  "close":   "**Where this is going:** ..." }
```

最后一卡用 `"kind": "check"`（跳过测验），结构相同：`what` = 本节回顾清单 + 门槛说明，`example` 可有，`quiz` ≥3 道。

### 允许的内容块

- `{"t":"definition","formal":"...","plain":"..."}` — **必须是 `what` 的第一个块**。`formal` 是严谨定义、每个术语就地括注；`plain` 是一句人话。
- `{"t":"p","md":"..."}`
- `{"t":"list","items":["..."],"ordered":true|false}`
- `{"t":"table","head":["..."],"rows":[["..."],["..."]]}`
- `{"t":"formula","tex":"...","note":"...","gloss":[{"sym":"...","md":"..."}]}`
- `{"t":"steps","items":[{"md":"...","why":"..."}]}` — 步进器，`why` 解释这一步为何成立
- `{"t":"callout","md":"...","tone":"warn"|"good"}` — 警示框 / 要点框
- `{"t":"calc","md":"..."}` — 算术行（等宽字体）
- `{"t":"h3","md":"..."}`

### 习题

- `{"t":"choice","level":"understand|apply|transfer","q":"...","opts":[{"md":"...","expl":"..."},{"md":"...","correct":true,"expl":"..."}]}`
  恰一个 `correct`，≥3 个选项，**每个**选项都要有 `expl`，且要说中「选它的人是怎么想的」。
- `{"t":"num","level":"...","q":"...","answer":数,"tol":数,"hint":"...","sol":"...","unit":"..."}`
  `hint` 不得泄露答案或中间值；`sol` 写完整算式。
- `{"t":"multi","level":"...","q":"...","opts":[...]}` — 至少一个正确项。

## 4 硬规则（构建脚本会强制，违反即构建失败）

1. 每张卡：`what`（首块是 `definition`）、`example`（≥1 块）、`quiz`（≥3 道）。
2. 每张卡的习题必须同时覆盖三个层次：`understand`、`apply`、`transfer`。
3. 单选题恰一个正确项、≥3 选项、每选项有 `expl`。
4. 数值题必须有 `answer`/`tol`/`hint`/`sol`。
5. **每个数字都必须先用 Python 算过再写。** 无法推导的数字不许出现——不许编造统计量、基准分数、日期或历史断言。可核实的归属（如某个模型是谁提出的）可以有，但不确定就别写。
6. `**粗体**` 与 `*斜体*` 必须成对；绝不出现落单的 `*`。
7. 行内公式写 `$...$`；展示公式写在 `formula` 块的 `tex` 里（不带 `$`），反斜杠在 JSON 里写 `\\`。
8. **`quiz` 的 `expl`/`hint`/`sol` 走属性通道，没有 TeX 渲染**——属性里的 LaTeX 会被降级成 Unicode，但最好直接在属性文本里写 Unicode（`≥`、`×`、`σ`、`√`、`x₁`），不要写 `$...$`。
9. 语气：严谨、直接、不吹。禁用 "simply"、"obviously"、"just"。每个失效情形都要具体。
10. 定义优先：**未定义的术语不许出现**。每张卡的「是什么」段要能回答四问：为什么需要它 / 它是什么 / 它怎么运作 / **它何时失效**（第四问最常被漏，漏了算不合格）。

## 5 交付报告

写完后回复：文件清单、卡片数、以及**你用过的每个数字连同产生它的 Python 检查**。不要写别的。
