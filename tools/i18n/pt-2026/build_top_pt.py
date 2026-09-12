# -*- coding: utf-8 -*-
"""
Build the five Portuguese top-level pages from their English originals:
/pt/produto.html, solucoes, sobre, contato and the hub /pt/recursos.html.

    PT_TOP_BRIEFS=<dir> python tools/i18n/pt-2026/build_top_pt.py <site-root>

Same method as build_pt.py: the English page edited in place, so stylesheets,
sprites and layout stay byte-identical. These pages reference their CSS, JS
and each other with RELATIVE paths, which would 404 under /pt/ -- the whole
page is made root-absolute FIRST (href, src, srcset, imagesrcset, poster; every
srcset candidate), then the chrome links are pointed at the Portuguese pages.

  head     html lang, <title>, description, canonical, og/twitter strings,
           og:locale, image alts, breadcrumbs; on the hub, the CollectionPage
           node (id, url, name, description, inLanguage, hasPart = every
           Portuguese article in data/resources.json) -- the node Spanish shipped in English (37c7b86)
  chrome   header, footer, skip link, back-to-top: build_pt.translate_chrome()
  main     the gated translation
  dialog   the waitlist dialog (translated once, on product; identical on all
           four English pages -- asserted) and the hub's request dialog
  hub      the no-JS fallback list, generated from the Portuguese rows in
           resources.json (as build_hub.py did for Spanish)
  links    alternates + switcher by langlinks.rewrite()

The hub is built from the pt rows of data/resources.json, however many there
are: the card list and hasPart are both that set, and the two are asserted
equal. It was 51 at launch and grows by one per translated article.
"""

import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gate, langlinks, locallinks
import build_pt as BP

SITE = BP.SITE
PAGES = [  # key, English file, Portuguese file, Spanish file
    ("product", "product.html", "pt/produto.html", "es/producto.html"),
    ("solutions", "solutions.html", "pt/solucoes.html", "es/soluciones.html"),
    ("about", "about.html", "pt/sobre.html", "es/nosotros.html"),
    ("contact", "contact.html", "pt/contato.html", "es/contacto.html"),
    ("resources", "resources.html", "pt/recursos.html", "es/recursos.html"),
]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
FALLBACK = re.compile(r"<!-- SEO:HUB-FALLBACK:START -->.*?<!-- SEO:HUB-FALLBACK:END -->", re.S)


def region(s, start, end):
    i = s.index(start)
    return i, s.index(end, i) + len(end)


def sub1(pat, new, s, label, flags=0):
    s2, n = re.subn(pat, lambda m: new, s, count=1, flags=flags)
    assert n == 1, label
    return s2


def ld_str(v):
    return json.dumps(v)[1:-1]


def fallback(rows, taxo):
    """The static card list hub.js replaces on load -- Portuguese rows, root-absolute."""
    one = dict((f["id"], f.get("label_one_pt") or f.get("label_pt") or f["label"]) for f in taxo["formats"])
    rows = sorted(rows, key=lambda r: r.get("published", ""), reverse=True)
    out = ["<!-- SEO:HUB-FALLBACK:START -->"]
    for r in rows:
        y, m, d = (int(x) for x in r["published"].split("-"))
        human = "%d de %s de %d" % (d, MESES[m - 1], y)
        parts = ['  <a class="hub-row" href="/%s">' % r["url"]]
        if r.get("thumb"):
            parts.append('    <span class="hub-row-thumb"><img src="/%s" alt="" width="480" height="270" '
                         'loading="lazy" decoding="async"></span>' % r["thumb"])
        parts += ['    <div class="hub-row-body">',
                  '      <h4 class="hub-row-h">%s</h4>' % esc(r["title"]),
                  '      <p class="hub-row-p">%s</p>' % esc(r["summary"]),
                  '      <div class="hub-row-meta"><span><time datetime="%s">%s</time></span>%s</div>'
                  % (r["published"], human, ("<span>%d min</span>" % r["minutes"]) if r.get("minutes") else ""),
                  "    </div>",
                  '    <span class="hub-row-tag">%s</span>' % esc(one.get(r.get("format"), "")),
                  "  </a>"]
        out.append("\n".join(parts))
    out.append("<!-- SEO:HUB-FALLBACK:END -->")
    return "\n".join(out), len(rows)


