# -*- coding: utf-8 -*-
"""new_paper.py —— 铺好一篇新论文的内容骨架（v5）

用法:
    python tools/new_paper.py <slug> "Paper Title" ["Author et al. · VENUE 2026"]

产出:
    content/<slug>/meta.json      七章骨架（title/pre/abstract/intro/method/experiments/conclusion + wrap/references）
    content/<slug>/cards/         空
    content/<slug>/figures/       空
    content/<slug>/widgets.js     实验台代码槽（可选）

之后：精读 → 图表提取 → 蓝图 → 讲解稿 topics/ → 写 cards/cNN.json → build_site.py
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent

CHAPTERS = [
    {"key": "title", "num": "1", "name": "Title"},
    {"key": "pre", "num": "2", "name": "Pre-knowledge"},
    {"key": "abstract", "num": "3", "name": "Abstract"},
    {"key": "intro", "num": "4", "name": "Introduction"},
    {"key": "method", "num": "5", "name": "Method"},
    {"key": "experiments", "num": "6", "name": "Experiments"},
    {"key": "conclusion", "num": "7", "name": "Conclusion"},
    {"key": "wrap", "num": "—", "name": "Wrap-up"},
    {"key": "references", "num": "—", "name": "References"},
]

WIDGETS = """/* ============ 站点专用 widget（实验台） ============
 * 这里只写实验台的交互逻辑。构建器会自动接上 initCore / 习题引擎 /
 * renderAllTex，并调用下面的 initLabs()。铁律：0 反引号 / 无 IIFE /
 * addEventListener / 用 piGet(id) 取元素。
 * ================================================= */

function initLabs() {
  /* 例：
  piGet('lab1run').addEventListener('click', function () { ... });
  */
}
"""


def main():
    if len(sys.argv) < 3:
        print('用法: python tools/new_paper.py <slug> "Paper Title" ["Author et al. · VENUE 2026"]')
        return 2
    slug = sys.argv[1]
    title = sys.argv[2]
    sub = sys.argv[3] if len(sys.argv) > 3 else ""

    cdir = ROOT / "content" / slug
    if cdir.exists():
        print("已存在，未覆盖: " + str(cdir))
        return 2
    (cdir / "cards").mkdir(parents=True)
    (cdir / "figures").mkdir()

    meta = {
        "slug": slug,
        "title": title,
        "head_title": title,
        "subtitle": sub,
        "authors": "",
        "venue": sub,
        "year": None,
        "chapters": CHAPTERS,
        "kps": [],
    }
    (cdir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                    encoding="utf-8")
    (cdir / "widgets.js").write_text(WIDGETS, encoding="utf-8")

    ddir = ROOT / "decomposition" / slug
    (ddir / "figs").mkdir(parents=True, exist_ok=True)
    (ddir / "topics").mkdir(exist_ok=True)

    print("已铺好 content/" + slug + "/（meta.json + cards/ + figures/ + widgets.js）")
    print("已铺好 decomposition/" + slug + "/（figs/ + topics/）")
    print()
    print("下一步：")
    print("  1. PyMuPDF 分页精读      -> decomposition/" + slug + "/paper_text.txt")
    print("  2. 提图 clips.json       -> decomposition/" + slug + "/figs/*.png")
    print("  3. 蓝图 blueprint.md     -> 章→节→卡 + 已验证数值 + 覆盖账")
    print("  4. 讲解稿 topics/*.md    -> 先讲清楚（不限长）")
    print("  5. 拆卡 cards/cNN.json   -> 再拆卡")
    print("  6. python tools/build_site.py " + slug)
    print("  7. python tools/validate.py " + slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
