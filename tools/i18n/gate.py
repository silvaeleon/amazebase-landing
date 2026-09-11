# -*- coding: utf-8 -*-
"""
The gate: refuse a translated article before it can reach a built page.

Generic over languages; es-2026/gate.py is the Spanish original it grew from.
It compares a translator's JSON against the English brief it was made from:

  structure   the ordered skeleton (every tag with id/class/href/src/style/...)
              of main, article_head, rail and cta must be IDENTICAL
  anchors     every id, every href, in order
  figures     the ordered list of numbers in every region
  leakage     English stopwords in the text; for Portuguese, Spanish-only words
              and European-Portuguese forms too
  register    per-language punctuation rules (Portuguese: 25%, curly quotes)
  head        every head string present; JSON-LD fields plain text, attribute
              fields entity-encoded
  slug        pattern, <= 50 characters AND <= 7 words. Refused, never trimmed.
  hero alt    8-14 words, and identical to og:image:alt, when there is a hero
  <pre>       per block: the ordered numbers and operators, the line count, and
              every column the English lines up (added 2026-09-11)
  labels      callout labels must equal the fixed strings in the language's
              glossary (GLOSSARIO-XX.md, FIXED-LABELS table)
  net revenue Portuguese only: "faturamento" is refused where the English text
              node says net revenue / net sales / after returns

CALIBRATE IT ON KNOWN-GOOD WORK BEFORE TRUSTING IT. A gate that has never
passed an approved translation cannot tell a real failure from noise, and one
that has never failed cannot be shown to work. pt-2026/calibrate.py runs it over
the three approved Spanish pilot pages (must pass) and runs the Portuguese
leakage rules over the same pages (must fail).

    python tools/i18n/gate.py pt <slug> --brief B.json --content C.json
"""

import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pipeline as P

FIELDS = ("main", "article_head", "rail", "cta")
SLUG_MAX_CHARS = 50
SLUG_MAX_WORDS = 7
ALT_WORDS = (8, 14)

# A comma is a thousands separator only when digits follow it. Without this,
# "antes del 14, y 900" reads as the number "14," and diverges from "the 14th".
NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
ENTITY = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);")
WORD = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*", re.U)

STOP_EN = P.STOP_EN

# Words that exist in Spanish and not in Brazilian Portuguese (hyphenated
# enclitics like "vende-los" stay one token, so "los" alone is safe), and forms
# that are European Portuguese or break the approved register. Only words that
# are NOT also Portuguese: "más" was removed 2026-09-11 -- it is Portuguese for
# "bad" (más decisões) and the gate made a translator reword correct text.
LEAK = {
    "pt": {
        "spanish": {"y", "el", "los", "las", "del", "una", "unas", "unos",
                    "con", "es", "muy", "pero", "usted", "ustedes", "puedes",
                    "tienes", "también", "sin", "hay", "ya", "cuando",
                    "mientras", "entonces", "aunque", "ahora", "siempre",
                    "inventario", "ventas", "quiebre", "reorden", "utilidad",
                    "proveedor", "dinero", "punto"},
        "register": {"tu", "teu", "tua", "teus", "tuas", "vós", "equipa",
                     "ecrã", "telemóvel", "facto", "registo", "utilizador",
                     "contacto", "pra", "inventário"},
    },
}


def untagged(frag):
    """The fragment with HTML comments and tags replaced by spaces. Comments
    FIRST: they never render, and a comment that mentions a tag ("<svg ...>")
    left its own words behind as 'text' when tags were stripped first -- found
    2026-09-11 by the Portuguese homepage translator (English survived, a
    straight quote) in developer comments nobody reads."""
    return re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", " ", frag or "", flags=re.S))


def text_of(frag):
    """Rendered text of a fragment: comments and tags out, entities decoded."""
    return html.unescape(untagged(frag))


# ------------------------------------------------------------- <pre> blocks
# Every <pre> in the corpus is a worked sum or formula written in words, sitting
# in <pre> for alignment (19 blocks in 6 articles, measured 2026-09-11; none is
# code). Words are translated; every number, operator and currency symbol must
# survive in order. Literal code -- commands, JSON, config -- would be copied
# byte-for-byte, and would pass this check trivially.
PRE_TOKEN = re.compile(u"\\$?\\d+(?:,\\d{3})*(?:\\.\\d+)?|[=+×÷≈~−–√*/%()<>≤≥→]")


