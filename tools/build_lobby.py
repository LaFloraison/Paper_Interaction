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


def main():
    papers = json.loads(PAPERS.read_text(encoding="utf-8"))
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
            '<tr><td class="kpid">%s</td><td><a href="%s">%s</a><div style="color:#7a8699;font-size:13px">%s</div></td>'
            '<td style="white-space:nowrap;color:#7a8699;font-size:13.5px">%s</td><td>%s</td></tr>'
            % (H.escape(k["id"]), H.escape(url), H.escape(k["en"]), H.escape(k["zh"]),
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
<li>Progress saves automatically in this browser, per paper. <strong>☰</strong> opens the outline; the top-right
corner always shows the chapter and section you are in; <strong>← →</strong> or A/D move between cards.</li>
<li>The <strong>✚</strong> button on any card inserts your own note card after it.</li>
<li>Arrow keys and <code>/</code> work on the keyboard; <code>/</code> here focuses the search box.</li>
</ul>
"""

if __name__ == "__main__":
    sys.exit(main())
