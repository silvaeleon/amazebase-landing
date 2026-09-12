# -*- coding: utf-8 -*-
"""
The homepage, the privacy policy and the terms of service, in every
translated language. Leon, 2026-09-11: "we need home page, pricing, privacy
and terms in all languages, portuguese and spanish for the moment. Pricing can
remain in usd." Pricing is the homepage's #pricing section.

    python tools/i18n/home_legal.py briefs <site-root> <out-dir>
    python tools/i18n/home_legal.py build  <site-root> <briefs-dir> [lang ...]
    python tools/i18n/home_legal.py verify <site-root> <briefs-dir>
    python tools/i18n/home_legal.py strict <brief.json> <translation.json>

The translations live in tools/i18n/home-legal/<lang>/<page>.json. The briefs
are regenerated from the English pages (build refuses if one is stale).

BRIEFS. Same shape as every other brief (gate.py checks them the same way),
with one difference: the homepage's <main> is 333 KB, 262 KB of it the
off-limits .abp block's embedded images. Nobody can copy that back reliably,
so before a translator sees it every data: URI, every <script> and <style>
body and every long SVG path is replaced by a placeholder @@T<n>@@; the
builder puts the originals back byte-for-byte and refuses a translation that
lost, duplicated or invented one. The homepage's brief shrinks to ~42 KB.

THE .abp AND .abc BLOCKS. Off-limits in index.html (blocks_guard.py proves it
untouched). The translated homepages carry COPIES with the text translated --
Leon's choice, 2026-09-11. Their one inline script is a placeholder, so it
comes back byte-identical and still hashes to the sha256 the Caddyfile's CSP
allows; blocks_guard.py checks that, and that each copy has the English
block's exact skeleton.

BUILD, per language and page, the English page edited in place (as
build_top_pt.py does), so stylesheets, sprites and layout stay identical:
  head    <html lang>, <title>, description, the SEO block (canonical, og:*,
          twitter:*, og:locale, JSON-LD breadcrumbs / software description)
  chrome  header, mobile nav, footer: a table DERIVED from that language's
          shipped product page (same tags as the English product page, so the
          text pairs up one-to-one -- the Portuguese derivation reproduces
          build_pt.CHROME_TEXT exactly, 29 of 29), plus STRINGS below for the
          few chrome strings the product page does not carry
  main    the gated translation, placeholders restored, then STRICT: every
          tag and every attribute identical to the English except the
          translatable ones (alt, title, aria-label, placeholder) -- the gate
          ignores most attributes, this does not
  dialog  the homepage's waitlist form: the one already shipped on that
          language's product page (the English forms are identical, asserted)
  note    privacy and terms: one line saying it is a translation and the
          English version governs (Leon, 2026-09-11), inserted after the gate
  links   switcher + alternates by langlinks.rewrite(); every link to an
          English page this language has by locallinks.localise()
"""

import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "pt-2026"))
import gate, langlinks, locallinks
import build_pt as BP

SITE = "https://amazebase.pro"
PAGES = {"home": "index.html", "privacy": "privacy.html", "terms": "terms.html"}
# where each page lives, per language (mirrored into languages.json "top")
LOCAL = {
    "es": {"home": "es/", "privacy": "es/privacidad.html", "terms": "es/terminos.html"},
    "pt": {"home": "pt/", "privacy": "pt/privacidade.html", "terms": "pt/termos.html"},
}
SLUG = {"es": {"home": "inicio", "privacy": "privacidad", "terms": "terminos"},
        "pt": {"home": "inicio", "privacy": "privacidade", "terms": "termos"}}
PRODUCT = {"es": "es/producto.html", "pt": "pt/produto.html"}
OG_LOCALE = {"es": "es_LA", "pt": "pt_BR"}
HOME_CRUMB = {"es": "Inicio", "pt": u"Início"}

