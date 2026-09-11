# -*- coding: utf-8 -*-
"""
Capitalised terms in the English legal pages: every one must be DEFINED.

In a contract, a capitalised word signals "this word has the meaning given
elsewhere in this document". Undefined, it signals a definitions section that
got lost. This asserts on the whole set, not the few somebody noticed:

  defined    the term appears in quotes inside a parenthetical definition,
             e.g. ("Customer", "User", or "you") or (the "Platform")
  names      proper nouns: people, companies, places, products, standards
  titles     the name of a document or a heading-style reference
  plural     "Customers" counts as "Customer"

Everything else that is capitalised mid-sentence is reported as UNDEFINED
and fails the check.

    python tools/legal_terms.py [page ...]      # default: terms.html privacy.html
"""

import html, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAMES = {"AmazeBase", "Silbros Trading LLC", "Silbros Trading", "LLC", "Amazon", "New Mexico",
         "United States", "Internet", "Albuquerque", "NM", "NE", "PL", "Mountain Road", "API", "APIs",
         "Stripe", "Google", "Seller Central", "Amazon Seller Central", "Amazon Advertising",
         "State of New Mexico", "EU", "UK", "GDPR", "CCPA", "European Union", "European Economic Area",
         "California", "AS IS", "AS AVAILABLE", "Effective Date", "Last Updated", "I"}
TITLES = {"Terms of Service", "Privacy Policy", "This Privacy Policy", "These Terms", "Terms"}


def text_blocks(s):
    main = re.search(r"<main\b.*?</main>", s, re.S).group(0)
    main = re.sub(r"<!--.*?-->", " ", main, flags=re.S)
    # the table of contents repeats the headings, which are title case by design
    main = re.sub(r"<(nav|aside)\b.*?</\1>", " ", main, flags=re.S)
    out = []
    for tag, body in re.findall(r"<(p|li|td|dd|dt)\b[^>]*>(.*?)</\1>", main, re.S):
        t = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())
        if t:
            out.append(t)
    return out


def definitions(blocks):
    """Quoted terms inside a parenthetical: ("A", "B", or "c") / (the "X") /
    (together, the "Y")."""
    d = set()
    for t in blocks:
        for par in re.findall(r"\(([^()]*[“\"][^()]*)\)", t):
            for q in re.findall(r"[“\"]([^”\"]+)[”\"]", par):
                d.add(q.strip(" ,.").rstrip(","))
        # the other form: "Customer Data" means ...
        for q in re.findall(r"[“\"]([^”\"]+)[”\"]\s+means\b", t):
            d.add(q.strip(" ,."))
    return d


CAP = re.compile(r"(?<![.!?:;“\"(]\s)(?<!^)\b([A-Z][a-zA-Z]+(?:\s+(?:of\s+)?[A-Z][a-zA-Z]+)*)")


def capitalised(blocks):
    """Capitalised runs NOT at the start of a sentence or list item."""
    found = {}
    for t in blocks:
        for sent in re.split(r"(?<=[.!?:;])\s+", t):
            words = sent.split()
            if not words:
                continue
            for m in re.finditer(r"\b[A-Z][A-Za-z]+(?:\s+(?:of\s+)?[A-Z][A-Za-z]+)*", sent):
                if m.start() == 0 or sent[:m.start()].rstrip().endswith(("“", '"', "(")):
                    continue
                found.setdefault(m.group(0), sent[:90])
    return found


def check(page):
    s = io.open(os.path.join(ROOT, page), encoding="utf-8").read()
    blocks = text_blocks(s)
    defs = definitions(blocks)
    caps = capitalised(blocks)
    undefined = {}
    ok = defs | NAMES | TITLES

    def known(w):
        return w in ok or (w.endswith("s") and w[:-1] in ok) or re.fullmatch(r"[A-Z]{2,6}s?", w)
    for term, where in caps.items():
        # a run is fine when it is itself known, or every word in it is
        # ("AmazeBase Platform", "Amazon APIs", "Customers")
        if known(term) or all(known(w) for w in term.replace(" of ", " ").split()):
            continue
        undefined[term] = where
    return defs, caps, undefined


if __name__ == "__main__":
    pages = sys.argv[1:] or ["terms.html", "privacy.html"]
    bad = 0
    for page in pages:
        defs, caps, undefined = check(page)
        print("== %s" % page)
        print("   defined (%d): %s" % (len(defs), ", ".join(sorted(defs))))
        print("   capitalised mid-sentence (%d distinct)" % len(caps))
        for term, where in sorted(undefined.items()):
            print("   UNDEFINED  %-24s in: %s" % (term, where))
        bad += len(undefined)
    print("\n%d undefined capitalised terms" % bad)
    raise SystemExit(1 if bad else 0)
