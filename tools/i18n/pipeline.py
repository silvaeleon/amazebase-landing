# -*- coding: utf-8 -*-
"""
Translation pipeline for the remaining 48 articles.

The mechanical half is deterministic and lives here. The language half is done
by a translator (a subagent), which returns only:

    * the Spanish <main> ... </main> block
    * a handful of head strings

Everything a translator returns is checked against the English original before
it is allowed anywhere near a built page. The check that matters is the
STRUCTURAL SKELETON: the ordered sequence of (tag, id, class, href, src) for
every element. If a translation drops a <li>, renames a class, invents a
heading or loses an anchor id, the skeletons differ and the build fails loudly.
That is the failure mode of machine-translated HTML, and it is the one thing a
human proof-reader is worst at catching.
"""

import io, os, re, json, html

SRC = "/mnt/user-data/uploads/amazebase-landing"
BRIEFS = "/home/claude/briefs"
CONTENT = "/home/claude/escontent"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


# ------------------------------------------------------------------ skeleton

def skeleton(frag):
    """Ordered structural fingerprint of an HTML fragment.

    Text is ignored. Attributes that carry meaning for layout, styling,
    anchoring or linking are kept; everything else (alt, title, aria-label,
    caption text) is translatable and therefore ignored."""
    KEEP = ("id", "class", "href", "src", "style", "colspan", "rowspan",
            "scope", "type", "width", "height", "points", "d", "viewBox",
            "data-reveal", "data-source", "datetime", "open", "selected")
    out = []
    for m in re.finditer(r"<(/?)([a-zA-Z][\w:-]*)([^>]*?)(/?)>", frag):
        close, tag, attrs, self_close = m.groups()
        tag = tag.lower()
        if close:
            out.append(("/" + tag,))
            continue
        kept = []
        # Boolean attributes (open, selected) are looked for OUTSIDE quoted
        # values. Searched in the raw tag, the word "open" inside an alt text
        # ("...open purchase orders...") read as an `open` attribute, so the
        # English skeleton had an attribute its correct translation could not
        # have (found 2026-09-11 on solutions.html).
        bare = re.sub(r'"[^"]*"', '""', attrs)
        for a in KEEP:
            am = re.search(r'\b%s="([^"]*)"' % re.escape(a), attrs)
            if am:
                v = am.group(1)
                # hrefs and ids must survive translation; a #anchor that
                # changes silently breaks the table of contents.
                kept.append((a, v))
            elif re.search(r"\b%s(?=[\s>]|$)" % re.escape(a), bare):
                kept.append((a, ""))
        out.append((tag, tuple(kept)))
        if tag in VOID or self_close:
            pass
    return out


def skeleton_diff(en, es):
    a, b = skeleton(en), skeleton(es)
    if a == b:
        return None
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return ("first difference at element %d\n  EN: %s\n  ES: %s"
                    % (i, a[i], b[i]))
    return "length differs: EN %d elements, ES %d" % (len(a), len(b))


# ------------------------------------------------------------------- extract

def region(s, start, end):
    i = s.index(start)
    j = s.index(end, i) + len(end)
    return s[i:j]


def head_strings(s):
    def one(pat, group=1):
        m = re.search(pat, s, re.S)
        return m.group(group) if m else None
    d = {
        "title":       one(u"<title>(.*?)\\s*(?:&mdash;|\u2014)\\s*AmazeBase</title>"),
        "desc":        one(r'<meta name="description" content="([^"]*)"'),
        "og_title":    one(r'<meta property="og:title" content="([^"]*)"'),
        "og_desc":     one(r'<meta property="og:description" content="([^"]*)"'),
        "og_img_alt":  one(r'<meta property="og:image:alt" content="([^"]*)"'),
        "ld_headline": one(r'"headline": "([^"]*)"'),
        "ld_desc":     one(r'"headline": "[^"]*",\s*\n\s*"description": "([^"]*)"'),
        "crumb":       one(r'"position": 3,\s*\n\s*"name": "([^"]*)"'),
    }
    kw = re.search(r'"keywords": \[(.*?)\]', s, re.S)
    d["keywords"] = re.findall(r'"([^"]*)"', kw.group(1)) if kw else []
    return d


