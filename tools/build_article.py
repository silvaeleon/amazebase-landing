# -*- coding: utf-8 -*-
"""
Build an English article from a content-first source file, into the site's
existing article template.

    python tools/build_article.py build  <slug>
    python tools/build_article.py verify <slug>

The source lives in version control: tools/articles/<slug>.md (tools/ is not
served, see the Caddyfile). The first article authored this way is
how-much-data-before-changing-a-campaign (2026-09-11).

THE SOURCE FORMAT
-----------------
  key: value lines, then a blank line     frontmatter: title, slug, summary,
                                          categories (hub label), hero_alt,
                                          reading_time
  paragraphs before the first "## "       the lead (first) and intro
  ## What's in this guide + "- item"      the contents block; item N links to
                                          the Nth question section
  ## <any other heading>                  a numbered section (h2 + .num)
  [[Label]] + paragraph or "1." list      the callout (.fixbox), that label
  "label | value" lines                   the worked-sum block: labelled rows
                                          (.report > ul.report-rows)
  "| a | b |" markdown table              .tblwrap > table
  [[FIGURE: alt]]                         a figure SLOT, commented out like the
                                          hero slots, carrying that alt
  ## Frequently asked + "**Q**" / answer  .faq > details > summary
  ## Final thoughts                       section.sec, the closing section
  the figures-disclaimer sentence         the rail's p.rail-src
  ## New terms                            NOT PUBLISHED: a working appendix; it
                                          stays in the source, never the page
  [[SEE: slug]]                           refused: a link to an article that
                                          must exist (resolve it in the source)

Anything the builder cannot place is refused, never guessed.

THE PAGE
--------
The shell is an existing English article (DONOR), edited in place, so the
head, header, footer, sprite and inline stylesheet are the ones every other
article carries. Replaced: <title>, the description, the article head, the
hero, <main>, the rail. The SEO block is removed: seo.py writes it from the hub
row (data/resources.json), and langlinks.py writes the language links. Two
rules the donor's stylesheet lacks are appended to it: the worked-sum rows,
copied from attribution-vs-incrementality.html, and a numbered list inside a
callout.

The rail's three key-figure cards are not in the source format. They are in
tools/articles/<slug>.rail.json: numbers and sentences taken from the article.
"""

import html, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "articles")
DONOR = "articles/true-product-margin-after-ads.html"
SITE = "https://amazebase.pro"
DISCLAIMER = "Figures from this article's worked examples, not an industry survey."
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]

EXTRA_CSS = """
/* ── WORKED-SUM ROWS: labelled rows, one per line, value right-aligned.
   Copied from attribution-vs-incrementality.html (.report / .report-rows);
   added by tools/build_article.py for content-first sources. ──────────── */
.report{
  margin:0 0 var(--s3);
  border:1px solid var(--line-strong);
  border-radius:16px;
  overflow:hidden;
}
/* scoped under .article ul: this template's `.article ul` / `.article ul li::before`
   (grid gap, 26px indent, violet dot) otherwise outrank these rules */
.article ul.report-rows{ list-style:none; margin:0; padding:0; display:block; gap:0; }
.article ul.report-rows li{
  display:flex; justify-content:space-between; align-items:baseline; gap:16px;
  margin:0; padding:14px 22px;
  border-bottom:1px solid var(--line);
  font-size:15px; line-height:1.5; color:var(--text-2);
}
.article ul.report-rows li::before{ content:none; }
.article ul.report-rows li:last-child{ border-bottom:0; }
.article ul.report-rows .v{ color:var(--text); font-weight:700; font-variant-numeric:tabular-nums; white-space:nowrap; }

/* ── A numbered list inside a callout ("What to do" steps). ─────────────── */
.fixbox ol{ margin:4px 0 0; padding-left:1.3em; color:var(--text); }
.fixbox ol li{ margin:6px 0; padding-left:2px; }
"""


# ------------------------------------------------------------------ parsing

def inline(t):
    """Source text -> the house style: & < > escaped, **bold**, curly quotes
    and apostrophes and dashes as named entities (as the other articles are)."""
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r'"([^"]*)"', r"&ldquo;\1&rdquo;", t)
    t = t.replace("'", "&rsquo;").replace("—", "&mdash;").replace("–", "&ndash;")
    assert not re.search(r"[^\x00-\x7f]", t), "unmapped character in %r" % t[:60]
    return t


