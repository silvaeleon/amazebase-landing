# -*- coding: utf-8 -*-
"""Independent gate over every translated article. Run before any build."""
import sys, io, json, re, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P

# A comma is a thousands separator only when digits follow it. Without this,
# "antes del 14, y 900" reads as the number "14," and diverges from "the 14th".
NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
ENTITY = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);")


def nums(frag):
    return NUM.findall(re.sub(r"<[^>]+>", " ", frag))


def audit(slug):
    es = json.load(io.open("/home/claude/escontent/%s.json" % slug, encoding="utf-8"))
    b = P.brief(slug)
    prob = []
    for field in ("main", "article_head", "rail", "cta"):
        en_v, es_v = b.get(field), es.get(field)
        if en_v is None:
            if es_v:
                prob.append("%s: EN has none, ES supplied one" % field)
            continue
        if not es_v:
            prob.append("%s: missing from the translation" % field)
            continue
        d = P.skeleton_diff(en_v, es_v)
        if d:
            prob.append("%s skeleton:\n%s" % (field, d))
    if prob:
        return es, prob

    for k, pat in (("ids", r'\bid="([^"]+)"'), ("hrefs", r'\bhref="([^"]+)"')):
        a, c = re.findall(pat, b["main"]), re.findall(pat, es["main"])
        if a != c:
            prob.append("%s differ\n  EN %s\n  ES %s" % (k, a, c))

    a, c = nums(b["main"]), nums(es["main"])
    if a != c:
        prob.append("figures differ\n  EN %s\n  ES %s" % (a, c))

    text = " " + re.sub(r"<[^>]+>", " ", es["main"]) + " "
    hits = [w for w in P.STOP_EN if w in text]
    if hits:
        prob.append("English survived: %s" % hits)

    # JSON-LD fields are plain text; an HTML entity there would render literally
    for k in ("ld_headline", "ld_desc", "crumb"):
        if es.get(k) and ENTITY.search(es[k]):
            prob.append("HTML entity in plain-text field %s: %r" % (k, es[k]))
    for k in es.get("keywords") or []:
        if ENTITY.search(k):
            prob.append("HTML entity in keyword %r" % k)

    # attribute-bound fields must NOT carry raw accents
    for k in ("title", "desc", "og_title", "og_desc", "og_img_alt", "hero_alt"):
        v = es.get(k)
        if v and re.search(u"[À-ſ]", v):
            prob.append("raw accented character in entity field %s: %r" % (k, v[:70]))
        if k in ("title", "desc", "og_title", "og_desc") and not v:
            prob.append("head string %s missing" % k)

    if not es.get("es_slug") or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", es["es_slug"]):
        prob.append("bad es_slug %r" % es.get("es_slug"))

    return es, prob


if __name__ == "__main__":
    files = sorted(glob.glob("/home/claude/escontent/*.json"))
    bad = 0
    for f in files:
        slug = os.path.basename(f)[:-5]
        es, prob = audit(slug)
        print("%-38s %-4s %s" % (slug, "OK" if not prob else "FAIL", es.get("es_slug", "")))
        for p in prob:
            bad += 1
            print("      " + p.replace("\n", "\n      "))
    print("\n%d files, %d problems" % (len(files), bad))
