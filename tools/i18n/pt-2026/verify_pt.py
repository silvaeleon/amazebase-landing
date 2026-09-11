# -*- coding: utf-8 -*-
"""
Postflight over every built Portuguese page. Whole document, head included.

    python tools/i18n/pt-2026/verify_pt.py <site-root> <content-dir> <briefs-dir>

HANDOVER 1.1: the Spanish postflight was scoped to the body, so a head that
declared the English URL, name and article list shipped past it. This one reads
the whole document. The ONLY things it does not read are <style> blocks and
HTML comments -- neither renders, and both carry the English source's own
comments. That exclusion is printed with every run so it cannot be forgotten.
"""

import glob, html, io, json, os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gate, langlinks, build_pt

SITE = build_pt.SITE
# Chrome pages that will exist when Portuguese is complete, not in the pilot.
PENDING = {"/pt/recursos.html", "/pt/produto.html", "/pt/solucoes.html",
           "/pt/sobre.html", "/pt/contato.html"}
VOID = gate.P.VOID


class Balance(HTMLParser):
    """Every non-void element closed, in order. The page parses as written."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append("line %d: </%s> but open is %s" % (
                self.getpos()[0], tag, self.stack[-1] if self.stack else None))
            names = [t for t, _ in self.stack]
            if tag in names:
                while self.stack and self.stack[-1][0] != tag:
                    self.stack.pop()
                self.stack.pop()
            return
        self.stack.pop()


def urls(s):
    out = []
    for name, val in re.findall(r'\b(href|src|srcset|imagesrcset|poster)="([^"]*)"', s):
        if name in ("srcset", "imagesrcset"):
            out += [(name, c.strip().split()[0]) for c in val.split(",") if c.strip()]
        else:
            out.append((name, val))
    return out


def body_skeleton(s, href_back):
    """Structural fingerprint of <body>, with the switcher rows removed (the
    Portuguese page has one more) and every href mapped back to English."""
    b = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    b = re.sub(r"<style>.*?</style>", "", b, flags=re.S)
    m = re.search(r"<body[\s>]", b)
    b = b[m.start():]
    b = langlinks.MENU_RUN.sub(lambda m: m.group(1) + m.group(3), b)
    b = build_pt.rootify(b)     # ../assets -> /assets on the English side, a no-op on ours
    b = re.sub(r'href="([^"]*)"', lambda m: 'href="%s"' % href_back(m.group(1)), b)
    return gate.P.skeleton(b)


def check_page(tree, tr, brief, pt_map):
    slug, sl = tr["slug"], tr["pt_slug"]
    en_rel, pt_rel = "articles/%s.html" % slug, "pt/artigos/%s.html" % sl
    en_url, pt_url = "%s/%s" % (SITE, en_rel), "%s/%s" % (SITE, pt_rel)
    raw = io.open(os.path.join(tree, pt_rel), "rb").read()
    s = raw.decode("utf-8")
    en = io.open(os.path.join(tree, en_rel), encoding="utf-8").read()
    P, facts = [], []

    if b"\r" in raw:
        P.append("CR bytes in file")
    if b"\xef\xbf\xbd" in raw:
        P.append("U+FFFD replacement character in file")

    # ---- slug: both caps, refused not trimmed
    nc, nw = len(sl), len(sl.split("-"))
    facts.append("slug %s = %d chars / %d words (caps 50 / 7)" % (sl, nc, nw))
    if nc > 50 or nw > 7:
        P.append("slug over the caps")

    # ---- parses as written
    bal = Balance()
    bal.feed(s)
    bal.close()
    if bal.errors or bal.stack:
        P.append("unbalanced: %s open %s" % (bal.errors[:3], [t for t, _ in bal.stack][:5]))

    # ---- head facts
    one = lambda pat: re.findall(pat, s)
    if one(r'<html lang="([^"]*)"') != ["pt"]:
        P.append("html lang %s" % one(r'<html lang="([^"]*)"'))
    if one(r'<link rel="canonical" href="([^"]*)"') != [pt_url]:
        P.append("canonical %s" % one(r'<link rel="canonical" href="([^"]*)"'))
    for prop, want in (("og:url", [pt_url]), ("og:locale", ["pt_BR"]),
                       ("og:locale:alternate", ["en_US"]),
                       ("og:title", [tr["og_title"]]), ("og:description", [tr["og_desc"]])):
        got = one(r'<meta property="%s" content="([^"]*)"' % re.escape(prop))
        if got != want:
            P.append("%s is %s, want %s" % (prop, got, want))
    if one(r"<title>(.*?) &mdash; AmazeBase</title>") != [tr["title"]]:
        P.append("title")
    alts = one(r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)"')
    want_alt = [("en", "%s/%s" % (SITE, en_rel))]
    esm = json.load(io.open(os.path.join(tree, "tools", "i18n", "slugs", "es.json"), encoding="utf-8"))
    if slug in esm:
        want_alt.append(("es", "%s/es/articulos/%s.html" % (SITE, esm[slug])))
    want_alt += [("pt", pt_url), ("x-default", "%s/%s" % (SITE, en_rel))]
    if alts != want_alt:
        P.append("alternates %s" % alts)
    facts.append("alternates: %s" % " ".join(h for h, _ in alts))

    # ---- JSON-LD: every block parses; the Article node is Portuguese
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    nodes = []
    for b in blocks:
        try:
            d = json.loads(b)
        except ValueError as e:
            P.append("JSON-LD does not parse: %s" % e)
            continue
        nodes += d.get("@graph", [d])
    if blocks:
        art = [n for n in nodes if n.get("@type") in ("Article", "BlogPosting")]
        crumbs = [n for n in nodes if n.get("@type") == "BreadcrumbList"]
        if len(art) != 1:
            P.append("%d Article nodes" % len(art))
        else:
            a = art[0]
            for k, want in (("@id", pt_url + "#article"), ("inLanguage", "pt"),
                            ("headline", tr["ld_headline"]), ("description", tr["ld_desc"]),
                            ("keywords", tr["keywords"])):
                if a.get(k) != want:
                    P.append("Article %s = %r" % (k, a.get(k)))
            if (a.get("mainEntityOfPage") or {}).get("@id") != pt_url:
                P.append("Article mainEntityOfPage")
        items = crumbs[0]["itemListElement"] if crumbs else []
        got = [(i.get("name"), i.get("item")) for i in items]
        want = [(u"Início", SITE + "/"), ("Central de Conhecimento", SITE + "/pt/recursos.html"),
                (tr["crumb"], None)]
        if [g[0] for g in got] != [w[0] for w in want] or got[1][1] != want[1][1]:
            P.append("breadcrumbs %s" % got)
        facts.append("JSON-LD: %d blocks parse, Article inLanguage pt, breadcrumbs %s"
                     % (len(blocks), " > ".join(g[0] for g in got)))
    else:
        facts.append("JSON-LD: none (the English page has none either)" if
                     "application/ld+json" not in en else "JSON-LD MISSING")
        if "application/ld+json" in en:
            P.append("English has JSON-LD, Portuguese has none")

    # ---- nothing English left, anywhere except <style> and comments
    visible = re.sub(r"<style>.*?</style>", " ", s, flags=re.S)
    visible = re.sub(r"<!--.*?-->", " ", visible, flags=re.S)
    for k in ("title", "desc", "og_title", "og_desc", "og_img_alt", "hero_alt",
              "ld_headline", "ld_desc", "crumb"):
        v = brief.get(k)
        if v and len(v) > 12 and (v in visible or build_pt.ld(v) in visible):
            P.append("English %s survives: %.60r" % (k, v))
    left = [t for t in build_pt.CHROME_TEXT if re.search(r">\s*%s\s*<" % re.escape(t), visible)]
    left += ["aria-label=%s" % a for a in build_pt.CHROME_ARIA
             if 'aria-label="%s"' % a in visible]
    for phrase in ("Skip to content", "min read", "The fix", "What to do", "Worked example",
                   "Key figures from this article", "Final thoughts", "Frequently asked"):
        if phrase in visible:
            left.append(phrase)
    if left:
        P.append("English chrome left: %s" % left)
    text = " " + re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", visible))) + " "
    # the switcher's own row names the English page in English, by design
    text = text.replace(" EN English ", " ")
    hits = [w for w in gate.STOP_EN if w in text]
    if hits:
        P.append("English stopwords in the rendered document: %s" % hits)

    # ---- every URL resolves; nothing relative
    # "Nothing relative" covers comments too: an empty hero slot is meant to be
    # uncommented one day, and under /pt/ a relative path would 404 the moment
    # it is. "Resolves" covers live markup only: the slot's image does not
    # exist yet by design (HANDOVER 6.7).
    rel = [(n, u) for n, u in urls(s) if not re.match(r"^(/|#|[a-z]+:)", u)]
    missing, pending = [], set()
    for name, u in urls(re.sub(r"<!--.*?-->", " ", s, flags=re.S)):
        if re.match(r"^(#|[a-z]+:)", u) or not u.startswith("/"):
            continue
        path = u.split("#")[0].split("?")[0]
        f = os.path.join(tree, path.lstrip("/"))
        if os.path.isfile(f) or os.path.isfile(f + ".html"):
            continue
        # a top-level page not built yet is pending; once it exists it is checked
        if path in PENDING:
            pending.add(path)
            continue
        missing.append((name, u))
    if rel:
        P.append("relative URLs: %s" % rel[:5])
    if missing:
        P.append("URLs that resolve to nothing: %s" % sorted(set(missing))[:8])
    facts.append("URLs: all resolve" + ("" if not pending else
                 "; %d point at Portuguese chrome pages not built yet: %s" % (len(pending), " ".join(sorted(pending)))))

    # ---- the hero alt: one string in three places, 8-14 words
    live = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    m = re.search(r'<figure class="hero-shot">.*?alt="([^"]*)"', live, re.S)
    og = one(r'<meta property="og:image:alt" content="([^"]*)"')
    tw = one(r'<meta name="twitter:image:alt" content="([^"]*)"')
    if m:
        alt = m.group(1)
        nwd = len(html.unescape(alt).split())
        if og != [alt] or tw != [alt]:
            P.append("hero alt / og:image:alt / twitter:image:alt disagree")
        if not 8 <= nwd <= 14:
            P.append("hero alt is %d words" % nwd)
        facts.append("hero alt %d words, identical in img / og:image:alt / twitter:image:alt" % nwd)
    else:
        # No hero: the share image is a placeholder (the hub's picture, as
        # og-<slug>.jpg) until the real one exists, and seo.py's fallback alt
        # is the page's og:title. So the alt must be present in both places
        # and be exactly the og:title -- anything else is a real mismatch.
        ogt = one(r'<meta property="og:title" content="([^"]*)"')
        img = one(r'<meta property="og:image" content="https://amazebase.pro/([^"]+)"')
        if og or tw or img:
            if og != ogt or tw != ogt:
                P.append("no hero: image alts must both equal og:title (og %s, twitter %s)" % (og, tw))
            if not img or not os.path.isfile(os.path.join(tree, img[0])):
                P.append("no hero: og:image missing or not on disk (%s)" % img)
        facts.append("no hero (empty slot); share image %s, alt = og:title in og and twitter"
                     % (img[0] if img else "absent"))

    # ---- body skeleton identical to the English page, hrefs mapped back
    back = dict((pt, en) for en, pt in build_pt.CHROME_HREF.items())
    back.update(("/pt/artigos/%s.html" % v, "/articles/%s.html" % k) for k, v in pt_map.items())

    def href_back(h):
        base, _, frag = h.partition("#")
        return back.get(base, base) + ("#" + frag if frag else "")
    ka, kb = body_skeleton(en, href_back), body_skeleton(s, href_back)
    d = None
    if ka != kb:
        n = min(len(ka), len(kb))
        i = next((x for x in range(n) if ka[x] != kb[x]), n)
        d = "element %d: EN %s / PT %s (EN %d, PT %d)" % (
            i, ka[i] if i < len(ka) else None, kb[i] if i < len(kb) else None, len(ka), len(kb))
        P.append("body skeleton differs from English: " + d)
    facts.append("body skeleton: %d elements, identical to the English page" % len(ka) if not d
                 else "body skeleton DIFFERS")
    return P, facts


def main(tree, content, briefs):
    trs = [json.load(io.open(f, encoding="utf-8"))
           for f in sorted(glob.glob(os.path.join(content, "*.json")))]
    pt_map = dict((t["slug"], t["pt_slug"]) for t in trs)
    print("verify_pt: whole document, head included. NOT checked: <style> blocks and"
          " HTML comments (never rendered; carry the English source's comments).\n")
    bad = 0
    for t in trs:
        brief = json.load(io.open(os.path.join(briefs, t["slug"] + ".json"), encoding="utf-8"))
        P, facts = check_page(tree, t, brief, pt_map)
        bad += len(P)
        print("%-4s /pt/artigos/%s.html" % ("OK" if not P else "FAIL", t["pt_slug"]))
        for f in facts:
            print("       " + f)
        for p in P:
            print("   !!  " + p)
    print("\n%d pages, %d problems" % (len(trs), bad))
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
