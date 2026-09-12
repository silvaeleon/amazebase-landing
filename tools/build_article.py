# -*- coding: utf-8 -*-
"""
Build an article from a content-first source file, into the site's existing
article template, in any of the site's languages.

    python tools/build_article.py build  <slug>
    python tools/build_article.py verify <slug>

LANGUAGES
---------
The language is never passed as a flag. A translated source names its English
original in `translation_of`, and language_of() asks which slug map sends that
original to this slug -- so a source whose tools/i18n/slugs/<lang>.json entry is
still null is refused before it can be written into the wrong directory.
Everything that then differs per language is one row of LANGS: the donor, the
output directory, the asset prefix, the month names, the three structural
headings, the figures disclaimer, the read-time wording and which category label
to read. Added 2026-09-11 with the Spanish and Portuguese twins of the first
content-first article.

Two things are deliberately NOT translated: the hero and figure FILES (one
picture serves all three languages, named for the English slug, only the alt
text changes) and the "## New terms" and "## Sources" appendix markers (working
notes for Leon, never page content)

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
  ## Frequently asked + "**Q**" / answer  .faq > details > summary; an answer
                                          may run to more than one paragraph
  ## Final thoughts                       section.sec, the closing section
  the figures-disclaimer sentence         the rail's p.rail-src
  ## New terms                            NOT PUBLISHED: a working appendix; it
  ## Sources                              stays in the source, never the page
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
from html.entities import codepoint2name as NAME

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# gate.py owns the FIXED-LABELS tables, and the builder reads the figures
# disclaimer from them rather than keeping a second list of its own
sys.path.insert(0, os.path.join(ROOT, "tools", "i18n"))
import gate

SRC = os.path.join(ROOT, "tools", "articles")
SITE = "https://amazebase.pro"

# Everything about a built page that depends on which language it is.
#
# The DONOR is that language's OWN twin of the English donor, never the English
# file patched afterwards. A translated article differs from its English source
# in more than prose: the breadcrumb is /es/recursos.html, the switcher chip is
# ES, and every asset path is ROOT-ABSOLUTE (/assets/img/...) where the English
# pages use ../assets/img/. Taking the real twin as the shell means none of that
# is retyped here and none of it can drift.
#
# "toc" is a prefix, not a whole heading: English carries both "What's in this
# guide" and "What's in this piece", and the other languages carry the matching
# pair.
LANGS = {
    "en": {
        "donor": "articles/true-product-margin-after-ads.html",
        "out": "articles",
        "assets": "../assets/img/",
        "back": "resources.html",
        "toc": ("What's in this",),
        "faq": "Frequently asked",
        "final": "Final thoughts",
        "disclaimer": "Figures from this article's worked examples, not an industry survey.",
        "read": "%d min read",
        "date": "%(d)d %(month)s %(y)d",
        "cat": "label",
        "months": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
    },
    "es": {
        "donor": "es/articulos/los-cinco-margenes-de-un-producto.html",
        "out": "es/articulos",
        "assets": "/assets/img/",
        "back": "es/recursos.html",
        "toc": ("Qué encontrarás",),
        "faq": "Preguntas frecuentes",
        "final": "Para cerrar",
        "disclaimer": "Cifras de los ejemplos trabajados de este artículo, "
                      "no de un estudio de mercado.",
        # a plain space: measured across the 48 Spanish articles that carry a
        # read time, every one of them uses one (Portuguese uses &nbsp;)
        "read": "%d min de lectura",
        "date": "%(d)d de %(month)s de %(y)d",
        "cat": "label_es",
        "months": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                   "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    },
    "pt": {
        "donor": "pt/artigos/as-cinco-margens-de-um-produto.html",
        "out": "pt/artigos",
        "assets": "/assets/img/",
        "back": "pt/recursos.html",
        "toc": ("O que você vai encontrar",),
        "faq": "Perguntas frequentes",
        "final": "Para fechar",
        "disclaimer": "Números dos exemplos deste artigo, "
                      "não de uma pesquisa de mercado.",
        "read": "%d&nbsp;min de leitura",
        "date": "%(d)d de %(month)s de %(y)d",
        "cat": "label_pt",
        "months": ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                   "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
    },
}

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
    and apostrophes and dashes as named entities (as the other articles are).

    Every OTHER non-ASCII character becomes its named entity too. That is not a
    nicety: the shipped Spanish and Portuguese articles hold &aacute; and
    &ccedil;, never a raw accent (measured across all 102 translated pages,
    2026-09-11), and gate.py refuses a raw accented character in an attribute.
    Spanish angle quotes arrive from the source as literal guillemets and become
    &laquo; / &raquo; here, so the straight-quote rule above stays English-and-
    Portuguese only -- which is right, as those are the two sources using "...".
    """
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r'"([^"]*)"', r"&ldquo;\1&rdquo;", t)
    t = t.replace("'", "&rsquo;").replace("—", "&mdash;").replace("–", "&ndash;")
    t = "".join(c if ord(c) < 128 else
                "&%s;" % NAME[ord(c)] if ord(c) in NAME else "&#%d;" % ord(c)
                for c in t)
    assert not re.search(r"[^\x00-\x7f]", t), "unmapped character in %r" % t[:60]
    return t


