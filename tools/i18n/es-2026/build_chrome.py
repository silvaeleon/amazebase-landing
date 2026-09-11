# -*- coding: utf-8 -*-
"""
Round two: the four chrome pages in Spanish, plus the knock-on changes.

  1. /es/producto.html, /es/soluciones.html, /es/nosotros.html, /es/contacto.html
  2. hreflang + language switcher on the four English originals
  3. js/waitlist.js reads its user-facing strings from data-msg-* on the dialog,
     falling back to the current English, so the Spanish form can speak Spanish
  4. the three Spanish articles' nav now points at the Spanish chrome pages
  5. sitemap.xml gains the four new URLs
"""

import io, os, sys, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import chrome_common as C
from chrome_common import rep, lang_switch, hreflang_block, SITE

import p_producto, p_soluciones, p_nosotros, p_contacto

SRC = "/mnt/user-data/uploads/amazebase-landing"
OUT = "/home/claude/esout2"

PAGES = [p_producto, p_soluciones, p_nosotros, p_contacto]


def out_path(rel):
    p = os.path.join(OUT, rel.lstrip("/"))
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    return p


def load(rel):
    p = os.path.join(OUT, rel.lstrip("/"))
    return io.open(p if os.path.exists(p) else os.path.join(SRC, rel.lstrip("/")),
                   encoding="utf-8").read()


def save(rel, s):
    io.open(out_path(rel), "w", encoding="utf-8", newline="\n").write(s)


# ===================================================== 1. Spanish chrome pages

for m in PAGES:
    s, n = C.build(SRC + m.EN_PATH, out_path(m.ES_PATH),
                   m.EN_PATH, m.ES_PATH, m.META, m.MAIN)
    print("built   %-24s  %d relative refs made root-absolute" % (m.ES_PATH, n))


# ============================== 2. English originals: hreflang + lang switcher

for m in PAGES:
    s = load(m.EN_PATH)
    assert "hreflang=" not in s, "hreflang already in " + m.EN_PATH
    anchor = '<link rel="canonical" href="%s%s">' % (SITE, m.EN_PATH)
    s = rep(s, anchor, anchor + "\n" + hreflang_block(m.EN_PATH, m.ES_PATH),
            label="canonical " + m.EN_PATH)

    sw = lang_switch(m.EN_PATH, m.ES_PATH, "en")
    a = ('  <div class="nav-actions">\n'
         '    <a class="btn btn--quiet" href="https://analytics.amazebase.pro/login">Log in</a>')
    s = rep(s, a,
            '  <div class="nav-actions">\n'
            + "\n".join("    " + ln for ln in sw.split("\n")) + "\n"
            + '    <a class="btn btn--quiet" href="https://analytics.amazebase.pro/login">Log in</a>',
            label="nav-actions " + m.EN_PATH)
    save(m.EN_PATH, s)
    print("patched", m.EN_PATH)


# ================================================ 3. waitlist.js: data-msg-*

js = load("/js/waitlist.js")
assert "data-msg-" not in js

js = rep(js, '''  function showError(msg) {''',
'''  /* User-facing strings live on the dialog as data-msg-* so a translated page
     can carry its own, and pages without them keep the English below. */
  function t(key, fallback) {
    var v = dialog.getAttribute("data-msg-" + key);
    return v ? v : fallback;
  }
  var submitLabel = submit ? submit.textContent : "Join the wait list";

  function showError(msg) {''', label="t() helper")

for old, new in [
    ('return showError("Please tell us your name.");',
     'return showError(t("name", "Please tell us your name."));'),
    ('return showError("That email address doesn\'t look right.");',
     'return showError(t("email", "That email address doesn\'t look right."));'),
    ('return showError("Please choose your main marketplace.");',
     'return showError(t("market", "Please choose your main marketplace."));'),
    ('submit.textContent = "Joining…";',
     'submit.textContent = t("sending", "Joining…");'),
    ('throw new Error("Too many attempts just now. Please try again in a little while.");',
     'throw new Error(t("rate", "Too many attempts just now. Please try again in a little while."));'),
    ('function (b) { throw new Error(b && b.detail ? String(b.detail) : "Something went wrong."); },\n'
     '          function ()  { throw new Error("Something went wrong."); }',
     'function (b) { throw new Error(b && b.detail ? String(b.detail) : t("generic", "Something went wrong.")); },\n'
     '          function ()  { throw new Error(t("generic", "Something went wrong.")); }'),
    (': "We couldn\'t reach the server. Please try again.");',
     ': t("network", "We couldn\'t reach the server. Please try again."));'),
    ('submit.textContent = "Join the wait list";',
     'submit.textContent = submitLabel;'),
]:
    js = rep(js, old, new, label="waitlist string")

for k in ("name", "email", "market", "sending", "rate", "generic", "network"):
    assert 't("%s"' % k in js, "waitlist.js: %s not made overridable" % k
assert js.count('t("generic"') == 2
assert js.count('submit.textContent = submitLabel;') == 1
save("/js/waitlist.js", js)
print("patched /js/waitlist.js  (8 strings now overridable)")


# ================== 4. Spanish articles: nav now points at the Spanish pages

ART = ["/es/articulos/punto-de-reorden.html",
       "/es/articulos/deja-de-optimizar-el-acos.html",
       "/es/articulos/y-si-tu-primer-producto-funciona.html"]

NAVMAP = [("/product.html",   "/es/producto.html"),
          ("/solutions.html", "/es/soluciones.html"),
          ("/about.html",     "/es/nosotros.html"),
          ("/contact.html",   "/es/contacto.html")]

for rel in ART:
    s = load(rel)
    # In a Spanish article every reference to these four pages is chrome (nav
    # menu, mobile drawer, footer). The body links only to /index.html#waitlist
    # and /resources.html?lang=es, so a document-wide swap is safe -- and the
    # assertion below proves none survived.
    total = 0
    for en, es in NAVMAP:
        for suffix in ["#modules", "#advertising", "#financials", "#ledger",
                       "#inventory", "#research", "#simulations", "#sales",
                       "#data", "#security", "#assistant",
                       "#beginners", "#experts", "#agencies", ""]:
            old = 'href="%s%s"' % (en, suffix)
            n = s.count(old)
            if n:
                s = s.replace(old, 'href="%s%s"' % (es, suffix))
                total += n
    assert total >= 20, "%s: only %d links repointed" % (rel, total)
    for en, _ in NAVMAP:
        assert 'href="%s' % en not in s, "%s: %s survived" % (rel, en)
    save(rel, s)
    print("repointed %-52s %d links" % (rel, total))


# ===================================================== 5. sitemap

sm = load("/sitemap.xml")
NEW = [(m.ES_PATH.lstrip("/"), "2026-09-10") for m in PAGES]
for u, _ in NEW:
    assert u not in sm, u
block = "".join('  <url>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n  </url>\n'
                % (SITE, u, d) for u, d in NEW)
sm = rep(sm, "</urlset>", block + "</urlset>", label="sitemap")
locs = re.findall(r"<loc>(.*?)</loc>", sm)
assert len(locs) == 66 and len(set(locs)) == 66, len(locs)
save("/sitemap.xml", sm)
print("sitemap 62 -> %d urls" % len(locs))


# ===================================================== postflight

print("\n--- files ---")
for p in sorted(glob.glob(OUT + "/**/*", recursive=True)):
    if os.path.isfile(p):
        print("   ", p[len(OUT) + 1:], os.path.getsize(p))
