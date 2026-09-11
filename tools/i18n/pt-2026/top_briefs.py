# -*- coding: utf-8 -*-
"""
Translator briefs for the five top-level pages: product, solutions, about,
contact and the hub (resources). Same shape as an article brief, so gate.py
checks them the same way:

  main       the <main id="main"> block. For the hub, the generated article
             list (SEO:HUB-FALLBACK) is cut out first -- it is built from
             resources.json, not translated.
  cta        re-used as the slot for the page's DIALOG: the waitlist dialog on
             product (identical on all four English pages, so translated once),
             the content-request dialog on the hub. The gate compares its
             skeleton like any other region.
  title/desc/og_* / og_img_alt / crumb   the head strings; `title_full` is the
             whole <title>, because these pages do not use "X -- AmazeBase".

    python tools/i18n/pt-2026/top_briefs.py <site-root> <out-dir>
"""

import html, io, json, os, re, sys

PAGES = {"product": "product.html", "solutions": "solutions.html",
         "about": "about.html", "contact": "contact.html", "resources": "resources.html"}
FALLBACK = re.compile(r"<!-- SEO:HUB-FALLBACK:START -->.*?<!-- SEO:HUB-FALLBACK:END -->", re.S)
MARK = "<!-- SEO:HUB-FALLBACK:START --><!-- SEO:HUB-FALLBACK:END -->"


def one(pat, s, flags=0):
    m = re.search(pat, s, flags)
    return m.group(1) if m else None


def brief(tree, key):
    s = io.open(os.path.join(tree, PAGES[key]), encoding="utf-8").read()
    main = one(r'(<main id="main">.*?</main>)', s, re.S)
    assert main, key
    if key == "resources":
        assert len(FALLBACK.findall(main)) == 1
        main = FALLBACK.sub(MARK, main)
    dialog = None
    if key == "product":
        dialog = one(r'(<dialog class="wl" id="waitlist".*?</dialog>)', s, re.S)
    elif key == "resources":
        dialog = one(r'(<dialog class="wl" id="request".*?</dialog>)', s, re.S) or \
                 one(r'(<dialog[^>]*rq-title.*?</dialog>)', s, re.S)
    assert key not in ("product", "resources") or dialog, key
    ld = one(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    crumb = None
    if ld:
        for n in json.loads(ld).get("@graph", []):
            if n.get("@type") == "BreadcrumbList":
                items = n["itemListElement"]
                crumb = items[-1]["name"] if len(items) > 1 else None
            if n.get("@type") == "CollectionPage":
                coll = (n.get("name"), n.get("description"))
    b = {
        "slug": key,
        "page": PAGES[key],
        "title_full": one(r"<title>(.*?)</title>", s, re.S),
        "title": one(r"<title>(.*?)</title>", s, re.S),
        "desc": one(r'<meta name="description" content="([^"]*)"', s),
        "og_title": one(r'<meta property="og:title" content="([^"]*)"', s),
        "og_desc": one(r'<meta property="og:description" content="([^"]*)"', s),
        "og_img_alt": one(r'<meta property="og:image:alt" content="([^"]*)"', s),
        "crumb": crumb,
        "ld_headline": None, "ld_desc": None, "keywords": [],
        "hero_alt": None, "article_head": None, "rail": None,
        "main": main,
        "cta": dialog,
        "words": len(re.sub(r"<[^>]+>", " ", main).split()),
    }
    if key == "resources":
        b["collection_name"], b["collection_desc"] = coll
    return b


if __name__ == "__main__":
    tree, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for k in PAGES:
        b = brief(tree, k)
        io.open(os.path.join(out, k + ".json"), "w", encoding="utf-8", newline="\n").write(
            json.dumps(b, ensure_ascii=False, indent=1))
        print("%-10s main %5d words, dialog %s, crumb %r, og_img_alt %s"
              % (k, b["words"], "yes" if b["cta"] else "no ", b["crumb"], "yes" if b["og_img_alt"] else "no"))
