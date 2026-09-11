# -*- coding: utf-8 -*-
"""
Calibrate the gate before it judges a single Portuguese sentence.

  1. POSITIVE: the three Spanish pilot pages Leon approved must PASS gate.audit()
     against today's English briefs. Otherwise the gate rejects good work and a
     later failure means nothing.
  2. NEGATIVE: the same pages must FAIL the Portuguese leakage and register
     rules -- Spanish words, 25 %, angle quotes. Otherwise those rules are
     assertions that cannot fail.
  3. MUTATIONS: one deliberate defect per check, each of which must be caught.

    python tools/i18n/pt-2026/calibrate.py <site-root> <briefs-dir>
"""

import copy, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gate

PILOT_ES = {
    "reorder-point": "punto-de-reorden",
    "stop-optimizing-acos": "deja-de-optimizar-el-acos",
    "first-product-succeeds-cash": "y-si-tu-primer-producto-funciona",
}

# History: on 2026-09-10 this calibration found the Spanish ACOS lead wrapping
# "Advertising Cost of Sales" in <em>, which the English never did. Fixed in
# 5c16b5c; the page must now pass outright.
#
# A REAL defect in a shipped page, found 2026-09-11 when the <pre> checks were
# added: the Spanish first-product page breaks the English line structure and
# column alignment of its worked sums. The page as shipped must FAIL, and every
# failure must be a <pre> failure; with the <pre> checks off it must PASS, which
# proves the gate saw that and nothing else. Not fixed here -- its own concern.
# FIXED 2026-09-11 (after Portuguese shipped): the four blocks re-laid on the
# English line structure, same words and numbers; the page must now pass
# outright, <pre> checks on. The mechanism stays for the next known defect.
KNOWN_PRE_DEFECT = set()


def region(s, start, end):
    i = s.index(start)
    return s[i:s.index(end, i) + len(end)]


def from_page(path, slug, local_slug):
    """A built page read back into the translator's JSON shape."""
    s = io.open(path, encoding="utf-8").read()
    d = {"slug": slug, "es_slug": local_slug}
    d.update(gate.P.head_strings(s))
    d["article_head"] = region(s, '<header class="article-head">', "</header>")
    d["main"] = region(s, "<main", "</main>")
    m = re.search(r'<aside class="rail".*?</aside>', s, re.S)
    d["rail"] = m.group(0) if m else None
    m = re.search(r'<aside class="cta">.*?</aside>', s, re.S)
    d["cta"] = m.group(0) if m else None
    live = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    m = re.search(r'<figure class="hero-shot">.*?alt="([^"]*)"', live, re.S)
    d["hero_alt"] = m.group(1) if m else None
    # JSON-LD on a built page is \\u-escaped JSON; the translator hands it over
    # as plain text. Decode so the gate sees the translator's form.
    for k in ("ld_headline", "ld_desc", "crumb"):
        if d.get(k):
            d[k] = json.loads('"%s"' % d[k])
    d["keywords"] = [json.loads('"%s"' % k) for k in d.get("keywords") or []]
    return d


