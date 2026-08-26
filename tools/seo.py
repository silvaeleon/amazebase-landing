#!/usr/bin/env python3
"""
Generate every machine-readable signal on the site from one source of truth.

    python3 tools/seo.py

Re-runnable and idempotent. Everything it writes into a page sits between
    <!-- SEO:START --> ... <!-- SEO:END -->
markers, so a second run replaces its own output instead of stacking. Hand
edits inside those markers are lost on the next run; change this file instead.

What it does
  1. canonical + Open Graph + Twitter Card on all 52 pages
  2. JSON-LD: Organization / WebSite / SoftwareApplication on the home page,
     Article + BreadcrumbList on every article, BreadcrumbList elsewhere
  3. a visible <time datetime> in each article's existing byline
  4. a static, crawlable list of every article inside resources.html, which
     hub.js clears and rebuilds on load. Without it the 44 articles are
     reachable only by executing JavaScript, which most AI crawlers do not do.
  5. sitemap.xml and robots.txt

Article og:title / og:description already written by hand are preserved.
"""
import ast, json, os, re, html, datetime

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE   = "https://amazebase.pro"
BRAND  = "AmazeBase"
LEGAL  = "Silbros Trading LLC"
EMAIL  = "contact@silbrostrading.com"
TODAY  = "2026-08-26"

START, END = "<!-- SEO:START -->", "<!-- SEO:END -->"

# Tags this script owns. Any of these found OUTSIDE the markers is removed, so
# the hand-written placeholders that used to sit in every <head> don't survive
# as duplicates.
OWNED = re.compile(
    r'^[ \t]*<(?:link[^>]*rel="canonical"|meta[^>]*(?:property="og:|name="twitter:))[^>]*>[ \t]*\r?\n',
    re.M | re.I)


def esc(s):
    return html.escape(html.unescape(s or ""), quote=True)


def txt(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8", newline="").read()


def write(p, s):
    open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="").write(s)


def tag(s, pattern):
    m = re.search(pattern, s, re.S | re.I)
    return m.group(1) if m else ""


def meta_desc(s):
    return tag(s, r'<meta name="description" content="([^"]*)"')


def page_title(s):
    return txt(tag(s, r"<title>(.*?)</title>"))


def ld(obj):
    body = json.dumps(obj, ensure_ascii=False, indent=2, separators=(",", ": "))
    # </script> can never appear inside a JSON-LD block
    body = body.replace("</", "<\\/")
    return '<script type="application/ld+json">\n%s\n</script>' % body


# --------------------------------------------------------------- shared nodes

ORG = {
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": BRAND,
    "legalName": LEGAL,
    "url": SITE + "/",
    "email": EMAIL,
    "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/og/og-home.jpg",
             "width": 1200, "height": 630},
    "address": {"@type": "PostalAddress", "addressLocality": "Albuquerque",
                "addressRegion": "NM", "addressCountry": "US"},
}

WEBSITE = {
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "url": SITE + "/",
    "name": BRAND,
    "publisher": {"@id": SITE + "/#organization"},
    "inLanguage": "en",
}


def breadcrumbs(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             **({"item": u} if u else {})}
            for i, (n, u) in enumerate(trail)
        ],
    }


# ------------------------------------------------------------ the 8 top pages

