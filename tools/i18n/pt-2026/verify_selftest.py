# -*- coding: utf-8 -*-
"""
Prove verify_pt.py can fail: plant one defect at a time in a built page, check
the verifier names it, then rebuild the page from its content JSON.

    PT_BRIEFS=<briefs-dir> python tools/i18n/pt-2026/verify_selftest.py <site-root> <content-dir> <slug>

A verifier that has only ever been seen green has not been seen working.
"""

import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_pt, verify_pt


def main(tree, content, slug):
    briefs = os.environ["PT_BRIEFS"]
    tr = json.load(io.open(os.path.join(content, slug + ".json"), encoding="utf-8"))
    brief = json.load(io.open(os.path.join(briefs, slug + ".json"), encoding="utf-8"))
    pt_map = dict((json.load(io.open(os.path.join(content, f), encoding="utf-8"))["slug"],
                   json.load(io.open(os.path.join(content, f), encoding="utf-8"))["pt_slug"])
                  for f in os.listdir(content) if f.endswith(".json"))
    path = os.path.join(tree, "pt", "artigos", tr["pt_slug"] + ".html")
    clean = io.open(path, encoding="utf-8", newline="").read()

    P, _ = verify_pt.check_page(tree, tr, brief, pt_map)
    assert not P, "the clean page must pass first: %s" % P
    print("control: clean page passes")

    en_title = brief["title"]
    cases = [
        ("English <title> left in the head",
         lambda s: re.sub(r"<title>.*?</title>", "<title>%s &mdash; AmazeBase</title>" % en_title, s, count=1),
         "English title survives"),
        ("canonical still points at the English page",
         lambda s: s.replace('<link rel="canonical" href="https://amazebase.pro/pt/artigos/',
                             '<link rel="canonical" href="https://amazebase.pro/articles/X', 1),
         "canonical"),
        ("hero src relative again (../assets)",
         lambda s: s.replace('src="/assets/img/hero-', 'src="../assets/img/hero-', 1),
         "relative URLs"),
        ("srcset with one relative candidate",
         lambda s: s.replace('<img src="/assets/img/hero-',
                             '<img srcset="/assets/img/a.webp 1x, assets/img/b.webp 2x" src="/assets/img/hero-', 1),
         "relative URLs"),
        ("og:image:alt differs from the hero alt",
         lambda s: re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r"\1outra coisa", s, count=1),
         "disagree"),
        ("one </div> removed",
         lambda s: s.replace("</div>", "", 1),
         "unbalanced"),
        ("JSON-LD made invalid",
         lambda s: s.replace('"@context"', '"@context" "', 1),
         "does not parse"),
        ("English 'Log in' left in the nav",
         lambda s: s.replace(">Entrar</a>", ">Log in</a>", 1),
         "English chrome left"),
        ("English sentence left in the body",
         lambda s: s.replace("</p>", " and the rest of your stock</p>", 1),
         "English stopwords"),
        ("link to a page that does not exist",
         # the wait-list link is /pt/#waitlist since the Portuguese homepage exists (2026-09-11)
         lambda s: s.replace('href="/pt/#waitlist"', 'href="/nowhere.html"', 1),
         "resolve to nothing"),
        ("a CRLF line ending",
         lambda s: s.replace("\n", "\r\n", 1),
         "CR bytes"),
        ("an extra <em> the English does not have",
         lambda s: s.replace('<p class="lead">', '<p class="lead"><em>x</em>', 1),
         "body skeleton differs"),
    ]
    ok = True
    try:
        for label, fn, expect in cases:
            m = fn(clean)
            assert m != clean, "mutation did not apply: " + label
            io.open(path, "w", encoding="utf-8", newline="").write(m)
            P, _ = verify_pt.check_page(tree, tr, brief, pt_map)
            hit = any(expect in p for p in P)
            ok &= hit
            print("  %-46s %s" % (label, "CAUGHT" if hit else "MISSED  <-- %s" % P[:2]))
    finally:
        io.open(path, "w", encoding="utf-8", newline="").write(clean)
    P, _ = verify_pt.check_page(tree, tr, brief, pt_map)
    assert not P, "restore failed"
    print("restored: clean page passes again")
    print("\nSELFTEST %s" % ("PASSED" if ok else "FAILED"))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