# The working appendices. They live in the source and never reach the page:
# "## New terms" is the translator's vocabulary note, "## Sources" the
# fact-check trail (it names Leon, cites screenshots, and records "matches the
# claim: yes"). Named once, because three call sites read the published part and
# a fourth checks the page for leakage; when the list lived at each site as a
# literal, adding Sources meant finding all of them, and the contents block
# silently counted it as a section (the article then had N+1 sections for N
# contents items, which is how it was found, 2026-09-12).
APPENDICES = ("\n## New terms", "\n## Sources")


def published_part(text):
    """The source with every working appendix cut off."""
    for a in APPENDICES:
        text = text.split(a, 1)[0]
    return text


def language_of(meta, slug):
    """Which language a source builds into, and the slug of its English source.

    Taken from the source itself, never from a flag that can be passed wrongly:
    a translated source names its English original in `translation_of`, and the
    language is whichever slug map sends that original to THIS slug. A source
    whose slug map entry is still null is therefore refused here, before it can
    be built into the wrong directory."""
    en = meta.get("translation_of")
    if not en:
        return "en", slug
    hits = []
    for code in LANGS:
        if code == "en":
            continue
        m = json.load(io.open(os.path.join(ROOT, "tools", "i18n", "slugs", code + ".json"),
                              encoding="utf-8"))
        if m.get(en) == slug:
            hits.append(code)
    assert len(hits) == 1, ("%r says it translates %r, but %d slug maps send that one to it "
                            "(fill tools/i18n/slugs/<lang>.json first): %s"
                            % (slug, en, len(hits), hits))
    return hits[0], en


def parse(slug):
    text = io.open(os.path.join(SRC, slug + ".md"), encoding="utf-8").read()
    head, body = text.split("\n\n", 1)
    meta = {}
    for line in head.splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    assert meta["slug"] == slug, "slug %r != file %r" % (meta["slug"], slug)
    body = published_part(body)                        # working appendices are never published
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
        # named for the ENGLISH slug, so all three languages point at one file:
        # the picture is the same picture, only its alt text is translated
        name = "fig-%s-%d.webp" % (section["en_slug"], n)
        return ("<!-- FIGURE GOES HERE. Drop the image in as assets/img/%s, uncomment:\n"
                "<figure class=\"art-figure\">\n"
                "  <img src=\"%s%s\"\n"
                "       alt=\"%s\"\n"
                "       loading=\"lazy\" decoding=\"async\">\n"
                "</figure>\n-->" % (name, section["assets"], name, alt))
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
    # A bullet list. Bare <ul>, as 107 body lists in the shipped corpus are;
    # the classed variants (ul.spec, ul.tradeoff) are hand-written pages and are
    # not something a source can ask for. Only OUTSIDE the contents block --
    # build_main takes that section before any block reaches here.
    if all(l.startswith("- ") for l in lines):
        return "<ul>\n%s\n  </ul>" % "\n".join("    <li>%s</li>" % inline(l[2:]) for l in lines)
    assert not any(l.startswith(("|", "[[", "- ", "#")) for l in lines), "unplaceable block: %r" % b[:80]
    return "<p>%s</p>" % inline(" ".join(lines))


