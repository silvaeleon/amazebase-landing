# -*- coding: utf-8 -*-
"""
Portuguese hub data: data/resources.json and js/hub.js.

    PT_BRIEFS=<article briefs> python tools/i18n/pt-2026/hub_pt.py <site-root>

resources.json
  * label_pt beside every label_es (and label_one_pt beside label_one_es) on
    the 6 categories, 7 formats, 2 levels and the language rows; a pt row
    appended to `languages`
  * 51 rows made by hubrows.translated_row(): the WHOLE English entry, with only
    id, title, summary, url, topics and language replaced. Title and summary
    come from the approved article translation wherever the English row copies
    the article's own head string (all 51 titles, 44 summaries); the other 7
    summaries and the 84 topic tags come from hub-data-pt.json.
  Text is inserted into the file as written, never re-serialised -- and the
  serialiser is proven first by regenerating an existing Spanish row with it
  and asserting it matches the file byte for byte.

js/hub.js
  * a `pt` column in STR (21 strings)
  * formatDate() picks pt-BR for Portuguese -- it was hard-wired to es/en
"""

import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import hubrows


def entry_text(e):
    """One resources[] entry exactly as the file writes it: 4-space base indent."""
    return "\n".join("    " + ln for ln in json.dumps(e, indent=2, ensure_ascii=False).split("\n"))


def insert_after_line(s, anchor_line, new_line, n=1):
    c = s.count(anchor_line)
    assert c == n, (anchor_line, c)
    return s.replace(anchor_line, anchor_line + new_line)


def patch_resources(tree, hd, briefs):
    p = os.path.join(tree, "data", "resources.json")
    s = io.open(p, encoding="utf-8", newline="").read()
    assert "\r" not in s
    data = json.loads(s)
    assert not any(r.get("language") == "pt" for r in data["resources"]), "pt rows already present"

    # ---- the serialiser must reproduce what is on disk
    es_row = [r for r in data["resources"] if r.get("language") == "es"][0]
    assert entry_text(es_row) in s, "entry_text() does not reproduce the file's formatting"

    # ---- taxonomy labels
    tx = hd["taxonomy"]
    for c in data["categories"]:
        s = insert_after_line(s, '      "label_es": %s,\n' % json.dumps(c["label_es"], ensure_ascii=False),
                              '      "label_pt": %s,\n' % json.dumps(tx["categories"][c["id"]], ensure_ascii=False))
    for f in data["formats"]:
        t = tx["formats"][f["id"]]
        s = insert_after_line(s, '      "label_es": %s,\n' % json.dumps(f["label_es"], ensure_ascii=False),
                              '      "label_pt": %s,\n' % json.dumps(t["label_pt"], ensure_ascii=False))
        s = insert_after_line(s, '      "label_one_es": %s,\n' % json.dumps(f["label_one_es"], ensure_ascii=False),
                              '      "label_one_pt": %s,\n' % json.dumps(t["label_one_pt"], ensure_ascii=False))
    # levels and languages end on label_es with no trailing comma
    for group, labels in (("levels", tx["levels"]), ("languages", tx["languages"])):
        for o in data[group]:
            old = '      "label_es": %s\n' % json.dumps(o["label_es"], ensure_ascii=False)
            assert s.count(old) == 1, old
            s = s.replace(old, '      "label_es": %s,\n      "label_pt": %s\n'
                          % (json.dumps(o["label_es"], ensure_ascii=False),
                             json.dumps(labels[o["id"]], ensure_ascii=False)), 1)
    # the pt language row. Its label follows the Spanish row, which is named in
    # its own language ("Español"), so this one is "Português".
    nl = {"id": "pt", "label": u"Português", "label_es": u"Portugués", "label_pt": u"Português"}
    last = json.loads(s)["languages"][-1]
    old_txt = "\n".join("    " + ln for ln in json.dumps(last, indent=2, ensure_ascii=False).split("\n"))
    assert s.count(old_txt + "\n  ]") == 1, "languages array end not found"
    s = s.replace(old_txt + "\n  ]", old_txt + ",\n" + "\n".join(
        "    " + ln for ln in json.dumps(nl, indent=2, ensure_ascii=False).split("\n")) + "\n  ]", 1)

    # ---- 51 Portuguese rows
    content = os.path.join(HERE, "content")
    data2 = json.loads(s)
    en_rows = [r for r in data2["resources"] if r.get("language") == "en"]
    new_rows = []
    for r in en_rows:
        slug = os.path.basename(r["url"])[:-5]
        b = json.load(io.open(os.path.join(briefs, slug + ".json"), encoding="utf-8"))
        t = json.load(io.open(os.path.join(content, slug + ".json"), encoding="utf-8"))
        title = None
        for k in ("title", "og_title", "ld_headline", "crumb"):
            if b.get(k) and html.unescape(b[k]) == r["title"]:
                title = html.unescape(t[k])
                break
        assert title, "no Portuguese title for %s" % slug
        summary = None
        for k in ("desc", "og_desc", "ld_desc"):
            if b.get(k) and html.unescape(b[k]) == r["summary"]:
                summary = html.unescape(t[k])
                break
        if summary is None:
            summary = hd["summaries"][r["id"]]
        topics = [hd["topics"][x] for x in r.get("topics") or []]
        new_rows.append(hubrows.translated_row(
            r, id=r["id"] + "-pt", title=title, summary=summary,
            url="pt/artigos/%s.html" % t["pt_slug"], topics=topics, language="pt"))
    tail = "\n  ],\n  \"_testimonials_README\""
    assert s.count(tail) == 1
    s = s.replace(tail, ",\n" + ",\n".join(entry_text(e) for e in new_rows) + tail, 1)

    final = json.loads(s)
    checked, prob = hubrows.check(final)
    assert not prob, prob[:5]
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    return len(new_rows), checked