def parse(slug):
    text = io.open(os.path.join(SRC, slug + ".md"), encoding="utf-8").read()
    head, body = text.split("\n\n", 1)
    meta = {}
    for line in head.splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    assert meta["slug"] == slug, "slug %r != file %r" % (meta["slug"], slug)
    body = body.split("\n## New terms", 1)[0]          # the working appendix is never published
    assert "[[SEE:" not in body, "[[SEE:]] left in the source: resolve or remove it first"
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    intro, sections = parts[0], list(zip(parts[1::2], parts[2::2]))
    return meta, intro, sections


def blocks(chunk):
    return [b.strip("\n") for b in re.split(r"\n\s*\n", chunk.strip()) if b.strip()]


def render_block(b, section):
    lines = b.splitlines()
    m = re.fullmatch(r"\[\[FIGURE: (.+)\]\]", lines[0])
    if m and len(lines) == 1:
        alt = inline(m.group(1))
        n = section["figures"] = section.get("figures", 0) + 1
        name = "fig-%s-%d.webp" % (section["slug"], n)
        return ("<!-- FIGURE GOES HERE. Drop the image in as assets/img/%s, uncomment:\n"
                "<figure class=\"art-figure\">\n"
                "  <img src=\"../assets/img/%s\"\n"
                "       alt=\"%s\"\n"
                "       loading=\"lazy\" decoding=\"async\">\n"
                "</figure>\n-->" % (name, name, alt))
    m = re.fullmatch(r"\[\[(.+)\]\]", lines[0])
    if m:
        label, rest = m.group(1), lines[1:]
        assert rest, "callout %r has no body" % label
        if all(re.match(r"\d+\. ", l) for l in rest):
            inner = "<ol>\n%s\n    </ol>" % "\n".join(
                "      <li>%s</li>" % inline(re.sub(r"^\d+\. ", "", l)) for l in rest)
        else:
            inner = "<p>%s</p>" % inline(" ".join(rest))
        section["labels"].append(label)
        return ('<div class="fixbox">\n    <span class="fixbox-k">%s</span>\n    %s\n  </div>'
                % (inline(label), inner))
    if all(re.fullmatch(r"[^|]+ \| [^|]+", l) for l in lines):
        rows = [l.split(" | ", 1) for l in lines]
        return ('<div class="report">\n    <ul class="report-rows">\n%s\n    </ul>\n  </div>'
                % "\n".join('      <li><span>%s</span><span class="v">%s</span></li>' % (inline(a), inline(v))
                            for a, v in rows))
    if all(l.startswith("|") for l in lines):
        cells = [[c.strip() for c in l.strip("|").split("|")] for l in lines]
        assert re.fullmatch(r"[-: |]+", lines[1]), "table without a separator row"
        head, rows = cells[0], cells[2:]
        return ('<div class="tblwrap">\n    <table>\n      <thead><tr>%s</tr></thead>\n      <tbody>\n%s\n      '
                '</tbody>\n    </table>\n  </div>'
                % ("".join("<th>%s</th>" % inline(c) for c in head),
                   "\n".join("        <tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows)))
    if all(re.match(r"\d+\. ", l) for l in lines):
        return "<ol>\n%s\n  </ol>" % "\n".join("    <li>%s</li>" % inline(re.sub(r"^\d+\. ", "", l)) for l in lines)
    assert not any(l.startswith(("|", "[[", "- ", "#")) for l in lines), "unplaceable block: %r" % b[:80]
    return "<p>%s</p>" % inline(" ".join(lines))


def build_main(meta, intro, sections):
    slug = meta["slug"]
    state = {"slug": slug, "labels": []}
    ib = blocks(intro)
    out = ['<main id="main" class="article">', '  <p class="lead">%s</p>' % inline(" ".join(ib[0].splitlines()))]
    toc, questions, faq, final = None, [], None, None
    for title, chunk in sections:
        if title.startswith("What's in this guide"):
            toc = (title, [re.sub(r"^- ", "", l) for l in chunk.strip().splitlines()])
        elif title == "Frequently asked":
            faq = (title, chunk)
        elif title == "Final thoughts":
            final = (title, chunk)
        else:
            questions.append((title, chunk))
    assert toc and len(toc[1]) == len(questions), \
        "contents lists %d items, the article has %d sections" % (len(toc[1]) if toc else 0, len(questions))
    out.append('  <nav class="toc" aria-labelledby="toc-title">')
    out.append('    <h2 id="toc-title">%s</h2>' % inline(toc[0]))
    out.append("    <ol>")
    out += ['      <li><a href="#s%d">%s</a></li>' % (i + 1, inline(t)) for i, t in enumerate(toc[1])]
    out += ["    </ol>", "  </nav>"]
    for b in ib[1:]:
        out.append("  " + render_block(b, state))
    for i, (title, chunk) in enumerate(questions):
        out.append('  <h2 id="s%d"><span class="num">%02d</span>%s</h2>' % (i + 1, i + 1, inline(title)))
        for b in blocks(chunk):
            out.append("  " + render_block(b, state))
    if faq:
        out.append('  <h2 id="faq">%s</h2>' % inline(faq[0]))
        out.append('  <div class="faq">')
        for b in blocks(faq[1]):
            lines = b.splitlines()
            q = re.fullmatch(r"\*\*(.+)\*\*", lines[0])
            assert q and len(lines) >= 2, "FAQ entry needs **question** then an answer: %r" % b[:60]
            out += ["    <details>", "      <summary>%s</summary>" % inline(q.group(1)),
                    "      <p>%s</p>" % inline(" ".join(lines[1:])), "    </details>"]
        out.append("  </div>")
    disclaimer = None
    if final:
        bs = blocks(final[1])
        if bs and bs[-1].strip() == DISCLAIMER:
            disclaimer = bs.pop()
        out.append('  <section class="sec">')
        out.append("    <h2>%s</h2>" % inline(final[0]))
        out += ["    <p>%s</p>" % inline(" ".join(b.splitlines())) for b in bs]
        out.append("  </section>")
    out.append("</main>")
    return "\n".join(out), state["labels"], disclaimer


def build_rail(slug, disclaimer):
    rail = json.load(io.open(os.path.join(SRC, slug + ".rail.json"), encoding="utf-8"))
    out = ['<aside class="rail" aria-label="Key figures from this article">']
    for c in rail["cards"]:
        cls = "rail-v" + (" is-%s" % c["tone"] if c.get("tone") else "")
        out += ['  <div class="rail-card">', '    <span class="rail-k">%s</span>' % inline(c["k"]),
                '    <span class="%s">%s</span>' % (cls, inline(c["v"])), "    <p>%s</p>" % inline(c["p"]), "  </div>"]
    assert disclaimer == DISCLAIMER, "the source must end its closing section with the figures disclaimer"
    out.append('  <p class="rail-src">%s</p>' % inline(disclaimer))
    out.append("</aside>")
    return "\n".join(out)


def split_title(t):
    """The h1 is plain + <span class="accent">, split at the word boundary
    nearest the middle, as the other articles' titles are."""
    words = t.split()
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(t) / 2))
    return " ".join(words[:best]), " ".join(words[best:])


def category_label(label):
    data = json.load(io.open(os.path.join(ROOT, "data", "resources.json"), encoding="utf-8"))
    ids = [c["id"] for c in data["categories"] if c["label"] == label]
    assert len(ids) == 1, "category %r is not one hub category" % label
    return ids[0]


# ------------------------------------------------------------------ building

def build(slug, published):
    meta, intro, sections = parse(slug)
    main, labels, disclaimer = build_main(meta, intro, sections)
    rail = build_rail(slug, disclaimer)
    y, m, d = (int(x) for x in published.split("-"))
    s = io.open(os.path.join(ROOT, DONOR), encoding="utf-8", newline="").read()
    assert "\r" not in s
    donor_slug = os.path.basename(DONOR)[:-5]

    def rep(pat, new, flags=re.S):
        nonlocal s
        s, n = re.subn(pat, lambda _: new, s, count=1, flags=flags)
        assert n == 1, pat

    rep(r"<title>.*?</title>", "<title>%s &mdash; AmazeBase</title>" % inline(meta["title"]))
    rep(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">'
        % inline(meta["summary"]).replace("&ldquo;", "&quot;").replace("&rdquo;", "&quot;"))
    rep(r"<!-- SEO:START -->.*?<!-- SEO:END -->\n?", "")          # seo.py writes it from the hub row
    plain, accent = split_title(meta["title"])
    head = "\n".join([
        '<header class="article-head">',
        '  <p class="eyebrow">%s</p>' % inline(meta["categories"]),
        '  <h1>%s <span class="accent">%s</span></h1>' % (inline(plain), inline(accent)),
        '  <p class="deck">%s</p>' % inline(meta["summary"]),
        '  <p class="meta">',
        "    <span>AmazeBase</span>",
        '    <span class="dot" aria-hidden="true"></span>',
        '    <span><time datetime="%s">%d %s %d</time></span>' % (published, d, MONTHS[m - 1], y),
        '    <span class="dot" aria-hidden="true"></span>',
        "    <span>%s min read</span>" % int(meta["reading_time"]),
        '    <span class="dot" aria-hidden="true"></span>',
        "    <span>%s</span>" % inline(meta["categories"]),
        "  </p>",
        "</header>"])
    rep(r'<header class="article-head">.*?</header>', head)
    hero = ("<!-- HERO IMAGE PLACEHOLDER. assets/img/hero-%s.webp is a stand-in at 1672x941 until the real\n"
            "     picture exists: replace that file, keep the name and this alt text, then run tools/build_og.py.\n"
            "     Tracked with the other awaiting-replacement heroes in HANDOVER.md section 6 item 7. -->\n"
            '<figure class="hero-shot">\n'
            '  <img src="../assets/img/hero-%s.webp"\n'
            '       alt="%s"\n'
            '       width="1672" height="941" loading="eager" decoding="async">\n'
            "</figure>") % (slug, slug, inline(meta["hero_alt"]))
    rep(r"<!-- HERO IMAGE GOES HERE\..*?-->", hero)
    rep(r'<main id="main" class="article">.*?</main>', main)
    rep(r'<aside class="rail".*?</aside>', rail)
    rep(r"\n</style>", EXTRA_CSS.rstrip("\n") + "\n</style>")
    # the switcher rows: the donor's point at the donor's translations; this
    # page's come from the manifest (an English-only article has one row)
    sys.path.insert(0, os.path.join(ROOT, "tools", "i18n"))
    import langlinks
    cfg, slugs = langlinks.load()
    en_slugs = sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, "articles")) if f.endswith(".html"))
    members = langlinks.groups(cfg, slugs, en_slugs + [slug]).get("articles/%s.html" % slug) or \
        {"en": "articles/%s.html" % slug}
    mm = langlinks.MENU_RUN.search(s)
    indent = re.match(r"[ \t]*", mm.group(2)).group(0)
    s = langlinks.MENU_RUN.sub(lambda m_: m_.group(1) + langlinks.menu_block(cfg, members, "en", indent)
                               + "\n" + m_.group(3), s, count=1)
    assert donor_slug not in s, "the donor's slug survived into the page: %s" % \
        s[max(0, s.find(donor_slug) - 80):s.find(donor_slug) + 40]
    out = os.path.join(ROOT, "articles", slug + ".html")
    io.open(out, "w", encoding="utf-8", newline="").write(s)
    print("built  articles/%s.html  (%d sections, callouts: %s)" % (slug, len([1 for t, _ in sections]), ", ".join(labels)))
    return meta, labels


