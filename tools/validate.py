# -*- coding: utf-8 -*-
"""validate.py v5 —— 独立校验器（数据层 + 渲染层）

用法:
    python tools/validate.py feng-2026-knowledge-hgnn        # 数据 + 构建产物
    python tools/validate.py sites/xxx.v5.html               # 只校验产物

它**独立于 build_site.py**：渲染器可能有 bug，校验器拿着磁盘上的实际数据与 HTML 重新判一遍。
输出每条铁律 PASS/FAIL，末尾给总判定。
"""
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
LEVELS = ("understand", "apply", "transfer")
NO_PHASE = {"narrative", "critique", "wrap", "summary", "cover"}
TWO_PHASE = {"practice", "check"}
KNOWN_KINDS = {
    "title", "kp-a", "kp-b", "formula", "figure", "table", "lab", "extension",
    "ext-overview", "reference", "abstract", "intro", "method", "experiment",
    "conclusion", "critique", "wrap", "narrative", "check", "practice",
    "cover", "summary", "include", "proof",
}
REQUIRED_IDS = ["progressFill", "topbar", "menuBtn", "chapStrip", "outline", "outlineList",
                "outlineClose", "scrim", "cardArea", "navbar", "navPrev", "navNext",
                "pageNum", "editorOverlay", "edAnchor", "edTitle", "edBody", "edSave", "edCancel"]

results = []          # (ok, 类别, 描述)


def ok(cond, cat, desc, detail=""):
    results.append((bool(cond), cat, desc + (("  → " + detail) if detail and not cond else "")))
    return bool(cond)


# ------------------------------------------------------------------ 数据层

def card_key(p):
    m = re.match(r"c(\d+)([a-z]*)$", p.stem)
    return (int(m.group(1)), m.group(2)) if m else (10 ** 9, p.stem)


def check_card_body(card, tag, cdir, slug, counter):
    """内容体检（不含 id / chapter 归属）。论文卡与拓展库卡片共用同一套标准。"""
    kind = card.get("kind")
    ok(card.get("title"), "数据", tag + " 有标题")
    ok(kind in KNOWN_KINDS, "数据", tag + " kind 合法", "kind=" + str(kind))
    if kind in NO_PHASE:
        ok(bool(card.get("body")), "数据", tag + " 有 body")
        return
    for ph in ("what", "quiz"):
        ok(bool(card.get(ph)), "数据", tag + " 有 " + ph + " 段")
    if kind not in TWO_PHASE:
        ok(bool(card.get("example")), "数据", tag + " 有 example 段")

    quizzes = card.get("quiz") or []
    counter["quiz"] += len(quizzes)
    if kind != "lab":
        ok(len(quizzes) >= 3, "数据", tag + " 习题 ≥3 道", "现 " + str(len(quizzes)))
        have = set(q.get("level") for q in quizzes)
        miss = [l for l in LEVELS if l not in have]
        ok(not miss, "数据", tag + " 习题覆盖三层", "缺 " + ",".join(miss))
    for i, q in enumerate(quizzes):
        qtag = tag + " Q" + str(i + 1)
        if kind != "lab":
            ok(q.get("level") in LEVELS, "数据", qtag + " level 合法", str(q.get("level")))
        t = q.get("t", "choice")
        if t == "choice":
            opts = q.get("opts") or []
            ok(len(opts) >= 3, "数据", qtag + " 选项 ≥3")
            ok(sum(1 for o in opts if o.get("correct")) == 1, "数据", qtag + " 恰一个正确项")
            ok(all(o.get("expl") for o in opts), "数据", qtag + " 每个选项都有解析")
        elif t == "multi":
            opts = q.get("opts") or []
            ok(sum(1 for o in opts if o.get("correct")) >= 1, "数据", qtag + " 至少一个正确项")
            ok(all(o.get("expl") for o in opts), "数据", qtag + " 每个选项都有解析")
        elif t == "num":
            ok(all(k in q for k in ("answer", "tol", "hint", "sol")), "数据", qtag + " 四件套齐全")
            try:
                float(q["answer"]); float(q["tol"])
            except Exception:
                ok(False, "数据", qtag + " answer/tol 是数字")
        else:
            ok(False, "数据", qtag + " 题型已知", str(t))

    for b in (card.get("what") or []) + (card.get("example") or []):
        if b.get("t") == "figure":
            name = b["src"]
            found = (ROOT / "decomposition" / slug / "figs" / name).exists()
            if cdir is not None:
                found = found or (cdir / "figures" / name).exists()
            ok(found, "数据", tag + " 图片存在", name)


