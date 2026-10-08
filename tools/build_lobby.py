# -*- coding: utf-8 -*-
"""build_lobby.py —— 由 shared/papers.json + 知识点登记表 + 各站点卡片，生成 index.html

用法: python tools/build_lobby.py

产出: index.html（论文列表按拆解日期倒序 + 全站检索 + 通用说明 + 知识点目录）
检索索引内嵌在页面里，离线可搜（不依赖 fetch，file:// 直接打开也能用）。
"""
import html as H
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
PAPERS = ROOT / "shared" / "papers.json"
REGISTRY = ROOT / "shared" / "knowledge-registry.md"
TEMPLATE = ROOT / "templates" / "lobby.html"


def read_cards(site_path: Path):
    """从站点 HTML 里取出每张卡的编号与标题（兼容 v4 的 data-title-en 与 v5 的 data-title）。"""
    if not site_path.exists():
        return []
    s = site_path.read_text(encoding="utf-8", errors="ignore")
    out = []
    for m in re.finditer(r'<section class="card"([^>]*)>', s):
        attrs = m.group(1)
        cid = re.search(r'data-c="([^"]+)"', attrs)
        if not cid:
            continue
        title = re.search(r'data-title="([^"]+)"', attrs)
        if title:
            t = title.group(1)
        else:
            en = re.search(r'data-title-en="([^"]+)"', attrs)
            zh = re.search(r'data-title-zh="([^"]+)"', attrs)
            t = (en or zh).group(1) if (en or zh) else "Card " + cid.group(1)
        chap = re.search(r'data-chapter="([^"]+)"', attrs)
        out.append({
            "id": cid.group(1),
            "title": t,
            "chapter": chap.group(1) if chap else "",
        })
    return out


def parse_registry():
    """解析知识点登记表的 markdown 表格。"""
    if not REGISTRY.exists():
        return []
    rows = []
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| kp-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        kp, en, zh, paper, status, note = cells[:6]
        rows.append({"id": kp, "en": en, "zh": zh, "paper": paper,
                     "status": status, "note": note.replace("\\|", "|")})
    return rows



# ---------------------------------------------------------------- 全局知识地图
KMAP = ROOT / "shared" / "knowledge-map.json"

ECOL = {"prereq": "#1a6bff", "related": "#16a34a", "contrast": "#dc2626", "cross": "#7c3aed"}


def wrap(text, n):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        lines.append(cur)
    return lines[:3]


def build_knowledge_map(kps):
    """按 knowledge-map.json 的 cluster/order 做确定性布局，手写 SVG。"""
    if not KMAP.exists():
        return ""
    km = json.loads(KMAP.read_text(encoding="utf-8"))
    by_id = {k["id"]: k for k in kps}

    NW, NH, GAPX, GAPY, PAD = 176, 52, 22, 16, 16
    maxrows = max(len(c["nodes"]) for c in km["clusters"])
    width = PAD * 2 + len(km["clusters"]) * NW + (len(km["clusters"]) - 1) * GAPX
    height = 34 + maxrows * (NH + GAPY) + 34

    pos = {}
    for ci, cl in enumerate(km["clusters"]):
        for nd in cl["nodes"]:
            x = PAD + ci * (NW + GAPX)
            y = 34 + (nd["order"] - 1) * (NH + GAPY)
            pos[nd["id"]] = (x, y, cl["key"])

    out = ['<div class="kmap"><svg viewBox="0 0 %d %d" width="100%%" role="img" '
           'aria-label="Global knowledge map: knowledge points grouped by area, with prerequisite and related links">'
           % (width, height)]
    out.append('<defs>')
    for t, c in ECOL.items():
        out.append('<marker id="km-%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
                   'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker>' % (t, c))
    out.append('</defs>')

    for t, edges in (("cross", []), ("contrast", []), ("related", []), ("prereq", [])):
        pass
    # 先画边，再画节点，保证节点压住线
    for e in km["edges"]:
        a, b = pos.get(e["from"]), pos.get(e["to"])
        if not a or not b:
            continue
        x1, y1 = a[0] + NW / 2, a[1] + NH / 2
        x2, y2 = b[0] + NW / 2, b[1] + NH / 2
        col = ECOL.get(e["type"], "#9aa6b8")
        dash = ' stroke-dasharray="5 4"' if e["type"] in ("contrast", "cross") else ""
        out.append('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s" stroke-width="1.6" '
                   'opacity="0.55"%s marker-end="url(#km-%s)"/>' % (x1, y1, x2, y2, col, dash, e["type"]))

    for ci, cl in enumerate(km["clusters"]):
        x0 = PAD + ci * (NW + GAPX)
        out.append('<text x="%.0f" y="20" font-size="12" font-weight="700" fill="#7a8699" letter-spacing="1">%s</text>'
                   % (x0, H.escape(cl["name"].upper())))

    for nd in [n for c in km["clusters"] for n in c["nodes"]]:
        k = by_id.get(nd["id"])
        x, y, ck = pos[nd["id"]]
        if not k:
            fill, stroke, txtc, label, url = "#f2f4f8", "#d7dce4", "#9aa6b8", nd["id"], None
        else:
            fill, stroke, txtc = "#eef4ff", "#1a6bff", "#24313f"
            label = k["en"]
            pap = next((pp for pp in PAPERS_LIST if pp["slug"] == k["paper"]), None)
            url = ("%s#%s" % (pap["site"], k["id"])) if pap else None
        g_open = '<a href="%s">' % H.escape(url) if url else '<g>'
        g_close = "</a>" if url else "</g>"
        out.append(g_open)
        out.append('<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="10" fill="%s" stroke="%s"/>'
                   % (x, y, NW, NH, fill, stroke))
        lines = wrap(label, 24)
        ty = y + (NH - (len(lines) - 1) * 13) / 2 + 1
        for i, ln in enumerate(lines):
            out.append('<text x="%.0f" y="%.0f" font-size="11.5" fill="%s" text-anchor="middle">%s</text>'
                       % (x + NW / 2, ty + i * 13, txtc, H.escape(ln)))
        out.append(g_close)

    out.append("</svg></div>")

    leg = "".join('<span class="kmleg"><i style="background:%s"></i>%s</span>'
                  % (ECOL.get(l["type"], "#9aa6b8"), H.escape(l["label"])) for l in km.get("legend", []))
    return "".join(out) + '<div class="kmlegend">' + leg + "</div>"