def brief(slug):
    p = os.path.join(SRC, "articles", slug + ".html")
    s = io.open(p, encoding="utf-8").read()

    b = {"slug": slug, "has_seo": "<!-- SEO:START -->" in s}
    b.update(head_strings(s))

    b["back_link"] = region(s, '<p class="back-link">', "</p>")
    b["article_head"] = region(s, '<header class="article-head">', "</header>")

    # hero: either a live <figure class="hero-shot"> or a commented-out slot
    # A hero inside an HTML comment is an empty slot, not a hero.
    live = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    m = re.search(r'<figure class="hero-shot">.*?</figure>', live, re.S)
    b["hero"] = m.group(0) if m else None
    b["hero_alt"] = None
    if m:
        am = re.search(r'alt="([^"]*)"', m.group(0))
        b["hero_alt"] = am.group(1) if am else None

    b["main"] = region(s, "<main", "</main>")

    mm = re.search(r'<aside class="rail".*?</aside>', s, re.S)
    b["rail"] = mm.group(0) if mm else None

    mm = re.search(r'<aside class="cta">.*?</aside>', s, re.S)
    b["cta"] = mm.group(0) if mm else None

    b["words"] = len(re.sub(r"<[^>]+>", " ", b["main"]).split())
    return b


def write_briefs(slugs):
    if not os.path.isdir(BRIEFS):
        os.makedirs(BRIEFS)
    for sl in slugs:
        b = brief(sl)
        io.open(os.path.join(BRIEFS, sl + ".json"), "w", encoding="utf-8").write(
            json.dumps(b, ensure_ascii=False, indent=1))
    return len(slugs)


# ------------------------------------------------------------------ validate

STOP_EN = [
    " the ", " and ", " your ", " you ", " that ", " with ", " this ",
    " what ", " which ", " because ", " every ", " most ", " when ",
    "Join the Wait List", "Knowledge Hub", "min read", "The fix", "What to do",
]


def check(slug, es_main, es_head):
    """Raise on anything wrong. Returns a list of soft warnings."""
    b = brief(slug)
    warn = []

    d = skeleton_diff(b["main"], es_main)
    assert d is None, "%s: markup skeleton changed --\n%s" % (slug, d)

    # every anchor id and every internal href must survive
    en_ids = re.findall(r'\bid="([^"]+)"', b["main"])
    es_ids = re.findall(r'\bid="([^"]+)"', es_main)
    assert en_ids == es_ids, "%s: ids changed\n  EN %s\n  ES %s" % (slug, en_ids, es_ids)

    en_href = re.findall(r'\bhref="([^"]+)"', b["main"])
    es_href = re.findall(r'\bhref="([^"]+)"', es_main)
    assert en_href == es_href, "%s: hrefs changed\n  EN %s\n  ES %s" % (slug, en_href, es_href)

    # numbers must not drift. Currency and quantities carry meaning.
    en_num = re.findall(r"\d[\d,\.]*", re.sub(r"<[^>]+>", " ", b["main"]))
    es_num = re.findall(r"\d[\d,\.]*", re.sub(r"<[^>]+>", " ", es_main))
    if en_num != es_num:
        warn.append("%s: figures differ\n  EN %s\n  ES %s"
                    % (slug, en_num[:24], es_num[:24]))

    text = " " + re.sub(r"<[^>]+>", " ", es_main) + " "
    hits = [w for w in STOP_EN if w in text]
    assert not hits, "%s: English survived in the body: %s" % (slug, hits)

    for k in ("title", "desc", "og_title", "og_desc"):
        assert es_head.get(k), "%s: head string %r missing" % (slug, k)

    return warn