# The figures disclaimer is a FAMILY, not one sentence. Three English forms are
# in use and all are legitimate: the plural "worked examples" (8 content-first
# sources), the singular "own worked example" (3), and "Examples from this
# article" (2 older shipped articles). Every form has a translation in each
# language's FIXED-LABELS table, which is where variants belong -- gate.py
# already checks a built page against that table, so the builder reading the
# same table is the two agreeing rather than a second list to keep in step.
# LANGS[lang]["disclaimer"] stays: it is the form a NEW source should prefer.
DISCLAIMER_TAIL = "not an industry survey."


def disclaimer_of(line, lang):
    """`line` if it is a recognised figures disclaimer for this language, else
    None.

    The table is keyed by English, so English matches the rule's pattern and a
    translation matches its right-hand side. The rules are written for RENDERED
    text, where inline() has already turned a source's straight apostrophe into
    &rsquo;, so the source line is curled before it is compared -- without that
    every English article fails, the rules carrying U+2019 and the sources
    U+0027.
    """
    _, rules = gate.load_labels("es" if lang == "en" else lang)
    found = False
    for r, tr in rules:
        if not r.pattern.rstrip("$").replace("\\.", ".").endswith(DISCLAIMER_TAIL):
            continue
        found = True
        if r.fullmatch(line.replace("'", "’")) if lang == "en" else line == tr:
            return line
    assert found, ("no figures-disclaimer rule in the %s FIXED-LABELS table -- the "
                   "variants live there, so an empty family means the table is broken" % lang)
    return None


def build_main(meta, intro, sections, lang, en_slug):
    L = LANGS[lang]
    state = {"slug": meta["slug"], "en_slug": en_slug, "assets": L["assets"], "labels": []}
    ib = blocks(intro)
    out = ['<main id="main" class="article">', '  <p class="lead">%s</p>' % inline(" ".join(ib[0].splitlines()))]
    toc, questions, faq, final = None, [], None, None
    for title, chunk in sections:
        if any(title.startswith(t) for t in L["toc"]):
            toc = (title, [re.sub(r"^- ", "", l) for l in chunk.strip().splitlines()])
        elif title == L["faq"]:
            faq = (title, chunk)
        elif title == L["final"]:
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
        # An answer may run to more than one paragraph. The threshold question
        # is the first that does: it gives the calculation, then says why the
        # 10% cutoff is a convention rather than a rule of the platform. A
        # block that does not open with **a question** continues the answer
        # above it; a block before the first question is still refused.
        entries = []
        for b in blocks(faq[1]):
            lines = b.splitlines()
            q = re.fullmatch(r"\*\*(.+)\*\*", lines[0])
            if q:
                assert len(lines) >= 2, "FAQ entry needs **question** then an answer: %r" % b[:60]
                entries.append((q.group(1), [" ".join(lines[1:])]))
            else:
                assert entries, "FAQ entry needs **question** then an answer: %r" % b[:60]
                entries[-1][1].append(" ".join(lines))
        for q, paras in entries:
            out += ["    <details>", "      <summary>%s</summary>" % inline(q)]
            out += ["      <p>%s</p>" % inline(p) for p in paras]
            out.append("    </details>")
        out.append("  </div>")
    disclaimer = None
    if final:
        bs = blocks(final[1])
        if bs and disclaimer_of(bs[-1].strip(), lang):
            disclaimer = bs.pop()
        out.append('  <section class="sec">')
        out.append("    <h2>%s</h2>" % inline(final[0]))
        out += ["    <p>%s</p>" % inline(" ".join(b.splitlines())) for b in bs]
        out.append("  </section>")
    out.append("</main>")
    return "\n".join(out), state["labels"], disclaimer