def esc(t):
    """Plain text -> house style: &amp; &lt; &gt; and a named entity for every
    non-ASCII character, exactly as normalise_pt writes text nodes."""
    import normalise_pt
    return normalise_pt.encode(t)


def build(tree, key, en_rel, pt_rel, es_rel, tr, dialog_pt, cfg, data):
    en_url, pt_url = "%s/%s" % (SITE, en_rel), "%s/%s" % (SITE, pt_rel)
    s = io.open(os.path.join(tree, en_rel), encoding="utf-8", newline="").read()
    assert "\r" not in s
    s = BP.rootify(s)

    # ---- head
    s = BP.rep(s, '<html lang="en">', '<html lang="pt">', label="html lang")
    s = sub1(r"<title>.*?</title>", "<title>%s</title>" % tr["title"], s, "title", re.S)
    s = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % tr["desc"], s, "desc")
    s = BP.rep(s, '<link rel="canonical" href="%s">' % en_url, '<link rel="canonical" href="%s">' % pt_url, label="canonical")
    s = BP.rep(s, '<meta property="og:locale" content="en_US">',
               '<meta property="og:locale" content="pt_BR">\n<meta property="og:locale:alternate" content="en_US">',
               label="og:locale")
    s = BP.rep(s, '<meta property="og:url" content="%s">' % en_url, '<meta property="og:url" content="%s">' % pt_url, label="og:url")
    for attr, k in (('property="og:title"', "og_title"), ('property="og:description"', "og_desc"),
                    ('name="twitter:title"', "og_title"), ('name="twitter:description"', "og_desc"),
                    ('property="og:image:alt"', "og_img_alt"), ('name="twitter:image:alt"', "og_img_alt")):
        s = sub1(r'<meta %s content="[^"]*">' % re.escape(attr), '<meta %s content="%s">' % (attr, tr[k]), s, attr)

    # ---- JSON-LD: breadcrumbs; the hub's CollectionPage
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    graph = json.loads(m.group(2))
    for n in graph["@graph"]:
        if n.get("@type") == "BreadcrumbList":
            items = n["itemListElement"]
            assert items[0]["name"] == "Home"
            items[0]["name"] = u"Início"
            items[0]["item"] = SITE + "/pt/"      # the Portuguese homepage (2026-09-11)
            items[-1]["name"] = tr["crumb"]
            if "item" in items[-1]:
                items[-1]["item"] = pt_url
        if n.get("@type") == "CollectionPage":
            n["@id"] = pt_url + "#collection"
            n["url"] = pt_url
            n["name"] = tr["collection_name"]
            n["description"] = tr["collection_desc"]
            n["inLanguage"] = "pt"
            rows = sorted([r for r in data["resources"] if r.get("language") == "pt"],
                          key=lambda r: r.get("published", ""), reverse=True)
            n["hasPart"] = [{"@type": "Article", "@id": "%s/%s#article" % (SITE, r["url"]),
                             "headline": r["title"], "url": "%s/%s" % (SITE, r["url"]),
                             "datePublished": r.get("published", "")} for r in rows]
    s = s[:m.start(2)] + "\n" + json.dumps(graph, indent=2, ensure_ascii=False) + "\n" + s[m.end(2):]

    # ---- chrome
    if ">Skip to content</a>" in s:
        s = BP.rep(s, ">Skip to content</a>", ">Pular para o conte&uacute;do</a>", label="skip")
    if 'aria-label="Back to top"' in s:
        s = BP.rep(s, 'aria-label="Back to top"', 'aria-label="Voltar ao topo"', label="to-top")
    a, b = region(s, '<header class="site-header">', "</header>")
    s = s[:a] + BP.translate_chrome(s[a:b], "header") + s[b:]
    a, b = region(s, '<footer class="footer">', "</footer>")
    s = s[:a] + BP.translate_chrome(s[a:b], "footer") + s[b:]

    # ---- main
    a, b = region(s, '<main id="main">', "</main>")
    main = tr["main"]
    if key == "resources":
        pt_rows = [r for r in data["resources"] if r.get("language") == "pt"]
        have_pt_rows = len(pt_rows)
        blk, n = fallback(pt_rows, data)
        assert n == have_pt_rows, (n, have_pt_rows)
        mark = "<!-- SEO:HUB-FALLBACK:START --><!-- SEO:HUB-FALLBACK:END -->"
        assert main.count(mark) == 1, "fallback marker missing from the hub translation"
        main = main.replace(mark, blk)
    s = s[:a] + BP.rootify(main) + s[b:]

    # ---- dialog
    if key == "resources":
        a, b = region(s, '<dialog class="wl" id="request"', "</dialog>")
        s = s[:a] + BP.rootify(tr["cta"]) + s[b:]
    else:
        a, b = region(s, '<dialog class="wl" id="waitlist"', "</dialog>")
        s = s[:a] + BP.rootify(dialog_pt) + s[b:]

    # ---- alternates + switcher
    members = {"en": en_rel, "es": es_rel, "pt": pt_rel}
    s = langlinks.rewrite(s, cfg, members, "pt")
    s, _ = locallinks.localise(s, cfg, "pt")

    s = BP.rootify(s)
    out = os.path.join(tree, pt_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="").write(s)
    return pt_rel