TOP = [
    dict(file="index.html",     slug="home",      url=SITE + "/",
         og="AmazeBase — the operating system for Amazon sellers",
         crumb=None,
         alt="The AmazeBase dashboard: revenue, net profit, cash flow and inventory health in one view"),
    dict(file="product.html",   slug="product",   url=SITE + "/product.html",
         og="Every module inside AmazeBase", crumb="Product",
         alt="An AmazeBase keyword verdict card lowering a bid from $1.40 to $0.90"),
    dict(file="solutions.html", slug="solutions", url=SITE + "/solutions.html",
         og="AmazeBase for new sellers, experienced sellers and agencies",
         crumb="Solutions", alt="AmazeBase reporting for a multi-account seller"),
    dict(file="resources.html", slug="resources", url=SITE + "/resources.html",
         og="Amazon Seller Knowledge Hub", crumb="Knowledge Hub",
         alt="The AmazeBase Knowledge Hub"),
    dict(file="about.html",     slug="about",     url=SITE + "/about.html",
         og="About AmazeBase — built from experience, refined with data",
         crumb="About", alt="Why AmazeBase is being built"),
    dict(file="contact.html",   slug="contact",   url=SITE + "/contact.html",
         og="Contact AmazeBase", crumb="Contact",
         alt="Messages arriving, being read, and shaping the AmazeBase product"),
    dict(file="privacy.html",   slug="privacy",   url=SITE + "/privacy.html",
         og="Privacy Policy — AmazeBase", crumb="Privacy Policy",
         alt="The AmazeBase dashboard"),
    dict(file="terms.html",     slug="terms",     url=SITE + "/terms.html",
         og="Terms of Service — AmazeBase", crumb="Terms of Service",
         alt="The AmazeBase dashboard"),
]


def head_block(url, og_title, description, image, alt, og_type, jsonld):
    L = [START,
         '<link rel="canonical" href="%s">' % url,
         '<meta property="og:site_name" content="%s">' % BRAND,
         '<meta property="og:locale" content="en_US">',
         '<meta property="og:type" content="%s">' % og_type,
         '<meta property="og:url" content="%s">' % url,
         '<meta property="og:title" content="%s">' % esc(og_title),
         '<meta property="og:description" content="%s">' % esc(description),
         '<meta property="og:image" content="%s">' % image,
         '<meta property="og:image:width" content="1200">',
         '<meta property="og:image:height" content="630">',
         '<meta property="og:image:alt" content="%s">' % esc(alt),
         '<meta name="twitter:card" content="summary_large_image">',
         '<meta name="twitter:title" content="%s">' % esc(og_title),
         '<meta name="twitter:description" content="%s">' % esc(description),
         '<meta name="twitter:image" content="%s">' % image,
         '<meta name="twitter:image:alt" content="%s">' % esc(alt),
         jsonld,
         END]
    return "\n".join(L)


def apply_head(path, block):
    """Drop any previous block, drop stray hand-written duplicates of the tags
    this script owns, then insert the fresh block just before </head>."""
    s = read(path)
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\r?\n?", "", s, flags=re.S)
    s = OWNED.sub("", s)
    assert "</head>" in s, path + " has no </head>"
    s = s.replace("</head>", block + "\n</head>", 1)
    write(path, s)


def og_url(slug):
    return "%s/assets/img/og/og-%s.jpg" % (SITE, slug)


# ------------------------------------------------------------------- articles

def load_resources():
    with open(os.path.join(ROOT, "data", "resources.json"), encoding="utf-8") as f:
        return json.load(f)["resources"]