def main():
    global PAPERS_LIST
    papers = json.loads(PAPERS.read_text(encoding="utf-8"))
    PAPERS_LIST = papers
    kps = parse_registry()
    kp_by_paper = {}
    for k in kps:
        kp_by_paper.setdefault(k["paper"], []).append(k)

    index = []          # 检索索引
    total_cards = 0

    # ---------- 论文卡 ----------
    cards_html = []
    for p in sorted(papers, key=lambda x: x["decomposed"], reverse=True):
        site = ROOT / p["site"]
        cards = read_cards(site)
        total_cards += len(cards)
        n_kp = len(kp_by_paper.get(p["slug"], []))

        index.append({
            "kind": "paper", "title": p["title"], "url": p["site"],
            "sub": "%s · %s · decomposed %s" % (p.get("short", ""), p.get("venue", ""), p["decomposed"]),
            "kw": " ".join(p.get("keywords", []) + [p.get("short", ""), p.get("authors", ""), p.get("affil", ""), p["decomposed"]]),
        })
        for c in cards:
            index.append({
                "kind": "card", "title": "%s · %s" % (p.get("short") or p["slug"], c["title"]),
                "url": "%s#c-%s" % (p["site"], c["id"]),
                "sub": "%s · card %s%s" % (p.get("short") or p["slug"], c["id"],
                                           " · " + c["chapter"] if c["chapter"] else ""),
                "kw": c["chapter"],
            })

        cards_html.append(
            '<a class="papercard" href="%s">'
            '<div class="pc-top"><div>'
            '<div class="pc-title">%s</div>'
            '<div class="pc-auth">%s</div>'
            '<div class="pc-auth" style="color:#9aa6b8">%s</div>'
            '</div><div class="pc-date">decomposed %s</div></div>'
            '<div class="pc-line">%s</div>'
            '<div class="pc-meta"><span>%d cards</span>%s</div>'
            '<div class="pc-prog"><div class="pc-bar"><div class="pc-fill" id="fill-%s"></div></div>'
            '<span class="pc-txt" id="txt-%s">not started · %d cards</span></div>'
            '</a>'
            % (H.escape(p["site"]), H.escape(p["title"]), H.escape(p.get("authors", "")),
               H.escape(p.get("venue", "")), H.escape(p["decomposed"]),
               H.escape(p.get("oneline", "")), len(cards),
               ('<span class="k">%d knowledge points</span>' % n_kp) if n_kp else "",
               H.escape(p["slug"]), H.escape(p["slug"]), len(cards))
        )

    # ---------- 知识点 ----------
    for k in kps:
        pap = next((p for p in papers if p["slug"] == k["paper"]), None)
        index.append({
            "kind": "kp", "title": k["en"] + " · " + k["zh"],
            "url": "%s#%s" % (pap["site"] if pap else "#", k["id"]),
            "sub": "%s · %s · %s" % (k["id"], (pap.get("short") if pap else k["paper"]), k["note"]),
            "kw": k["id"] + " " + k["zh"] + " " + (pap.get("short", "") if pap else ""),
        })

    kp_rows = []
    for k in kps:
        pap = next((p for p in papers if p["slug"] == k["paper"]), None)
        url = "%s#%s" % (pap["site"], k["id"]) if pap else "#"
        kp_rows.append(
            '<tr><td class="kpid">%s</td><td><a href="%s">%s</a></td>'
            '<td style="white-space:nowrap;color:#7a8699;font-size:13.5px">%s</td><td>%s</td></tr>'
            % (H.escape(k["id"]), H.escape(url), H.escape(k["en"]),
               H.escape(pap.get("short") if pap else k["paper"]), H.escape(k["note"]))
        )
    kp_tab = ('<table class="kptab"><thead><tr><th>id</th><th>knowledge point</th>'
              '<th>first taught in</th><th>in one line</th></tr></thead><tbody>'
              + "".join(kp_rows) + "</tbody></table>")

    # ---------- 统计 ----------
    stats = ("".join([
        '<div class="stat"><b>%d</b><span>papers</span></div>' % len(papers),
        '<div class="stat"><b>%d</b><span>cards</span></div>' % total_cards,
        '<div class="stat"><b>%d</b><span>knowledge points</span></div>' % len(kps),
    ]))

    # ---------- 通用说明（从每篇站点里挪出来，只在大厅讲一次） ----------
    howto = HOWTO

    tpl = TEMPLATE.read_text(encoding="utf-8")
    out = (tpl
           .replace("{{STATS}}", stats)
           .replace("{{PAPERS}}", "\n".join(cards_html))
           .replace("{{HOWTO}}", howto)
           .replace("{{KNOWLEDGEMAP}}", build_knowledge_map(kps))
           .replace("{{KPCOUNT}}", str(len(kps)))
           .replace("{{KPTAB}}", kp_tab)
           .replace("{{SEARCH_INDEX}}", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
           .replace("{{PAPER_PROGRESS}}",
                    json.dumps([{"slug": p["slug"], "total": p["cards"]} for p in papers],
                               ensure_ascii=False)))
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print("index.html 已生成 | 论文 %d | 卡片索引 %d | 知识点 %d | %d KB"
          % (len(papers), total_cards, len(kps), len(out.encode('utf-8')) // 1024))
    return 0


HOWTO = """
<h4>What these sites are</h4>
<p>Each paper is taken apart until it is actually understood — not summarised. The reader is assumed to be a
mathematically mature student who has <em>not</em> read the paper and may not know its subject at all. Every claim,
figure, table and equation in the original has a card; wherever the paper is unclear, the card is not; and wherever
background is missing, a section supplies it from zero.</p>

<h4>Every teaching card runs in the same three phases</h4>
<ul>
<li><span class="phase ph-what">WHAT</span> opens with a <strong>definition box</strong> — a formal definition with every
term glossed, then one sentence in plain words — followed by the motivation, the intuition built up in blocks, and
finally the formula if there is one.</li>
<li><span class="phase ph-ex">EXAMPLE</span> works two or more instances from small to large, showing the arithmetic
rather than only the answer.</li>
<li><span class="phase ph-quiz">EXERCISES</span> tests at three levels — understand, apply, transfer. Every wrong
option carries an explanation of the mistake it represents, because the mistake is the useful part.</li>
</ul>

<h4>Where things are</h4>
<ul>
<li><strong>Chapters follow the paper:</strong> Title, Pre-knowledge, Abstract, Introduction, Method, Experiments,
Conclusion. Figures, tables and equations are taught in whichever chapter they belong to, so the PDF can stay open
alongside and the two stay in step.</li>
<li><strong>Extension sections</strong> (<code>Extension: …</code>) build the background the paper assumes — graph
theory, decision trees, gradient boosting, evaluation protocols and more. They are written once and reused across
papers, and each ends with a skip quiz so you can jump past what you already know.</li>
<li><strong>Practice cards</strong> are a big topic's exercises moved onto their own card, so the teaching card stays
readable.</li>
<li><strong>Reference appendices</strong> explain why each cited work is cited: a one-line table for the whole
bibliography, full cards for the handful of references the paper actually leans on, and a lineage diagram.</li>
</ul>

<h4>Reading one</h4>
<ul>
<li>Progress saves automatically in this browser, per paper. <strong>← →</strong> or A/D move between cards, and the
top-right corner always shows the chapter and section you are in.</li>
<li><strong>☰ opens the outline</strong>, which runs chapter → section → card. Chapters and sections fold away, and the
numbering restarts inside each chapter (1.1, 1.2 … 6.1, 6.2 …) rather than counting straight through the whole site.
Each card in the outline carries the page of the paper it was built from.</li>
<li><strong>＋ Add card</strong> on any card inserts your own note card after it. It is stored in this browser, never
uploaded, and can be deleted again from the card itself.</li>
<li><strong>▥ Paper</strong> splits the screen: your card on the left, one paragraph of the paper on the right — set in
the paper's own serif on white, with the passage that card was built from highlighted, and a screenshot of that
spot in the PDF underneath — keywords highlighted — whenever the card is about a table or figure. Clicking a paragraph jumps back to the card that reads it; <code>◀ ▶</code> reads
the paper a paragraph at a time. Press <code>P</code> to toggle it.</li>
<li>Arrow keys, <code>P</code> and <code>/</code> work on the keyboard; <code>/</code> here focuses the search box.</li>
</ul>
"""

if __name__ == "__main__":
    sys.exit(main())