# ------------------------------------------------------------------ placeholder hero

def placeholder(slug):
    """A stand-in hero at 1672x941 until the real picture exists: the site's
    background, its violet and blue glows, a faint grid and the brand mark at
    22% -- no text, so nobody mistakes it for the picture. Needs Pillow."""
    from PIL import Image, ImageDraw
    W, H = 1672, 941
    img = Image.new("RGB", (W, H), (3, 9, 23))

    def glow(cx, cy, r, rgb, alpha):
        # radial_gradient() reads 255 at the CORNER, ~179 at the circle's edge:
        # normalise to the circle so the glow reaches 0 inside its square
        g = Image.radial_gradient("L").resize((2 * r, 2 * r))
        mask = g.point(lambda v: int(255 * alpha * max(0.0, 1 - v / 179.0) ** 1.8))
        img.paste(Image.new("RGB", (2 * r, 2 * r), rgb), (int(cx - r), int(cy - r)), mask)
    glow(W * .72, H * .28, 720, (139, 59, 241), .34)
    glow(W * .24, H * .78, 640, (59, 130, 246), .26)
    glow(W * .50, H * .50, 380, (91, 79, 230), .16)
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    for x in range(0, W + 1, 64):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 9))
    for y in range(0, H + 1, 64):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 9))
    k, ox, oy = 6, W / 2 - 16 * 6, H / 2 - 16 * 6
    pt = lambda pts: [(ox + x * k, oy + y * k) for x, y in pts]
    d.polygon(pt([(16, 3.2), (29, 27.5), (22.6, 27.5), (16, 14.1), (9.4, 27.5), (3, 27.5)]), fill=(122, 69, 236, 56))
    d.polygon(pt([(16, 17.6), (20.4, 25.8), (11.6, 25.8)]), fill=(197, 107, 245, 48))
    img = Image.alpha_composite(img.convert("RGBA"), over).convert("RGB")
    out = os.path.join(ROOT, "assets", "img", "hero-%s.webp" % slug)
    img.save(out, "WEBP", quality=90, method=6)
    print("placeholder  assets/img/hero-%s.webp  %dx%d  %d bytes" % (slug, W, H, os.path.getsize(out)))