def main(tree, briefs):
    es_map = json.load(io.open(os.path.join(tree, "tools", "i18n", "slugs", "es.json"),
                               encoding="utf-8"))
    back = dict(("/es/articulos/%s.html" % v, "/articles/%s.html" % k) for k, v in es_map.items())
    back.update({"/es/recursos.html": "/resources.html", "/es/producto.html": "/product.html",
                 "/es/soluciones.html": "/solutions.html", "/es/nosotros.html": "/about.html",
                 "/es/contacto.html": "/contact.html"})

    def href_back(h):
        base, frag = (h.split("#", 1) + [""])[:2]
        b = back.get(base, base)
        return b + ("#" + frag if frag else "")

    pages, total, ok = {}, 0, True
    print("1. POSITIVE CONTROL -- approved Spanish pilot pages must pass")
    for slug, es_slug in PILOT_ES.items():
        brief = json.load(io.open(os.path.join(briefs, slug + ".json"), encoding="utf-8"))
        tr = from_page(os.path.join(tree, "es", "articulos", es_slug + ".html"), slug, es_slug)
        pages[slug] = (brief, tr)
        per = []
        for f in gate.FIELDS:
            if brief.get(f):
                per.append("%s %d" % (f, len(gate.P.skeleton(brief[f]))))
        n, prob = gate.audit(brief, tr, "es", slug_key="es_slug", href_back=href_back)
        label = "PASS" if not prob else "FAIL"
        if slug in KNOWN_PRE_DEFECT:
            only_pre = bool(prob) and all("<pre>" in p for p in prob)
            print("   %-30s %-4s as shipped (expected: known <pre> defect; all %d failures are <pre>: %s)"
                  % (slug, label, len(prob), only_pre))
            for p in prob:
                print("        " + p.replace("\n", "\n        "))
            ok &= only_pre
            n, prob = gate.audit(brief, tr, "es", slug_key="es_slug", href_back=href_back, pre=False)
            label = ("PASS" if not prob else "FAIL") + " with the <pre> checks off"
        total += n
        ok &= not prob
        print("   %-30s %-4s %4d elements identical  (%s)  slug %s = %s"
              % (slug, label, n, ", ".join(per), es_slug, gate.slug_report(es_slug)))
        for p in prob:
            print("        " + p.replace("\n", "\n        "))
    print("   total: %d elements identical across the three pilot pages" % total)
    main_only = sum(len(gate.P.skeleton(b["main"])) for b, _ in pages.values())
    print("   (of which <main> alone: %d)" % main_only)

    print("\n2. NEGATIVE CONTROL -- the same pages under the PORTUGUESE rules must fail")
    for slug, (brief, tr) in pages.items():
        t = dict(tr, pt_slug=tr["es_slug"])
        n, prob = gate.audit(brief, t, "pt", href_back=href_back)
        caught = [p.replace("\n", " ")[:90] for p in prob]
        good = any("spanish words" in p for p in prob)
        ok &= good
        print("   %-30s %s  %d problems" % (slug, "CAUGHT" if good else "MISSED", len(prob)))
        for c in caught[:6]:
            print("        " + c)

    print("\n3. MUTATIONS -- each deliberate defect must be caught")
    brief, tr = pages["reorder-point"]

    def mut(label, fn, expect):
        t = copy.deepcopy(tr)
        fn(t)
        n, prob = gate.audit(brief, t, "es", slug_key="es_slug", href_back=href_back)
        hit = any(expect in p for p in prob)
        print("   %-52s %s" % (label, "CAUGHT" if hit else "MISSED  <-- " + repr(prob[:2])))
        return hit

    ok &= mut("drop one </li> from main", lambda t: t.__setitem__(
        "main", t["main"].replace("</li>", "", 1)), "skeleton")
    ok &= mut("rename one class in main", lambda t: t.__setitem__(
        "main", t["main"].replace('class="fixbox"', 'class="fix-box"', 1)), "skeleton")
    ok &= mut("change a figure (1,200 -> 1,300)", lambda t: t.__setitem__(
        "main", t["main"].replace("1,200", "1,300", 1)), "figures differ")
    ok &= mut("leave an English sentence in", lambda t: t.__setitem__(
        "main", t["main"].replace("</p>", " and the rest of your stock</p>", 1)), "English survived")
    ok &= mut("slug of 51 characters, 6 words", lambda t: t.__setitem__(
        "es_slug", "a" * 10 + "-" + "b" * 10 + "-" + "c" * 10 + "-" + "d" * 10 + "-" + "e" * 5 + "-" + "f"),
        "the caps are")
    ok &= mut("slug of 8 words, 23 characters", lambda t: t.__setitem__(
        "es_slug", "a-bb-cc-dd-ee-ff-gg-hhh"), "the caps are")
    ok &= mut("hero alt of 20 words", lambda t: t.__setitem__(
        "hero_alt", " ".join(["palabra"] * 20)), "hero_alt is 20 words")
    ok &= mut("og:image:alt differs from hero alt", lambda t: t.__setitem__(
        "og_img_alt", "otra cosa distinta"), "differ")
    ok &= mut("HTML entity in JSON-LD headline", lambda t: t.__setitem__(
        "ld_headline", "F&oacute;rmula"), "HTML entity")
    ok &= mut("raw accent in title attribute", lambda t: t.__setitem__(
        "title", u"Fórmula"), "raw accented")

    # the 2026-09-11 checks, on the approved Portuguese pilot (the Spanish page
    # with <pre> blocks is the known defect above, so it cannot be the base)
    content = os.path.join(tree, "tools", "i18n", "pt-2026", "content")
    pb = json.load(io.open(os.path.join(briefs, "first-product-succeeds-cash.json"), encoding="utf-8"))
    pt = json.load(io.open(os.path.join(content, "first-product-succeeds-cash.json"), encoding="utf-8"))
    n, prob = gate.audit(pb, pt, "pt")
    print("   control: Portuguese first-product passes           %s" % ("PASS" if not prob else "FAIL %s" % prob[:2]))
    ok &= not prob

    def mut_pt(label, fn, expect):
        t = copy.deepcopy(pt)
        fn(t)
        n, prob = gate.audit(pb, t, "pt")
        hit = any(expect in p for p in prob)
        print("   %-52s %s" % (label, "CAUGHT" if hit else "MISSED  <-- " + repr(prob[:2])))
        return hit

    def sub(field, old, new):
        def f(t):
            assert t[field].count(old) >= 1, "mutation anchor missing: %r" % old
            t[field] = t[field].replace(old, new, 1)
        return f

    ok &= mut_pt("<pre>: $30,000 -> $30.000 inside a worked sum",
                 sub("main", "$30,000 / ~$12,000", "$30.000 / ~$12,000"), "numbers/operators differ")
    ok &= mut_pt("<pre>: two operands swapped",
                 sub("main", "$30,000 / ~$12,000", "~$12,000 / $30,000"), "numbers/operators differ")
    ok &= mut_pt("<pre>: one aligned column pushed right",
                 sub("main", "para a Ana                 =", "para a Ana                  ="), "alignment broken")
    ok &= mut_pt("<pre>: a line split in two",
                 sub("main", u"≈ 2 produtos", u"≈\n 2 produtos"), "lines, English")
    ok &= mut_pt("fixed label drifted (Guia -> Manual de crescimento)",
                 sub("article_head", ">Guia de crescimento<", ">Manual de crescimento<"), "must be the fixed string")
    hit = any("net revenue" in p for p in gate.check_net_revenue(
        '<main><p class="lead">Net revenue fell.</p></main>',
        '<main><p class="lead">O faturamento caiu.</p></main>', "main"))
    print("   %-52s %s" % ("faturamento where the English says net revenue", "CAUGHT" if hit else "MISSED"))
    ok &= hit
    # the sentence a translator caught that STOP_EN missed (ppc-flywheel)
    en_s = "<main><p>That&rsquo;s why great Amazon businesses often seem impossible to catch.</p></main>"
    for label, tr_s, expect in (
            ("English sentence left untranslated (no STOP_EN word)", en_s, "identical to the English"),
            ("English clause inside a Portuguese sentence",
             "<main><p>Por isso as grandes empresas, and the rank is what compounds.</p></main>", "English words")):
        hit = any(expect in p for p in gate.check_untranslated(en_s, tr_s, "main"))
        print("   %-52s %s" % (label, "CAUGHT" if hit else "MISSED"))
        ok &= hit
    clean = gate.check_untranslated(en_s, "<main><p>O or&ccedil;amento de an&uacute;ncios nos pain&eacute;is, "
                                           "o lead time e a Buy Box.</p></main>", "main")
    print("   %-52s %s" % ("control: accented Portuguese + allowed English terms", "PASS" if not clean else "FAIL %s" % clean))
    ok &= not clean

    print("\nCALIBRATION %s" % ("PASSED" if ok else "FAILED"))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
