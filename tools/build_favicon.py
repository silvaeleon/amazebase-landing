# -*- coding: utf-8 -*-
"""
Build the site's favicons from the header's brand mark, and link them from
every page.

The mark is the <svg class="brand-mark" viewBox="0 0 32 32"> in every header:
two paths, the outer "A" filled with #markGrad (#5B4FE6 -> #A93BF1, top-left
to bottom-right of its bounding box) and the inner triangle #C56BF5 at .85
opacity. Leon approved using it as the favicon on 2026-09-11.

Writes
  favicon.ico                    16, 32 and 48 px (PNG-in-ICO). At the site
                                 root because browsers ask for /favicon.ico
                                 whether or not a page links it.
  assets/img/favicon.svg         the mark itself, for browsers that take SVG
  assets/img/apple-touch-icon.png  180 px on the site background (#030917):
                                 iOS paints a transparent icon black

and puts the three <link> lines after the viewport meta of every live page
(every tracked .html outside _*, index-*, editor, graphify-out, assets/).
Pure Python -- no imaging library on this machine: the two polygons are
rasterised with 8x8 supersampling per pixel.

    python tools/build_favicon.py            # write
    python tools/build_favicon.py --check    # what would change; writes nothing
"""

import io, os, re, struct, subprocess, sys, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = "--check" in sys.argv

OUTER = [(16, 3.2), (29, 27.5), (22.6, 27.5), (16, 14.1), (9.4, 27.5), (3, 27.5)]  # M16 3.2 29 27.5h-6.4L16 14.1 9.4 27.5H3z
INNER = [(16, 17.6), (20.4, 25.8), (11.6, 25.8)]                                    # M16 17.6l4.4 8.2h-8.8z
G0, G1 = (0x5B, 0x4F, 0xE6), (0xA9, 0x3B, 0xF1)
INNER_RGB, INNER_A = (0xC5, 0x6B, 0xF5), 0.85
BG = (0x03, 0x09, 0x17)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#5B4FE6"/><stop offset="100%" stop-color="#A93BF1"/></linearGradient></defs>
<path d="M16 3.2 29 27.5h-6.4L16 14.1 9.4 27.5H3z" fill="url(#g)"/>
<path d="M16 17.6l4.4 8.2h-8.8z" fill="#C56BF5" opacity=".85"/>
</svg>
"""

LINKS = ('<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
         '<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">\n'
         '<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">\n')
VIEWPORT = '<meta name="viewport" content="width=device-width,initial-scale=1">\n'


def inside(pt, poly):
    x, y = pt
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def render(size, pad=0.0, bg=None, ss=8):
    """RGBA rows. The 32-unit viewBox is scaled into size*(1-2*pad), centred."""
    bx0, by0 = min(p[0] for p in OUTER), min(p[1] for p in OUTER)
    bw, bh = max(p[0] for p in OUTER) - bx0, max(p[1] for p in OUTER) - by0
    inner = size * (1 - 2 * pad)
    k, off = inner / 32.0, size * pad
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            r = g = b = a = 0.0
            for sy in range(ss):
                for sx in range(ss):
                    x = ((px + (sx + .5) / ss) - off) / k
                    y = ((py + (sy + .5) / ss) - off) / k
                    cr, cg, cb, ca = (bg + (1.0,)) if bg else (0, 0, 0, 0.0)
                    if inside((x, y), OUTER):
                        t = min(1, max(0, ((x - bx0) / bw + (y - by0) / bh) / 2))
                        cr, cg, cb = [G0[i] + (G1[i] - G0[i]) * t for i in range(3)]
                        ca = 1.0
                    if inside((x, y), INNER):
                        a2 = INNER_A
                        na = a2 + ca * (1 - a2)
                        cr, cg, cb = [(INNER_RGB[i] * a2 + c * ca * (1 - a2)) / na
                                      for i, c in enumerate((cr, cg, cb))]
                        ca = na
                    r += cr * ca; g += cg * ca; b += cb * ca; a += ca
            n = ss * ss
            if a:
                row += bytes((round(r / a), round(g / a), round(b / a), round(255 * a / n)))
            else:
                row += bytes((0, 0, 0, 0))
        rows.append(bytes(row))
    return rows


def png(rows):
    size = len(rows)
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def ico(pngs):
    head = struct.pack("<HHH", 0, 1, len(pngs))
    off = 6 + 16 * len(pngs)
    dirs, data = b"", b""
    for size, blob in pngs:
        dirs += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(blob), off + len(data))
        data += blob
    return head + dirs + data


def live_pages():
    # google<token>.html is Google Search Console's verification file: one line
    # of text with an .html name, which Google reads verbatim. It is not a page
    # and must not be touched.
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "*.html"], capture_output=True, text=True).stdout.split()
    return [p for p in out if not re.match(r"(_|index-|editor|graphify-out/|assets/|google[0-9a-f]+\.html)", p)]


def write(rel, data):
    p = os.path.join(ROOT, rel)
    old = open(p, "rb").read() if os.path.exists(p) else None
    if old == data:
        return False
    if not CHECK:
        os.makedirs(os.path.dirname(p) or ROOT, exist_ok=True)
        open(p, "wb").write(data)
    return True


def main():
    changed = []
    files = {
        "favicon.ico": ico([(s, png(render(s))) for s in (16, 32, 48)]),
        "assets/img/favicon.svg": SVG.encode("utf-8"),
        "assets/img/apple-touch-icon.png": png(render(180, pad=0.14, bg=BG)),
    }
    for rel, data in files.items():
        if write(rel, data):
            changed.append(rel)
        print("%-32s %6d bytes" % (rel, len(data)))

    pages = live_pages()
    linked = 0
    for rel in pages:
        p = os.path.join(ROOT, rel)
        s = io.open(p, encoding="utf-8", newline="").read()
        assert "\r" not in s, rel
        if LINKS in s:
            linked += 1
            continue
        assert 'rel="icon"' not in s and "apple-touch-icon" not in s, "%s has a different icon link" % rel
        assert s.count(VIEWPORT) == 1, "%s: expected one viewport meta" % rel
        s = s.replace(VIEWPORT, VIEWPORT + LINKS, 1)
        if write(rel, s.encode("utf-8")):
            changed.append(rel)
    print("%d live pages; already linked %d; %s %d" % (len(pages), linked, "would link" if CHECK else "linked",
                                                       len(pages) - linked))
    if CHECK:
        print("--check: %d files would change" % len(changed))


if __name__ == "__main__":
    main()