def patch_hubjs(tree, strmap):
    p = os.path.join(tree, "js", "hub.js")
    s = io.open(p, encoding="utf-8", newline="").read()
    assert "\r" not in s and "\n    pt: {" not in s
    a = s.index("  var STR = {")
    es_keys = re.findall(r'^      "([^"]+)":', s[a:s.index("\n  };", a)], re.M)
    keys = [json.loads('"%s"' % k) for k in es_keys]
    assert set(keys) == set(strmap), (set(keys) ^ set(strmap))
    lines = []
    for k in keys:
        lines.append('      %s:\n        %s' % (json.dumps(k), json.dumps(strmap[k])))
    col = "    pt: {\n" + ",\n".join(lines) + "\n    }"
    end = s.index("\n  };", a)
    before = s[:end]
    assert before.rstrip().endswith("}"), "es column end not found"
    s = before + ",\n" + col + s[end:]
    old = 'return d.toLocaleDateString(LANG === "es" ? "es-ES" : "en-GB",'
    new = 'return d.toLocaleDateString({ es: "es-ES", pt: "pt-BR" }[LANG] || "en-GB",'
    assert s.count(old) == 1
    s = s.replace(old, new)
    old = "  /* The hub exists at /resources.html and /es/recursos.html and is driven by"
    new = "  /* The hub exists at /resources.html, /es/recursos.html and /pt/recursos.html, driven by"
    assert s.count(old) == 1
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    return len(keys)


if __name__ == "__main__":
    tree = sys.argv[1]
    hd = json.load(io.open(os.path.join(HERE, "hub-data-pt.json"), encoding="utf-8"))
    n, checked = patch_resources(tree, hd, os.environ["PT_BRIEFS"])
    print("resources.json: %d Portuguese rows added; hubrows.check: %d translations checked, 0 problems" % (n, checked))
    k = patch_hubjs(tree, hd["str"])
    print("hub.js: pt column with %d strings; formatDate picks pt-BR" % k)
