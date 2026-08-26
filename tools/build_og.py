#!/usr/bin/env python3
"""
Build 1200x630 Open Graph share images into assets/img/og/.

No type is set into the image on purpose: every social platform renders the
og:title next to the card, and the site's brand face (Inter) is loaded from
Google Fonts rather than shipped, so baking text here would mean setting it
in whatever substitute the build machine happens to have. Artwork only.

  - articles      hero-<slug>.webp (1672x941) -> cover-cropped
  - top-level     the page's own artwork, cover-cropped when its aspect is
                  near 1.91:1, otherwise contained on a branded field

Re-runnable: overwrites whatever is already there.
    python3 tools/build_og.py
"""
import json, os, glob
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, "assets", "img")
OUT  = os.path.join(IMG, "og")
W, H = 1200, 630
TARGET = W / H                      # 1.905
BG = (3, 9, 23)                     # #030917, the site's theme-color

# page -> source artwork (None = branded field only)
PAGES = {
    "home":      "dashboard.jpg",
    "about":     "about-hero.webp",
    "product":   "product-ppc-verdict.webp",
    "solutions": "sol-reporting.webp",
    "resources": "hub-hero-land.jpg",
    "contact":   "contact-message-loop.webp",
    # legal pages get the product shot rather than an anonymous gradient
    "privacy":   "dashboard.jpg",
    "terms":     "dashboard.jpg",
}


def field():
    """The branded background: near-black with the site's four corner glows."""
    base = Image.new("RGB", (W, H), BG)
    glows = [
        ("glow-2-top-magenta.webp",       (0.50, 0.00), 0.95),
        ("glow-1-left-blue.webp",         (0.02, 0.35), 0.80),
        ("glow-3-right-violet.webp",      (0.98, 0.30), 0.80),
        ("glow-4-bottomright-purple.webp",(0.85, 0.95), 0.85),
    ]
    for name, (ax, ay), scale in glows:
        p = os.path.join(IMG, name)
        if not os.path.exists(p):
            continue
        g = Image.open(p).convert("RGBA")
        gw = int(W * scale)
        g = g.resize((gw, max(1, int(g.height * gw / g.width))), Image.LANCZOS)
        x = int(ax * W - g.width / 2)
        y = int(ay * H - g.height / 2)
        base.paste(g, (x, y), g)
    return base


def cover(im):
    """Fill the frame, cropping the long axis. Bias slightly above centre so
    a subject sitting in the upper half survives the crop."""
    a = im.width / im.height
    if a > TARGET:                       # too wide -> crop the sides
        nh = im.height
        nw = int(nh * TARGET)
        x = (im.width - nw) // 2
        im = im.crop((x, 0, x + nw, nh))
    else:                                # too tall -> crop top/bottom
        nw = im.width
        nh = int(nw / TARGET)
        y = int((im.height - nh) * 0.42)
        im = im.crop((0, y, nw, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def contain(im, pad=0.90):
    """Sit the artwork whole on the branded field, with a soft shadow so the
    letterboxing reads as a deliberate frame rather than a fit failure."""
    canvas = field()
    box_w, box_h = int(W * pad), int(H * pad)
    r = min(box_w / im.width, box_h / im.height)
    nw, nh = max(1, int(im.width * r)), max(1, int(im.height * r))
    art = im.resize((nw, nh), Image.LANCZOS)
    x, y = (W - nw) // 2, (H - nh) // 2

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 170), (x, y + 10, x + nw, y + nh + 10))
    canvas.paste(Image.alpha_composite(
        canvas.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(22))).convert("RGB"), (0, 0))
    canvas.paste(art, (x, y))
    return canvas


def build(src, dst):
    if src is None:
        img = field()
    else:
        p = os.path.join(IMG, src)
        if not os.path.exists(p):
            print("  ! missing source", src)
            return False
        im = Image.open(p).convert("RGB")
        a = im.width / im.height
        img = cover(im) if abs(a - TARGET) <= 0.45 else contain(im)
    img.save(dst, "JPEG", quality=84, optimize=True, progressive=True)
    return True


def main():
    os.makedirs(OUT, exist_ok=True)
    made = 0

    for name, src in PAGES.items():
        if build(src, os.path.join(OUT, "og-%s.jpg" % name)):
            made += 1

    with open(os.path.join(ROOT, "data", "resources.json"), encoding="utf-8") as f:
        resources = json.load(f)["resources"]

    for r in resources:
        slug = r["url"].rsplit("/", 1)[-1].replace(".html", "")
        hero = r.get("hero") or ("assets/img/hero-%s.webp" % slug)
        src = hero.split("assets/img/")[-1]
        if build(src, os.path.join(OUT, "og-%s.jpg" % slug)):
            made += 1

    sizes = [os.path.getsize(p) for p in glob.glob(os.path.join(OUT, "*.jpg"))]
    print("built %d images, %d on disk, largest %.0f KB, total %.1f MB"
          % (made, len(sizes), max(sizes) / 1024, sum(sizes) / 1024 / 1024))


if __name__ == "__main__":
    main()