def pretty_date(iso):
    d = datetime.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def do_articles(resources):
    n = 0
    for r in resources:
        rel = r["url"]                                   # articles/<slug>.html
        slug = rel.rsplit("/", 1)[-1][:-5]
        s = read(rel)

        # keep the per-article social copy that was written by hand
        og_title = txt(tag(s, r'<meta property="og:title" content="([^"]*)"')) \
            or page_title(s).split(" — ")[0]
        og_desc = txt(tag(s, r'<meta property="og:description" content="([^"]*)"')) \
            or txt(meta_desc(s))
        alt = txt(tag(s, r'<figure class="hero-shot">\s*<img[^>]*\salt="([^"]*)"')) \
            or og_title
        url = "%s/%s" % (SITE, rel)
        img = og_url(slug)

        article = {
            "@type": "Article",
            "@id": url + "#article",
            "isPartOf": {"@id": SITE + "/#website"},
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "headline": txt(r["title"]),
            "description": txt(r.get("summary") or og_desc),
            "image": {"@type": "ImageObject", "url": img, "width": 1200, "height": 630},
            "datePublished": r["published"],
            "dateModified": r["published"],
            "author": {"@id": SITE + "/#organization"},
            "publisher": {"@id": SITE + "/#organization"},
            "inLanguage": r.get("language", "en"),
        }
        topics = r.get("topics")
        if isinstance(topics, str):          # stored as a python-style list literal
            try:
                topics = ast.literal_eval(topics)
            except (ValueError, SyntaxError):
                topics = []
        if topics:
            article["keywords"] = [txt(t) for t in topics]
        if r.get("minutes"):
            article["timeRequired"] = "PT%dM" % int(r["minutes"])

        graph = ld({"@context": "https://schema.org", "@graph": [
            ORG, WEBSITE, article,
            breadcrumbs([("Home", SITE + "/"),
                         ("Knowledge Hub", SITE + "/resources.html"),
                         (txt(r["title"]), None)]),
        ]})

        apply_head(rel, head_block(url, og_title, og_desc, img, alt, "article", graph))
        byline(rel, r["published"])
        n += 1
    return n


BYLINE = re.compile(r'(<p class="meta">\s*\n\s*<span>[^<]*</span>)(?!\s*\n\s*<span class="dot"[^>]*></span>\s*\n\s*<span><time)', re.I)


def byline(rel, published):
    """Put a real <time datetime> into the byline the article already has.
    The date sits straight after the author, before the read time."""
    s = read(rel)
    s = re.sub(r'\s*<span class="dot" aria-hidden="true"></span>\s*\n\s*<span><time[^>]*>[^<]*</time></span>',
               "", s)                                    # undo a previous run
    m = BYLINE.search(s)
    if not m:
        print("  ! no byline in", rel)
        return
    ins = ('%s\n    <span class="dot" aria-hidden="true"></span>\n'
           '    <span><time datetime="%s">%s</time></span>'
           % (m.group(1), published, pretty_date(published)))
    write(rel, s[:m.start()] + ins + s[m.end():])


# ----------------------------------------------------------------- top pages

def do_top(resources):
    for p in TOP:
        s = read(p["file"])
        desc = txt(meta_desc(s))
        trail = [("Home", SITE + "/")]
        if p["crumb"]:
            trail.append((p["crumb"], None))

        if p["slug"] == "home":
            nodes = [ORG, WEBSITE, {
                "@type": "SoftwareApplication",
                "@id": SITE + "/#software",
                "name": BRAND,
                "url": SITE + "/",
                "applicationCategory": "BusinessApplication",
                "applicationSubCategory": "Amazon seller analytics and advertising software",
                "operatingSystem": "Web browser",
                "description": desc,
                "publisher": {"@id": SITE + "/#organization"},
                "featureList": [
                    "Advertising and PPC optimisation judged against real break-even ACoS",
                    "Financials and profit reporting on true landed cost per unit",
                    "Cost ledger", "Inventory and restock forecasting",
                    "Product research", "Scenario simulations",
                    "Sales analytics", "Automated Amazon data sync",
                ],
            }]
        elif p["slug"] == "resources":
            nodes = [ORG, WEBSITE, {
                "@type": "CollectionPage",
                "@id": p["url"] + "#collection",
                "url": p["url"],
                "name": "Amazon Seller Knowledge Hub",
                "description": desc,
                "isPartOf": {"@id": SITE + "/#website"},
                "publisher": {"@id": SITE + "/#organization"},
                "hasPart": [{"@type": "Article",
                             "@id": "%s/%s#article" % (SITE, r["url"]),
                             "headline": txt(r["title"]),
                             "url": "%s/%s" % (SITE, r["url"]),
                             "datePublished": r["published"]} for r in resources],
            }, breadcrumbs(trail)]
        else:
            nodes = [ORG, WEBSITE, breadcrumbs(trail)]

        apply_head(p["file"], head_block(
            p["url"], p["og"], desc, og_url(p["slug"]), p["alt"], "website",
            ld({"@context": "https://schema.org", "@graph": nodes})))
    return len(TOP)