# Chrome strings the shipped product pages do not carry, so the derived table
# cannot supply them. Terms has its own minimal header; every page has a
# skip link and the homepage a back-to-top control.
STRINGS = {
    "es": {"&larr; Back to site": "&larr; Volver al sitio",
           "Skip to content": "Saltar al contenido",
           "Back to top": "Volver arriba"},
    "pt": {"&larr; Back to site": "&larr; Voltar ao site",
           "Skip to content": "Pular para o conte&uacute;do",
           "Back to top": "Voltar ao topo"},
}
# The translation note (privacy, terms). The link names its language, so
# locallinks leaves it pointing at the English page, which is the point.
NOTE = {
    "es": ('<p class="translation-note"><em>Esta es una traducci&oacute;n. Si difiere de la '
           '<a href="/%s" hreflang="en" lang="en">versi&oacute;n en ingl&eacute;s</a>, '
           'prevalece la versi&oacute;n en ingl&eacute;s.</em></p>'),
    "pt": ('<p class="translation-note"><em>Esta &eacute; uma tradu&ccedil;&atilde;o. Se divergir da '
           '<a href="/%s" hreflang="en" lang="en">vers&atilde;o em ingl&ecirc;s</a>, '
           'prevalece a vers&atilde;o em ingl&ecirc;s.</em></p>'),
}
# where the note goes: right after the page's heading block
NOTE_AFTER = {"privacy": re.compile(r'<h1 class="legal-title">.*?</h1>\n', re.S),
              "terms": re.compile(r'<p class="page-lead">.*?</p>\n', re.S)}

# the gated translations, one JSON per language and page: the source a rebuild reads
CONTENT = os.path.join(HERE, "home-legal")

MAIN = re.compile(r'<main\b[^>]*\bid="main"[^>]*>.*?</main>', re.S)
TEXT_ATTRS = ("alt", "title", "aria-label", "placeholder")


# ------------------------------------------------------------------ tokens

def tokenise(frag):
    """(fragment with placeholders, [originals]). Order: <script> and <style>
    bodies whole, then data: URIs, then SVG path data of 120+ characters."""
    toks = []

    def keep(v):
        toks.append(v)
        return "@@T%d@@" % len(toks)
    frag = re.sub(r"(<script\b[^>]*>)(.*?)(</script>)", lambda m: m.group(1) + keep(m.group(2)) + m.group(3),
                  frag, flags=re.S)
    frag = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + keep(m.group(2)) + m.group(3),
                  frag, flags=re.S)
    frag = re.sub(r"data:[a-z]+/[^\"')\s]+", lambda m: keep(m.group(0)), frag)
    frag = re.sub(r'(\sd=")([^"]{120,})(")', lambda m: m.group(1) + keep(m.group(2)) + m.group(3), frag)
    return frag, toks


def restore(frag, toks):
    found = [int(n) for n in re.findall(r"@@T(\d+)@@", frag)]
    assert sorted(found) == list(range(1, len(toks) + 1)), \
        "placeholders lost, duplicated or invented: %d expected, got %s" % (len(toks), sorted(found)[:12])
    return re.sub(r"@@T(\d+)@@", lambda m: toks[int(m.group(1)) - 1], frag)


def strict(frag):
    """Every tag with every attribute, translatable attribute VALUES blanked.

    Whitespace INSIDE a tag is collapsed: where a long tag's attributes wrap is
    formatting, not structure, and a page hand-edited after it was built can
    wrap them differently from its source (found 2026-09-11 on the privacy
    pages' Google opt-out link)."""
    out = []
    for t in re.findall(r"<[^>]+>", re.sub(r"<!--.*?-->", "", frag, flags=re.S)):
        for a in TEXT_ATTRS:
            t = re.sub(r'(\s%s=")[^"]*(")' % a, r"\1\2", t)
        out.append(re.sub(r"\s+", " ", t))
    return out


# ------------------------------------------------------------------ briefs

def one(pat, s, flags=0):
    m = re.search(pat, s, flags)
    return m.group(1) if m else None


