# -*- coding: utf-8 -*-
"""
Point every link on a translated page at the page in ITS OWN language.

THE PROBLEM
-----------
On 2026-09-11, 48 Spanish articles still sent their menus to the ENGLISH
product, solutions, about and contact pages -- written before the Spanish ones
existed, never revisited -- and every Spanish and Portuguese page sent
"Pricing", the logo, the wait-list buttons, "Privacy" and "Terms" to the
English homepage and legal pages: 1,797 links on 56 Spanish pages, 589 on 56
Portuguese ones. Nothing errors; a Spanish reader just lands in English.

WHAT IT DOES
------------
For each translated language, languages.json says which top-level pages exist
("top"). An <a href> on that language's pages that points at the ENGLISH
version of one of them is pointed at the local one, #fragment kept:

    /product.html#ledger  ->  /es/producto.html#ledger
    /index.html#waitlist  ->  /es/#waitlist        (the homepage is a folder)

Left alone, on purpose:
  * the language switcher and anything else carrying hreflang= -- a link that
    names its language is MEANT to cross (the translated legal pages' "English
    version" link is one);
  * <link rel="alternate">, canonicals and every absolute URL -- they are not
    root-relative;
  * pages the language does not have yet (no manifest entry): those links stay
    English until the page exists.

langlinks.py runs check() on every run, so a translated page that links to an
English page it has a local version of fails the build, like a slug-map hole.

    python tools/i18n/locallinks.py <site-root>            # rewrite
    python tools/i18n/locallinks.py <site-root> --check    # report, write nothing
"""

import io, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

A_TAG = re.compile(r"<a\b[^>]*>")
HREF = re.compile(r'\bhref="([^"]*)"')


def link_map(cfg, lang):
    """English root-relative path -> local path, for each top page `lang` has."""
    en = cfg["languages"][0]["top"]
    loc = next(l for l in cfg["languages"] if l["code"] == lang).get("top", {})
    m = {}
    for key, p in en.items():
        if key not in loc:
            continue
        m["/" + p] = "/" + loc[key]
        if not p.endswith(".html"):
            # a folder (the homepage): English pages link it as /index.html
            m["/" + p + "index.html"] = "/" + loc[key]
    return m


def back_map(cfg, lang):
    """local path -> the English path as English pages write it (the homepage
    as /index.html). For verifiers that compare a built page with its source."""
    back = {}
    for en, local in link_map(cfg, lang).items():
        if en.endswith(".html"):
            back[local] = en
    return back


def localise(s, cfg, lang):
    """(new text, number of hrefs changed)."""
    m = link_map(cfg, lang)
    n = [0]

    def href(h):
        base, sep, frag = h.group(1).partition("#")
        if base in m:
            n[0] += 1
            return 'href="%s%s%s"' % (m[base], sep, frag)
        return h.group(0)

    def tag(t):
        tg = t.group(0)
        return tg if "hreflang=" in tg else HREF.sub(href, tg)

    return A_TAG.sub(tag, s), n[0]


def pages(tree, cfg):
    """(lang, relpath) for every page under a translated language's folder."""
    out = []
    for lang in cfg["languages"][1:]:
        c = lang["code"]
        for p in sorted(glob.glob(os.path.join(tree, c, "**", "*.html"), recursive=True)):
            out.append((c, os.path.relpath(p, tree).replace(os.sep, "/")))
    return out


def check(tree, cfg):
    """[(page, n)] for every translated page with links still pointing at English."""
    bad = []
    for c, rel in pages(tree, cfg):
        s = io.open(os.path.join(tree, rel), encoding="utf-8").read()
        _, n = localise(s, cfg, c)
        if n:
            bad.append((rel, n))
    return bad


def fragments(tree, cfg):
    """Every local href#fragment on a translated page must name an id on its target."""
    import langlinks
    ids, bad = {}, []
    for c, rel in pages(tree, cfg):
        s = io.open(os.path.join(tree, rel), encoding="utf-8").read()
        for tg in A_TAG.findall(s):
            h = HREF.search(tg)
            if not h or not h.group(1).startswith("/") or "#" not in h.group(1):
                continue
            base, _, frag = h.group(1).partition("#")
            f = langlinks.file_of(base.lstrip("/")) if base != "/" else "index.html"
            full = os.path.join(tree, f)
            if not os.path.exists(full):
                bad.append((rel, h.group(1), "no such page"))
                continue
            if f not in ids:
                ids[f] = set(re.findall(r'\bid="([^"]+)"', io.open(full, encoding="utf-8").read()))
            if frag and frag not in ids[f]:
                bad.append((rel, h.group(1), "no id"))
    return bad


def run(tree, check_only=False):
    import langlinks
    cfg, _ = langlinks.load()
    total, touched = 0, 0
    for c, rel in pages(tree, cfg):
        p = os.path.join(tree, rel)
        s = io.open(p, encoding="utf-8", newline="").read()
        new, n = localise(s, cfg, c)
        if n:
            total += n
            touched += 1
            if not check_only:
                io.open(p, "w", encoding="utf-8", newline="").write(new)
    print("%s %d links on %d translated pages" % ("would localise" if check_only else "localised", total, touched))
    bad = fragments(tree, cfg)
    print("%d local links with a #fragment their target page lacks" % len(bad))
    for b in bad[:12]:
        print("   %s -> %s (%s)" % b)
    return total, bad


if __name__ == "__main__":
    a = sys.argv[1:]
    total, bad = run(a[0], check_only="--check" in a)
    if "--check" in a and (total or bad):
        raise SystemExit(1)
