# -*- coding: utf-8 -*-
"""
Defined terms in the legal pages, in every language: each capitalised term is
DEFINED, and defined BEFORE it is used.

In a contract a capitalised word signals "this word has the meaning given in
this document". Two defects look alike:
  - UNDEFINED: the term is never defined (a definitions section got lost);
  - USED BEFORE DEFINED: prose relies on a meaning the reader has not met yet.
The first version of this check (2026-09-11) caught only the first. Privacy
passed it while section 2 said "We do not sell Customer Data ..." and section
3 defined "Customer Data" below it. A contract that uses a term before
defining it is the same class of defect as one that never defines it, so both
are asserted, on the whole set, not on the terms somebody happened to notice.

  prose      <p> <li> <td> <dd> <dt> inside <main>. Headings, the table of
             contents (<nav>, <aside>) and comments are not prose.
  defined    a quoted term inside a parenthetical ("Customer", "User", or
             "you") / (the "Platform"), or the form "X" means ... (es/pt:
             significa). The definition applies from the paragraph it is in.
  names      proper nouns, places, products, standards, per language
  titles     the names of documents
  plural     "Customers" and "Clientes" count as the term

A defined term's use as part of a longer proper name is not a use: the legal
name "Silbros Trading LLC" precedes its short form ("Silbros Trading").

    python tools/legal_terms.py [page ...]      # default: the six legal pages
"""

import html, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["terms.html", "privacy.html", "es/terminos.html", "es/privacidad.html",
         "pt/termos.html", "pt/privacidade.html"]

COMMON = {"AmazeBase", "Silbros Trading LLC", "LLC", "Amazon", "Internet", "Albuquerque", "NM", "NE",
          "PL", "Mountain Road", "Stripe", "Google", "Seller Central", "Amazon Seller Central",
          "Amazon Advertising", "GDPR", "CCPA", "I", "Mountain Road PL NE", "Helium",
          # the analytics disclosure, added with GA4 (2026-09-11)
          "Google Analytics", "Google Analytics 4", "Google Ads", "Google Consent Mode",
          # the session-recording disclosure, added with Clarity (2026-09-12)
          "Microsoft", "Microsoft Clarity", "Microsoft Corporation"}
NAMES = {
    "en": COMMON | {"New Mexico", "United States", "State of New Mexico", "European Union",
                    "European Economic Area", "California", "AS IS", "AS AVAILABLE",
                    "Effective Date", "Last Updated", "United Kingdom", "Switzerland"},
    "es": COMMON | {"Nuevo México", "Estados Unidos", "Estado de Nuevo México", "Unión Europea",
                    "TAL CUAL", "SEGÚN DISPONIBILIDAD", "Fecha de entrada en vigor", "Última actualización",
                    "Espacio Económico Europeo", "Reino Unido", "Suiza",
                    "Modo"},   # heads "Modo de consentimiento de Google", whose tail is lowercase
    "pt": COMMON | {"Novo México", "Estados Unidos", "Estado do Novo México", "União Europeia",
                    "NO ESTADO EM QUE SE ENCONTRA", "CONFORME DISPONÍVEL", "Data de vigência",
                    "Última atualização", "Espaço Econômico Europeu", "Reino Unido", "Suíça",
                    "Modo"},   # heads "Modo de consentimento do Google", whose tail is lowercase
}
TITLES = {
    "en": {"Terms of Service", "Privacy Policy", "This Privacy Policy", "These Terms", "Terms"},
    "es": {"Términos del Servicio", "Política de Privacidad", "Esta Política de Privacidad", "Estos Términos",
           "Términos"},
    "pt": {"Termos de Serviço", "Política de Privacidade", "Esta Política de Privacidade", "Estes Termos",
           "Termos"},
}
MEANS = {"en": r"means", "es": r"significa", "pt": r"significa"}
# lowercase words that may sit inside a capitalised run ("State of New Mexico", "Datos del Cliente")
JOIN = {"en": r"of", "es": r"de|del", "pt": r"de|do|da|dos|das"}
WORD = r"[A-ZÀ-Ý][A-Za-zÀ-ÿ]+"


def lang_of(s):
    return re.search(r'<html lang="([a-z]+)', s).group(1)


def text_blocks(s, with_sections=False):
    """Prose blocks in document order; with_sections=True also gives the
    number of the numbered <h2> ("3. Customer Data") each block sits under."""
    main = re.search(r"<main\b.*?</main>", s, re.S).group(0)
    main = re.sub(r"<!--.*?-->", " ", main, flags=re.S)
    # the table of contents repeats the headings, which are title case by design
    main = re.sub(r"<(nav|aside)\b.*?</\1>", " ", main, flags=re.S)
    out, sec = [], None
    for tag, body in re.findall(r"<(h2|p|li|td|dd|dt)\b[^>]*>(.*?)</\1>", main, re.S):
        t = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())
        if tag == "h2":
            m = re.match(r"(\d+)\.", t)
            sec = m.group(1) if m else sec
            continue
        if t:
            out.append((sec, t) if with_sections else t)
    return out


