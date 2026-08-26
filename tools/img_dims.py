#!/usr/bin/env python3
"""
Add real width/height (and decoding="async") to content images that lack them.

Why it matters, precisely: on desktop .mod-figure and .sec-figure carry a fixed
aspect-ratio, so the slot is reserved before the image arrives and there is no
layout shift. At <=900px responsive.css sets `aspect-ratio:auto` and
`img{height:auto}` so the slot hugs the artwork instead — and there the box has
no height until the image loads, which shifts everything below it. width/height
attributes give the browser the ratio up front and close that gap on phones.

index.html is deliberately skipped: its images without dimensions are the
decorative glows and the base64 pipeline nodes, which are positioned by CSS in
percentages and must not be given intrinsic sizes.

loading="lazy" is NOT added. Getting it onto an above-the-fold image delays the
LCP element, and which image that is differs per page and per breakpoint --
that is a judgement call, not a mechanical one.

Re-runnable: only touches <img> tags that are missing width or height.
    python3 tools/img_dims.py [--dry-run]
"""
import os, re, sys, glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry-run" in sys.argv

PAGES = ["product.html", "solutions.html", "about.html",
         "contact.html", "resources.html"] + sorted(
    os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "articles", "*.html")))

IMG = re.compile(r'<img\b[^>]*>', re.S)


def resolve(src, page):
    if src.startswith(("data:", "http://", "https://")):
        return None
    if src.startswith("/"):
        return os.path.join(ROOT, src.lstrip("/"))
    return os.path.normpath(os.path.join(ROOT, os.path.dirname(page), src))


def main():
    touched = added = skipped = 0
    for page in PAGES:
        path = os.path.join(ROOT, page)
        s = open(path, encoding="utf-8", newline="").read()
        out, changed = [], 0
        last = 0

        for m in IMG.finditer(s):
            tag = m.group(0)
            if "width=" in tag and "height=" in tag:
                continue
            src = re.search(r'src="([^"]+)"', tag)
            if not src:
                continue
            f = resolve(src.group(1), page)
            if not f or not os.path.exists(f):
                skipped += 1
                continue
            with Image.open(f) as im:
                w, h = im.size

            new = tag
            if "width=" not in new:
                new = new.replace("<img", '<img width="%d"' % w, 1)
            if "height=" not in new:
                new = new.replace('width="%d"' % w, 'width="%d" height="%d"' % (w, h), 1)
            if "decoding=" not in new:
                new = new[:-1].rstrip() + ' decoding="async">'

            out.append(s[last:m.start()])
            out.append(new)
            last = m.end()
            changed += 1

        if changed:
            out.append(s[last:])
            if not DRY:
                open(path, "w", encoding="utf-8", newline="").write("".join(out))
            touched += 1
            added += changed
            print("  %-42s %d image%s" % (page, changed, "" if changed == 1 else "s"))

    print("%s%d images in %d files%s"
          % ("[dry run] " if DRY else "", added, touched,
             (", %d skipped (no local file)" % skipped) if skipped else ""))


if __name__ == "__main__":
    main()
