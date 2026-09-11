# -*- coding: utf-8 -*-
"""
Prove home_legal.py verify and blocks_guard.py can fail: plant one defect at a
time in a BUILT page, require it to be caught, restore the page byte-identical.

    python tools/i18n/home_legal_selftest.py <site-root> <briefs-dir>
"""

import contextlib, io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import home_legal as H


def run_verify(tree, briefs, lang):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        bad = H.verify(tree, briefs, [lang])
    return bad, buf.getvalue()


def guard(tree):
    r = subprocess.run([sys.executable, os.path.join(HERE, "blocks_guard.py"), tree], capture_output=True, text=True)
    return r.returncode, r.stdout


MUTATIONS = [
    # (page, label, old, new, expect-in-output, which checker)
    ("es/index.html", "html lang back to English", '<html lang="es">', '<html lang="en">', "html lang", "verify"),
    ("es/index.html", "canonical pointing at English", '<link rel="canonical" href="https://amazebase.pro/es/">',
     '<link rel="canonical" href="https://amazebase.pro/">', "canonical", "verify"),
    ("es/index.html", "English 'Log in' left in the nav", ">Iniciar sesi&oacute;n<", ">Log in<", "English left", "verify"),
    ("es/index.html", "a honeypot renamed", 'name="referral_code"', 'name="referral"', "waitlist dialog damaged", "verify"),
    ("es/index.html", "a link to a page that does not exist", 'href="/es/#pricing"', 'href="/es/nowhere.html"',
     "unresolved", "verify"),
    ("es/index.html", "an attribute dropped in main", "data-waitlist-open data-source=\"hero\"", "data-source=\"hero\"",
     "body differs", "verify"),
    ("es/index.html", "one space in the hashed script", "<script>", "<script> ", "hash matches the Caddyfile: False", "guard"),
    ("es/index.html", "a block tag changed in the copy", 'class="abc-vs"', 'class="abc-vs x"', "skeleton differs", "guard"),
    ("pt/privacidade.html", "the translation note removed", '<p class="translation-note">', '<p class="translation-nota">',
     "translation note missing", "verify"),
    ("pt/termos.html", "an English sentence left in", "</p>", " and you agree to all of this</p>", "English stopwords",
     "verify"),
]


def main(tree, briefs):
    ok = True
    for rel, label, old, new, expect, which in MUTATIONS:
        p = os.path.join(tree, rel)
        clean = io.open(p, "rb").read()
        s = clean.decode("utf-8")
        assert old in s, "mutation does not apply: %s (%r not in %s)" % (label, old, rel)
        io.open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new, 1))
        try:
            if which == "verify":
                bad, out = run_verify(tree, briefs, rel.split("/")[0])
                hit = bad > 0 and expect in out
            else:
                code, out = guard(tree)
                hit = code != 0 and expect in out
        finally:
            io.open(p, "wb").write(clean)
        assert io.open(p, "rb").read() == clean
        ok &= hit
        print("  %-42s %s" % (label, "CAUGHT" if hit else "MISSED"))
    bad = sum(run_verify(tree, briefs, lang)[0] for lang in H.LOCAL)
    code, _ = guard(tree)
    print("restored: every page byte-identical; verify %d problems, blocks guard exit %d" % (bad, code))
    ok &= bad == 0 and code == 0
    print("\nSELFTEST %s" % ("PASSED" if ok else "FAILED"))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