def build_rail(slug, disclaimer, lang, body=None):
    rail = json.load(io.open(os.path.join(SRC, slug + ".rail.json"), encoding="utf-8"))
    out = ['<aside class="rail" aria-label="Key figures from this article">']
    for c in rail["cards"]:
        # A card quotes the article; it does not paraphrase it. verify() checks
        # that the rail's NUMBERS are in the article, which is not enough: when
        # the ad-conversion-rate correction landed (2026-09-12), the middle card
        # of all three languages still read "your conversion rate" while the
        # callout it quotes had become "your AD conversion rate". The number 22
        # was still right, so nothing caught it. The sentence must be there.
        assert body is None or c["p"] in body, (
            "rail card %r quotes a sentence the article does not contain:\n  %r\n"
            "Rail cards quote the body verbatim -- fix the card, or the source it "
            "quotes, so the two agree." % (c["k"], c["p"]))
        cls = "rail-v" + (" is-%s" % c["tone"] if c.get("tone") else "")
        out += ['  <div class="rail-card">', '    <span class="rail-k">%s</span>' % inline(c["k"]),
                '    <span class="%s">%s</span>' % (cls, inline(c["v"])), "    <p>%s</p>" % inline(c["p"]), "  </div>"]
    assert disclaimer and disclaimer_of(disclaimer, lang), \
        "the source must end its closing section with a recognised %s figures disclaimer.\n" \
        "  got  %r\n  one of the FIXED-LABELS variants is required; the usual one is\n  %r" \
        % (lang, disclaimer, LANGS[lang]["disclaimer"])
    out.append('  <p class="rail-src">%s</p>' % inline(disclaimer))
    out.append("</aside>")
    return "\n".join(out)


def split_title(t):
    """The h1 is plain + <span class="accent">, split at the word boundary
    nearest the middle, as the other articles' titles are."""
    words = t.split()
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(t) / 2))
    return " ".join(words[:best]), " ".join(words[best:])


def categories(spec):
    """Every hub category the source names, in order. `categories:` holds one
    English hub label or several separated by commas -- the taxonomy key, named
    in English on a page of any language. Refused, never guessed, when a name is
    not exactly one of them.

    More than one is allowed because data/resources.json has always carried the
    plural `categories` list (hubrows.english_row builds it and sets the older
    singular `category` to its first entry), and four of the PPC articles
    genuinely sit in two or three. Before 2026-09-12 this function took the
    whole field as one label, so a source naming two was refused with
    "'PPC & Advertising, Profit & Finances' is not one hub category" -- which
    read as an invalid category rather than as a builder that could not count.
    """
    data = json.load(io.open(os.path.join(ROOT, "data", "resources.json"), encoding="utf-8"))
    known = dict((c["label"], c) for c in data["categories"])
    names = [n.strip() for n in spec.split(",") if n.strip()]
    assert names, "categories is empty"
    bad = [n for n in names if n not in known]
    assert not bad, ("%s is not a hub category. The categories are: %s"
                     % (", ".join(repr(b) for b in bad), ", ".join(sorted(known))))
    return [known[n] for n in names]


def category(spec):
    """The PRIMARY category: the first one named. It is the page eyebrow and the
    singular `category` field of the hub row."""
    return categories(spec)[0]


def category_id(spec):
    return category(spec)["id"]


def category_ids(spec):
    return [c["id"] for c in categories(spec)]


def category_label(label, lang):
    """That category's label in the page's own language. data/resources.json
    holds label / label_es / label_pt on every category, which is also what the
    hub tiles read, so the page and the tile can never disagree."""
    c = category(label)
    key = LANGS[lang]["cat"]
    assert key in c, "category %r has no %s (data/resources.json)" % (c["id"], key)
    return c[key]


# ------------------------------------------------------------------ building