# ------------------------------------------------------------------ verify

def verify(slug):
    sys.path.insert(0, os.path.join(ROOT, "tools", "i18n"))
    sys.path.insert(0, os.path.join(ROOT, "tools", "i18n", "pt-2026"))
    import verify_pt as VP, gate
    P, facts = [], []
    rel = "articles/%s.html" % slug
    raw = io.open(os.path.join(ROOT, rel), "rb").read()
    s = raw.decode("utf-8")
    meta, intro, sections = parse(slug)
    if b"\r" in raw:
        P.append("CR bytes")
    bal = VP.Balance(); bal.feed(s); bal.close()
    if bal.errors or bal.stack:
        P.append("unbalanced HTML: %s %s" % (bal.errors[:3], [t for t, _ in bal.stack][:4]))
    live = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    main = re.search(r'<main id="main" class="article">.*?</main>', live, re.S).group(0)
    for bad, why in (("[[", "a source marker"), ("New terms", "the unpublished appendix"),
                     ("Everyday phrase", "the unpublished appendix"), ("true-product-margin", "the donor")):
        if bad in live:
            P.append("%s survived into the page: %r" % (why, bad))
    # order of the standard regions, as every article has them
    order = ['<p class="back-link">', '<header class="article-head">', '<figure class="hero-shot">',
             '<div class="shell">', '<main id="main" class="article">', '<p class="lead">', '<nav class="toc"',
             '<aside class="rail"', '<p class="rail-src">', '</div><!-- /.wrap -->']
    pos = [(s if x.startswith("</div><!--") else live).find(x) for x in order]   # the wrap end IS a comment
    if -1 in pos or pos != sorted(pos):
        P.append("standard regions missing or out of order: %s" % dict(zip(order, pos)))
    facts.append("regions in order: back link, article head, hero, shell, main, lead, contents, rail, rail-src")
    # contents -> sections
    toc = re.findall(r'<li><a href="#(s\d+)">', main)
    ids = re.findall(r'<h2 id="(s\d+)"><span class="num">', main)
    if toc != ids:
        P.append("contents %s != sections %s" % (toc, ids))
    facts.append("contents: %d entries, each an h2 with its .num" % len(toc))
    # callout labels: approved ones only (GLOSSARIO-PT's fixed-label table is the approved English set)
    approved = set(gate.load_labels("pt")[0]) if isinstance(gate.load_labels("pt"), tuple) else set(gate.load_labels("pt"))
    labels = [html.unescape(x) for x in re.findall(r'<span class="fixbox-k">([^<]*)</span>', main)]
    unknown = [l for l in labels if l not in approved]
    if unknown:
        P.append("callout labels not in the approved set: %s" % unknown)
    facts.append("callouts: %s (all approved labels)" % ", ".join(labels))
    # every figure in the source body is on the page, in order, and nothing else
    # in ORDER. Structural numbering is not a figure: the page's section numbers
    # (.num "01") and the source's "1." step markers (rendered as an <ol>).
    body_src = intro + "\n".join("\n" + c for t, c in sections if not t.startswith("What's in this guide"))
    body_src = re.sub(r"^\d+\. ", "", re.sub(r"\[\[FIGURE:.*?\]\]", "", body_src), flags=re.M)
    src_nums = gate.nums(html.escape(body_src.replace(DISCLAIMER, "")))
    page_main = re.sub(r'<nav class="toc".*?</nav>|<span class="num">\d+</span>', " ", main, flags=re.S)
    page_nums = gate.nums(page_main)
    rail = re.search(r'<aside class="rail".*?</aside>', live, re.S).group(0)
    if src_nums != page_nums:
        i = next((k for k in range(min(len(src_nums), len(page_nums))) if src_nums[k] != page_nums[k]),
                 min(len(src_nums), len(page_nums)))
        P.append("figures differ from the source at #%d:\n  src  %s\n  page %s" % (i + 1, src_nums[i:i + 8], page_nums[i:i + 8]))
    facts.append("figures: %d numbers in the body, identical to the source and in the same order" % len(page_nums))
    rail_nums = set(gate.nums(rail))
    if not rail_nums <= set(src_nums):
        P.append("the rail quotes a number the article does not: %s" % sorted(rail_nums - set(src_nums)))
    facts.append("rail: %d cards, every number in it is in the article" % rail.count('class="rail-card"'))
    # links and files
    miss = []
    for _, u in VP.urls(live):
        if re.match(r"^(#|[a-z]+:)", u):
            if u.startswith("#") and len(u) > 1 and 'id="%s"' % u[1:] not in s:
                miss.append(u)
            continue
        p = u.split("#")[0].split("?")[0]
        f = os.path.normpath(os.path.join(ROOT, "articles", p)) if not p.startswith("/") else os.path.join(ROOT, p.lstrip("/"))
        if not os.path.isfile(f) and not os.path.isfile(os.path.join(ROOT, p.lstrip("/"), "index.html")):
            miss.append(u)
    if miss:
        P.append("links or files that resolve to nothing: %s" % sorted(set(miss))[:8])
    facts.append("every link and file on the page resolves")
    hero = "assets/img/hero-%s.webp" % slug
    hb = io.open(os.path.join(ROOT, hero), "rb").read() if os.path.exists(os.path.join(ROOT, hero)) else b""
    if hb[:4] != b"RIFF" or hb[8:12] != b"WEBP":
        P.append("%s missing or not a WebP" % hero)
    alt = re.search(r'<figure class="hero-shot">\s*<img[^>]*alt="([^"]*)"', live, re.S)
    if not alt or html.unescape(alt.group(1)) != meta["hero_alt"]:
        P.append("hero alt is not the source's hero_alt")
    facts.append("hero: %s (%d bytes, WebP), alt = source hero_alt, %d words" % (hero, len(hb), len(meta["hero_alt"].split())))
    if "HERO IMAGE PLACEHOLDER" not in s:
        P.append("the hero is not marked as a placeholder")
    scripts = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>", s)
    if scripts:
        P.append("%d inline scripts (the CSP allows none on articles)" % len(scripts))
    # head, once seo.py and langlinks.py have run
    for pat, want in ((r'<link rel="canonical" href="([^"]*)"', "%s/%s" % (SITE, rel)),
                      (r'<meta property="og:image:alt" content="([^"]*)"', inline(meta["hero_alt"]))):
        got = re.findall(pat, s)
        if got != [want]:
            P.append("%s is %s, want %s" % (pat[:40], got, want))
    facts.append("head: canonical, og:image:alt = hero alt (seo.py)")
    print("%-4s /%s" % ("OK" if not P else "FAIL", rel))
    for f in facts:
        print("       " + f)
    for p in P:
        print("   !!  " + p)
    print("\n%d problems" % len(P))
    return len(P)


if __name__ == "__main__":
    cmd, slug = sys.argv[1], sys.argv[2]
    if cmd == "build":
        build(slug, sys.argv[3] if len(sys.argv) > 3 else "2026-09-11")
    elif cmd == "verify":
        raise SystemExit(1 if verify(slug) else 0)
    elif cmd == "placeholder":
        placeholder(slug)
    else:
        raise SystemExit("usage: build_article.py build|verify <slug> [published YYYY-MM-DD]")
