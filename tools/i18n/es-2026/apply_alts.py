# -*- coding: utf-8 -*-
"""
Apply the rewritten decorative alt text, both languages.

Scope, as decided: hero images and the two marketing figures. Product
screenshots and data figures (sol-*, product-*, about-*) keep their long
descriptions -- a screen-reader user cannot see the numbers in those, so length
is correct there. This touches 92 of the site's 155 non-empty alts.

Each page carries the same string in up to three places: the hero <img alt>,
og:image:alt and twitter:image:alt. All three move together.
"""

import io, os, re, json, glob, html

AUDIT = "/home/claude/audit"          # a copy of the current repo state
OUT = "/home/claude/altfix"
SMAP = json.load(io.open("/home/claude/briefs/_slugmap.json", encoding="utf-8"))

# the two non-article decorative images, written here rather than farmed out
EXTRA = {
    "/resources.html": ("hub-hero-land",
        "Advertising, inventory, cash and margin connected in one view for an Amazon seller"),
    "/es/recursos.html": ("hub-hero-land",
        "Publicidad, inventario, efectivo y margen conectados en una sola vista "
        "para vendedores de Amazon"),
    "/contact.html": ("contact-message-loop",
        "Seller messages arriving, read, and turning into changes in the product"),
    "/es/contacto.html": ("contact-message-loop",
        "Mensajes de vendedores que llegan, se leen y se vuelven cambios en el producto"),
}


def out_path(rel):
    p = os.path.join(OUT, rel.lstrip("/"))
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    return p


def esc(t):
    """Accents to entities, matching how the rest of these files are written."""
    return "".join("&%s;" % {
        "á": "aacute", "é": "eacute", "í": "iacute", "ó": "oacute", "ú": "uacute",
        "ñ": "ntilde", "Á": "Aacute", "É": "Eacute", "Í": "Iacute", "Ó": "Oacute",
        "Ú": "Uacute", "Ñ": "Ntilde", "ü": "uuml", "¿": "iquest", "¡": "iexcl",
    }[c] if c in "áéíóúñÁÉÍÓÚÑü¿¡" else c for c in t)


def patch(rel, img_stem, new_alt):
    """Replace the alt on <img src=...img_stem...> and on the og/twitter pair."""
    src = os.path.join(AUDIT, rel.lstrip("/"))
    cur = out_path(rel)
    s = io.open(cur if os.path.exists(cur) else src, encoding="utf-8").read()
    n = 0

    def img_sub(m):
        nonlocal n
        n += 1
        return m.group(1) + new_alt + m.group(3)

    # the <img> whose src contains this stem, in either attribute order
    pat = (r'(<img\b[^>]*?src="[^"]*%s[^"]*"[^>]*?\balt=")([^"]*)(")' % re.escape(img_stem))
    s, k = re.subn(pat, img_sub, s)
    if not k:
        pat = (r'(<img\b[^>]*?\balt=")([^"]*)("[^>]*?src="[^"]*%s[^"]*")' % re.escape(img_stem))
        s, k = re.subn(pat, lambda m: m.group(1) + new_alt + m.group(3), s)
        n += k
    assert k, "%s: no <img> matching %s" % (rel, img_stem)

    # the social-card alts describe the same artwork
    s, k = re.subn(r'(<meta (?:property="og:image:alt"|name="twitter:image:alt") content=")[^"]*(")',
                   lambda m: m.group(1) + new_alt + m.group(2), s)
    n += k

    io.open(out_path(rel), "w", encoding="utf-8", newline="\n").write(s)
    return n


if __name__ == "__main__":
    total = pages = 0

    for f in sorted(glob.glob("/home/claude/altout/*.json")):
        d = json.load(io.open(f, encoding="utf-8"))
        en_slug = d["en_slug"]
        es_slug = SMAP[en_slug]
        stem = "hero-%s." % en_slug          # the image keeps its English filename

        k = patch("/articles/%s.html" % en_slug, stem, d["en_alt"])
        total += k; pages += 1
        k = patch("/es/articulos/%s.html" % es_slug, stem, esc(d["es_alt"]))
        total += k; pages += 1

    for rel, (stem, alt) in EXTRA.items():
        total += patch(rel, stem, esc(alt) if "/es/" in rel else alt)
        pages += 1

    print("%d alt strings rewritten across %d pages" % (total, pages))

    # ---- postflight
    bad = []
    for p in sorted(glob.glob(OUT + "/**/*.html", recursive=True)):
        rel = p[len(OUT):]
        s = io.open(p, encoding="utf-8").read()
        for m in re.finditer(r'<img\b[^>]*?src="[^"]*/(hero-[^"/]+|hub-hero-land[^"/]*|contact-message-loop[^"/]*)"[^>]*?>', s):
            tag = m.group(0)
            a = re.search(r'\balt="([^"]*)"', tag)
            if not a:
                continue
            w = len(html.unescape(a.group(1)).split())
            if not (8 <= w <= 15):
                bad.append((rel, "%d words: %s" % (w, a.group(1)[:60])))
        # Raw accents are fine in HTML comments and required inside JSON-LD.
        # The convention that matters is attribute VALUES, which use entities.
        if "/es/" in rel:
            for m in re.finditer(r'\b(alt|content)="([^"]*)"', s[:s.index("</head>")]):
                # Em dashes and angle quotes are raw on the English pages too
                # and render fine in UTF-8. The entity convention is about
                # ACCENTED LETTERS, so only flag those.
                if re.search(u"[\u00c0-\u024f\u00bf\u00a1]", m.group(2)):
                    bad.append((rel, "raw accent in %s=%r" % (m.group(1), m.group(2)[:50])))
    assert not bad, bad
    print("postflight clean: every decorative alt is 8-15 words")
