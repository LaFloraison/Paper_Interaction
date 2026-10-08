# -*- coding: utf-8 -*-
"""build_site.py —— 把 content/{slug}/ 的卡片数据编译成 sites/{slug}.html

用法:
    python tools/build_site.py <slug>            # 编译
    python tools/build_site.py <slug> --no-katex # 跳过 KaTeX 内嵌（调试用）

流程: cards/*.json + meta.json + templates/ + shared/core.js
      -> 渲染 -> 内嵌图片 base64 -> 写 sites/<slug>.html -> 内嵌 KaTeX

设计目标（v5 规范 §6）: 属性引号破损 / 拼接乱序 / 三段式缺段 / 习题四件套缺失 /
业务区反引号 / 占位符残留 —— 全部在结构上不可能发生。
"""
import base64
import html as H
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent

KIND_CLASS = {
    "title": "k-title", "kp-a": "k-pre", "kp-b": "k-pre", "formula": "k-math",
    "figure": "k-fig", "table": "k-fig", "lab": "k-lab",
    "extension": "k-ext", "ext-overview": "k-extsec", "reference": "k-ref",
    "abstract": "k-abs", "intro": "k-intro", "method": "k-math",
    "experiment": "k-fig", "conclusion": "k-conc", "critique": "k-conc",
    "wrap": "k-wrap", "narrative": "k-story", "check": "k-check",
    "practice": "k-prac", "proof": "k-math",
}
# 无三段式的卡片类别
NO_PHASE = {"narrative", "critique", "wrap", "summary", "cover"}
# 习题卡：what + quiz 必需，example 可选（放一道完全讲解的样板题）
TWO_PHASE = {"practice", "check"}
LEVELS = ("understand", "apply", "transfer")


def card_key(p):
    """c37.json -> (37, ''); c37p.json -> (37, 'p')。顺序即文档顺序。"""
    m = re.match(r"c(\d+)([a-z]*)$", p.stem)
    if not m:
        raise SystemExit("[build] 卡片文件名须形如 c37.json / c37p.json，现为 " + p.name)
    return (int(m.group(1)), m.group(2))


# ---------------------------------------------------------------- 拓展库
# 通用性强的拓展小节写在 shared/kp-library/<key>/ 里，写一次、各站编译复用。
# 论文卡的序列里放一个 include 占位：
#   { "id": "10", "kind": "include", "library": "graph-theory",
#     "chapter": "pre", "section": "2.1 Foundations" }
# 构建时把该小节的卡片就地展开成 10a, 10b, ...（承接占位的章与节）。

LIBDIR = ROOT / "shared" / "kp-library"


def load_library(key):
    d = LIBDIR / key
    if not d.exists():
        raise SystemExit("[build] 拓展库小节不存在: shared/kp-library/" + str(key))
    secp = d / "section.json"
    if not secp.exists():
        raise SystemExit("[build] 拓展库小节缺 section.json: " + str(d))
    sec = json.loads(secp.read_text(encoding="utf-8"))
    files = sorted(d.glob("c*.json"), key=lambda p: int(re.sub(r"\D", "", p.stem)))
    if not files:
        raise SystemExit("[build] 拓展库小节无卡片: " + str(d))
    return sec, files


def expand_include(placeholder, stem_id):
    sec, files = load_library(placeholder.get("library"))
    n = len(files)
    out = []
    for i, lf in enumerate(files):
        c = json.loads(lf.read_text(encoding="utf-8"))
        c["id"] = stem_id + chr(ord("a") + i)
        c["chapter"] = placeholder.get("chapter")
        c["section"] = placeholder.get("section") or sec["name"]
        c.setdefault("kind", "extension")
        c["kicker"] = placeholder.get("kicker") or ("Extension · " + sec["name"])
        if i == 0:
            c["kicker"] = c["kicker"] + "  1/" + str(n)
            c["band"] = sec.get("blurb", "")
            # 占位可指定 kp：登记表的锚点落在小节总览卡上
            if placeholder.get("kp"):
                c["kp"] = placeholder["kp"]
            if sec.get("title"):
                c["title"] = c.get("title") or sec["title"]
        else:
            c["kicker"] = c["kicker"] + "  " + str(i + 1) + "/" + str(n)
        out.append(c)
    return sec, out


# ---------------------------------------------------------------- 文本渲染


def esc(s):
    return H.escape(str(s), quote=True)


def md(s):
    """转义后的轻标记: **粗** / *斜* / `行内代码` / $行内公式$ / [文字](链接)
    反引号在这里被转成 <code>，所以产物业务区永远不会出现字面反引号。"""
    t = esc(s)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"`([^`]+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\$([^$]+?)\$", r'<span data-tex="\1"></span>', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