def ld_graph(s):
    m = re.search(r'<!-- SEO:START -->.*?<script type="application/ld\+json">(.*?)</script>', s, re.S)
    return json.loads(m.group(1))["@graph"]


def brief(tree, key):
    s = io.open(os.path.join(tree, PAGES[key]), encoding="utf-8", newline="").read()
    main = MAIN.search(s).group(0)
    tmain, toks = tokenise(main)
    g = ld_graph(s)
    crumbs = [n for n in g if n.get("@type") == "BreadcrumbList"]
    items = crumbs[0]["itemListElement"] if crumbs else []
    soft = [n for n in g if n.get("@type") == "SoftwareApplication"]
    b = {
        "slug": key,
        "page": PAGES[key],
        "title": one(r"<title>(.*?)</title>", s, re.S),
        "desc": one(r'<meta name="description" content="([^"]*)"', s),
        "og_title": one(r'<meta property="og:title" content="([^"]*)"', s),
        "og_desc": one(r'<meta property="og:description" content="([^"]*)"', s),
        "og_img_alt": one(r'<meta property="og:image:alt" content="([^"]*)"', s),
        "crumb": items[-1]["name"] if len(items) > 1 else None,
        "features": soft[0]["featureList"] if soft else None,
        "ld_headline": None, "ld_desc": None, "keywords": [],
        "hero_alt": None, "article_head": None, "rail": None, "cta": None,
        "main": tmain,
        "placeholders": len(toks),
        "words": len(html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"@@T\d+@@", " ", tmain))).split()),
    }
    return b, toks


def write_briefs(tree, out):
    os.makedirs(out, exist_ok=True)
    for key in PAGES:
        b, toks = brief(tree, key)
        io.open(os.path.join(out, key + ".json"), "w", encoding="utf-8", newline="\n").write(
            json.dumps(b, ensure_ascii=False, indent=1))
        print("%-8s main %6d bytes (%d placeholders), %4d words, crumb %r, features %s"
              % (key, len(b["main"]), len(toks), b["words"], b["crumb"],
                 len(b["features"]) if b["features"] else None))


# ------------------------------------------------------------------ chrome

REGIONS = (("header", '<header class="site-header">', "</header>"),
           ("nav-mobile", '<div class="nav-mobile" id="navMobile">', "</div>"),
           ("footer", '<footer class="footer">', "</footer>"))
SWITCH = re.compile(r'\n[ \t]*<div class="nav-item lang-switch">.*?</div>\n[ \t]*</div>', re.S)


def region(s, start, end):
    i = s.find(start)
    if i < 0:
        return None
    return i, s.index(end, i) + len(end)


def texts(seg):
    return [t.strip() for t in re.findall(r">([^<]+)<", seg) if t.strip()]


def chrome_table(tree, lang):
    """English chrome string -> this language's, DERIVED from the shipped
    product pages: same tags in the same order, so the text pairs up. Refuses
    a pairing that is ambiguous (one English string, two translations)."""
    read = lambda rel: BP.rootify(io.open(os.path.join(tree, rel), encoding="utf-8", newline="").read())
    en, tr = read("product.html"), read(PRODUCT[lang])
    tmap, amap = {}, {}
    for name, a, b in REGIONS:
        ra, rb = region(en, a, b), region(tr, a, b)
        sa, sb = SWITCH.sub("", en[ra[0]:ra[1]]), SWITCH.sub("", tr[rb[0]:rb[1]])
        xa, xb = texts(sa), texts(sb)
        assert len(xa) == len(xb), "%s %s: %d English texts, %d translated" % (lang, name, len(xa), len(xb))
        for x, y in zip(xa, xb):
            assert tmap.setdefault(x, y) == y, "%s: %r is both %r and %r" % (lang, x, tmap[x], y)
        la = re.findall(r'aria-label="([^"]*)"', sa)
        lb = re.findall(r'aria-label="([^"]*)"', sb)
        assert len(la) == len(lb), "%s %s aria-labels" % (lang, name)
        for x, y in zip(la, lb):
            assert amap.setdefault(x, y) == y, "%s: aria %r is both %r and %r" % (lang, x, amap[x], y)
    for x, y in STRINGS[lang].items():
        tmap.setdefault(x, y)
    return tmap, amap


