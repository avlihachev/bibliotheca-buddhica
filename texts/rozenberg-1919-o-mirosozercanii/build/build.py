#!/usr/bin/env python3
"""Assemble an epub of O. O. Rosenberg, "On the Worldview of Contemporary Buddhism
in the Far East" (a public lecture, Petrograd 1919).

Source: PSYLIB electronic library, a single cp1251 HTML page.
The nine editorial notes are by A. N. Ignatovich (1991) and still under copyright,
so both the notes and their in-text markers are stripped.
"""

import pathlib
import re
import subprocess
import sys
import urllib.request

URL = "https://psylib.org.ua/books/_rozeo01.htm"
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = HERE / "cache"
CLEAN = HERE / "clean"


def fetch():
    CACHE.mkdir(exist_ok=True)
    dst = CACHE / "source.htm"
    if not dst.exists():
        print("fetch", URL)
        with urllib.request.urlopen(URL) as r:
            dst.write_bytes(r.read())
    return dst.read_bytes().decode("cp1251", "replace")


def extract_body(s):
    """keep only the lecture itself: drop psylib chrome, the title block,
    the back-to-top bar and everything from the first Ignatovich note onwards"""
    start = re.search(r"<HR SIZE=4></DIV>", s, re.I)
    if not start:
        raise SystemExit("title block boundary not found — source layout changed")
    s = s[start.end():]
    end = re.search(r"<P><BR><DIV ALIGN=CENTER><HR SIZE=1>", s, re.I)
    if not end:
        raise SystemExit("end-of-text boundary not found — source layout changed")
    return s[:end.start()]


def strip_notes(s):
    # in-text markers pointing at the 1991 notes
    s = re.sub(r"<sup>\s*<A [^>]*href=\"#s\d+\"[^>]*>.*?</A>\s*</sup>", "", s,
               flags=re.I | re.S)
    return s


def normalise(s):
    s = re.sub(r"<style[^>]*>.*?</style>", "", s, flags=re.I | re.S)
    s = re.sub(r"<img[^>]*>|<link[^>]*>", "", s, flags=re.I)
    s = re.sub(r"\son[A-Za-z]+\s*=\s*\"[^\"]*\"", "", s)
    s = re.sub(r"<a name=\"[^\"]*\"></a>", "", s, flags=re.I)
    # section headings: <H3>I. ПУТЬ МЫШЛЕНИЯ</H3> -> <h1>
    s = re.sub(r"<H3>(.*?)</H3>", lambda m: "<h1>%s</h1>" % " ".join(
        re.sub(r"<[^>]+>", " ", m.group(1)).split()), s, flags=re.I | re.S)
    return s


def clean():
    s = fetch()
    s = extract_body(s)
    s = strip_notes(s)
    s = normalise(s)
    CLEAN.mkdir(exist_ok=True)
    out = CLEAN / "lecture.html"
    out.write_text(
        '<html><head><meta charset="utf-8"></head><body>\n%s\n</body></html>' % s,
        encoding="utf-8")
    heads = re.findall(r"<h1>(.*?)</h1>", s)
    print("sections:", heads)
    return out


def build(body):
    cover = HERE / "cover.jpg"
    if not cover.exists():
        subprocess.run([sys.executable, str(HERE / "cover.py")], check=True)
    out = ROOT / "rozenberg-o-mirosozercanii.epub"
    subprocess.run([
        "pandoc", str(body), str(HERE / "colophon.html"),
        "-f", "html", "-t", "epub3",
        "--metadata-file", str(HERE / "metadata.yaml"),
        "-M", "title=О миросозерцании современного буддизма на Дальнем Востоке",
        "--epub-cover-image", str(cover),
        "--toc", "--toc-depth=1", "--split-level=1",
        "-o", str(out),
    ], check=True)
    print("built", out, f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    build(clean())
