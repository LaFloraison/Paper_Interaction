# -*- coding: utf-8 -*-
"""从论文 PDF 提取图表为高清 PNG（供站点 base64 内嵌）
用法: python tools/extract_figures.py
输出: decomposition/<slug>/figs/figN.png
区域为逐图人工核对的 clip 矩形（PDF 坐标, 单位 pt）
"""
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PDF = Path(__file__).parent.parent / "Paper" / "jrevak,+AAAI_PerraultA-5897.pdf"
OUT = Path(__file__).parent.parent / "decomposition" / "perrault-2020-game-focused" / "figs"

# (页码1基, clip(x0,y0,x1,y1), 输出名)
FIGS = [
    (3, (56, 46, 162, 130), "fig1a"),   # 盗猎套索照片
    (3, (166, 46, 294, 124), "fig1b"),  # w 的 MLE 收敛曲线
    (3, (306, 48, 506, 274), "fig2"),   # 两阶段 vs 博弈聚焦管线（矢量）
    (7, (52, 48, 554, 191), "fig3"),    # 合成实验 2x3 结果网格
    (7, (58, 232, 546, 306), "fig4"),   # 人类数据结果
    (8, (314, 48, 558, 150), "fig5"),   # 假设2散点（交叉熵 vs DEU差）
    (8, (314, 190, 558, 277), "fig6"),  # 假设3散点（贡献 vs 误差）
]

ZOOM = 3.0


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    for pno, clip, name in FIGS:
        page = doc[pno - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=fitz.Rect(*clip))
        fp = OUT / (name + ".png")
        pix.save(fp)
        print(name + ".png  " + str(pix.width) + "x" + str(pix.height) + "  " + str(fp.stat().st_size // 1024) + " KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
