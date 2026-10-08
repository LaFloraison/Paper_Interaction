# -*- coding: utf-8 -*-
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

b = "decomposition/feng-2026-knowledge-hgnn/blueprint.md"
t = open(b, encoding="utf-8").read()

r = [
    ("| c48 | 批判 1/2 (plain) | 数字-文本 8 处不一致（全部已验证）+ 与 BGNN 的界线（自 c36 移入）+ 论文自认边界 | —",
     "| c48 | 批判 1/2 (plain) | 十笔实据账（全部已验证）+ 与 BGNN 的界线（附注形式） | 批12/R1 FAIL(缩写裸奔/一卡两主题/B5 不自足/C3 矛盾)→修→待复审"),
    ("| c49 | 批判 2/2 (plain) | 读者追问：GBDT 任务从哪来/新顶点规则失效?/可扩展性/μc 0/1 粒度 | —",
     "| c49 | 批判 2/2 (plain) | 六个追问（预训练标签边界/μc 粒度/开销/k 敏感性/维度/ Github 反常） | 批12/R2 FAIL(术语裸奔/外引/缺后果)→修→R2b PASS（再补 HGNN·直推行 nit）"),
    ("| c50 | 后测 (k-check) | 7 题终章 | —",
     "| c50 | 后测 (k-check) | 7 题终章（3 理解 / 2 应用 / 2 迁移） | 批12/R3 FAIL(Q7 干扰项解析反向肯定/**残留)→修→R3b PASS"),
    ("| c51 | 总结 (plain) | 知识地图 + 登记表跳转 + 下篇预告 | —",
     "| c51 | 总结 (plain) | 知识地图 + 数字索引 + 六知识点登记 + 下篇预告 | 抽检通过（无审查门要求）"),
]
for o, n in r:
    if o in t:
        t = t.replace(o, n, 1)
        print("ok:", o[:12])
    else:
        print("MISS:", o[:34])

lesson = u"""
## 10. 收尾事故与教训（批 12）
- **卡片乱序 bug**：卡片源文件（cards/cN.html）末尾各带 `<!-- NEXT-CARD -->` 标记，拼接脚本把后续批次插到了**第一个**嵌入标记处，导致 39/40/42-44/46-49 段落错位（页码与内容不符）。发现方式：headless 截图核对页码（#c-41 落到 40/52 而非 42/52）。修复：按 data-c 重排全部 section（脚本见 tools/，一次性排序 + 清除 12 个残留标记）。**教训：拼接脚本应对"目标文档末尾的最后一块"用 rfind，或在源文件里不带标记。**
- 收尾清单：embed_figs（13 图）→ embed_katex（11 个 data-tex）→ validate 全绿 0 警告 → headless PI-OK + 4 张截图（封面/表 V/实验室/大厅）人工核对 → index.html（Paper #2 卡 + 6 知识点行 + 按 slug 的进度总数）→ shared/knowledge-registry.md（+6 行，共 19）。
"""
if u"## 10. 收尾事故与教训" not in t:
    t = t.rstrip() + u"\n" + lesson
open(b, "w", encoding="utf-8").write(t)
print("blueprint updated")
