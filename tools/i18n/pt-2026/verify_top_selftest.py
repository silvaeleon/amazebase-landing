# -*- coding: utf-8 -*-
"""
Prove verify_top_pt.py can fail: plant one defect at a time in a built page,
check the verifier names it, restore the page byte-identical.

    python tools/i18n/pt-2026/verify_top_selftest.py <site-root>
"""

import hashlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import verify_top_pt as VT, build_top_pt as BT


def main(tree):
    pt_map = json.load(io.open(os.path.join(tree, "tools", "i18n", "slugs", "pt.json"), encoding="utf-8"))
    content = os.path.join(HERE, "content-top")
    pages = dict((k, (en, pt, es)) for k, en, pt, es in BT.PAGES)
    cases = [
        ("product", "honeypot company_website renamed", 'name="company_website"', 'name="company_site"', "dialog lost"),
        ("product", "honeypot referral_code removed", 'name="referral_code"', 'name="ref"', "dialog lost"),
        ("product", "a data-msg-* string dropped", 'data-msg-rate="', 'data-rate="', "data-msg-*"),
        ("product", "developer comment translated", "Honeypots. Hidden from humans", "Honeypots. Ocultos", "not verbatim"),
        ("solutions", "English left in the dialog", ">Entre na lista de espera</button>", ">Join the wait list</button>", "English chrome left"),
        ("resources", "CollectionPage left English", '"inLanguage": "pt"', '"inLanguage": "en"', "CollectionPage"),
        ("resources", "fallback card to a missing page", 'class="hub-row" href="/pt/artigos/', 'class="hub-row" href="/pt/artigos/nao-existe-', "fallback rows"),
        ("contact", "relative stylesheet again", 'href="/css/base.css"', 'href="css/base.css"', "relative URLs"),
        ("about", "canonical left English", 'rel="canonical" href="https://amazebase.pro/pt/sobre.html"',
         'rel="canonical" href="https://amazebase.pro/about.html"', "canonical"),
    ]
    ok = True
    for key, label, old, new, expect in cases:
        en_rel, pt_rel, es_rel = pages[key]
        path = os.path.join(tree, pt_rel)
        clean = io.open(path, "rb").read()
        h0 = hashlib.sha256(clean).hexdigest()
        s = clean.decode("utf-8")
        assert s.count(old) >= 1, "anchor missing: " + label
        tr = json.load(io.open(os.path.join(content, key + ".json"), encoding="utf-8"))
        try:
            io.open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new, 1))
            P, _ = VT.check(tree, key, en_rel, pt_rel, es_rel, tr, pt_map)
        finally:
            io.open(path, "wb").write(clean)
        assert hashlib.sha256(io.open(path, "rb").read()).hexdigest() == h0, "restore failed"
        hit = any(expect in p for p in P)
        ok &= hit
        print("  %-10s %-38s %s" % (key, label, "CAUGHT" if hit else "MISSED  <-- %s" % P[:2]))
    print("all pages restored byte-identical")
    print("\nSELFTEST %s" % ("PASSED" if ok else "FAILED"))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1])