# "(as defined in section 3)": a forward reference is not a use before
# definition -- provided the section it names really holds the definition.
XREF = {"en": r"\(as defined in section (\d+)\)",
        "es": r"\(tal como se define en la sección (\d+)\)",
        "pt": r"\(conforme definido na seção (\d+)\)"}


def definitions(blocks, lang):
    """{term: index of the first block that defines it}"""
    d = {}
    for i, t in enumerate(blocks):
        found = []
        for par in re.findall(r"\(([^()]*[“\"][^()]*)\)", t):
            found += re.findall(r"[“\"]([^”\"]+)[”\"]", par)
        found += re.findall(r"[“\"]([^”\"]+)[”\"]\s+(?:%s)\b" % MEANS[lang], t)
        for q in found:
            d.setdefault(q.strip(" ,.").rstrip(","), i)
    return d


def capitalised(blocks, lang):
    """Capitalised runs NOT at the start of a sentence or list item."""
    run = re.compile(r"\b%s(?:\s+(?:(?:%s)\s+)?%s)*" % (WORD, JOIN[lang], WORD))
    found = {}
    for t in blocks:
        for sent in re.split(r"(?<=[.!?:;])\s+", t):
            for m in run.finditer(sent):
                if m.start() == 0 or sent[:m.start()].rstrip().endswith(("“", '"', "(", "¿", "¡")):
                    continue
                found.setdefault(m.group(0), sent[:90])
    return found


def first_use(blocks, term, names, lang=None, def_section=None, bad_xref=None):
    """Index of the first block whose prose uses `term` (or its plural) other
    than inside a longer proper name, or with a CORRECT forward reference.
    A reference naming the wrong section is recorded in bad_xref."""
    longer = [n for n in names if term in n and n != term]
    pat = re.compile(r"\b%s(?:s|es)?\b" % re.escape(term))
    for i, t in enumerate(blocks):
        for m in pat.finditer(t):
            if any(t.find(n, max(0, m.start() - len(n)), m.end() + len(n)) >= 0 and
                   t.find(n, max(0, m.start() - len(n))) <= m.start() for n in longer):
                continue
            x = re.match(r"\s*" + XREF[lang], t[m.end():]) if lang else None
            if x:
                if x.group(1) == def_section:
                    continue
                if bad_xref is not None:
                    bad_xref[term] = (x.group(0), def_section)
            return i, t[max(0, m.start() - 40):m.end() + 40]
    return None, None


def check(page):
    s = io.open(os.path.join(ROOT, page), encoding="utf-8").read()
    lang = lang_of(s)
    blocks = text_blocks(s)
    defs = definitions(blocks, lang)
    caps = capitalised(blocks, lang)
    ok = set(defs) | NAMES[lang] | TITLES[lang]

    def known(w):
        return w in ok or (w.endswith("s") and w[:-1] in ok) or (w.endswith("es") and w[:-2] in ok) \
            or re.fullmatch(r"[A-Z]{2,6}s?", w)
    undefined = {}
    for term, where in caps.items():
        words = re.sub(r"\s(?:%s)\s" % JOIN[lang], " ", term).split()
        if known(term) or all(known(w) for w in words):
            continue
        undefined[term] = where
    sections = [sec for sec, _ in text_blocks(s, with_sections=True)]
    early, bad_xref = {}, {}
    for term, at in defs.items():
        if not term[:1].isupper():
            continue                       # "we", "you", "nosotros": pronouns, not capitalised terms
        i, where = first_use(blocks, term, NAMES[lang] | TITLES[lang], lang, sections[at], bad_xref)
        if i is not None and i < at:
            early[term] = (i, at, where)
    return lang, defs, caps, undefined, early, bad_xref


if __name__ == "__main__":
    pages = sys.argv[1:] or PAGES
    n_undef = n_early = n_xref = 0
    for page in pages:
        lang, defs, caps, undefined, early, bad_xref = check(page)
        for term, (ref, sec) in sorted(bad_xref.items()):
            print("   WRONG REFERENCE     %-22s says %r, but it is defined in section %s" % (term, ref, sec))
        print("== %s (%s)" % (page, lang))
        print("   defined (%d): %s" % (len(defs), ", ".join(sorted(defs))))
        print("   capitalised mid-sentence: %d distinct" % len(caps))
        for term, where in sorted(undefined.items()):
            print("   UNDEFINED           %-22s in: %s" % (term, where))
        for term, (i, at, where) in sorted(early.items()):
            print("   USED BEFORE DEFINED %-22s paragraph %d, defined in %d: ...%s..." % (term, i + 1, at + 1, where))
        n_undef += len(undefined)
        n_early += len(early)
        n_xref += len(bad_xref)
    print("\n%d undefined capitalised terms, %d terms used before their definition, "
          "%d wrong section references, across %d pages" % (n_undef, n_early, n_xref, len(pages)))
    raise SystemExit(1 if n_undef or n_early or n_xref else 0)