def pre_blocks(frag):
    return [html.unescape(re.sub(r"<[^>]+>", "", p))
            for p in re.findall(r"<pre\b[^>]*>(.*?)</pre>", frag or "", re.S)]


def pre_columns(block):
    """For each line, the column a reader's eye lines up: the = or ~= sign if the
    line has one, else where a value starts after a 2+ space gap, else the
    indent of a continuation line. None for blank or unaligned lines."""
    out = []
    for ln in block.split("\n"):
        if not ln.strip():
            out.append(None)
            continue
        m = re.search(u" [=≈](?= |$)", ln)
        if m:
            out.append(m.start() + 1)
            continue
        m = re.match(r" {2,}(?=\S)", ln)
        if m:
            out.append(m.end())
            continue
        m = re.search(r"\S {2,}(?=\S)", ln)
        out.append(m.end() if m else None)
    return out


def check_pre(en_v, tr_v, field):
    prob = []
    a, b = pre_blocks(en_v), pre_blocks(tr_v)
    for i, (x, y) in enumerate(zip(a, b), 1):
        tx, ty = PRE_TOKEN.findall(x), PRE_TOKEN.findall(y)
        if tx != ty:
            prob.append("%s <pre> #%d numbers/operators differ\n  EN %s\n  TR %s" % (field, i, tx, ty))
        # alignment: lines the English lines up in a column must still line up
        cx, cy = pre_columns(x), pre_columns(y)
        if len(cx) != len(cy):
            prob.append("%s <pre> #%d has %d lines, English %d" % (field, i, len(cy), len(cx)))
            continue
        groups = {}
        for ln, col in enumerate(cx):
            if col is not None:
                groups.setdefault(col, []).append(ln)
        for col, lines in groups.items():
            if len(lines) < 2:
                continue
            got = [cy[ln] for ln in lines]
            if None in got or len(set(got)) != 1:
                prob.append("%s <pre> #%d column alignment broken on lines %s (English aligns them at col %d; translation %s)"
                            % (field, i, [l + 1 for l in lines], col, got))
    return prob


# ----------------------------------------------------------- fixed labels
# Callout labels recur across articles ("The fix" in 14, "Related reading" in
# 35). Forty-eight parallel translators would otherwise produce six variants of
# each. The table lives in the language's glossary, between FIXED-LABELS
# markers, so the glossary is the one source and this check cannot drift from it.
LABEL_CLASSES = {"fixbox-k", "rail-k", "label", "lab", "eyebrow", "player-kind"}


def load_labels(lang):
    p = os.path.join(HERE, "briefs", "GLOSSARIO-%s.md" % lang.upper())
    if not os.path.exists(p):
        return {}, []
    s = io.open(p, encoding="utf-8").read()
    m = re.search(r"<!-- FIXED-LABELS:START -->(.*?)<!-- FIXED-LABELS:END -->", s, re.S)
    if not m:
        return {}, []
    exact, rules = {}, []
    for row in m.group(1).split("\n"):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("English", "") or set(cells[0]) <= set("-: "):
            continue
        en, tr = cells[0].strip("`"), cells[1].strip("`")
        if en.startswith("re:"):
            rules.append((re.compile(en[3:].strip()), tr))
        else:
            exact[en] = tr
    return exact, rules


def load_vocab(lang):
    """[(variant, settled)] from the glossary's VOCAB-SETTLE table."""
    p = os.path.join(HERE, "briefs", "GLOSSARIO-%s.md" % lang.upper())
    if not os.path.exists(p):
        return []
    s = io.open(p, encoding="utf-8").read()
    m = re.search(r"<!-- VOCAB-SETTLE:START -->(.*?)<!-- VOCAB-SETTLE:END -->", s, re.S)
    out = []
    for row in (m.group(1).split("\n") if m else []):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("Variant", "") or set(cells[0]) <= set("-: "):
            continue
        out.append((cells[0], cells[1]))
    return out


def settle(text, vocab):
    """Plain text with every variant replaced; a leading capital is kept."""
    for var, good in vocab:
        def sub(m, good=good):
            return good[0].upper() + good[1:] if m.group(0)[0].isupper() else good
        text = re.sub(re.escape(var), sub, text, flags=re.I)
    return text


def check_vocab(tr_v, field, lang):
    vocab = load_vocab(lang)
    t = norm(untagged(tr_v)).lower()
    return ["%s: %r is a settled variant; use %r" % (field, var, good)
            for var, good in vocab if var.lower() in t]