def translate_chrome(seg, tmap, amap, label):
    seg = re.sub(r'aria-label="([^"]*)"', lambda m: 'aria-label="%s"' % amap.get(m.group(1), m.group(1)), seg)

    def text(m):
        raw = m.group(1)
        core = raw.strip()
        return ">" + raw.replace(core, tmap[core]) + "<" if core in tmap else m.group(0)
    seg = re.sub(r">([^<]+)<", text, seg)
    # the set check: every text node and aria-label is now translated or the same in every language
    ok = set(tmap.values()) | set(amap.values()) | {"English", u"Español", u"Português", "EN", "ES", "PT",
                                                    "Idioma / Language"}   # the switcher: one label, every language
    left = [t for t in texts(seg) if t not in ok]
    aria = [a for a in re.findall(r'aria-label="([^"]*)"', seg) if a not in ok]
    assert not left and not aria, "%s: untranslated chrome %s %s" % (label, left, aria)
    return seg


# ------------------------------------------------------------------- build

def sub1(pat, new, s, label, flags=0):
    s2, n = re.subn(pat, lambda m: new, s, count=1, flags=flags)
    assert n == 1, label
    return s2


def urls_of(lang, key, cfg):
    en = next(l for l in cfg["languages"] if l["code"] == "en")["top"][key]
    loc = next(l for l in cfg["languages"] if l["code"] == lang)["top"][key]
    assert loc == LOCAL[lang][key], "languages.json and LOCAL disagree on %s/%s" % (lang, key)
    return "%s/%s" % (SITE, en), "%s/%s" % (SITE, loc)


