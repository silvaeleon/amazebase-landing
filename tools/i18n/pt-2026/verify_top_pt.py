# -*- coding: utf-8 -*-
"""
Postflight over the five Portuguese top-level pages. Whole document.

    python tools/i18n/pt-2026/verify_top_pt.py <site-root>

NOT checked, printed every run: <style> blocks and HTML comments (never
rendered). <script> blocks are excluded from the English-stopword scan only --
the JSON-LD is parsed and its localised nodes checked field by field instead,
because the Organization and WebSite nodes describe the English site and stay
English, as they do on every Spanish page.
"""

import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gate, langlinks, locallinks, build_pt as BP, verify_pt as VP, build_top_pt as BT

SITE = BP.SITE


def check(tree, key, en_rel, pt_rel, es_rel, tr, pt_map):
    P, facts = [], []
    raw = io.open(os.path.join(tree, pt_rel), "rb").read()
    s = raw.decode("utf-8")
    en = io.open(os.path.join(tree, en_rel), encoding="utf-8").read()
    pt_url = "%s/%s" % (SITE, pt_rel)
    if b"\r" in raw:
        P.append("CR bytes")
    if b"\xef\xbf\xbd" in raw:
        P.append("U+FFFD in file")

    bal = VP.Balance()
    bal.feed(s)
    bal.close()
    if bal.errors or bal.stack:
        P.append("unbalanced: %s %s" % (bal.errors[:3], [t for t, _ in bal.stack][:4]))

    one = lambda pat: re.findall(pat, s)
    for pat, want in ((r'<html lang="([^"]*)"', ["pt"]),
                      (r'<link rel="canonical" href="([^"]*)"', [pt_url]),
                      (r'<meta property="og:url" content="([^"]*)"', [pt_url]),
                      (r'<meta property="og:locale" content="([^"]*)"', ["pt_BR"]),
                      (r'<meta property="og:title" content="([^"]*)"', [tr["og_title"]]),
                      (r'<meta property="og:image:alt" content="([^"]*)"', [tr["og_img_alt"]]),
                      (r"<title>(.*?)</title>", [tr["title"]])):
        if one(pat) != want:
            P.append("%s -> %s" % (pat[:40], one(pat)[:2]))
    alts = [h for h, _ in one(r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)"')]
    if alts != ["en", "es", "pt", "x-default"]:
        P.append("alternates %s" % alts)
    facts.append("alternates: %s" % " ".join(alts))

    # JSON-LD
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    g = json.loads(m.group(1))["@graph"]
    crumbs = [n for n in g if n.get("@type") == "BreadcrumbList"][0]["itemListElement"]
    names = [c["name"] for c in crumbs]
    if names[0] != u"Início" or names[-1] != tr["crumb"]:
        P.append("breadcrumbs %s" % names)
    facts.append("JSON-LD parses; breadcrumbs %s" % " > ".join(names))
    if key == "resources":
        cp = [n for n in g if n.get("@type") == "CollectionPage"][0]
        parts = cp.get("hasPart", [])
        ok = (cp.get("inLanguage") == "pt" and cp.get("url") == pt_url and cp.get("@id") == pt_url + "#collection"
              and len(parts) == 51 and all("/pt/artigos/" in p_["url"] for p_ in parts)
              and all(os.path.isfile(os.path.join(tree, p_["url"].split(SITE + "/")[1])) for p_ in parts))
        if not ok:
            P.append("CollectionPage not Portuguese / hasPart wrong")
        facts.append("CollectionPage inLanguage %s, %d hasPart, all /pt/artigos/ and on disk: %s"
                     % (cp.get("inLanguage"), len(parts), ok))
        rows = re.findall(r'<a class="hub-row" href="([^"]+)"', s)
        missing = [h for h in rows if not os.path.isfile(os.path.join(tree, h.lstrip("/")))]
        if len(rows) != 51 or missing or not all(h.startswith("/pt/artigos/") for h in rows):
            P.append("fallback rows %d, missing %s" % (len(rows), missing[:3]))
        facts.append("fallback: %d rows, all /pt/artigos/, all on disk" % len(rows))

    # English left in the rendered page
    visible = re.sub(r"<style>.*?</style>|<!--.*?-->|<script\b.*?</script>", " ", s, flags=re.S)
    left = [t for t in BP.CHROME_TEXT if re.search(r">\s*%s\s*<" % re.escape(t), visible)]
    for phrase in ("Skip to content", "Back to top", "Join the wait list", "Knowledge Hub"):
        if phrase in visible:
            left.append(phrase)
    if left:
        P.append("English chrome left: %s" % left)
    text = " " + re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", visible))) + " "
    text = text.replace(" EN English ", " ")
    hits = [w for w in gate.STOP_EN if w in text]
    if hits:
        P.append("English stopwords: %s" % hits)

    # the waitlist / request dialog
    if key != "resources":
        d = re.search(r'<dialog class="wl" id="waitlist".*?</dialog>', s, re.S).group(0)
        for keep in ('name="company_website"', 'name="referral_code"', 'data-waitlist-submit', 'name="marketplace"'):
            if keep not in d:
                P.append("dialog lost %s" % keep)
        msgs = re.findall(r'\bdata-msg-(\w+)="([^"]+)"', d[:d.index(">")])
        if [k for k, _ in msgs] != ["name", "email", "market", "sending", "rate", "generic", "network"]:
            P.append("data-msg-* %s" % msgs)
        en_c = re.search(r"<!-- Honeypots\..*?-->", en, re.S).group(0)
        if en_c not in d:
            P.append("the English honeypot comment is not verbatim")
        facts.append("dialog: honeypots company_website + referral_code intact, 7 data-msg-* strings, "
                     "developer comment verbatim")
    else:
        d = re.search(r'<dialog class="wl" id="request".*?</dialog>', s, re.S).group(0)
        if 'name="company_website"' not in d:
            P.append("request dialog lost its honeypot")
        facts.append("request dialog: honeypot company_website intact")

    # URLs
    rel = [(n, u) for n, u in VP.urls(s) if not re.match(r"^(/|#|[a-z]+:)", u)]
    live = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    miss = []
    for n, u in VP.urls(live):
        if re.match(r"^(#|[a-z]+:)", u) or not u.startswith("/"):
            continue
        f = os.path.join(tree, u.split("#")[0].split("?")[0].lstrip("/"))
        folder = os.path.join(tree, langlinks.file_of(u.split("#")[0].split("?")[0].lstrip("/")))
        if not os.path.isfile(f) and not os.path.isfile(f + ".html") and not os.path.isfile(folder):
            miss.append(u)
    if rel:
        P.append("relative URLs %s" % rel[:4])
    if miss:
        P.append("URLs resolving to nothing %s" % sorted(set(miss))[:6])
    facts.append("URLs: none relative, all resolve")

    # body structure against the English page
    back = dict((pt, en_) for en_, pt in BP.CHROME_HREF.items())
    back.update(("/pt/artigos/%s.html" % v, "/articles/%s.html" % k) for k, v in pt_map.items())
    back.update(locallinks.back_map(BP.load_cfg()[0], "pt"))

    def hb(h):
        b_, _, f_ = h.partition("#")
        return back.get(b_, b_) + ("#" + f_ if f_ else "")
    ka, kb = VP.body_skeleton(en, hb), VP.body_skeleton(s, hb)
    if ka != kb:
        n = min(len(ka), len(kb))
        i = next((x for x in range(n) if ka[x] != kb[x]), n)
        P.append("body skeleton differs at element %d: EN %s / PT %s (EN %d, PT %d)"
                 % (i, ka[i] if i < len(ka) else None, kb[i] if i < len(kb) else None, len(ka), len(kb)))
    else:
        facts.append("body skeleton: %d elements, identical to the English page" % len(ka))
    return P, facts


def main(tree):
    pt_map = json.load(io.open(os.path.join(tree, "tools", "i18n", "slugs", "pt.json"), encoding="utf-8"))
    content = os.path.join(HERE, "content-top")
    print("verify_top_pt: whole document. NOT checked: <style> blocks and HTML comments; "
          "<script> excluded from the stopword scan only (JSON-LD checked field by field).\n")
    bad = n = 0
    for key, en_rel, pt_rel, es_rel in BT.PAGES:
        if not os.path.exists(os.path.join(tree, pt_rel)):
            print("MISSING /%s" % pt_rel)
            bad += 1
            continue
        n += 1
        tr = json.load(io.open(os.path.join(content, key + ".json"), encoding="utf-8"))
        P, facts = check(tree, key, en_rel, pt_rel, es_rel, tr, pt_map)
        bad += len(P)
        print("%-4s /%s" % ("OK" if not P else "FAIL", pt_rel))
        for f in facts:
            print("       " + f)
        for p in P:
            print("   !!  " + p)
    print("\n%d pages, %d problems" % (n, bad))
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1])
