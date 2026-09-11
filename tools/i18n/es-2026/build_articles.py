# -*- coding: utf-8 -*-
"""
Build all 48 Spanish article pages, and patch their English originals.

The Spanish body is assembled by replacing four regions INSIDE the English
wrap block rather than by writing a new one, so whatever the original page's
structure was -- extra blank lines, a commented-out hero slot, a missing CTA --
survives untouched. Only the translated regions change.
"""

import io, os, sys, re, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common
import pipeline as P
from common import rep, lang_switch, hreflang_block, SITE

SRC = "/mnt/user-data/uploads/amazebase-landing"
OUT = "/home/claude/esout3"
CONTENT = "/home/claude/escontent"

BACK_ES = ('<p class="back-link"><a href="/resources.html?lang=es">'
           '&larr; Centro de Conocimiento</a></p>')


def out_path(rel):
    p = os.path.join(OUT, rel.lstrip("/"))
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    return p


def region(s, start, end):
    i = s.index(start)
    j = s.index(end, i) + len(end)
    return i, j, s[i:j]


def build_one(slug, es):
    en_path = "/articles/%s.html" % slug
    es_path = "/es/articulos/%s.html" % es["es_slug"]
    src = os.path.join(SRC, "articles", slug + ".html")
    s = io.open(src, encoding="utf-8").read()

    # ---- the wrap block, edited in place
    i, j, wrap = region(s, '<div class="wrap">', "</div><!-- /.wrap -->")

    a, b, cur = region(wrap, '<p class="back-link">', "</p>")
    wrap = wrap[:a] + BACK_ES + wrap[b:]

    a, b, cur = region(wrap, '<header class="article-head">', "</header>")
    wrap = wrap[:a] + es["article_head"] + wrap[b:]

    a, b, cur = region(wrap, "<main", "</main>")
    wrap = wrap[:a] + es["main"] + wrap[b:]

    if es.get("rail"):
        a, b, cur = region(wrap, '<aside class="rail"', "</aside>")
        wrap = wrap[:a] + es["rail"] + wrap[b:]

    if es.get("cta"):
        a, b, cur = region(wrap, '<aside class="cta">', "</aside>")
        wrap = wrap[:a] + es["cta"] + wrap[b:]

    # hero: root-absolute src (the page now lives two directories deep) and a
    # Spanish alt. A commented-out slot is left commented, path fixed anyway.
    wrap = wrap.replace('src="../assets/img/', 'src="/assets/img/')
    if es.get("hero_alt"):
        m = re.search(r'(<figure class="hero-shot">.*?alt=")([^"]*)(")', wrap, re.S)
        assert m, "%s: hero_alt supplied but no hero figure" % slug
        wrap = wrap[:m.start(2)] + es["hero_alt"] + wrap[m.end(2):]

    # the six late articles never close .shell or their trailing <section>
    d = len(re.findall(r"<div\b", wrap)) - len(re.findall(r"</div>", wrap))
    sec = len(re.findall(r"<section\b", wrap)) - len(re.findall(r"</section>", wrap))
    if (d, sec) == (1, 1):
        wrap = rep(wrap, "</aside>\n\n\n</div><!-- /.wrap -->",
                         "</aside>\n\n</div><!-- /.shell -->\n\n</div><!-- /.wrap -->",
                   label="close shell " + slug)
        k = wrap.rindex('<section class="sec">')
        e = wrap.index("</main>", k)
        wrap = wrap[:e].rstrip() + "\n    </section>\n\n  \n" + wrap[e:]
        d = len(re.findall(r"<div\b", wrap)) - len(re.findall(r"</div>", wrap))
        sec = len(re.findall(r"<section\b", wrap)) - len(re.findall(r"</section>", wrap))
    assert (d, sec) == (0, 0), "%s: unbalanced %s" % (slug, (d, sec))

    meta = dict(
        title=es["title"], desc=es["desc"],
        og_title=es["og_title"], og_desc=es["og_desc"],
        headline=es.get("ld_headline") or es["title"],
        ld_desc=es.get("ld_desc") or es["desc"],
        breadcrumb=es.get("crumb") or es["title"],
        keywords=es.get("keywords") or [],
    )
    common.build_es(src, out_path(es_path), en_path, es_path, meta, wrap)

    # og:image:alt / twitter:image:alt were left English on the pilot pages;
    # supply the Spanish one here where the translator produced it.
    if es.get("og_img_alt"):
        p = out_path(es_path)
        t = io.open(p, encoding="utf-8").read()
        t2, n = re.subn(r'(<meta (?:property="og:image:alt"|name="twitter:image:alt") content=")[^"]*(")',
                        lambda m: m.group(1) + es["og_img_alt"] + m.group(2), t)
        if n:
            io.open(p, "w", encoding="utf-8", newline="\n").write(t2)
    return es_path


def patch_english(slug, es_slug):
    en_path = "/articles/%s.html" % slug
    es_path = "/es/articulos/%s.html" % es_slug
    s = io.open(os.path.join(SRC, "articles", slug + ".html"), encoding="utf-8").read()
    assert "hreflang=" not in s, slug

    hl = hreflang_block(en_path, es_path)
    if "<!-- SEO:START -->" in s:
        anchor = '<link rel="canonical" href="%s%s">' % (SITE, en_path)
        s = rep(s, anchor, anchor + "\n" + hl, label="canonical " + slug)
    else:
        anchor = '<link rel="stylesheet" href="/css/site-footer.css">'
        s = rep(s, anchor,
                anchor + '\n<link rel="canonical" href="%s%s">\n%s' % (SITE, en_path, hl),
                label="no-seo anchor " + slug)

    sw = lang_switch(en_path, es_path, "en")
    a = ('  <div class="nav-actions">\n'
         '    <a class="btn btn--quiet" href="https://analytics.amazebase.pro/login">Log in</a>')
    s = rep(s, a,
            '  <div class="nav-actions">\n'
            + "\n".join("    " + ln for ln in sw.split("\n")) + "\n"
            + '    <a class="btn btn--quiet" href="https://analytics.amazebase.pro/login">Log in</a>',
            label="nav-actions " + slug)
    io.open(out_path(en_path), "w", encoding="utf-8", newline="\n").write(s)


if __name__ == "__main__":
    slugs = [os.path.basename(f)[:-5] for f in sorted(glob.glob(CONTENT + "/*.json"))]
    assert len(slugs) == 48
    built = []
    for sl in slugs:
        es = json.load(io.open(os.path.join(CONTENT, sl + ".json"), encoding="utf-8"))
        built.append(build_one(sl, es))
        patch_english(sl, es["es_slug"])
        print("built + patched  %-36s -> %s" % (sl, es["es_slug"]))
    print("\n%d Spanish pages, %d English pages patched" % (len(built), len(slugs)))
