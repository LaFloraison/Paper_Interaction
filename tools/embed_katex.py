# -*- coding: utf-8 -*-
"""KaTeX 载入即渲染内嵌器 (无需 Node)

用法: python tools/embed_katex.py sites/<slug>.html

把 katex.min.css(+woff2 字体 base64) 与 katex.min.js 全部内嵌进 HTML,
并注入渲染引导脚本: 打开页面时对 [data-tex] 元素做本地渲染。
产物保持单文件零 CDN。幂等 — 重复运行安全。
"""
import base64
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIST = Path(__file__).parent / "katex_pkg" / "package" / "dist"

BOOT_JS = """<script id="pi-tex-boot">
function renderAllTex() {
  var els = document.querySelectorAll('[data-tex]');
  var i, el, tex, isDisplay;
  for (i = 0; i < els.length; i++) {
    el = els[i];
    tex = el.getAttribute('data-tex');
    isDisplay = el.classList.contains('tex-display');
    try {
      el.innerHTML = katex.renderToString(tex, { displayMode: isDisplay, throwOnError: false });
    } catch (e) {
      el.innerHTML = '<span style="color:#dc2626">[公式渲染失败]</span>';
    }
  }
  if (!/PI-OK/.test(document.title)) {
    document.title = document.title.replace('PI-LOADING', 'PI-OK');
  }
}
</script>"""


def build_style() -> str:
    css = (DIST / "katex.min.css").read_text(encoding="utf-8")
    cache = {}

    def font_uri(m):
        rel = m.group(1)
        if rel not in cache:
            fp = DIST / rel
            b64 = base64.b64encode(fp.read_bytes()).decode("ascii")
            cache[rel] = "data:font/woff2;base64," + b64
        return "url(" + cache[rel] + ")"

    css = re.sub(r"url\((fonts/[^)]+?\.woff2)\)", font_uri, css)
    return "<style id=\"katex-inline\">" + css + "</style>"


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python tools/embed_katex.py <html文件>")
        return 2
    target = Path(sys.argv[1])
    if not target.exists():
        print("文件不存在: " + str(target))
        return 2

    html = target.read_text(encoding="utf-8")
    vendor_js = "<script id=\"katex-vendor\">" + (DIST / "katex.min.js").read_text(encoding="utf-8") + "</script>"
    style = build_style()

    n_tex = len(re.findall(r"data-tex=", html))

    if 'id="katex-vendor"' in html:
        html = re.sub(r'<script id="katex-vendor">.*?</script>', lambda m: vendor_js, html, flags=re.S)
    else:
        html = html.replace("</head>", vendor_js + "\n" + style + "\n" + BOOT_JS + "\n</head>")

    if 'id="katex-inline"' not in html:
        html = html.replace("</head>", style + "\n</head>")

    if 'id="pi-tex-boot"' in html:
        html = re.sub(r'<script id="pi-tex-boot">.*?</script>', lambda m: BOOT_JS, html, flags=re.S)
    else:
        html = html.replace("</head>", BOOT_JS + "\n</head>")

    target.write_text(html, encoding="utf-8")
    size_kb = target.stat().st_size // 1024
    print("OK — " + str(n_tex) + " 个 data-tex 待页面本地渲染, 内嵌 CSS+20 字体+min.js, 文件 " + str(size_kb) + " KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