def text_nodes(frag):
    """[(class of the tag that opens this text, text)] -- aligned index by index
    between two fragments whose skeletons are identical."""
    frag = re.sub(r"<!--.*?-->", "", frag or "", flags=re.S)
    parts = re.split(r"(<[^>]+>)", frag)
    out, prev = [], None
    for p in parts:
        if p.startswith("<"):
            prev = p
            continue
        cls = None
        if prev and not prev.startswith("</"):
            m = re.search(r'\bclass="([^"]*)"', prev)
            cls = m.group(1) if m else ""
        out.append((cls, p))
    return out


def norm(t):
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def expected_label(en_text, cls, exact, rules):
    """The fixed string an English text node demands, or None."""
    t = norm(en_text)
    if not t:
        return None
    if cls is not None and cls.split()[0:1] and cls.split()[0] in LABEL_CLASSES:
        if " · " in t:                     # dual eyebrow: "Growth Playbook · Profit & Finances"
            bits = t.split(" · ")
            if all(b in exact for b in bits):
                return " · ".join(exact[b] for b in bits)
        if t in exact:
            return exact[t]
    for rx, tr in rules:                          # rules apply wherever they match
        m = rx.match(t)
        if m:
            return m.expand(tr)
    return None


def check_labels(en_v, tr_v, field, lang):
    exact, rules = load_labels(lang)
    if not exact and not rules:
        return []
    a, b = text_nodes(en_v), text_nodes(tr_v)
    if len(a) != len(b):
        return ["%s: cannot align text nodes for the label check (%d vs %d)" % (field, len(a), len(b))]
    prob = []
    for (cls, et), (_, tt) in zip(a, b):
        want = expected_label(et, cls, exact, rules)
        if want is not None and norm(tt) != want:
            prob.append("%s: label %r must be the fixed string %r, is %r" % (field, norm(et), want, norm(tt)))
    return prob


# English left behind. STOP_EN matches a handful of space-padded words; a
# translator found (2026-09-11, ppc-flywheel) a whole English sentence --
# "That's why great Amazon businesses often seem impossible to catch" -- that
# contains none of them, and the gate said OK. Two structural checks instead:
# a text node IDENTICAL to its English counterpart, and a node carrying two or
# more distinct English function words once the allowed English terms are
# removed. Words that are also Portuguese or Spanish (do, as, no, so, for --
# "se a resposta for sim" -- has -- "has usado") are not on the list. Tokens
# are whole Unicode words: an ASCII-only tokenizer splits "orçamento" into
# "or" + "amento" and fires on every accented word (it did, 16 times).
EN_FUNC = {"the", "and", "of", "to", "is", "are", "with", "that", "this",
           "it", "you", "your", "on", "in", "be", "can", "not", "will", "what",
           "which", "why", "how", "but", "or", "if", "they", "their", "than",
           "from", "by", "at", "an", "was", "were", "have", "does",
           "into", "about", "we", "our", "there", "its", "it's", "that's", "don't"}
EN_ALLOWED = ("Advertising Cost of Sales", "lead time", "Lead time", "Buy Box",
              "Seller Central", "Campaign Manager", "Sponsored Products",
              "Sponsored Brands", "Sponsored Display", "Sponsored Brand",
              "trade-off", "trade dress", "venture capital", "landed cost",
              "Landed cost", "flywheel", "bulksheet", "listing", "Q4")


