# -*- coding: utf-8 -*-
"""
Give the Spanish and Portuguese twins of an English article the SEO block that
tools/seo.py wrote for the English -- localised, never copied.

    python tools/i18n/seo_twins.py <site-root> <en-slug> [...]

Written 2026-09-11 for the seven articles published after seo.py last ran:
they had no og:image, no Twitter card and no Article/Breadcrumb JSON-LD in
ANY language. seo.py now writes English pages only, so each translation is
completed here from the English block:

  canonical, og:url, @id         -> the translation's own URL
  alternates                      -> unchanged (langlinks owns them; identical
                                     in every member of a group)
  og:locale                       -> es_LA / pt_BR, plus og:locale:alternate en_US
  og/twitter title + description  -> the translation's own, already on the page
  og:image / twitter:image        -> the same image file as the English
  image alt                       -> the translation's og:title (seo.py's own
                                     fallback when an article has no hero)
  Article headline / description / keywords -> the translation's hub row
                                     (title, summary, topics), as seo.py uses
                                     the English row
  inLanguage                      -> es / pt
  breadcrumbs                     -> Inicio / Início, the language's hub, title
  byline                          -> the publication date, in the language

Portuguese is completed through its content files + build_pt.py (see
complete_pt); Spanish has no re-runnable builder, so its pages are patched.
"""

import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "pt-2026"))
SITE = "https://amazebase.pro"
START, END = "<!-- SEO:START -->", "<!-- SEO:END -->"
OWNED = re.compile(
    r'^[ \t]*<(?:link[^>]*rel="(?:canonical|alternate)"|meta[^>]*(?:property="og:|name="twitter:))[^>]*>[ \t]*\r?\n',
    re.M | re.I)
MONTHS = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
           "septiembre", "octubre", "noviembre", "diciembre"],
    "pt": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
           "setembro", "outubro", "novembro", "dezembro"],
}
LANG = {
    "es": dict(locale="es_LA", home="Inicio", hub="Centro de Conocimiento", hub_url=SITE + "/es/recursos.html"),
    "pt": dict(locale="pt_BR", home=u"Início", hub="Central de Conhecimento", hub_url=SITE + "/pt/recursos.html"),
}


def rows(tree):
    d = json.load(io.open(os.path.join(tree, "data", "resources.json"), encoding="utf-8"))
    en = dict((r["id"], r) for r in d["resources"] if r["language"] == "en")
    tr = dict(((r["translationOf"], r["language"]), r) for r in d["resources"] if r.get("translationOf"))
    return en, tr


def local_date(iso, lang):
    y, m, dd = (int(x) for x in iso.split("-"))
    return "%d de %s de %d" % (dd, MONTHS[lang][m - 1], y)


def byline_span(iso, lang, encode):
    return ('\n    <span class="dot" aria-hidden="true"></span>\n'
            '    <span><time datetime="%s">%s</time></span>' % (iso, encode(local_date(iso, lang))))


def add_byline(fragment, iso, lang, encode):
    """After the author, as seo.py does for English. Refuses a second date."""
    assert "<time datetime=" not in fragment, "byline already has a date"
    m = re.search(r'(<p class="meta">\s*\n\s*<span>[^<]*</span>)', fragment)
    assert m, "no byline"
    return fragment[:m.end()] + byline_span(iso, lang, encode) + fragment[m.end():]