def seo_twin(lang, slug, en_slug, meta):
    """The translated page's SEO block, localised from the English page's.

    seo.py deliberately writes ENGLISH pages only, so a twin's head is somebody
    else's job. tools/i18n/seo_twins.py already does the localising and is the
    code that produced the other 102 twins -- its localise_block() is reused
    here verbatim. What is NOT reused is its complete_es/complete_pt glue: those
    read loose og tags the old Spanish builder left on the page, and a
    pt-2026/content/<slug>.json that only the Portuguese builder writes. A
    content-first article has neither, so this supplies the same two values
    (title, summary) straight from the source and hands them over.

    So the English page must already carry its own block: run tools/seo.py
    after building the English article and before building its twins. The
    assert below says so rather than writing a half-localised head.
    """
    sys.path.insert(0, os.path.join(ROOT, "tools", "i18n"))
    import seo_twins as ST
    en_page = os.path.join(ROOT, "articles", en_slug + ".html")
    en_html = io.open(en_page, encoding="utf-8").read()
    assert ST.START in en_html, (
        "articles/%s.html has no SEO block yet, so there is nothing to localise. "
        "Run: python tools/seo.py  (it writes the English block), then rebuild this page."
        % en_slug)
    rel = "%s/%s.html" % (LANGS[lang]["out"], slug)
    row = [r for r in json.load(io.open(os.path.join(ROOT, "data", "resources.json"),
                                       encoding="utf-8"))["resources"] if r.get("url") == rel]
    assert len(row) == 1, ("data/resources.json has %d rows for %s; add the hub row first "
                           "(tools/i18n/hubrows.py translated_row)" % (len(row), rel))
    b = ST.localise_block(ST.en_block(ROOT, en_slug), lang,
                          "%s/%s" % (SITE, rel), "%s/articles/%s.html" % (SITE, en_slug),
                          inline(meta["title"]), inline(meta["summary"]), row[0])
    # localise_block sets the image alt to the title -- seo.py's fallback for an
    # article with NO hero. This one has a hero, so its alt is the translated
    # hero_alt, which is also what verify() requires.
    for attr in ('property="og:image:alt"', 'name="twitter:image:alt"'):
        b, n = re.subn(r'<meta %s content="[^"]*">' % re.escape(attr),
                       lambda _m: '<meta %s content="%s">' % (attr, inline(meta["hero_alt"])), b)
        assert n == 1, attr
    return b


