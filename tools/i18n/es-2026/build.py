# -*- coding: utf-8 -*-
"""
Build the three Spanish pilot pages, patch their English originals with
hreflang + the language switcher, and fix two defects the seven late-published
articles shipped with.
"""

import io, os, sys, re, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common
from common import rep, lang_switch, hreflang_block, SITE

import a1_punto_de_reorden as A1
import a2_acos as A2
import a3_primer_producto as A3

SRC = "/mnt/user-data/uploads/amazebase-landing"
OUT = "/home/claude/esout"

PAIRS = [A1, A2, A3]

# The seven articles published from _drafts last session.
LATE = ["automate-cash-flow-inventory", "data-gaps-seep-everywhere",
        "fba-reorder-date-velocity", "first-product-succeeds-cash",
        "invented-numbers-amazon-analytics", "supplier-payment-schedules-margins",
        "true-product-margin-after-ads"]

RAILWAY = "https://amz-analytics-production.up.railway.app/login"
LOGIN   = "https://analytics.amazebase.pro/login"


def out_path(p):
    q = OUT + p
    d = os.path.dirname(q)
    if not os.path.isdir(d):
        os.makedirs(d)
    return q


def load(p):
    """Read from OUT if a previous pass already wrote it, else from SRC."""
    q = OUT + p
    return io.open(q if os.path.exists(q) else SRC + p, encoding="utf-8").read()


def save(p, s):
    io.open(out_path(p), "w", encoding="utf-8", newline="\n").write(s)


def balance(s):
    i = s.index('<div class="wrap">')
    j = s.index('</div><!-- /.wrap -->') + len("</div>")
    w = s[i:j]
    return (len(re.findall(r"<div\b", w)) - len(re.findall(r"</div>", w)),
            len(re.findall(r"<section\b", w)) - len(re.findall(r"</section>", w)))


# ============================================ FIX 1+2 on the seven late pages

for slug in LATE:
    p = "/articles/%s.html" % slug
    s = load(p)

    # (1) the login button still points at the Railway host
    s = rep(s, RAILWAY, LOGIN, n=2, label="railway login " + slug)

    # (2) <div class="shell"> and <section class="sec"> are never closed, so
    #     the footer renders inside an 820px grid track instead of full width.
    d, sec = balance(s)
    assert (d, sec) == (1, 1), "%s unexpected balance %s" % (slug, (d, sec))

    s = rep(s, "</aside>\n\n\n</div><!-- /.wrap -->",
               "</aside>\n\n</div><!-- /.shell -->\n\n</div><!-- /.wrap -->",
            label="close shell " + slug)

    # the trailing <section class="sec"> is the last one before </main>
    k = s.rindex('<section class="sec">')
    e = s.index("</main>", k)
    tail = s[k:e]
    assert "</section>" not in tail, "unexpected </section> in tail of " + slug
    s = s[:e].rstrip() + "\n    </section>\n\n  \n" + s[e:]

    d, sec = balance(s)
    assert (d, sec) == (0, 0), "%s still unbalanced %s" % (slug, (d, sec))
    save(p, s)
    print("fixed  ", p)


# ==================================================== Spanish mirrors

for m in PAIRS:
    src = OUT + m.EN_PATH if os.path.exists(OUT + m.EN_PATH) else SRC + m.EN_PATH
    common.build_es(src, out_path(m.ES_PATH), m.EN_PATH, m.ES_PATH, m.META, m.BODY)
    print("built  ", m.ES_PATH)


# ================================ English originals: hreflang + switcher

for m in PAIRS:
    s = load(m.EN_PATH)

    hl = hreflang_block(m.EN_PATH, m.ES_PATH)
    assert "hreflang=" not in s, "hreflang already present in " + m.EN_PATH
    if "<!-- SEO:START -->" in s:
        anchor = '<link rel="canonical" href="%s%s">' % (SITE, m.EN_PATH)
        s = rep(s, anchor, anchor + "\n" + hl, label="en canonical")
    else:
        anchor = '<link rel="stylesheet" href="/css/site-footer.css">'
        s = rep(s, anchor,
                anchor + '\n<link rel="canonical" href="%s%s">\n%s'
                % (SITE, m.EN_PATH, hl),
                label="en no-seo anchor")

    sw = lang_switch(m.EN_PATH, m.ES_PATH, "en")
    anchor = ('  <div class="nav-actions">\n'
              '    <a class="btn btn--quiet" href="%s">Log in</a>' % LOGIN)
    s = rep(s, anchor,
            '  <div class="nav-actions">\n'
            + "\n".join("    " + ln for ln in sw.split("\n")) + "\n"
            + '    <a class="btn btn--quiet" href="%s">Log in</a>' % LOGIN,
            label="en nav-actions")

    save(m.EN_PATH, s)
    print("patched", m.EN_PATH)


# ========================================================== postflight

for p in sorted(glob.glob(OUT + "/articles/*.html") + glob.glob(OUT + "/es/articulos/*.html")):
    s = io.open(p, encoding="utf-8").read()
    d, sec = balance(s)
    assert (d, sec) == (0, 0), "%s unbalanced %s" % (p, (d, sec))
    assert "railway.app" not in s, "railway link left in " + p
print("postflight OK -- %d files in %s" % (
    len(glob.glob(OUT + "/articles/*.html")) + len(glob.glob(OUT + "/es/articulos/*.html")), OUT))