def localise_block(en_block, lang, loc_url, en_url, og_title, og_desc, row):
    L = LANG[lang]
    b = en_block
    assert b.count('<link rel="canonical" href="%s">' % en_url) == 1
    b = b.replace('<link rel="canonical" href="%s">' % en_url, '<link rel="canonical" href="%s">' % loc_url)
    assert b.count('<meta property="og:locale" content="en_US">') == 1
    b = b.replace('<meta property="og:locale" content="en_US">',
                  '<meta property="og:locale" content="%s">\n<meta property="og:locale:alternate" content="en_US">'
                  % L["locale"])
    b = b.replace('<meta property="og:url" content="%s">' % en_url, '<meta property="og:url" content="%s">' % loc_url)
    for attr, val in (('property="og:title"', og_title), ('property="og:description"', og_desc),
                      ('name="twitter:title"', og_title), ('name="twitter:description"', og_desc),
                      ('property="og:image:alt"', og_title), ('name="twitter:image:alt"', og_title)):
        b, n = re.subn(r'<meta %s content="[^"]*">' % re.escape(attr),
                       lambda m, v=val: '<meta %s content="%s">' % (attr, v), b)
        assert n == 1, attr
    m = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n</script>)', b, re.S)
    g = json.loads(m.group(2))
    for n_ in g["@graph"]:
        if n_.get("@type") == "Article":
            n_["@id"] = loc_url + "#article"
            n_["mainEntityOfPage"]["@id"] = loc_url
            n_["headline"] = row["title"]
            n_["description"] = row["summary"]
            n_["inLanguage"] = lang
            n_["keywords"] = row.get("topics") or []
        if n_.get("@type") == "BreadcrumbList":
            it = n_["itemListElement"]
            it[0]["name"] = L["home"]
            it[1]["name"], it[1]["item"] = L["hub"], L["hub_url"]
            it[2]["name"] = row["title"]
    body = json.dumps(g, ensure_ascii=False, indent=2, separators=(",", ": ")).replace("</", "<\\/")
    b = b[:m.start(2)] + body + b[m.end(2):]
    assert en_url not in b.replace('hreflang="en" href="%s"' % en_url, "").replace(
        'hreflang="x-default" href="%s"' % en_url, ""), "English URL survived outside the alternates"
    return b


def en_block(tree, slug):
    s = io.open(os.path.join(tree, "articles", slug + ".html"), encoding="utf-8").read()
    i, j = s.index(START), s.index(END) + len(END)
    return s[i:j]


def complete_es(tree, slug, en_rows, tr_rows):
    import normalise_pt
    enc = normalise_pt.encode
    es_map = json.load(io.open(os.path.join(HERE, "slugs", "es.json"), encoding="utf-8"))
    rel = "es/articulos/%s.html" % es_map[slug]
    p = os.path.join(tree, rel)
    s = io.open(p, encoding="utf-8", newline="").read()
    assert "\r" not in s and START not in s, "%s already has an SEO block" % rel
    en_row = [r for r in en_rows.values() if r["url"] == "articles/%s.html" % slug][0]
    row = tr_rows[(en_row["id"], "es")]
    og_title = re.search(r'<meta property="og:title" content="([^"]*)"', s).group(1)
    og_desc = re.search(r'<meta property="og:description" content="([^"]*)"', s).group(1)
    block = localise_block(en_block(tree, slug), "es", "%s/%s" % (SITE, rel),
                           "%s/articles/%s.html" % (SITE, slug), og_title, og_desc, row)
    s = OWNED.sub("", s)
    s = s.replace("</head>", block + "\n</head>", 1)
    i = s.index('<header class="article-head">')
    j = s.index("</header>", i)
    s = s[:i] + add_byline(s[i:j], en_row["published"], "es", enc) + s[j:]
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    return rel


def complete_pt(tree, slug, en_rows, tr_rows):
    """The content file gains what the page needs; build_pt.py then builds it
    through the same has-SEO path as the other 44."""
    import normalise_pt
    enc = normalise_pt.encode
    p = os.path.join(HERE, "pt-2026", "content", slug + ".json")
    t = json.load(io.open(p, encoding="utf-8"))
    en_row = [r for r in en_rows.values() if r["url"] == "articles/%s.html" % slug][0]
    row = tr_rows[(en_row["id"], "pt")]
    t["article_head"] = add_byline(t["article_head"], en_row["published"], "pt", enc)
    t["ld_headline"] = row["title"]
    t["crumb"] = row["title"]
    t["ld_desc"] = row["summary"]
    t["keywords"] = row.get("topics") or []
    t["og_img_alt"] = t["og_title"]
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(t, ensure_ascii=False, indent=1) + "\n")
    return p


