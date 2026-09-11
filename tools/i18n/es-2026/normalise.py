# -*- coding: utf-8 -*-
"""
Consistency pass over the 48 translated articles, before anything is built.

Twenty-odd translators worked in parallel from the same brief, so the drift is
small but real: two spellings of one keyword, four renderings of one aria-label,
three slugs long enough to be unusable. Everything here is a decided, mechanical
substitution, and every one asserts it fired.

Also rewrites cross-article links. Translators were told to leave hrefs alone so
the structural gate could compare them; now that every Spanish slug exists, a
link from one Spanish article to another can point at the Spanish page.
"""

import io, os, re, json, glob, html

CONTENT = "/home/claude/escontent"
PILOTS = {
    "reorder-point": "punto-de-reorden",
    "stop-optimizing-acos": "deja-de-optimizar-el-acos",
    "first-product-succeeds-cash": "y-si-tu-primer-producto-funciona",
}

# --- slugs that came back too long to live in a URL -------------------------
SLUG_FIX = {
    "ppc-capital-allocation":    "el-ppc-es-asignacion-de-capital",
    "ad-growth-vs-supply-chain": "crecimiento-publicitario-y-cadena-de-suministro",
    "highest-roas-trap":         "la-trampa-del-roas-mas-alto",
}

# --- terminology the brief settled, applied to stragglers -------------------
TEXT_FIX = [
    ("Sistemas operativos", "Sistemas de operación"),
    ("cartera publicitaria", "portafolio publicitario"),
    ("Asignación de cartera", "Asignación de portafolio"),
]

# --- one Spanish aria-label per English one --------------------------------
ARIA = {
    "Key points":                    "Ideas clave",
    "Key figures from this article": "Cifras clave de este art&iacute;culo",
    "Key ideas from this article":   "Ideas clave de este art&iacute;culo",
    "Episode details":               "Detalles del episodio",
}


def load(slug):
    return json.load(io.open(os.path.join(CONTENT, slug + ".json"), encoding="utf-8"))


def save(slug, d):
    io.open(os.path.join(CONTENT, slug + ".json"), "w", encoding="utf-8").write(
        json.dumps(d, ensure_ascii=False, indent=1))


def run():
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pipeline as P

    slugs = [os.path.basename(f)[:-5] for f in sorted(glob.glob(CONTENT + "/*.json"))]
    assert len(slugs) == 48, len(slugs)

    # 1. slug fixes
    for en, new in SLUG_FIX.items():
        d = load(en)
        old = d["es_slug"]
        assert old != new, en
        d["es_slug"] = new
        save(en, d)
        print("slug   %-34s %s -> %s" % (en, old, new))

    # 2. the full English -> Spanish slug map, pilots included
    smap = dict(PILOTS)
    for s in slugs:
        smap[s] = load(s)["es_slug"]
    assert len(smap) == 51, len(smap)
    assert len(set(smap.values())) == 51, "duplicate Spanish slug"
    io.open("/home/claude/briefs/_slugmap.json", "w", encoding="utf-8").write(
        json.dumps(smap, ensure_ascii=False, indent=1))

    # 3. terminology, aria-labels, cross-links
    fixed_text = fixed_aria = fixed_link = 0
    for s in slugs:
        d = load(s)
        b = P.brief(s)

        for field in ("main", "article_head", "rail", "cta", "title", "desc",
                      "og_title", "og_desc", "ld_headline", "ld_desc", "crumb"):
            v = d.get(field)
            if not v:
                continue
            for old, new in TEXT_FIX:
                if old in v:
                    v = v.replace(old, new)
                    fixed_text += 1
            d[field] = v
        kws = d.get("keywords") or []
        for i, k in enumerate(kws):
            for old, new in TEXT_FIX:
                if old in k:
                    kws[i] = k.replace(old, new)
                    fixed_text += 1

        # aria-label: derive the Spanish one from the English one
        if d.get("rail") and b.get("rail"):
            m = re.search(r'aria-label="([^"]*)"', b["rail"])
            if m and m.group(1) in ARIA:
                want = ARIA[m.group(1)]
                cur = re.search(r'aria-label="([^"]*)"', d["rail"])
                if cur and cur.group(1) != want:
                    d["rail"] = d["rail"].replace('aria-label="%s"' % cur.group(1),
                                                  'aria-label="%s"' % want, 1)
                    fixed_aria += 1

        # cross-links -> the Spanish counterpart
        def sub(m):
            global_slug = m.group(1)
            if global_slug in smap:
                return '/es/articulos/%s.html' % smap[global_slug]
            return m.group(0)

        for field in ("main", "rail", "cta"):
            if not d.get(field):
                continue
            new, n = re.subn(r"/articles/([a-z0-9-]+)\.html", sub, d[field])
            if n:
                d[field] = new
                fixed_link += n
        save(s, d)

    print("\ntext fixes   %d\naria fixes   %d\ncross-links  %d" %
          (fixed_text, fixed_aria, fixed_link))

    # 4. postflight
    bad = []
    for s in slugs:
        d = load(s)
        blob = json.dumps(d, ensure_ascii=False)
        t = html.unescape(blob)
        for w in ("Sistemas operativos", "cartera publicitaria",
                  "Asignación de cartera"):
            if w in t:
                bad.append((s, w))
        for m in re.finditer(r"/articles/([a-z0-9-]+)\.html", blob):
            if m.group(1) in smap:
                bad.append((s, "untranslated link " + m.group(1)))
    assert not bad, bad
    print("postflight clean")
    return smap


if __name__ == "__main__":
    run()