# 属性通道没有 TeX 渲染（core.js 以 innerHTML 注入，不经过 renderAllTex），
# 所以属性里的 LaTeX 必须降级成可读的 Unicode 文本。
# 用「贪婪整词」匹配命令名，避免 \le 吃掉 \left、\in 吃掉 \infty 这类前缀冲突。
TEX_SYM = {
    "times": "×", "cdot": "·", "odot": "⊙", "Vert": "‖", "top": "ᵀ",
    "ge": "≥", "geq": "≥", "le": "≤", "leq": "≤", "neq": "≠", "approx": "≈",
    "pm": "±", "ll": "≪", "infty": "∞", "sum": "Σ", "in": "∈", "propto": "∝",
    "rightarrow": "→", "leftarrow": "←", "to": "→", "mapsto": "↦",
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "lambda": "λ", "mu": "μ", "nu": "ν", "rho": "ρ", "sigma": "σ", "tau": "τ",
    "theta": "θ", "Theta": "Θ", "varphi": "φ", "phi": "φ", "psi": "ψ",
    "pi": "π", "eta": "η", "kappa": "κ", "omega": "ω",
    "left": "", "right": "", "big": "", "Big": "", "bigg": "",
    "mathsf": "", "mathcal": "", "mathbb": "", "mathrm": "", "text": "",
    "tilde": "", "hat": "", "bar": "", "quad": " ", "qquad": " ",
}
SUB = "₀₁₂₃₄₅₆₇₈₉"
SUB_L = {"a": "ₐ", "e": "ₑ", "h": "ₕ", "i": "ᵢ", "j": "ⱼ", "k": "ₖ", "l": "ₗ",
         "m": "ₘ", "n": "ₙ", "o": "ₒ", "p": "ₚ", "r": "ᵣ", "s": "ₛ", "t": "ₜ",
         "u": "ᵤ", "v": "ᵥ", "x": "ₓ"}
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def plain_tex(s):
    """把 LaTeX 降级为可读 Unicode（仅用于属性通道）。"""
    t = s.replace("$$", "").replace("$", "")
    t = t.replace(chr(92) + "{", chr(1)).replace(chr(92) + "}", chr(2))
    t = re.sub(r"\\sqrt\{([^{}]*)\}", r"√(\1)", t)
    t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", t)
    t = re.sub(r"\\tilde\{([A-Za-z])\}", lambda m: m.group(1) + "\u0303", t)
    t = re.sub(r"\\([A-Za-z]+)", lambda m: TEX_SYM.get(m.group(1), m.group(1)), t)
    t = re.sub(r"\\[,;:! ]", " ", t)
    t = re.sub(r"\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"([A-Za-z])_\{?(\d)\}?", lambda m: m.group(1) + SUB[int(m.group(2))], t)
    t = re.sub(r"([A-Za-z])_\{?([a-z])\}?",
               lambda m: m.group(1) + SUB_L.get(m.group(2), "_" + m.group(2)), t)
    t = re.sub(r"([A-Za-z])\^\{?-?1\}", r"\1⁻¹", t)
    t = re.sub(r"([A-Za-z])\^\{?2\}?", r"\1²", t)
    t = re.sub(r"([A-Za-z])\^\{?([0-9])\}?", lambda m: m.group(1) + SUP[int(m.group(2))], t)
    t = re.sub(r"([A-Za-z])\^\{?" + "\u1d40" + r"\}?", r"\1ᵀ", t)
    t = t.replace(chr(1), "{").replace(chr(2), "}")
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def attr_md(s):
    """属性里的轻标记（data-expl / data-hint / data-sol）。
    属性值不能承载 HTML 或 TeX，所以 LaTeX 降级为 Unicode、反引号去掉只留内容；
    **粗** / *斜* 转成 <b> / <i>：这些属性由 JS 以 innerHTML 注入，仍可显示样式。"""
    t = esc(s)
    t = plain_tex(t)
    t = re.sub(r"`([^`]+?)`", r"\1", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<i>\1</i>", t)
    return t


def blocks(items, ctx):
    """渲染一组内容块"""
    out = []
    for b in (items or []):
        t = b.get("t")
        if t == "definition":
            out.append(
                '<div class="defbox"><span class="dlab">DEFINITION</span>'
                '<span class="dformal">' + md(b["formal"]) + "</span>"
                '<span class="dplain">' + md(b["plain"]) + "</span></div>"
            )
        elif t == "p":
            out.append("<p>" + md(b["md"]) + "</p>")
        elif t == "h3":
            out.append("<h3>" + md(b["md"]) + "</h3>")
        elif t == "calc":
            out.append('<div class="calc">' + md(b["md"]) + "</div>")
        elif t == "callout":
            tone = (" " + b["tone"]) if b.get("tone") else ""
            out.append('<div class="callout' + tone + '">' + md(b["md"]) + "</div>")
        elif t == "quote":
            out.append("<blockquote>" + md(b["md"]) + "</blockquote>")
        elif t == "list":
            lis = "".join("<li>" + md(x) + "</li>" for x in b["items"])
            tag = "ol" if b.get("ordered") else "ul"
            out.append("<" + tag + ">" + lis + "</" + tag + ">")
        elif t == "grid2":
            cells = "".join('<div class="cell">' + md(x) + "</div>" for x in b["items"])
            out.append('<div class="grid2">' + cells + "</div>")
        elif t == "steps":
            inner = []
            for i, it in enumerate(b["items"]):
                why = ('<div class="why">' + md(it["why"]) + "</div>") if it.get("why") else ""
                inner.append('<div class="step">' + md(it["md"]) + why + "</div>")
            out.append(
                '<div class="stepper">' + "".join(inner)
                + '<button class="step-btn">Next step →</button></div>'
            )
        elif t == "reveal":
            out.append(
                '<div class="reveal"><button class="reveal-btn">' + md(b["label"]) + "</button>"
                '<div class="reveal-body">' + md(b["md"]) + "</div></div>"
            )
        elif t == "faq":
            out.append("<details class=\"faq\"><summary>" + md(b["q"]) + "</summary><p>"
                       + md(b["a"]) + "</p></details>")
        elif t == "formula":
            parts = ['<div class="fblock">',
                     '<div class="tex-display" data-tex="' + esc(b["tex"]) + '"></div>']
            if b.get("note"):
                parts.append('<div class="formula-note">' + md(b["note"]) + "</div>")
            if b.get("gloss"):
                rows = "".join(
                    "<tr><td><span data-tex=\"" + esc(g["sym"]) + "\"></span></td><td>"
                    + md(g["md"]) + "</td></tr>" for g in b["gloss"]
                )
                parts.append('<table class="symtab"><tr><th>Symbol</th><th>What it means</th></tr>'
                             + rows + "</table>")
            parts.append("</div>")
            out.append("".join(parts))
        elif t == "figure":
            cap = ('<div class="figcap">' + md(b["cap"]) + "</div>") if b.get("cap") else ""
            out.append('<div class="figbox"><img data-fig="' + esc(b["src"].replace(".png", ""))
                       + '" alt="' + esc(b.get("alt", "")) + '">' + cap + "</div>")
        elif t == "table":
            head = b.get("head") or []
            th = ("<tr>" + "".join("<th>" + md(x) + "</th>" for x in head) + "</tr>") if head else ""
            rows = "".join(
                "<tr>" + "".join('<td class="' + esc(c.get("cls", "")) + '">' + md(c["md"]) + "</td>"
                                 if isinstance(c, dict) else "<td>" + md(c) + "</td>" for c in r)
                + "</tr>" for r in b["rows"]
            )
            out.append('<table class="reftable">' + th + rows + "</table>")
        elif t == "html":
            out.append(b["html"])          # 受信内容（实验台 / 谱系图）
        else:
            raise SystemExit("[build] 未知内容块类型: " + str(t) + "  (卡 " + ctx + ")")
    return "\n".join(out)


# ---------------------------------------------------------------- 习题渲染

LETTERS = "ABCDEFGH"


def quiz_block(q, cid):
    t = q.get("t", "choice")
    lv = q.get("level")
    if lv is not None and lv not in LEVELS:
        raise SystemExit("[build] 卡 " + cid + " 的 level 非法: " + str(lv))
    tag = ('<span class="ex-tag">' + lv.upper() + "</span>") if lv else ""

    if t == "choice":
        opts = q["opts"]
        n_correct = sum(1 for o in opts if o.get("correct"))
        if n_correct != 1:
            raise SystemExit("[build] 卡 " + cid + " 单选必须恰一个正确项（现 " + str(n_correct) + "）")
        if len(opts) < 3:
            raise SystemExit("[build] 卡 " + cid + " 选择题至少 3 个选项")
        body = []
        for i, o in enumerate(opts):
            if not o.get("expl"):
                raise SystemExit("[build] 卡 " + cid + " 选项 " + LETTERS[i] + " 缺解析")
            body.append(
                '<button class="opt" data-correct="' + ("1" if o.get("correct") else "0")
                + '" data-expl="' + attr_md(o["expl"]) + '">' + LETTERS[i] + ". " + md(o["md"]) + "</button>"
            )
        return ('<div class="quiz"><p class="quiz-q">' + tag + md(q["q"]) + '</p><div class="opts">'
                + "".join(body) + '</div><div class="expl"></div></div>')

    if t == "multi":
        opts = q["opts"]
        ok = [o for o in opts if o.get("correct")]
        if not ok:
            raise SystemExit("[build] 卡 " + cid + " 多选题无正确项")
        body = []
        for i, o in enumerate(opts):
            if not o.get("expl"):
                raise SystemExit("[build] 卡 " + cid + " 选项 " + LETTERS[i] + " 缺解析")
            body.append(
                '<button class="opt" data-key="' + LETTERS[i] + '" data-correct="'
                + ("1" if o.get("correct") else "0") + '" data-expl="' + attr_md(o["expl"]) + '">'
                + LETTERS[i] + ". " + md(o["md"]) + "</button>"
            )
        return ('<div class="quiz quiz-multi"><p class="quiz-q">' + tag + md(q["q"])
                + ' <span class="dim">(select all that apply)</span></p><div class="opts">' + "".join(body)
                + '</div><button class="mulbtn">Submit</button><div class="expl"></div></div>')

    if t == "num":
        for k in ("answer", "tol", "hint", "sol"):
            if k not in q:
                raise SystemExit("[build] 卡 " + cid + " 数值题缺 " + k + "（四件套）")
        unit = (' <span class="dim">' + md(q["unit"]) + "</span>") if q.get("unit") else ""
        return ('<div class="quiz quiz-num" data-answer="' + esc(q["answer"])
                + '" data-tol="' + esc(q["tol"]) + '" data-hint="' + attr_md(q["hint"])
                + '" data-sol="' + attr_md(q["sol"]) + '">'
                + '<p class="quiz-q">' + tag + md(q["q"]) + unit + "</p>"
                + '<div class="numrow"><input class="numin" inputmode="decimal" '
                  'placeholder="your answer"><button class="numbtn">Check</button></div>'
                + '<div class="expl"></div></div>')

    raise SystemExit("[build] 卡 " + cid + " 未知题型: " + str(t))


def check_levels(items, cid, kind):
    """题数不设上限；但三层必须都有——这是"够不够读者理解"的可检查代理。"""
    if len(items) < 3:
        raise SystemExit("[build] 卡 " + cid + " 习题 " + str(len(items)) + " 道，少于 3 道")
    have = set(q.get("level") for q in items)
    missing = [l for l in LEVELS if l not in have]
    if missing:
        raise SystemExit("[build] 卡 " + cid + " 习题未覆盖层次: " + ", ".join(missing)
                         + "（理解 / 应用 / 迁移 三层每层至少一道；题数不设上限，按读者要理解多少决定）")


# ---------------------------------------------------------------- 卡片渲染


def render_card(card, chap):
    cid = str(card["id"])
    kind = card.get("kind", "narrative")
    kick = KIND_CLASS.get(kind, "k-story")
    title = card["title"]
    attrs = [
        'class="card"', 'data-c="' + cid + '"', 'id="c-' + cid + '"',
        'data-title="' + esc(title) + '"',
        'data-chapter="' + esc(chap["name"]) + '"',
        'data-chapter-num="' + esc(chap["num"]) + '"',
    ]
    if card.get("_secnum"):
        attrs.append('data-sec-num="' + esc(card["_secnum"]) + '"')
    if card.get("section"):
        attrs.append('data-section="' + esc(card["section"]) + '"')
    if card.get("_page"):
        attrs.append('data-pdf="' + esc(card["_page"]) + '"')
    if card.get("_rect"):
        attrs.append('data-pdf-rect="' + esc(card["_rect"]) + '"')
    if card.get("_quote"):
        attrs.append('data-quote="' + esc(card["_quote"]) + '"')
    if card.get("_clip"):
        attrs.append('data-clip="' + esc(card["_clip"]) + '"')
    if card.get("kp"):
        attrs.append('data-kp="' + esc(card["kp"]) + '"')

    head = []
    kicker = card.get("kicker") or (chap["num"] + " · " + chap["name"])
    head.append('<div class="card-kicker ' + kick + '">' + esc(kicker) + "</div>")
    head.append("<h2>" + md(title) + "</h2>")
    if card.get("band"):
        head.append('<div class="ext-band">' + md(card["band"]) + "</div>")
    if kind == "practice" and card.get("for"):
        head.append('<div class="ext-band">Practice set for card <a href="#c-'
                    + esc(card["for"]) + '">' + esc(card["for"]) + "</a> — the number of items "
                    "here is whatever it takes to cover this topic, not a fixed quota.</div>")

    body = []
    if kind in NO_PHASE:
        body.append(blocks(card.get("body"), cid))
    else:
        seq = [("what", "WHAT", "ph-what")]
        if kind not in TWO_PHASE or card.get("example"):
            seq.append(("example", "EXAMPLE", "ph-ex"))
        seq.append(("quiz", "EXERCISES", "ph-quiz"))
        for key, label, cls in seq:
            items = card.get(key)
            if not items:
                raise SystemExit("[build] 卡 " + cid + " 缺 " + key + " 段"
                                 + ("（习题卡可省 example）" if kind in TWO_PHASE else "（三段式）"))
            body.append('<div class="phase ' + cls + '"><span>' + label + "</span></div>")
            if key == "quiz":
                if kind == "lab":
                    if len(items) < 1:
                        raise SystemExit("[build] 卡 " + cid + " 实验卡至少 1 道收束题")
                else:
                    check_levels(items, cid, kind)
                body.append("\n".join(quiz_block(q, cid) for q in items))
            else:
                body.append(blocks(items, cid))

    tail = []
    if card.get("close"):
        tail.append('<div class="callout good">' + md(card["close"]) + "</div>")
    tail.append('<div class="foot-space"></div>')

    return ("<section " + " ".join(attrs) + '>\n<div class="card-inner">\n'
            + "\n".join(head) + "\n" + "\n".join(body) + "\n" + "\n".join(tail)
            + "\n</div>\n</section>")


# ---------------------------------------------------------------- 主流程



# ---------------------------------------------------------------- 章节编号 + PDF 对应
NUM_PREFIX = re.compile(r"^(?:[0-9]+[.][0-9]+[a-z]?|[A-Z][0-9]+)\s+")
CHAP_LETTER = {"wrap": "W", "references": "R"}


def assign_section_numbers(sections, chap_meta):
    """每个章内部独立编号：章 1 的节是 1.1/1.2…，不跨章累计。
    section 字段存的是名字（构建时剥掉旧编号）；编号在这里重新推导，避免手写漂移。"""
    by_id = {}
    for c in sections:
        by_id[str(c.get("id"))] = c
    for c in sections:
        raw = (c.get("section") or "").strip()
        if c.get("kind") == "practice" and c.get("for"):
            src = by_id.get(str(c["for"]))
            if src and src.get("section"):
                raw = src["section"]
        c["_secname"] = NUM_PREFIX.sub("", raw)
    counters, seen = {}, {}
    for c in sections:
        ck = c.get("chapter", "main")
        meta = chap_meta.get(ck, {})
        num = str(meta.get("num", ""))
        name = c["_secname"]
        if ck not in seen:
            seen[ck] = {}
        key = ck + "|" + name
        if name and key not in seen[ck]:
            seen[ck][key] = len(seen[ck]) + 1
        n = seen[ck].get(key)
        if not name:
            c["_secnum"] = ""
            c["section"] = raw = ""
            continue
        if num == "0":
            c["_secnum"] = ""
        elif num and num != "—":
            c["_secnum"] = num + "." + str(n)
        else:
            c["_secnum"] = CHAP_LETTER.get(ck, "X") + str(n)
        c["section"] = (c["_secnum"] + " " + name).strip()



def find_text_block(blocks, text):
    """在某一页的文本块里找包含 text 的块，返回块下标；找不到返回 None。
    大小写敏感：表题注是全大写（TABLE VII），正文引用是混合大小写。"""
    want = " ".join(text.split())
    for bi, b in enumerate(blocks):
        if want in b["t"]:
            return bi
    return None




import fitz               # 论文截图与题注定位都靠它

CAP_GUTTER = 295          # 双栏中缝
PAGE_X = (32.0, 562.0)    # 版心左右界


def _norm_alnum(x):
    return re.sub(r"[^A-Za-z0-9]", "", x)


def find_caption_rect(page, text):
    """把整页词拼成一条“去标点字符流”，在其中定位目标，再映射回词的矩形。
    这样前缀（'III. PRELIMINAR' 命中 'III. PRELIMINARIES'）与跨连字符的词
    （'Abstract—Hypergraph'）都能命中。全大写目标优先取全大写的那次出现，
    以免命中正文里的 'Table VII' 引用。"""
    want = _norm_alnum(text).upper()
    if not want:
        return None
    words = page.get_text("words")
    chars, owner = [], []
    for wi, w in enumerate(words):
        for ch in _norm_alnum(w[4]).upper():
            chars.append(ch)
            owner.append(wi)
    stream = "".join(chars)
    at = 0
    while True:
        k = stream.find(want, at)
        if k < 0:
            return None
        wids = sorted(set(owner[k:k + len(want)]))
        chunk = [words[i] for i in wids]
        if text == text.upper() and any(w[4] != w[4].upper() for w in chunk):
            at = k + 1
            continue
        return fitz.Rect(min(w[0] for w in chunk), min(w[1] for w in chunk),
                         max(w[2] for w in chunk), max(w[3] for w in chunk))


def compute_clip(page, blocks, cap, is_table):
    """题注矩形 -> 截图矩形（连图形一起取）。
    表：题注起，到同栏下一个文本块止；图：上一个文本块起，到题注止。"""
    crosses = cap.x0 < CAP_GUTTER < cap.x1
    if crosses:
        x0, x1 = PAGE_X
    elif cap.x1 <= CAP_GUTTER:
        x0, x1 = PAGE_X[0], CAP_GUTTER
    else:
        x0, x1 = CAP_GUTTER, PAGE_X[1]
    cand = [b for b in blocks
            if b["x1"] > x0 + 8 and b["x0"] < x1 - 8]
    if is_table:
        y0 = cap.y0 - 4
        below = [b for b in cand if b["y0"] >= cap.y1 - 1]
        y1 = (min(b["y0"] for b in below) - 4) if below else page.rect.height - 28
    else:
        y1 = cap.y1 + 6
        above = [b for b in cand if b["y1"] <= cap.y0 + 1]
        y0 = (max(b["y1"] for b in above) + 4) if above else 28
    y1 = min(y1, page.rect.height - 26)
    return fitz.Rect(x0, max(26, y0), x1, y1)

def load_pdf_map(cdir, chap_meta):
    """读 pdf-map.json：每卡的页号、文本块下标、原文截图。"""
    import base64
    f = cdir / "pdf-map.json"
    if not f.exists():
        return {}, None
    m = json.loads(f.read_text(encoding="utf-8"))
    pages, frags, quotes, clips, clipkeys = {}, {}, {}, {}, {}
    defaults = m.get("defaults", {})
    for cid, pg in (m.get("cards") or {}).items():
        pages[str(cid)] = int(pg)
    pdf = ROOT / m["file"] if m.get("file") else None
    doc = None
    if pdf and pdf.exists():
        try:
            import fitz
            doc = fitz.open(str(pdf))
        except Exception as e:
            print("  [pdf] 打不开 " + str(pdf) + "：" + str(e))
    pages_blocks = []
    if doc is not None:
        for pi in range(doc.page_count):
            kept = []
            for b in doc[pi].get_text("blocks", flags=fitz.TEXTFLAGS_TEXT | fitz.TEXT_DEHYPHENATE):
                if b[6] != 0:
                    continue
                t = " ".join(b[4].split())
                if not t or is_boilerplate(t):
                    continue
                kept.append({"t": t, "x0": b[0], "y0": b[1], "x1": b[2], "y1": b[3]})
            pages_blocks.append(kept)
    for cid, a in (m.get("anchors") or {}).items():
        pg = int(a["page"])
        pages[str(cid)] = pg
        if doc is None:
            continue
        fr = find_text_block(pages_blocks[pg - 1], a["text"])
        if fr is not None:
            frags[str(cid)] = "%d:%d" % (pg, fr)
            quotes[str(cid)] = a["text"]
        else:
            print("  [pdf] 第 %d 页找不到锚点 %r" % (pg, a["text"]))
        if doc is None:
            continue
        page = doc[pg - 1]
        cap = find_caption_rect(page, a["text"])
        if cap is None:
            continue
        keys = [a["text"]] + list(a.get("keys") or [])
        hrects = []
        for k in keys:
            r = find_caption_rect(page, k)
            if r:
                hrects.append(r)
        for r in hrects:
            try:
                ann = page.add_highlight_annot(r)
                if ann:
                    ann.set_colors(stroke=(1.0, 0.86, 0.35))
                    ann.update()
            except Exception:
                pass
        key = "%d|%s" % (pg, a["text"])
        clipkeys[str(cid)] = key
        if key not in clips:
            clip = compute_clip(page, pages_blocks[pg - 1], cap, a["text"].startswith("TABLE"))
            pix = page.get_pixmap(clip=clip, dpi=140)
            clips[key] = base64.b64encode(pix.tobytes("png")).decode("ascii")
    meta = {"doc": doc, "defaults": defaults, "pages": pages, "frags": frags, "quotes": quotes, "clips": clips, "clipkeys": clipkeys,
            "blocks": pages_blocks}
    return meta, doc

BOILER = ("Authorized licensed use limited", "FENG et al.: KNOWLEDGE-EMBEDDED",
          "IEEE TRANSACTIONS ON PATTERN ANALYSIS")


def is_boilerplate(t):
    if t.startswith(BOILER):
        return True
    if t.isdigit() and len(t) <= 4:
        return True
    return False


def embed_paper_text(meta):
    """论文全文的文本块（隐藏数据源）+ 单段显示所需的面板骨架之外的仅数据部分。"""
    pages_blocks = meta["blocks"]
    parts = ['<div id="paperPages" hidden>']
    for key, b64 in sorted(meta.get("clips", {}).items()):
        parts.append('<img data-clip="%s" alt="" src="data:image/png;base64,%s">' % (H.escape(key), b64))
    for pi, blocks in enumerate(pages_blocks):
        parts.append('<div class="pgt" data-page="%d">' % (pi + 1))
        for bi, b in enumerate(blocks):
            parts.append('<p class="pb" data-page="%d" data-b="%d">%s</p>'
                         % (pi + 1, bi, H.escape(b["t"])))
        parts.append("</div>")
    parts.append("</div>")
    return "".join(parts)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("用法: python tools/build_site.py <slug>")
        return 2
    slug = args[0]
    do_katex = "--no-katex" not in sys.argv

    cdir = ROOT / "content" / slug
    if not cdir.exists():
        print("未找到内容目录: " + str(cdir))
        return 2

    meta = json.loads((cdir / "meta.json").read_text(encoding="utf-8"))
    chap_meta = {c["key"]: c for c in meta.get("chapters", [])}

    files = sorted((cdir / "cards").glob("c*.json"), key=card_key)
    if not files:
        print("未找到卡片: " + str(cdir / "cards"))
        return 2

    sections = []
    seen = set()
    for f in files:
        card = json.loads(f.read_text(encoding="utf-8"))
        cid = f.stem[1:]                       # 文件名即 id：c37.json -> 37；c37p.json -> 37p
        if card.get("kind") == "include":
            if str(card.get("id", cid)) != cid:
                raise SystemExit("[build] " + f.name + " 的 id 字段与文件名不符")
            if card.get("chapter") not in chap_meta:
                raise SystemExit("[build] " + f.name + " 的 chapter 未声明")
            sec, cards = expand_include(card, cid)
            for c in cards:
                if c["id"] in seen:
                    raise SystemExit("[build] 卡 id 重复: " + c["id"])
                seen.add(c["id"])
                sections.append(c)
            print("  [库] " + card["library"] + " → " + str(len(cards)) + " 张卡（"
                  + cards[0]["id"] + "…" + cards[-1]["id"] + "）")
            continue
        if str(card.get("id", cid)) != cid:
            raise SystemExit("[build] " + f.name + " 的 id 字段与文件名不符: " + str(card.get("id")))
        if cid in seen:
            raise SystemExit("[build] 卡 id 重复: " + cid)
        seen.add(cid)
        card["id"] = cid
        ck = card.get("chapter", "main")
        if ck not in chap_meta:
            raise SystemExit("[build] 卡 " + f.name + " 的 chapter " + ck + " 未在 meta.json 的 chapters 里声明")
        sections.append(card)

    assign_section_numbers(sections, chap_meta)
    pdfmeta, pdfdoc = load_pdf_map(cdir, chap_meta)
    if pdfmeta:
        for c in sections:
            cid = str(c.get("id"))
            pg = pdfmeta["pages"].get(cid)
            if not pg:
                pg = pdfmeta["defaults"].get(c.get("chapter", ""))
            if pg:
                c["_page"] = str(pg)
            if cid in pdfmeta["frags"]:
                c["_rect"] = pdfmeta["frags"][cid]
            if cid in pdfmeta["quotes"]:
                c["_quote"] = pdfmeta["quotes"][cid]
            if cid in pdfmeta["clipkeys"]:
                c["_clip"] = pdfmeta["clipkeys"][cid]

    for c in sections:
        c["_html"] = render_card(c, chap_meta[c.get("chapter", "main")])

    card_html = "\n\n".join(c["_html"] for c in sections)

    tpl = (ROOT / "templates" / "site.html").read_text(encoding="utf-8")
    css = (ROOT / "templates" / "styles.css").read_text(encoding="utf-8")
    core = (ROOT / "shared" / "core.js").read_text(encoding="utf-8")

    widgets = ""
    wpath = cdir / "widgets.js"
    if wpath.exists():
        widgets = wpath.read_text(encoding="utf-8")
    widgets = widgets + """

/* ============ 标准初始化（构建器注入） ============ */
function initSite() {
  initCore('""" + slug + """');
  initQuizzes();
  initNumQuizzes();
  initMultiQuizzes();
  initSteppers();
  initReveals();
  if (typeof initLabs === 'function') { initLabs(); }
  if (typeof renderAllTex === 'function') { renderAllTex(); }
}
initSite();
"""

    out = tpl
    out = out.replace("<!--PI-STYLE-->", css)
    out = out.replace("<!--PI-CORE-->", core)
    out = out.replace("<!--PI-WIDGETS-->", widgets)
    out = out.replace("<!--CARD-CONTENT-->", card_html)
    out = out.replace("{{TITLE}}", H.escape(meta["title"]))
    out = out.replace("{{HEAD_TITLE}}", H.escape(meta.get("head_title", meta["title"])))
    out = out.replace("{{SUBTITLE}}", H.escape(meta.get("subtitle", "")))
    out = out.replace("{{COUNT}}", str(len(sections)))
    # ---- 原 PDF 页面（可被 deploy 阶段整段剥掉） ----
    if pdfdoc is not None and "--no-pages" not in sys.argv:
        pane = embed_paper_text(pdfmeta)
        out = out.replace("{{PAPER-PAGES}}",
                          "<!--PI-PAGES-START-->" + pane + "<!--PI-PAGES-END-->")
        print("  论文文本已内嵌：" + str(sum(len(b) for b in pdfmeta["blocks"])) + " 个段落")
    else:
        out = out.replace("{{PAPER-PANE}}", "")

    # ---- 图片内嵌 ----
    fig_dirs = [cdir / "figures", ROOT / "decomposition" / slug / "figs"]
    cache = {}

    def repl(m):
        name = m.group(1)
        if name not in cache:
            fp = None
            for d in fig_dirs:
                if (d / (name + ".png")).exists():
                    fp = d / (name + ".png")
                    break
            if fp is None:
                raise SystemExit("[build] 找不到图: " + name + " (查过 " + ", ".join(str(d) for d in fig_dirs) + ")")
            cache[name] = "data:image/png;base64," + base64.b64encode(fp.read_bytes()).decode("ascii")
        return m.group(0).replace('data-fig="' + name + '"', 'src="' + cache[name] + '"')

    out, n_fig = re.subn(r'<img data-fig="([A-Za-z0-9_\-]+)"[^>]*>', repl, out)

    left = out.count("data-fig=")
    if left:
        raise SystemExit("[build] 仍有 " + str(left) + " 个未内嵌的 data-fig")

    # ---- 反引号体检（业务区 0 反引号） ----
    body_part = out[out.find("<body"):]
    if "`" in re.sub(r"<script.*?</script>", "", body_part, flags=re.S):
        bad = re.findall(r".{0,40}`.{0,40}", re.sub(r"<script.*?</script>", "", body_part, flags=re.S))
        raise SystemExit("[build] 业务区出现反引号: " + str(bad[:3]))

    if "<!--" in out.replace("<!--CARD-CONTENT-->", ""):
        pass  # 保留注释无妨，占位符检查在下面
    for marker in ("{{TITLE}}", "{{COUNT}}", "<!--CARD-CONTENT-->", "<!--PI-STYLE-->", "<!--PI-CORE-->"):
        if marker in out:
            raise SystemExit("[build] 占位符残留: " + marker)

    dest = ROOT / "sites" / (slug + ".html")
    dest.parent.mkdir(parents=True, exist_ok=True)

    # ---- 防误覆盖：目标已存在且不是 v5 站点时，默认写到 <slug>.v5.html ----
    archived = None
    if dest.exists():
        old = dest.read_text(encoding="utf-8", errors="ignore")
        if 'name="pi-spec" content="v5"' not in old:
            if "--inplace" in sys.argv:
                adir = ROOT / "sites" / "_archive"
                adir.mkdir(parents=True, exist_ok=True)
                archived = adir / (slug + "-pre-v5.html")
                dest.replace(archived)
                print("[build] 已归档旧站点 -> " + str(archived))
            else:
                dest = ROOT / "sites" / (slug + ".v5.html")
                print("[build] 目标已有非 v5 站点，本次写入 " + dest.name
                      + "（要就地替换请加 --inplace，会先归档到 sites/_archive/）")

    dest.write_text(out, encoding="utf-8")

    n_quiz = sum(len(c.get("quiz") or []) for c in sections if c.get("kind") not in NO_PHASE)
    n_num = sum(1 for c in sections for q in (c.get("quiz") or []) if q.get("t") == "num")
    n_ph = sum(1 for c in sections if c.get("kind") not in NO_PHASE)
    print("OK — %s | 卡 %d | 图 %d | 习题 %d（数值 %d）| 三段式卡 %d | 大小 %d KB"
          % (dest, len(sections), n_fig, n_quiz, n_num, n_ph, dest.stat().st_size // 1024))

    if do_katex:
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "embed_katex.py"), str(dest)])
        if r.returncode != 0:
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