def build(slug, published):
    meta, intro, sections = parse(slug)
    lang, en_slug = language_of(meta, slug)
    L = LANGS[lang]
    main, labels, disclaimer = build_main(meta, intro, sections, lang, en_slug)
    src = io.open(os.path.join(SRC, slug + ".md"), encoding="utf-8", newline="").read()
    rail = build_rail(slug, disclaimer, lang, published_part(src))
    y, m, d = (int(x) for x in published.split("-"))
    s = io.open(os.path.join(ROOT, L["donor"]), encoding="utf-8", newline="").read()
    assert "\r" not in s
    donor_slug = os.path.basename(L["donor"])[:-5]

    def rep(pat, new, flags=re.S):
        nonlocal s
        s, n = re.subn(pat, lambda _: new, s, count=1, flags=flags)
        assert n == 1, pat

    rep(r"<title>.*?</title>", "<title>%s &mdash; AmazeBase</title>" % inline(meta["title"]))
    rep(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">'
        % inline(meta["summary"]).replace("&ldquo;", "&quot;").replace("&rdquo;", "&quot;"))
    rep(r"<!-- SEO:START -->.*?<!-- SEO:END -->\n?", "")          # seo.py writes it from the hub row
    seo_block = seo_twin(lang, slug, en_slug, meta) if lang != "en" else None
    plain, accent = split_title(meta["title"])
    # The eyebrow and the last meta span carry the hub category in the page's
    # OWN language. The source names the English hub label in every language,
    # because that is the taxonomy key; data/resources.json holds the rest.
    eyebrow = inline(category_label(meta["categories"], lang))
    date = L["date"] % {"d": d, "month": L["months"][m - 1], "y": y}
    head = "\n".join([
        '<header class="article-head">',
        '  <p class="eyebrow">%s</p>' % eyebrow,
        '  <h1>%s <span class="accent">%s</span></h1>' % (inline(plain), inline(accent)),
        '  <p class="deck">%s</p>' % inline(meta["summary"]),
        '  <p class="meta">',
        "    <span>AmazeBase</span>",
        '    <span class="dot" aria-hidden="true"></span>',
        '    <span><time datetime="%s">%s</time></span>' % (published, inline(date)),
        '    <span class="dot" aria-hidden="true"></span>',
        "    <span>%s</span>" % (L["read"] % int(meta["reading_time"])),
        '    <span class="dot" aria-hidden="true"></span>',
        "    <span>%s</span>" % eyebrow,
        "  </p>",
        "</header>"])
    rep(r'<header class="article-head">.*?</header>', head)
    # ONE hero file for all three languages, named for the English slug: the
    # picture is the same picture and only the alt text is translated, so a
    # replacement drops in once instead of three times.
    hero_file = "hero-%s.webp" % en_slug
    hero = ("<!-- HERO IMAGE PLACEHOLDER. assets/img/%s is a stand-in at 1672x941 until the real\n"
            "     picture exists: replace that file, keep the name and this alt text, then run tools/build_og.py.\n"
            "     Tracked with the other awaiting-replacement heroes in HANDOVER.md section 6 item 7. -->\n"
            '<figure class="hero-shot">\n'
            '  <img src="%s%s"\n'
            '       alt="%s"\n'
            '       width="1672" height="941" loading="eager" decoding="async">\n'
            "</figure>") % (hero_file, L["assets"], hero_file, inline(meta["hero_alt"]))
    # the English donor still has an empty hero slot; the translated donors were
    # built with the hero already commented out around a <figure>
    rep(r"<!-- HERO IMAGE (?:GOES HERE|PLACEHOLDER)\..*?-->", hero)
    rep(r'<main id="main" class="article">.*?</main>', main)
    rep(r'<aside class="rail".*?</aside>', rail)
    rep(r"\n</style>", EXTRA_CSS.rstrip("\n") + "\n</style>")
    # the switcher rows: the donor's point at the donor's translations; this
    # page's come from the manifest (an English-only article has one row)
    sys.path.insert(0, os.path.join(ROOT, "tools", "i18n"))
    import langlinks
    cfg, slugs = langlinks.load()
    en_slugs = sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, "articles")) if f.endswith(".html"))
    rel = "%s/%s.html" % (L["out"], slug)
    # groups() is keyed by every member's own file, so a translated page looks
    # itself up by its own path without having to know the English one
    members = langlinks.groups(cfg, slugs, en_slugs + [en_slug]).get(rel) or {lang: rel}
    mm = langlinks.MENU_RUN.search(s)
    indent = re.match(r"[ \t]*", mm.group(2)).group(0)
    s = langlinks.MENU_RUN.sub(lambda m_: m_.group(1) + langlinks.menu_block(cfg, members, lang, indent)
                               + "\n" + m_.group(3), s, count=1)
    if seo_block:
        assert s.count("</head>") == 1
        s = s.replace("</head>", seo_block + "\n</head>", 1)
    assert donor_slug not in s, "the donor's slug survived into the page: %s" % \
        s[max(0, s.find(donor_slug) - 80):s.find(donor_slug) + 40]
    out = os.path.join(ROOT, L["out"], slug + ".html")
    io.open(out, "w", encoding="utf-8", newline="").write(s)
    print("built  %s  [%s]  (%d sections, callouts: %s)"
          % (rel, lang, len([1 for t, _ in sections]), ", ".join(labels)))
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


# --------------------------------------------------------------- logo hero

LOGO_BG = (0x03, 0x09, 0x17)      # --bg in css/variables.css
LOGO_BOX = 480                    # the 32-unit viewBox scaled to this square


