#!/usr/bin/env python3
"""Assemble an epub of O. O. Rosenberg, "Problems of Buddhist Philosophy" (1918).

Source: PSYLIB electronic library (cp1251 HTML, one file per chapter).
Only the public-domain part is included: preface, 19 chapters and Rosenberg's
own endnotes. The 1991 editorial apparatus by A. N. Ignatovich is still under
copyright and is deliberately left out.
"""

import html
import pathlib
import re
import subprocess
import sys
import urllib.request

BASE = "https://psylib.org.ua/books/rozeo02/"
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = HERE / "cache"
CLEAN = HERE / "clean"

# preface, chapters I-XIX, author's own endnotes
PAGES = ["txt00"] + [f"txt{i:02d}" for i in range(1, 20)] + ["refer"]

FALLBACK_TITLES = {"refer": "Примечания"}


def fetch():
    CACHE.mkdir(exist_ok=True)
    for name in PAGES:
        dst = CACHE / f"{name}.htm"
        if dst.exists():
            continue
        print("fetch", name)
        with urllib.request.urlopen(BASE + name + ".htm") as r:
            dst.write_bytes(r.read())


def strip_chrome(s):
    """drop the prev/index/next navbar, psylib footer, styles and images"""
    m = re.search(r"<BODY[^>]*>", s, re.I)
    if m:
        start = m.end()
        hr = re.search(r"<HR[^>]*>", s[start:], re.I)
        if hr and hr.start() < 1200:
            s = s[:start] + s[start + hr.end():]
    s = re.sub(r"<P align=center>\s*<A href=\"txt.*?</BODY>", "</BODY>", s,
               flags=re.I | re.S)
    s = re.sub(r"<H5><A HREF=\"mailto:.*?</H5>", "", s, flags=re.I | re.S)
    s = re.sub(r"<style[^>]*>.*?</style>", "", s, flags=re.I | re.S)
    s = re.sub(r"<TITLE>.*?</TITLE>", "", s, flags=re.I | re.S)
    s = re.sub(r"<link[^>]*>|<img[^>]*>", "", s, flags=re.I)
    return s


def rewrite_links(s):
    """flatten cross-file references so they survive the merge into one epub"""
    s = re.sub(r'href="refer\.htm#', 'href="#', s, flags=re.I)
    s = re.sub(r'href="(komen|sokra|index)\.htm[^"]*"', 'href="#"', s, flags=re.I)
    s = re.sub(r'href="txt\d+\.htm(#[^"]*)?"', 'href="#"', s, flags=re.I)
    s = re.sub(r"\starget=_blank", "", s, flags=re.I)
    return s


def promote_heading(s, fallback=None):
    """psylib splits a chapter head into <H3>numeral</H3> + <H2>title</H2>"""
    m = re.search(r"<H3>(.*?)</H3>\s*<H2>(.*?)</H2>", s, re.I | re.S)
    if m:
        num = re.sub(r"<[^>]+>", " ", m.group(1))
        ttl = re.sub(r"<[^>]+>", " ", re.sub(r"<BR>", " ", m.group(2), flags=re.I))
        head = " ".join(f"{num.strip()} {ttl.strip()}".split())
        return s[:m.start()] + f"<h1>{html.escape(head)}</h1>" + s[m.end():]
    m = re.search(r"<H([12])>(.*?)</H\1>", s, re.I | re.S)
    if m:
        ttl = re.sub(r"<[^>]+>", " ", re.sub(r"<BR>", " ", m.group(2), flags=re.I))
        head = " ".join(ttl.split())
        return s[:m.start()] + f"<h1>{html.escape(head)}</h1>" + s[m.end():]
    if fallback:
        return re.sub(r"(<BODY[^>]*>)", r"\1<h1>" + fallback + "</h1>", s,
                      count=1, flags=re.I)
    return s


def clean():
    CLEAN.mkdir(exist_ok=True)
    for name in PAGES:
        s = (CACHE / f"{name}.htm").read_bytes().decode("cp1251", "replace")
        s = strip_chrome(s)
        s = rewrite_links(s)
        s = promote_heading(s, FALLBACK_TITLES.get(name))
        s = re.sub(r"charset=windows-1251", "charset=utf-8", s, flags=re.I)
        (CLEAN / f"{name}.html").write_text(s, encoding="utf-8")


def build():
    cover = HERE / "cover.jpg"
    if not cover.exists():
        subprocess.run([sys.executable, str(HERE / "cover.py")], check=True)
    out = ROOT / "rozenberg-problemy-buddiyskoy-filosofii.epub"
    cmd = [
        "pandoc",
        *[str(CLEAN / f"{n}.html") for n in PAGES],
        str(HERE / "colophon.html"),
        "-f", "html", "-t", "epub3",
        "--metadata-file", str(HERE / "metadata.yaml"),
        "-M", "title=Проблемы буддийской философии",
        "--epub-cover-image", str(cover),
        "--toc", "--toc-depth=1", "--split-level=1",
        "-o", str(out),
    ]
    subprocess.run(cmd, check=True)
    print("built", out, f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    fetch()
    clean()
    build()
