# -*- coding: utf-8 -*-
"""图表内嵌器：把 <img data-fig="figN"> 替换为 base64 data URI（单文件零依赖）
用法: python tools/embed_figs.py sites/<slug>.html
PNG 来源: decomposition/<slug>/figs/
"""
import base64
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

root = Path(__file__).parent.parent


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python tools/embed_figs.py <html文件>")
        return 2
    target = Path(sys.argv[1])
    html = target.read_text(encoding="utf-8")
    m = re.search(r"decomposition/([a-z0-9\-]+)/figs", html)
    figs_dir = root / "decomposition"
    # 从站点 slug 推断 figs 目录
    slug = target.stem
    figs = root / "decomposition" / slug / "figs"
    if not figs.exists():
        print("未找到图表目录: " + str(figs))
        return 2

    cache = {}

    def repl(mm):
        name = mm.group(1)
        if name not in cache:
            fp = figs / (name + ".png")
            if not fp.exists():
                print("警告: 缺图 " + name)
                return mm.group(0)
            b64 = base64.b64encode(fp.read_bytes()).decode("ascii")
            cache[name] = "data:image/png;base64," + b64
        return mm.group(0).replace('data-fig="' + name + '"', 'src="' + cache[name] + '"')

    html2, n = re.subn(r'<img data-fig="([a-z0-9]+)"[^>]*>', repl, html)
    target.write_text(html2, encoding="utf-8")
    print("OK — 内嵌 " + str(len(cache)) + " 张图, 文件 " + str(target.stat().st_size // 1024) + " KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