def verify(tree, slug, lang, en_rows, tr_rows):
    """Everything the block must say, read back from the built page."""
    m_ = json.load(io.open(os.path.join(HERE, "slugs", "%s.json" % lang), encoding="utf-8"))
    rel = "%s/%s.html" % ({"es": "es/articulos", "pt": "pt/artigos"}[lang], m_[slug])
    url = "%s/%s" % (SITE, rel)
    s = io.open(os.path.join(tree, rel), encoding="utf-8").read()
    en_row = [r for r in en_rows.values() if r["url"] == "articles/%s.html" % slug][0]
    row = tr_rows[(en_row["id"], lang)]
    P = []
    one = lambda pat: re.findall(pat, s)
    if s.count(START) != 1 or s.count(END) != 1:
        P.append("SEO blocks: %d" % s.count(START))
    for prop in ("og:title", "og:description", "og:url", "og:locale", "og:image", "og:image:alt", "og:type"):
        if len(one(r'<meta property="%s" content="' % re.escape(prop))) != 1:
            P.append("%s appears %d times" % (prop, len(one(r'<meta property="%s" content="' % re.escape(prop)))))
    if one(r'<link rel="canonical" href="([^"]*)"') != [url]:
        P.append("canonical")
    if [h for h, _ in one(r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)"')] != ["en", "es", "pt", "x-default"]:
        P.append("alternates")
    if one(r'<meta property="og:locale" content="([^"]*)"') != [LANG[lang]["locale"]]:
        P.append("og:locale")
    ogt = one(r'<meta property="og:title" content="([^"]*)"')
    if one(r'<meta property="og:image:alt" content="([^"]*)"') != ogt or \
            one(r'<meta name="twitter:image:alt" content="([^"]*)"') != ogt:
        P.append("image alts differ from og:title")
    img = one(r'<meta property="og:image" content="https://amazebase.pro/([^"]+)"')
    if not img or not os.path.isfile(os.path.join(tree, img[0])):
        P.append("og:image missing on disk")
    g = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))["@graph"]
    art = [n for n in g if n.get("@type") == "Article"][0]
    crumbs = [c["name"] for c in [n for n in g if n.get("@type") == "BreadcrumbList"][0]["itemListElement"]]
    for k, want in (("@id", url + "#article"), ("inLanguage", lang), ("headline", row["title"]),
                    ("description", row["summary"])):
        if art.get(k) != want:
            P.append("Article %s = %r" % (k, art.get(k)))
    if crumbs != [LANG[lang]["home"], LANG[lang]["hub"], row["title"]]:
        P.append("breadcrumbs %s" % crumbs)
    if s.count("<time datetime=") != 1:
        P.append("byline dates: %d" % s.count("<time datetime="))
    return rel, P


if __name__ == "__main__" and "--verify" in sys.argv:
    tree = sys.argv[1]
    slugs = [a for a in sys.argv[2:] if not a.startswith("--")]
    en_rows, tr_rows = rows(tree)
    bad = 0
    for sl in slugs:
        for lang in ("es", "pt"):
            rel, P = verify(tree, sl, lang, en_rows, tr_rows)
            bad += len(P)
            print("%-4s %s%s" % ("OK" if not P else "FAIL", rel, "" if not P else "  " + "; ".join(P)))
    print("\n%d twins, %d problems" % (2 * len(slugs), bad))
    raise SystemExit(1 if bad else 0)

if __name__ == "__main__":
    tree, slugs = sys.argv[1], sys.argv[2:]
    en_rows, tr_rows = rows(tree)
    for sl in slugs:
        print("es  %s" % complete_es(tree, sl, en_rows, tr_rows))
        print("pt  %s (content; rebuild with build_pt.py)" % os.path.basename(complete_pt(tree, sl, en_rows, tr_rows)))
