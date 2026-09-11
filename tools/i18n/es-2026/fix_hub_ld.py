# -*- coding: utf-8 -*-
"""
Fix the JSON-LD on both hub pages.

Two faults, one mine and one inherited:

  * /es/recursos.html shipped the English page's structured data verbatim. It
    told search engines the page was https://amazebase.pro/resources.html, gave
    an English name and description, and listed 44 English articles. Nothing a
    visitor sees, everything a crawler does.

  * /resources.html's own hasPart still listed 44 articles, not 51 -- the same
    staleness the static no-JS fallback had.

My postflight missed the first because it only checked the rendered body:
`body = s[s.index("</head>"):]`. The JSON-LD lives in the head. The check at
the bottom of this file now covers the whole document.
"""

import io, os, re, json

OUT = "/home/claude/esout3"
SITE = "https://amazebase.pro"

ES_NAME = "Centro de Conocimiento para vendedores de Amazon"
ES_DESC = ("Artículos, guías y podcasts para vendedores de Amazon: inventario, "
           "publicidad, utilidad, flujo de caja e investigación de productos.")


def ld_block(s):
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    assert m, "no JSON-LD"
    return m


def has_part(resources, lang):
    rows = [r for r in resources if r.get("language") == lang]
    rows.sort(key=lambda r: r.get("published", ""), reverse=True)
    out = []
    for r in rows:
        url = "%s/%s" % (SITE, r["url"])
        out.append({
            "@type": "Article",
            "@id": url + "#article",
            "headline": r["title"],
            "url": url,
            "datePublished": r.get("published", ""),
        })
    return out


def patch(path, lang, name=None, desc=None, page_url=None):
    p = os.path.join(OUT, path.lstrip("/"))
    s = io.open(p, encoding="utf-8").read()
    m = ld_block(s)
    d = json.loads(m.group(2))

    taxo = json.load(io.open(os.path.join(OUT, "data", "resources.json"), encoding="utf-8"))
    cp = [n for n in d["@graph"] if n["@type"] == "CollectionPage"]
    assert len(cp) == 1
    cp = cp[0]

    before = len(cp.get("hasPart", []))
    if page_url:
        cp["@id"] = page_url + "#collection"
        cp["url"] = page_url
    if name:
        cp["name"] = name
    if desc:
        cp["description"] = desc
    cp["inLanguage"] = lang
    cp["hasPart"] = has_part(taxo["resources"], lang)

    body = json.dumps(d, indent=2, ensure_ascii=False)
    s = s[:m.start(2)] + "\n" + body + "\n" + s[m.end(2):]
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("%-22s hasPart %d -> %d, inLanguage=%s%s"
          % (path, before, len(cp["hasPart"]), lang,
             ", url/name/description localised" if page_url else ""))
    return s


if __name__ == "__main__":
    patch("/resources.html", "en")
    es = patch("/es/recursos.html", "es", ES_NAME, ES_DESC, SITE + "/es/recursos.html")

    # ---- postflight over the WHOLE document, head included. The miss that
    #      produced this file was a check scoped to the body.
    for bad in ("Knowledge Hub", "Amazon Seller Knowledge Hub",
                "Actionable insights", SITE + "/resources.html#collection"):
        assert bad not in es, "Spanish hub still carries %r" % bad
    for good in ('"inLanguage": "es"', SITE + "/es/recursos.html#collection",
                 ES_NAME):
        assert good in es, "Spanish hub missing %r" % good
    d = json.loads(ld_block(es).group(2))
    cp = [n for n in d["@graph"] if n["@type"] == "CollectionPage"][0]
    assert len(cp["hasPart"]) == 51
    assert all("/es/articulos/" in a["url"] for a in cp["hasPart"])
    en = io.open(os.path.join(OUT, "resources.html"), encoding="utf-8").read()
    d2 = json.loads(ld_block(en).group(2))
    cp2 = [n for n in d2["@graph"] if n["@type"] == "CollectionPage"][0]
    assert len(cp2["hasPart"]) == 51
    assert all("/articles/" in a["url"] for a in cp2["hasPart"])
    print("postflight clean (whole document, head included)")