def validate_data(slug):
    cdir = ROOT / "content" / slug
    if not cdir.exists():
        return ok(False, "数据", "content/" + slug + " 存在")
    ok(True, "数据", "content/" + slug + " 存在")
    mpath = cdir / "meta.json"
    if not ok(mpath.exists(), "数据", "meta.json 存在"):
        return
    meta = json.loads(mpath.read_text(encoding="utf-8"))
    for f in ("slug", "title", "chapters"):
        ok(f in meta and meta[f], "数据", "meta." + f + " 非空")
    ok(meta.get("slug") == slug, "数据", "meta.slug 与目录名一致")
    chap_keys = [c["key"] for c in meta.get("chapters", [])]
    ok(len(chap_keys) == len(set(chap_keys)), "数据", "chapters 无重复 key")
    for c in meta.get("chapters", []):
        ok(all(k in c for k in ("key", "num", "name")), "数据", "chapter 字段齐备: " + str(c.get("key")))

    files = sorted((cdir / "cards").glob("c*.json"), key=card_key) if (cdir / "cards").exists() else []
    if not ok(files, "数据", "cards/ 下有卡片"):
        return

    seen_ids, seen_kp = set(), {}
    counter = {"quiz": 0}
    n_cards = 0
    keys = [card_key(p) for p in files]
    ok(keys == sorted(keys), "数据", "卡片文件名有序")

    for p in files:
        cid = p.stem[1:]
        try:
            card = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            ok(False, "数据", p.name + " 是合法 JSON", str(e))
            continue
        if not ok(str(card.get("id", cid)) == cid, "数据", p.name + " id 与文件名一致"):
            continue

        if card.get("kind") == "include":
            lib = card.get("library")
            d = ROOT / "shared" / "kp-library" / str(lib)
            if not ok(d.exists(), "数据", p.name + " 指向的库小节存在", str(lib)):
                continue
            ok((d / "section.json").exists(), "数据", "库小节有 section.json: " + str(lib))
            lf = sorted(d.glob("c*.json"), key=lambda q: int(re.sub(r"\D", "", q.stem)))
            if not ok(lf, "数据", "库小节有卡片: " + str(lib)):
                continue
            n_cards += len(lf)
            for q in lf:
                check_card_body(json.loads(q.read_text(encoding="utf-8")),
                                "lib:" + str(lib) + "/" + q.name, None, slug, counter)
            continue

        ok(cid not in seen_ids, "数据", p.name + " id 唯一")
        seen_ids.add(cid)
        n_cards += 1
        ok(card.get("chapter") in chap_keys, "数据", p.name + " chapter 已声明",
           "chapter=" + str(card.get("chapter")))
        kp = card.get("kp")
        if kp:
            ok(re.match(r"^kp-[a-z0-9\-]+$", kp) is not None, "数据", p.name + " kp 格式合法", kp)
            ok(kp not in seen_kp, "数据", p.name + " kp 唯一", "已被 " + str(seen_kp.get(kp)) + " 占用")
            seen_kp[kp] = cid
        check_card_body(card, p.name, cdir, slug, counter)

    n_quiz = counter["quiz"]
    ok(n_quiz > 0, "数据", "全站习题数 > 0", str(n_quiz))
    print("  数据层：%d 张卡（含拓展库展开），%d 道习题，%d 个知识点" % (n_cards, n_quiz, len(seen_kp)))
    return n_cards


# ------------------------------------------------------------------ 渲染层