def logohero(en_slug):
    """The interim hero: the site's own mark, centred on the site background.

    Leon asked for the logo rather than a blank stand-in while the real picture
    is drawn (2026-09-11), so the page shows something deliberate instead of an
    empty frame. Nothing else is on it -- no glow, no grid, no wordmark, because
    there is no wordmark file and a wordmark set in the wrong face would be
    worse than none.

    The mark is not redrawn here. tools/build_favicon.py already holds the two
    polygons and the #5B4FE6 -> #A93BF1 gradient as the single source of truth
    for the brand mark, and this calls its renderer, so the hero cannot drift
    from the favicon.

    One file serves all three languages -- see build(): the hero is named for
    the English slug because the picture is the same picture.
    """
    from PIL import Image
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import build_favicon as BF
    W, H = 1672, 941
    rows = BF.render(LOGO_BOX, pad=0.0, bg=None, ss=4)      # RGBA, transparent ground
    mark = Image.frombytes("RGBA", (LOGO_BOX, LOGO_BOX), b"".join(rows))
    # Centre the MARK, not its square: the outer polygon spans y 3.2..27.5 of a
    # 32-unit box, so its centre sits above the square's own centre.
    k = LOGO_BOX / 32.0
    cx = (min(p[0] for p in BF.OUTER) + max(p[0] for p in BF.OUTER)) / 2.0
    cy = (min(p[1] for p in BF.OUTER) + max(p[1] for p in BF.OUTER)) / 2.0
    img = Image.new("RGB", (W, H), LOGO_BG)
    img.paste(mark, (int(round(W / 2.0 - cx * k)), int(round(H / 2.0 - cy * k))), mark)
    out = os.path.join(ROOT, "assets", "img", "hero-%s.webp" % en_slug)
    img.save(out, "WEBP", quality=92, method=6)
    print("logo hero  assets/img/hero-%s.webp  %dx%d  %d bytes  (mark %d tall, centred)"
          % (en_slug, W, H, os.path.getsize(out),
             round((max(p[1] for p in BF.OUTER) - min(p[1] for p in BF.OUTER)) * k)))


# ------------------------------------------------------------------ verify