# ------------------------------------------------- crawlable list in the hub

HUB_START = "<!-- SEO:HUB-FALLBACK:START -->"
HUB_END   = "<!-- SEO:HUB-FALLBACK:END -->"


def do_hub(resources):
    """resources.html builds its list in JavaScript from data/resources.json.
    A crawler that does not run JS therefore sees an empty page and never
    reaches a single article. This writes the same list into the HTML, with the
    same classes and element types hub.js uses, inside the container hub.js
    clears before it renders -- so a browser gets the interactive list, and a
    crawler (or a visitor whose JS failed) gets the links."""
    with open(os.path.join(ROOT, "data", "resources.json"), encoding="utf-8") as f:
        labels = {f_["id"]: f_["label"] for f_ in json.load(f).get("formats", [])}

    rows = []
    for r in sorted(resources, key=lambda x: x["published"], reverse=True):
        tag_ = re.sub(r"s$", "", labels.get(r.get("format"), r.get("format", "")))
        mins = ("<span>%s min</span>" % r["minutes"]) if r.get("minutes") else ""
        thumb = ('<span class="hub-row-thumb"><img src="%s" alt="" width="480" height="270"'
                 ' loading="lazy" decoding="async"></span>' % r["thumb"]) if r.get("thumb") else ""
        rows.append(
            '  <a class="hub-row" href="%s">\n'
            '    %s\n'
            '    <div class="hub-row-body">\n'
            '      <h4 class="hub-row-h">%s</h4>\n'
            '      <p class="hub-row-p">%s</p>\n'
            '      <div class="hub-row-meta"><span><time datetime="%s">%s</time></span>%s</div>\n'
            '    </div>\n'
            '    <span class="hub-row-tag">%s</span>\n'
            '  </a>'
            % (r["url"], thumb, esc(r["title"]), esc(r.get("summary", "")),
               r["published"], pretty_date(r["published"]), mins, esc(tag_)))

    block = "\n".join([HUB_START] + rows + [HUB_END])
    s = read("resources.html")
    if HUB_START in s:
        s = re.sub(re.escape(HUB_START) + r".*?" + re.escape(HUB_END),
                   lambda _: block, s, flags=re.S)
    else:
        target = '<div class="hub-list" data-hub-list></div>'
        assert target in s, "hub list container not found"
        s = s.replace(target, '<div class="hub-list" data-hub-list>\n%s\n</div>' % block, 1)
    write("resources.html", s)
    return len(rows)


# ------------------------------------------------------- sitemap and robots

def do_sitemap(resources):
    urls = [(p["url"], TODAY) for p in TOP]
    urls += [("%s/%s" % (SITE, r["url"]), r["published"]) for r in
             sorted(resources, key=lambda x: x["published"], reverse=True)]
    body = "\n".join(
        "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>" % (u, d)
        for u, d in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + body + "\n</urlset>\n")
    return len(urls)


def do_robots():
    write("robots.txt", """# https://amazebase.pro
# Everything here is public and meant to be read, by people and by machines.

User-agent: *
Allow: /

# Named explicitly so the intent is on the record for the crawlers that read
# and answer questions about this site, not only the ones that index it.
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: https://amazebase.pro/sitemap.xml
""")


def main():
    resources = load_resources()
    t = do_top(resources)
    a = do_articles(resources)
    h = do_hub(resources)
    u = do_sitemap(resources)
    do_robots()
    print("head blocks: %d top-level + %d articles" % (t, a))
    print("hub fallback rows: %d" % h)
    print("sitemap urls: %d" % u)
    print("robots.txt written")


if __name__ == "__main__":
    main()