def validate_html(slug, path):
    if not ok(path.exists(), "产物", path.name + " 存在"):
        return
    s = path.read_text(encoding="utf-8")
    spec = (re.search(r'name="pi-spec" content="([^"]+)"', s) or [None, "?"])[1]
    body = s[s.find("<body"):]
    scriptless = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    styleless = re.sub(r"<style.*?</style>", "", scriptless, flags=re.S)

    # ---- 通用铁律（v4 / v5 通用）----
    ok("`" not in styleless, "产物", "业务区 0 反引号",
       str(re.findall(r".{0,30}`.{0,30}", styleless)[:2]))
    ok("data-fig=" not in s, "产物", "0 个未内嵌图片占位")
    ext = re.findall(r'(?:src|href)="https?://[^"]+', s)
    ok(not ext, "产物", "零外部 CDN", str(ext[:2]))
    ok("(function" not in scriptless and "( () =>" not in scriptless, "产物", "业务区无 IIFE")
    ok(re.search(r"\.card\s*\{[^}]*overflow:\s*hidden", s) is not None, "产物", ".card overflow:hidden")
    ok("{{" not in scriptless and "<!--CARD-CONTENT-->" not in s, "产物", "0 占位符残留")
    noexpl = len(re.findall(r'<button class="opt"(?![^>]*data-expl)', s))
    ok(noexpl == 0, "产物", "所有选项都带 data-expl", str(noexpl) + " 个缺失")
    cards = re.findall(r'<section class="card"[^>]*data-c="([^"]+)"', s)
    ok(cards, "产物", "有卡片")
    ok(len(cards) == len(set(cards)), "产物", "data-c 唯一")

    if spec != "v5":
        # v4 / 更早的冻结产物：只跑通用铁律，不套 v5 的三段式与习题层次检查
        ok("PI-LOADING" in s or "PI-OK" in s, "产物", "title 标记存在")
        for eid in ("progressFill", "cardArea", "navPrev", "navNext", "pageNum", "outlineList"):
            ok(('id="' + eid + '"') in s, "产物", "元素存在 #" + eid)
        n_tex = s.count("data-tex=")
        if n_tex:
            ok('id="katex-vendor"' in s, "产物", "含公式 → KaTeX vendor 已内嵌")
        n_fig = len(re.findall(r'<img[^>]*base64', s))
        print("  [冻结产物 spec=%s，仅通用铁律] %d 张卡，%d 张图，%d 处公式，%d KB"
              % (spec, len(cards), n_fig, n_tex, path.stat().st_size // 1024))
        return len(cards)

    # ---- v5 专有 ----
    ok(spec == "v5", "产物", "pi-spec = v5", "实为 " + str(spec))
    ok("PI-LOADING" in s, "产物", "title 含 PI-LOADING（JS 跑起来才翻 PI-OK）")
    for eid in REQUIRED_IDS:
        ok(('id="' + eid + '"') in s, "产物", "元素存在 #" + eid)
    n_tex = s.count("data-tex=")
    if n_tex:
        ok('id="katex-vendor"' in s, "产物", "含公式 → KaTeX vendor 已内嵌")
        ok('id="pi-tex-boot"' in s, "产物", "含公式 → 渲染引导已注入")

    bad_order = []
    for m in re.finditer(r'<section class="card"(.*?)</section>', s, flags=re.S):
        seg = m.group(1)
        ph = re.findall(r'class="phase ph-(\w+)"', seg)
        if not ph:
            continue
        if ph not in (["what", "ex", "quiz"], ["what", "quiz"]):
            cid = re.search(r'data-c="([^"]+)"', seg)
            bad_order.append((cid.group(1) if cid else "?") + ": " + ",".join(ph))
    ok(not bad_order, "产物", "三段式顺序正确（what → ex → quiz）", str(bad_order[:3]))

    n_fig = len(re.findall(r'<img[^>]*base64', s))
    print("  渲染层：%d 张卡，%d 张内嵌图，%d 处公式，%d KB"
          % (len(cards), n_fig, n_tex, path.stat().st_size // 1024))
    return len(cards)


# ------------------------------------------------------------------ 主流程

def main():
    if len(sys.argv) < 2:
        print("用法: python tools/validate.py <slug 或 站点路径>")
        return 2
    arg = sys.argv[1]
    if arg.endswith(".html"):
        path = Path(arg)
        if not path.exists():
            path = ROOT / "sites" / Path(arg).name
        slug = path.stem.replace(".v5", "")
        validate_html(slug, path)
    else:
        slug = arg
        n_data = validate_data(slug)
        v5 = ROOT / "sites" / (slug + ".v5.html")
        plain = ROOT / "sites" / (slug + ".html")
        path = plain if plain.exists() else v5          # 正式产物优先（v5.html 只是未定稿时的暂存名）
        n_html = validate_html(slug, path)
        if n_data is not None and n_html is not None:
            ok(n_data == n_html, "交叉", "数据卡数 = 产物卡数",
               "数据 %s vs 产物 %s" % (n_data, n_html))

    n_fail = sum(1 for r in results if not r[0])
    for good, cat, desc in results:
        if not good:
            print("  FAIL [" + cat + "] " + desc)
    print()
    if n_fail == 0:
        print("PASS — 全部铁律通过（%d 项）" % len(results))
        return 0
    print("FAIL — %d / %d 项未通过" % (n_fail, len(results)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