def main(tree):
    briefs = os.environ["PT_TOP_BRIEFS"]
    content = os.path.join(HERE, "content-top")
    cfg, _ = BP.load_cfg()
    data = json.load(io.open(os.path.join(tree, "data", "resources.json"), encoding="utf-8"))
    have_pt_rows = sum(1 for r in data["resources"] if r.get("language") == "pt")

    # the waitlist dialog is identical on the four English pages: translate once, assert it
    dialogs = set()
    for key, en_rel, _, _ in PAGES[:4]:
        s = io.open(os.path.join(tree, en_rel), encoding="utf-8").read()
        dialogs.add(re.search(r'<dialog class="wl" id="waitlist".*?</dialog>', s, re.S).group(0))
    assert len(dialogs) == 1, "the waitlist dialog differs between the English pages"
    dialog_pt = json.load(io.open(os.path.join(content, "product.json"), encoding="utf-8"))["cta"]
    for keep in ('name="company_website"', 'name="referral_code"', 'data-waitlist-submit',
                 'data-waitlist-done', 'name="marketplace"'):
        assert keep in dialog_pt, "dialog lost %s" % keep
    msgs = re.findall(r'\bdata-msg-(\w+)="', dialog_pt[:dialog_pt.index(">")])
    assert msgs == ["name", "email", "market", "sending", "rate", "generic", "network"], msgs

    built = []
    for key, en_rel, pt_rel, es_rel in PAGES:
        if key == "resources" and not have_pt_rows:
            print("skip   resources (data/resources.json has no pt rows)")
            continue
        brief = json.load(io.open(os.path.join(briefs, key + ".json"), encoding="utf-8"))
        tr = json.load(io.open(os.path.join(content, key + ".json"), encoding="utf-8"))
        n, prob = gate.audit(brief, tr, "pt")
        assert not prob, "%s refused by the gate:\n  %s" % (key, "\n  ".join(prob))
        built.append(build(tree, key, en_rel, pt_rel, es_rel, tr, dialog_pt, cfg, data))
        print("built  %-10s -> /%-18s gate %d elements" % (key, pt_rel, n))
    return built


if __name__ == "__main__":
    main(sys.argv[1])