def verify(slug):
    sys.path.insert(0, os.path.join(ROOT, "tools", "i18n"))
    sys.path.insert(0, os.path.join(ROOT, "tools", "i18n", "pt-2026"))
    import verify_pt as VP, gate
    P, facts = [], []
    meta, intro, sections = parse(slug)
    lang, en_slug = language_of(meta, slug)
    L = LANGS[lang]
    rel = "%s/%s.html" % (L["out"], slug)
    raw = io.open(os.path.join(ROOT, rel), "rb").read()
    s = raw.decode("utf-8")
    if b"\r" in raw:
        P.append("CR bytes")
    bal = VP.Balance(); bal.feed(s); bal.close()
    if bal.errors or bal.stack:
        P.append("unbalanced HTML: %s %s" % (bal.errors[:3], [t for t, _ in bal.stack][:4]))
    live = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    main = re.search(r'<main id="main" class="article">.*?</main>', live, re.S).group(0)
    donor_slug = os.path.basename(L["donor"])[:-5]
    for bad, why in (("[[", "a source marker"), ("New terms", "the unpublished appendix"),
                     ("Sources", "the unpublished appendix"),
                     ("matches the claim", "the unpublished appendix"),
                     ("Everyday phrase", "the unpublished appendix"), (donor_slug, "the donor")):
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
    # Callout labels: approved ones only. Which COLUMN of the fixed-label table
    # is the approved set depends on the language. An English page's labels are
    # the table's English keys; a translated page's labels are its translations,
    # so comparing a Spanish page against the English column would reject every
    # label it has. English reads the Portuguese table because that table's
    # English column is the corpus-wide approved English set.
    exact, rules = gate.load_labels("pt" if lang == "en" else lang)
    approved = set(exact) if lang == "en" else set(exact.values())
    assert approved, ("no fixed-label table for %s: gate.load_labels found none, so this "
                      "check would pass vacuously" % lang)
    labels = [html.unescape(x) for x in re.findall(r'<span class="fixbox-k">([^<]*)</span>', main)]
    unknown = [l for l in labels if l not in approved
               and not any(r.match(l) for r, _ in rules)]
    if unknown:
        P.append("callout labels not in the approved set: %s" % unknown)
    facts.append("callouts: %s (all approved %s labels, of %d in the table)"
                 % (", ".join(labels), lang, len(approved)))
    # every figure in the source body is on the page, in order, and nothing else
    # in ORDER. Structural numbering is not a figure: the page's section numbers
    # (.num "01") and the source's "1." step markers (rendered as an <ol>).
    body_src = intro + "\n".join("\n" + c for t, c in sections
                                 if not any(t.startswith(x) for x in L["toc"]))
    body_src = re.sub(r"^\d+\. ", "", re.sub(r"\[\[FIGURE:.*?\]\]", "", body_src), flags=re.M)
    # the disclaimer is the rail's source line, not body prose: strip whichever
    # recognised variant THIS source ends with, not the language's usual one
    final_bs = blocks(next((c for t, c in sections if t == L["final"]), ""))
    disc = disclaimer_of(final_bs[-1].strip(), lang) if final_bs else None
    src_nums = gate.nums(html.escape(body_src.replace(disc or L["disclaimer"], "")))
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
        # a relative link resolves against the page's OWN directory, which is
        # es/articulos or pt/artigos on a translated page
        f = os.path.normpath(os.path.join(ROOT, L["out"], p)) if not p.startswith("/") else os.path.join(ROOT, p.lstrip("/"))
        if not os.path.isfile(f) and not os.path.isfile(os.path.join(ROOT, p.lstrip("/"), "index.html")):
            miss.append(u)
    if miss:
        P.append("links or files that resolve to nothing: %s" % sorted(set(miss))[:8])
    facts.append("every link and file on the page resolves")
    hero = "assets/img/hero-%s.webp" % en_slug
    hb = io.open(os.path.join(ROOT, hero), "rb").read() if os.path.exists(os.path.join(ROOT, hero)) else b""
    if hb[:4] != b"RIFF" or hb[8:12] != b"WEBP":
        P.append("%s missing or not a WebP" % hero)
    alt = re.search(r'<figure class="hero-shot">\s*<img[^>]*alt="([^"]*)"', live, re.S)
    # Compare what a READER sees, not the bytes. inline() turns a source
    # apostrophe into &rsquo; (and " into &ldquo;, -- into &mdash;), so the page
    # attribute unescapes to a curly apostrophe while the source holds a
    # straight one -- and this check could never pass for a hero_alt containing
    # one. Found 2026-09-12: the PPC batch held the first two in the corpus.
    want_alt = html.unescape(inline(meta["hero_alt"]))
    if not alt or html.unescape(alt.group(1)) != want_alt:
        P.append("hero alt is not the source's hero_alt: page %r, source %r"
                 % (html.unescape(alt.group(1)) if alt else None, want_alt))
    facts.append("hero: %s (%d bytes, WebP), alt = source hero_alt, %d words" % (hero, len(hb), len(meta["hero_alt"].split())))
    if "HERO IMAGE PLACEHOLDER" not in s:
        P.append("the hero is not marked as a placeholder")
    scripts = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>", s)
    if scripts:
        P.append("%d inline scripts (the CSP allows none on articles)" % len(scripts))
    # head, once seo.py and langlinks.py have run
    # og:image:alt is compared unescaped for the same reason, and for a second
    # one: seo.py writes English heads with RAW non-ascii (measured 2026-09-12:
    # 24 English pages already carry it) while seo_twins.py writes entities into
    # the 88 translated heads. Both render the same text; only a byte comparison
    # sees a difference, and it saw one the moment an English alt first carried
    # an apostrophe.
    for pat, want in ((r'<link rel="canonical" href="([^"]*)"', "%s/%s" % (SITE, rel)),
                      (r'<meta property="og:image:alt" content="([^"]*)"', want_alt)):
        got = [html.unescape(g) for g in re.findall(pat, s)]
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
    elif cmd == "logohero":
        logohero(slug)
    else:
        raise SystemExit("usage: build_article.py build|verify|placeholder|logohero <slug> "
                         "[published YYYY-MM-DD]\n"
                         "  logohero takes the ENGLISH slug: one hero serves all languages")