def build(tree, lang, key, b, toks, tr, cfg, tables, dialog):
    tmap, amap = tables
    en_url, loc_url = urls_of(lang, key, cfg)
    s = io.open(os.path.join(tree, PAGES[key]), encoding="utf-8", newline="").read()
    assert "\r" not in s
    en_main = MAIN.search(s).group(0)
    s = BP.rootify(s)

    # ---- head
    s = BP.rep(s, '<html lang="en">', '<html lang="%s">' % lang, label="html lang")
    s = sub1(r"<title>.*?</title>", "<title>%s</title>" % tr["title"], s, "title", re.S)
    s = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % tr["desc"],
             s, "desc")
    s = BP.rep(s, '<link rel="canonical" href="%s">' % en_url, '<link rel="canonical" href="%s">' % loc_url,
               label="canonical")
    s = BP.rep(s, '<meta property="og:locale" content="en_US">',
               '<meta property="og:locale" content="%s">\n<meta property="og:locale:alternate" content="en_US">'
               % OG_LOCALE[lang], label="og:locale")
    s = BP.rep(s, '<meta property="og:url" content="%s">' % en_url, '<meta property="og:url" content="%s">' % loc_url,
               label="og:url")
    for attr, k in (('property="og:title"', "og_title"), ('property="og:description"', "og_desc"),
                    ('name="twitter:title"', "og_title"), ('name="twitter:description"', "og_desc"),
                    ('property="og:image:alt"', "og_img_alt"), ('name="twitter:image:alt"', "og_img_alt")):
        s = sub1(r'<meta %s content="[^"]*">' % re.escape(attr), '<meta %s content="%s">' % (attr, tr[k]), s, attr)

    m = re.search(r'(<!-- SEO:START -->.*?<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    graph = json.loads(m.group(2))
    home_url = "%s/%s" % (SITE, LOCAL[lang]["home"])
    for n in graph["@graph"]:
        if n.get("@type") == "BreadcrumbList":
            items = n["itemListElement"]
            assert items[0]["name"] == "Home"
            items[0]["name"] = HOME_CRUMB[lang]
            items[0]["item"] = home_url
            if len(items) > 1:
                items[-1]["name"] = tr["crumb"]
        if n.get("@type") == "SoftwareApplication":
            n["@id"] = loc_url + "#software"
            n["url"] = loc_url
            n["description"] = html.unescape(tr["desc"])
            n["featureList"] = tr["features"]
            n["inLanguage"] = lang
    s = s[:m.start(2)] + "\n" + json.dumps(graph, indent=2, ensure_ascii=False) + "\n" + s[m.end(2):]

    # ---- chrome
    for en_t, loc_t in (("Skip to content", STRINGS[lang]["Skip to content"]),):
        s = BP.rep(s, ">%s</a>" % en_t, ">%s</a>" % loc_t, label="skip link")
    if 'aria-label="Back to top"' in s:
        s = BP.rep(s, 'aria-label="Back to top"', 'aria-label="%s"' % STRINGS[lang]["Back to top"], label="to-top")
    for name, a_, b_ in REGIONS:
        r = region(s, a_, b_)
        if r:
            s = s[:r[0]] + translate_chrome(s[r[0]:r[1]], tmap, amap, "%s %s %s" % (lang, key, name)) + s[r[1]:]

    # ---- main: the gated translation, placeholders back, then STRICT
    main = restore(tr["main"], toks)
    a, c = strict(en_main), strict(main)
    assert a == c, "%s/%s: main differs from English beyond text (run the strict command)" % (lang, key)
    main = BP.rootify(main)
    if key in NOTE_AFTER:
        mm = NOTE_AFTER[key].search(main)
        assert mm, "%s/%s: note anchor not found" % (lang, key)
        main = main[:mm.end()] + "  " + NOTE[lang] % PAGES[key] + "\n" + main[mm.end():]
    r = MAIN.search(s)
    s = s[:r.start()] + main + s[r.end():]

    # ---- the homepage's waitlist form: the one shipped on this language's product page
    r = region(s, '<dialog class="wl" id="waitlist"', "</dialog>")
    if r:
        s = s[:r[0]] + dialog + s[r[1]:]

    # ---- links
    g = langlinks.groups(cfg, {}, [])
    members = g[langlinks.file_of(LOCAL[lang][key])]
    s = langlinks.rewrite(s, cfg, members, lang)
    s, _ = locallinks.localise(s, cfg, lang)

    out = os.path.join(tree, langlinks.file_of(LOCAL[lang][key]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="").write(s)
    return out


def local_dialog(tree, lang):
    """The waitlist dialog shipped on this language's product page -- after
    asserting the English homepage's and product page's are identical."""
    rd = lambda rel: BP.rootify(io.open(os.path.join(tree, rel), encoding="utf-8", newline="").read())
    grab = lambda s: s[slice(*region(s, '<dialog class="wl" id="waitlist"', "</dialog>"))]
    assert grab(rd("index.html")) == grab(rd("product.html")), "the English waitlist forms differ"
    d = grab(rd(PRODUCT[lang]))
    for keep in ('name="company_website"', 'name="referral_code"', "data-waitlist-submit", 'name="marketplace"'):
        assert keep in d, "%s dialog lost %s" % (lang, keep)
    return d


def build_all(tree, briefs, langs):
    cfg, _ = langlinks.load()
    content = CONTENT
    built = []
    for lang in langs:
        tables = chrome_table(tree, lang)
        dialog = local_dialog(tree, lang)
        for key in PAGES:
            b, toks = brief(tree, key)
            saved = json.load(io.open(os.path.join(briefs, key + ".json"), encoding="utf-8"))
            assert saved["main"] == b["main"], "%s: the English page changed since its brief was written" % key
            tr = json.load(io.open(os.path.join(content, lang, key + ".json"), encoding="utf-8"))
            n, prob = gate.audit(b, tr, lang)
            prob += strict_problems(b, tr)
            assert not prob, "%s/%s refused:\n  %s" % (lang, key, "\n  ".join(prob))
            out = build(tree, lang, key, b, toks, tr, cfg, tables, dialog)
            built.append(out)
            print("built  %s/%-8s -> /%-22s gate %d elements, strict %d tags"
                  % (lang, key, os.path.relpath(out, tree).replace(os.sep, "/"), n, len(strict(b["main"]))))
    return built


# ------------------------------------------------------------------ verify

def verify(tree, briefs, langs=None):
    """Whole document, every built page. NOT read: <style> bodies and HTML
    comments (never rendered). <script> bodies are excluded from the English
    scan only; JSON-LD is parsed and checked field by field."""
    sys.path.insert(0, os.path.join(HERE, "pt-2026"))
    import verify_pt as VP
    cfg, _ = langlinks.load()
    content = CONTENT
    bad = 0
    print("verify: whole document. NOT read: <style> bodies, HTML comments; <script> excluded "
          "from the English scan only (JSON-LD checked field by field).\n")
    for lang in langs or list(LOCAL):
        tmap, amap = chrome_table(tree, lang)
        back = locallinks.back_map(cfg, lang)
        for key in PAGES:
            P, facts = [], []
            rel = langlinks.file_of(LOCAL[lang][key])
            en_url, loc_url = urls_of(lang, key, cfg)
            raw = io.open(os.path.join(tree, rel), "rb").read()
            s = raw.decode("utf-8")
            en = io.open(os.path.join(tree, PAGES[key]), encoding="utf-8", newline="").read()
            tr = json.load(io.open(os.path.join(content, lang, key + ".json"), encoding="utf-8"))
            if b"\r" in raw or b"\xef\xbf\xbd" in raw:
                P.append("CR or U+FFFD bytes")
            bal = VP.Balance()
            bal.feed(s)
            bal.close()
            if bal.errors or bal.stack:
                P.append("unbalanced: %s %s" % (bal.errors[:3], [t for t, _ in bal.stack][:4]))

            one = lambda pat: re.findall(pat, s)
            for pat, want in ((r'<html lang="([^"]*)"', [lang]),
                              (r'<link rel="canonical" href="([^"]*)"', [loc_url]),
                              (r'<meta property="og:url" content="([^"]*)"', [loc_url]),
                              (r'<meta property="og:locale" content="([^"]*)"', [OG_LOCALE[lang]]),
                              (r'<meta property="og:title" content="([^"]*)"', [tr["og_title"]]),
                              (r'<meta name="description" content="([^"]*)"', [tr["desc"]]),
                              (r"<title>(.*?)</title>", [tr["title"]]),
                              (r'<meta name="robots" content="([^"]*)"',
                               re.findall(r'<meta name="robots" content="([^"]*)"', en))):
                if one(pat) != want:
                    P.append("%s -> %s, want %s" % (pat[:36], one(pat)[:2], want))
            alts = one(r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)"')
            want_alts = [(c, "%s/%s" % (SITE, next(l for l in cfg["languages"] if l["code"] == c)["top"][key]))
                         for c in ("en", "es", "pt")] + [("x-default", en_url)]
            if alts != want_alts:
                P.append("alternates %s" % alts)
            facts.append("head: lang %s, canonical %s, og:locale %s, alternates %s"
                         % (lang, loc_url.replace(SITE, ""), OG_LOCALE[lang], " ".join(h for h, _ in alts)))

            m = re.search(r'<!-- SEO:START -->.*?<script type="application/ld\+json">(.*?)</script>', s, re.S)
            g = json.loads(m.group(1))["@graph"]
            crumbs = [(i["name"], i.get("item")) for n in g if n.get("@type") == "BreadcrumbList"
                      for i in n["itemListElement"]]
            want_c = [(HOME_CRUMB[lang], "%s/%s" % (SITE, LOCAL[lang]["home"]))] + \
                     ([(tr["crumb"], None)] if tr.get("crumb") else [])
            if crumbs and crumbs != want_c:
                P.append("breadcrumbs %s" % crumbs)
            soft = [n for n in g if n.get("@type") == "SoftwareApplication"]
            if soft and (soft[0].get("inLanguage") != lang or soft[0].get("featureList") != tr["features"]
                         or soft[0].get("url") != loc_url):
                P.append("SoftwareApplication not localised")
            facts.append("JSON-LD parses; breadcrumbs %s%s" % (" > ".join(c for c, _ in crumbs) or "none",
                         "; SoftwareApplication %s, %d features" % (lang, len(soft[0]["featureList"])) if soft else ""))

            # English left anywhere rendered
            visible = re.sub(r"<style\b.*?</style>|<!--.*?-->|<script\b.*?</script>", " ", s, flags=re.S)
            visible = langlinks.MENU_RUN.sub(lambda m_: m_.group(1) + m_.group(3), visible)
            left = [k for k, v in tmap.items() if k != v and re.search(r">\s*%s\s*<" % re.escape(k), visible)]
            left += ["aria " + k for k, v in amap.items() if k != v and 'aria-label="%s"' % k in visible]
            for phrase in ("Skip to content", "Back to top", "Join the wait list", "Join the Wait List"):
                if phrase in visible:
                    left.append(phrase)
            if left:
                P.append("English left: %s" % left)
            text = " " + re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", visible))) + " "
            hits = [w for w in gate.STOP_EN if w in text]
            if hits:
                P.append("English stopwords in the page: %s" % hits)

            # the body against English: every tag and attribute but the text ones, links mapped back
            def body(x, mapped):
                x = re.sub(r"<!--.*?-->", "", x, flags=re.S)
                x = x[re.search(r"<body[\s>]", x).start():]
                x = langlinks.MENU_RUN.sub(lambda m_: m_.group(1) + m_.group(3), x)
                x = BP.rootify(x)
                x = re.sub(r'<p class="translation-note">.*?</p>\n?', "", x, flags=re.S)
                x = re.sub(r"(<dialog class=\"wl\" id=\"waitlist\").*?</dialog>", r"\1></dialog>", x, flags=re.S)
                if mapped:
                    def hb(mm):
                        h = mm.group(1)
                        base, sep, frag = h.partition("#")
                        return 'href="%s%s%s"' % (back.get(base, base), sep, frag)
                    x = re.sub(r'href="([^"]*)"', hb, x)
                else:
                    x = re.sub(r'href="/"', 'href="/index.html"', x)
                return strict(x)
            ka, kb = body(en, False), body(s, True)
            if ka != kb:
                i = next((k for k in range(min(len(ka), len(kb))) if ka[k] != kb[k]), min(len(ka), len(kb)))
                P.append("body differs from English at tag %d: EN %.120s / %s %.120s"
                         % (i + 1, ka[i] if i < len(ka) else None, lang.upper(), kb[i] if i < len(kb) else None))
            else:
                facts.append("body: %d tags, every tag and attribute identical to English (text attributes aside)"
                             % len(ka))

            # URLs: none relative, every root-relative one on disk, fragments real
            live = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
            relu = [u for _, u in VP.urls(live) if not re.match(r"^(/|#|[a-z]+:)", u)]
            miss = []
            for _, u in VP.urls(live):
                if not u.startswith("/"):
                    continue
                base, _, frag = u.partition("#")
                f = os.path.join(tree, langlinks.file_of(base.lstrip("/")) if not os.path.splitext(base)[1]
                                 else base.lstrip("/"))
                if not os.path.isfile(f):
                    miss.append(u)
                elif frag and 'id="%s"' % frag not in io.open(f, encoding="utf-8").read():
                    miss.append(u)
            if relu or miss:
                P.append("relative URLs %s; unresolved %s" % (relu[:4], sorted(set(miss))[:6]))
            facts.append("URLs: none relative, every link and #fragment resolves")

            scripts = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>", s)
            if len(scripts) != (1 if key == "home" else 0):
                P.append("%d inline scripts" % len(scripts))
            if key == "home":
                d = s[slice(*region(s, '<dialog class="wl" id="waitlist"', "</dialog>"))]
                msgs = re.findall(r'\bdata-msg-(\w+)="', d[:d.index(">")])
                if msgs != ["name", "email", "market", "sending", "rate", "generic", "network"] or \
                        'name="company_website"' not in d or 'name="referral_code"' not in d:
                    P.append("waitlist dialog damaged")
                facts.append("waitlist form: 7 data-msg-* strings, honeypots intact")
            if key in NOTE_AFTER:
                note = NOTE[lang] % PAGES[key]
                if s.count(note) != 1:
                    P.append("translation note missing")
                facts.append("translation note present; its link -> /%s (hreflang=en)" % PAGES[key])

            bad += len(P)
            print("%-4s /%s" % ("OK" if not P else "FAIL", rel))
            for f in facts:
                print("       " + f)
            for p in P:
                print("   !!  " + p)
    print("\n%d problems" % bad)
    return bad


def strict_problems(b, tr):
    """What the builder refuses beyond the gate: placeholders, and any tag or
    attribute (other than the translatable ones) that differs from English."""
    prob = []
    n = b.get("placeholders", 0)
    found = sorted(int(x) for x in re.findall(r"@@T(\d+)@@", tr.get("main") or ""))
    if found != list(range(1, n + 1)):
        miss = sorted(set(range(1, n + 1)) - set(found))
        extra = sorted(set(found) - set(range(1, n + 1)))
        dup = sorted(set(x for x in found if found.count(x) > 1))
        prob.append("placeholders: %d expected; missing %s, invented %s, repeated %s" % (n, miss, extra, dup))
    a, c = strict(b["main"]), strict(tr.get("main") or "")
    if a != c:
        i = next((k for k in range(min(len(a), len(c))) if a[k] != c[k]), min(len(a), len(c)))
        prob.append("tag %d of %d differs:\n  EN %s\n  TR %s" % (
            i + 1, len(a), a[i][:160] if i < len(a) else None, c[i][:160] if i < len(c) else None))
    if bool(b.get("features")) != bool(tr.get("features")) or \
            (b.get("features") and len(b["features"]) != len(tr["features"])):
        prob.append("features: English has %s, translation %s" % (
            len(b["features"] or []), len(tr.get("features") or [])))
    for f in tr.get("features") or []:
        if gate.ENTITY.search(f):
            prob.append("HTML entity in a features item (JSON-LD is plain text): %r" % f)
    return prob


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "briefs":
        write_briefs(a[0], a[1])
    elif cmd == "build":
        build_all(a[0], a[1], a[2:] or list(LOCAL))
    elif cmd == "verify":
        raise SystemExit(1 if verify(a[0], a[1], a[2:] or None) else 0)
    elif cmd == "tables":
        for lang in a[1:] or list(LOCAL):
            t, ar = chrome_table(a[0], lang)
            print("%s: %d text pairs, %d aria pairs" % (lang, len(t), len(ar)))
            if lang == "pt":
                dis = dict((k, v) for k, v in t.items() if k in BP.CHROME_TEXT and v != BP.CHROME_TEXT[k])
                print("   vs build_pt.CHROME_TEXT: %d shared keys, %d disagree %s"
                      % (len([k for k in t if k in BP.CHROME_TEXT]), len(dis), dis))
    elif cmd == "strict":
        b = json.load(io.open(a[0], encoding="utf-8"))
        tr = json.load(io.open(a[1], encoding="utf-8"))
        prob = strict_problems(b, tr)
        for p in prob:
            print(p)
        print("\nSTRICT: %d problems (%d tags compared)" % (len(prob), len(strict(b["main"]))))
        raise SystemExit(1 if prob else 0)
    else:
        raise SystemExit("unknown command %r" % cmd)
