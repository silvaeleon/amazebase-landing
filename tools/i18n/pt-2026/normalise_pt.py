# -*- coding: utf-8 -*-
"""
Settle cross-translator drift in the Portuguese content, deterministically.

    python tools/i18n/pt-2026/normalise_pt.py <site-root> <content-dir> <briefs-dir> [--check]

Runs AFTER each translation has passed the gate and BEFORE the build:

  1. fixed labels  every callout label the glossary fixes (GLOSSARIO-PT.md §6)
                   is written in exactly, aligned to the English text node by
                   position. Editing a row in the glossary and re-running this is
                   how a label changes across all 51 articles.
  2. nbsp          a number and its unit word are joined by &nbsp; so a line can
                   never wrap between them (outside <pre>, where nothing wraps).
  3. slugs        unique, and inside both caps -- the gate refuses; this confirms
                   across the whole set.
  4. review lists every "custo total de importação" and every "faturamento",
                   printed with the English beside it, for a human to check the
                   two glossary conditions a regex cannot decide.

Cross-article links are NOT rewritten here: build_pt.py does that from the
same content set, once every slug exists (README: do not merge that step into
translation).

--check reports what would change and writes nothing.
"""

import html, io, json, os, re, sys
from html.entities import codepoint2name

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gate

FIELDS = ("main", "article_head", "rail", "cta")
UNITS = (r"dias?|semanas?|meses|m&ecirc;s|anos?|horas?|unidades?|minutos?|min")
NBSP = re.compile(r"(\d(?:[\d,]*\d)?(?:\.\d+)?) +(%s)\b" % UNITS)