def check_untranslated(en_v, tr_v, field):
    a, b = text_nodes(en_v), text_nodes(tr_v)
    if len(a) != len(b):
        return []
    prob = []
    for (_, et), (_, tt) in zip(a, b):
        e, t = norm(et), norm(tt)
        # identical AND English: a postal address, a name or a product code
        # is legitimately identical in every language (contact.html's
        # "1209 Mountain Road Pl NE # 11990"); an English sentence carries at
        # least one English function word ("That's why great Amazon ...").
        ident_words = set(w.lower() for w in re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", t))
        if len(WORD.findall(e)) >= 4 and e == t and ident_words & EN_FUNC:
            prob.append("%s: text left identical to the English: %r" % (field, t[:80]))
            continue
        stripped = t
        for term in EN_ALLOWED:
            stripped = stripped.replace(term, " ")
        hits = sorted(set(w.lower() for w in re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", stripped)) & EN_FUNC)
        if len(hits) >= 2:
            prob.append("%s: English words %s in %r" % (field, hits, t[:80]))
    return prob


# Revenue after returns is not gross revenue. GLOSSARIO-PT: faturamento is
# GROSS; where the English means net of returns it must be "receita líquida".
NET_REVENUE_EN = re.compile(r"\bnet (?:revenue|sales)\b|\brevenue (?:after|net of) (?:returns|refunds)\b|"
                            r"\bafter (?:returns|refunds)\b", re.I)


def check_net_revenue(en_v, tr_v, field):
    a, b = text_nodes(en_v), text_nodes(tr_v)
    if len(a) != len(b):
        return []
    return ["%s: English says net revenue (%r) but the translation uses faturamento (%r)"
            % (field, norm(et)[:70], norm(tt)[:70])
            for (_, et), (_, tt) in zip(a, b)
            if NET_REVENUE_EN.search(norm(et)) and "faturamento" in norm(tt).lower()]


def nums(frag):
    # Entities are decoded first: "&#215;" is the sign x, not the number 215.
    # Without this, a translation that writes the same sign as &times; fails
    # the figure check (found 2026-09-11 by a translator, growth-vs-complexity).
    return NUM.findall(html.unescape(untagged(frag)))


def words(s):
    return html.unescape(s or "").split()


def audit(brief, tr, lang, slug_key=None, href_back=None, leak=True, pre=True):
    """Returns (elements_compared, problems). `href_back` maps a translated
    page's own local hrefs back to their English form -- used only when
    calibrating on BUILT pages, whose links were rewritten after the gate."""
    slug_key = slug_key or "%s_slug" % lang
    hb = href_back or (lambda h: h)
    prob, compared = [], 0

    for field in FIELDS:
        en_v, tr_v = brief.get(field), tr.get(field)
        if en_v is None:
            if tr_v:
                prob.append("%s: English has none, translation supplied one" % field)
            continue
        if not tr_v:
            prob.append("%s: missing from the translation" % field)
            continue
        if href_back:
            # built pages: links were rewritten AFTER the gate, by design;
            # compare structure as the gate originally saw it
            tr_v = re.sub(r'href="([^"]*)"', lambda m: 'href="%s"' % hb(m.group(1)), tr_v)
        d = P.skeleton_diff(en_v, tr_v)
        if d:
            prob.append("%s skeleton: %s" % (field, d))
            continue
        compared += len(P.skeleton(en_v))

        for k, pat in (("ids", r'\bid="([^"]+)"'), ("hrefs", r'\bhref="([^"]+)"')):
            a = re.findall(pat, en_v)
            c = re.findall(pat, tr_v)
            if k == "hrefs":
                c = [hb(h) for h in c]
            if a != c:
                prob.append("%s %s differ\n  EN %s\n  %s %s" % (field, k, a, lang.upper(), c))

        a, c = nums(en_v), nums(tr_v)
        if a != c:
            prob.append("%s figures differ\n  EN %s\n  %s %s" % (field, a, lang.upper(), c))

        if pre:
            prob += check_pre(en_v, tr_v, field)
        prob += check_labels(en_v, tr_v, field, lang)
        prob += check_untranslated(en_v, tr_v, field)
        prob += check_vocab(tr_v, field, lang)
        if lang == "pt":
            prob += check_net_revenue(en_v, tr_v, field)

        t = " " + re.sub(r"\s+", " ", text_of(tr_v)) + " "
        hits = [w for w in STOP_EN if w in t]
        if hits:
            prob.append("%s: English survived: %s" % (field, hits))

        if leak and lang in LEAK:
            # dotted tokens are identifiers, not words: Amazon.es, Amazon.com.br,
            # resources.json. Split, "Amazon.es" read as the Spanish word "es"
            # (found 2026-09-11 in the waitlist dialog's marketplace list).
            plain = re.sub(r"\b[\w-]+(?:\.[\w-]+)+\b", " ", text_of(tr_v))
            toks = set(w.lower() for w in WORD.findall(plain))
            for kind, bad in sorted(LEAK[lang].items()):
                hit = sorted(toks & bad)
                if hit:
                    prob.append("%s: %s words: %s" % (field, kind, hit))

        if lang == "pt":
            plain = text_of(tr_v)
            if re.search(r"\d[  ]%", plain):
                prob.append("%s: percentage with a space (decision 2 says 25%%)" % field)
            if "«" in plain or "»" in plain:
                prob.append("%s: angle quotes (decision 2 says curly quotes)" % field)
            if '"' in untagged(tr_v):
                prob.append("%s: straight double quote in text (use &ldquo; &rdquo;)" % field)

    if prob:
        return compared, prob

    # ---- customer lifetime value (GLOSSARIO-PT §3): the long form once per
    # article, carrying (LTV); every later use is plain LTV
    if lang == "pt":
        whole = norm(" ".join(text_of(tr.get(f)) for f in FIELDS if tr.get(f)))
        uses = [m.start() for m in re.finditer(r"valor vital[ií]cio do cliente", whole, re.I)]
        if len(uses) > 1:
            prob.append("'valor vitalício do cliente' appears %d times; first use only, then LTV" % len(uses))
        for u in uses:
            if not whole[u:u + 40].lower().startswith("valor vitalício do cliente (ltv)"):
                prob.append("'valor vitalício do cliente' without '(LTV)': %r" % whole[u:u + 50])

    # ---- head strings
    for k in ("title", "desc", "og_title", "og_desc"):
        if not tr.get(k):
            prob.append("head string %s missing" % k)
    for k in ("ld_headline", "ld_desc", "crumb"):
        if brief.get(k) and not tr.get(k):
            prob.append("JSON-LD field %s missing (English has one)" % k)
        if tr.get(k) and ENTITY.search(tr[k]):
            prob.append("HTML entity in plain-text field %s: %r" % (k, tr[k][:60]))
    if len(tr.get("keywords") or []) != len(brief.get("keywords") or []):
        prob.append("keywords: English has %d, translation %d"
                    % (len(brief.get("keywords") or []), len(tr.get("keywords") or [])))
    for k in tr.get("keywords") or []:
        if ENTITY.search(k):
            prob.append("HTML entity in keyword %r" % k)
    for k in ("title", "desc", "og_title", "og_desc", "og_img_alt", "hero_alt"):
        v = tr.get(k)
        if v and re.search(u"[À-ſ]", v):
            prob.append("raw accented character in attribute field %s: %r" % (k, v[:60]))
        if v and '"' in v:
            prob.append("raw double quote in attribute field %s" % k)

    # ---- hero alt: presence follows the English; 8-14 words; one string, three places
    for k in ("hero_alt", "og_img_alt"):
        if bool(brief.get(k)) != bool(tr.get(k)):
            prob.append("%s: English %s one, translation %s"
                        % (k, "has" if brief.get(k) else "has no",
                           "has one" if tr.get(k) else "has none"))
    if tr.get("hero_alt"):
        n = len(words(tr["hero_alt"]))
        if not ALT_WORDS[0] <= n <= ALT_WORDS[1]:
            prob.append("hero_alt is %d words; the rule is %d-%d" % ((n,) + ALT_WORDS))
        if tr.get("og_img_alt") and tr["og_img_alt"] != tr["hero_alt"]:
            prob.append("hero_alt and og_img_alt differ; they describe one picture")

    # ---- slug: refused, never trimmed
    sl = tr.get(slug_key)
    if not sl or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", sl):
        prob.append("bad %s %r" % (slug_key, sl))
    else:
        nc, nw = len(sl), len(sl.split("-"))
        if nc > SLUG_MAX_CHARS or nw > SLUG_MAX_WORDS:
            prob.append("%s %r is %d chars / %d words; the caps are %d chars AND %d words"
                        % (slug_key, sl, nc, nw, SLUG_MAX_CHARS, SLUG_MAX_WORDS))
    return compared, prob


def slug_report(sl):
    return "%d chars / %d words" % (len(sl), len(sl.split("-")))


if __name__ == "__main__":
    a = sys.argv[1:]
    def opt(name):
        i = a.index(name)
        v = a[i + 1]
        del a[i:i + 2]
        return v
    brief_p, content_p = opt("--brief"), opt("--content")
    lang, slug = a[0], a[1]
    brief = json.load(io.open(brief_p, encoding="utf-8"))
    tr = json.load(io.open(content_p, encoding="utf-8"))
    assert brief["slug"] == slug == tr.get("slug"), "slug mismatch: brief %r, content %r, arg %r" % (
        brief["slug"], tr.get("slug"), slug)
    n, prob = audit(brief, tr, lang)
    sl = tr.get("%s_slug" % lang) or ""
    print("%-30s %-4s %s (%s)  %d elements compared"
          % (slug, "OK" if not prob else "FAIL", sl, slug_report(sl) if sl else "-", n))
    for p in prob:
        print("      " + p.replace("\n", "\n      "))
    print("\n%d problems" % len(prob))
    raise SystemExit(1 if prob else 0)