def encode(t):
    """House style: named entities for every non-ASCII character."""
    out = []
    for ch in t:
        o = ord(ch)
        if o < 128:
            out.append({"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(ch, ch))
        else:
            name = codepoint2name.get(o)
            out.append("&%s;" % name if name else "&#x%X;" % o)
    return "".join(out)


def tokens(frag):
    return re.split(r"(<!--.*?-->|<[^>]+>)", frag, flags=re.S)


def logical_nodes(toks):
    """Text nodes as gate.text_nodes() sees them (comments transparent):
    [(class, [token indices of the text pieces])]."""
    nodes, cur, prev_tag = [], None, None
    for i, t in enumerate(toks):
        if t.startswith("<!--"):
            continue
        if t.startswith("<"):
            if cur is not None:
                nodes.append(cur)
                cur = None
            prev_tag = t
            continue
        if cur is None:
            cls = None
            if prev_tag and not prev_tag.startswith("</"):
                m = re.search(r'\bclass="([^"]*)"', prev_tag)
                cls = m.group(1) if m else ""
            cur = (cls, [])
        cur[1].append(i)
    if cur is not None:
        nodes.append(cur)
    return nodes


def apply_labels(en_frag, pt_frag, exact, rules, log, where):
    en_nodes = gate.text_nodes(en_frag)
    toks = tokens(pt_frag)
    pt_nodes = logical_nodes(toks)
    assert len(en_nodes) == len(pt_nodes), "%s: cannot align (%d vs %d)" % (where, len(en_nodes), len(pt_nodes))
    for (cls, et), (_, idx) in zip(en_nodes, pt_nodes):
        want = gate.expected_label(et, cls, exact, rules)
        if want is None:
            continue
        cur = "".join(toks[i] for i in idx)
        if gate.norm(cur) == want:
            continue
        lead = re.match(r"\s*", cur).group(0)
        trail = re.search(r"\s*$", cur).group(0)
        toks[idx[0]] = lead + encode(want) + trail
        for i in idx[1:]:
            toks[i] = ""
        log.append("%s: label %r  %r -> %r" % (where, gate.norm(et), gate.norm(cur), want))
    return "".join(toks)


def apply_vocab(frag, vocab, log, where):
    """Settled vocabulary (GLOSSARIO-PT.md §7), text nodes only; a node is
    re-encoded only if something in it changed."""
    toks, n = tokens(frag), 0
    for i, t in enumerate(toks):
        if not t or t.startswith("<"):
            continue
        plain = html.unescape(t)
        new = gate.settle(plain, vocab)
        if new != plain:
            toks[i] = encode(new)
            n += 1
    if n:
        log.append("%s: %d text nodes had a settled-vocabulary variant replaced" % (where, n))
    return "".join(toks)


def apply_nbsp(frag, log, where):
    out, n = [], 0
    in_pre = False
    for t in tokens(frag):
        if t.startswith("<"):
            low = t.lower()
            if re.match(r"<(pre|code)\b", low):
                in_pre = True
            elif re.match(r"</(pre|code)\b", low):
                in_pre = False
            out.append(t)
            continue
        if not in_pre:
            t, k = NBSP.subn(r"\1&nbsp;\2", t)
            n += k
        out.append(t)
    if n:
        log.append("%s: %d number-unit spaces made non-breaking" % (where, n))
    return "".join(out)


def review(brief, tr, needle, en_hint):
    """(english node, portuguese node) pairs where the Portuguese uses `needle`."""
    rows = []
    for f in FIELDS:
        if not brief.get(f) or not tr.get(f):
            continue
        a, b = gate.text_nodes(brief[f]), gate.text_nodes(tr[f])
        if len(a) != len(b):
            continue
        for (_, et), (_, tt) in zip(a, b):
            if needle in gate.norm(tt).lower():
                rows.append((gate.norm(et), gate.norm(tt), bool(re.search(en_hint, gate.norm(et), re.I))))
    return rows


def main(tree, content, briefs, check=False):
    exact, rules = gate.load_labels("pt")
    vocab = gate.load_vocab("pt")
    files = sorted(f for f in os.listdir(content) if f.endswith(".json"))
    log, slugs, fat, lc = [], {}, [], []
    for fn in files:
        p = os.path.join(content, fn)
        tr = json.load(io.open(p, encoding="utf-8"))
        brief = json.load(io.open(os.path.join(briefs, tr["slug"] + ".json"), encoding="utf-8"))
        before = json.dumps(tr, ensure_ascii=False, sort_keys=True)
        for f in FIELDS:
            if tr.get(f) and brief.get(f):
                tr[f] = apply_labels(brief[f], tr[f], exact, rules, log, "%s/%s" % (tr["slug"], f))
                tr[f] = apply_vocab(tr[f], vocab, log, "%s/%s" % (tr["slug"], f))
                tr[f] = apply_nbsp(tr[f], log, "%s/%s" % (tr["slug"], f))
        # plain-text fields: JSON-LD strings and keywords carry real characters;
        # head strings carry entities -- settle each in its own encoding
        for k in ("ld_headline", "ld_desc", "crumb"):
            if tr.get(k):
                new = gate.settle(tr[k], vocab)
                if new != tr[k]:
                    log.append("%s/%s: settled vocabulary" % (tr["slug"], k))
                    tr[k] = new
        if tr.get("keywords"):
            new = [gate.settle(k, vocab) for k in tr["keywords"]]
            if new != tr["keywords"]:
                log.append("%s/keywords: settled vocabulary %s" % (tr["slug"], [k for k in new if k not in tr["keywords"]]))
                tr["keywords"] = new
        for k in ("title", "desc", "og_title", "og_desc", "hero_alt", "og_img_alt"):
            if tr.get(k):
                plain = html.unescape(tr[k])
                new = gate.settle(plain, vocab)
                if new != plain:
                    log.append("%s/%s: settled vocabulary" % (tr["slug"], k))
                    tr[k] = encode(new)
        slugs.setdefault(tr["pt_slug"], []).append(tr["slug"])
        fat += [(tr["slug"],) + r for r in review(brief, tr, "faturamento", r"\bnet\b|return|refund")]
        lc += [(tr["slug"],) + r for r in review(brief, tr, "custo total de importa",
                                                  r"import|freight|customs|duty|overseas|china|supplier|ocean")]
        if json.dumps(tr, ensure_ascii=False, sort_keys=True) != before and not check:
            io.open(p, "w", encoding="utf-8", newline="\n").write(
                json.dumps(tr, ensure_ascii=False, indent=1) + "\n")

    dup = dict((s, v) for s, v in slugs.items() if len(v) > 1)
    print("normalise_pt: %d translations%s" % (len(files), " (--check: nothing written)" if check else ""))
    for line in log:
        print("  " + line)
    print("  %d changes" % len(log))
    print("\nslugs: %d unique of %d%s" % (len(slugs), len(files),
                                          "" if not dup else "  DUPLICATES: %s" % dup))
    print("\nreview -- faturamento (%d). Glossary: gross revenue only; net of returns is receita liquida."
          % len(fat))
    for slug, et, tt, hint in fat:
        print("  %s %-26s EN: %.90s\n  %s %-26s PT: %.90s" % ("!" if hint else " ", slug, et, " ", "", tt))
    print("\nreview -- custo total de importação (%d). Glossary: imported goods only." % len(lc))
    for slug, et, tt, hint in lc:
        print("  %s %-26s EN: %.90s\n  %s %-26s PT: %.90s" % (" " if hint else "!", slug, et, " ", "", tt))
    if dup:
        raise SystemExit(1)


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    main(a[0], a[1], a[2], check="--check" in sys.argv)
