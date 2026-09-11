# -*- coding: utf-8 -*-
"""
The homepage's .abp and .abc blocks are pasted, self-contained and OFF-LIMITS
(Leon's standing rule). This proves nothing touched them.

  1. index.html's two blocks are byte-identical to a reference commit
     (default HEAD, so uncommitted work is what gets checked; on 2026-09-11
     they were also byte-identical to c000043, the commit that pasted .abc).
  2. The one inline <script> on every homepage -- English and each
     translation -- hashes to the sha256 the Caddyfile's CSP allows. The
     translated homepages carry copies of the blocks with the TEXT translated
     (Leon, 2026-09-11); their script must stay byte-identical, or the browser
     refuses to run it and the pipeline section goes static without an error.
  3. A translated homepage's block copy has the same skeleton as the English
     block: same tags, attributes and data: URIs, in the same order. Only the
     text between tags (and aria-label/alt/title) may differ.

    python tools/i18n/blocks_guard.py <site-root> [--ref <commit>]
"""

import base64, hashlib, io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import langlinks

TEXT_ATTRS = ("aria-label", "alt", "title")


def block(s, cls):
    m = re.search(r'<section[^>]*class="%s"' % cls, s)
    assert m, "no .%s block" % cls
    i, depth = m.start(), 0
    for t in re.finditer(r'<(/?)section\b[^>]*>', s[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return s[i:i + t.end()]
    raise AssertionError("unclosed .%s block" % cls)


def skeleton(b):
    """The block with its text taken out: tags and attributes only, and the
    text attributes blanked. Two copies that differ only in language match."""
    b = re.sub(r'<script>.*?</script>', '<script></script>', b, flags=re.S)
    b = re.sub(r'<style>.*?</style>', lambda m: m.group(0), b, flags=re.S)
    for a in TEXT_ATTRS:
        b = re.sub(r'(\s%s=")[^"]*(")' % a, r'\1\2', b)
    out, pos = [], 0
    for m in re.finditer(r'<[^>]+>', b):
        out.append(m.group(0))
    # <style> bodies are CSS, not text: keep them in the comparison
    styles = re.findall(r'<style>.*?</style>', b, flags=re.S)
    return "\n".join(out), styles


def csp_hash(tree):
    c = io.open(os.path.join(tree, "Caddyfile"), encoding="utf-8").read()
    h = re.findall(r"'sha256-([A-Za-z0-9+/=]+)'", c)
    assert len(h) == 1, "expected one script hash in the Caddyfile, found %d" % len(h)
    return h[0]


def script_hashes(s):
    return [base64.b64encode(hashlib.sha256(x.encode("utf-8")).digest()).decode()
            for x in re.findall(r"<script>(.*?)</script>", s, re.S)]


def main(tree, ref=None):
    problems = []
    read = lambda p: io.open(os.path.join(tree, p), encoding="utf-8", newline="").read()
    en = read("index.html")
    ref = ref or "HEAD"
    old = subprocess.run(["git", "-C", tree, "show", "%s:index.html" % ref],
                         capture_output=True).stdout.decode("utf-8")
    assert old, "git could not read index.html at %s" % ref
    for cls in ("abp", "abc"):
        same = block(en, cls) == block(old, cls)
        print("index.html .%s   byte-identical to %s: %s (%d bytes)" % (cls, ref, same, len(block(en, cls))))
        if not same:
            problems.append("index.html .%s differs from %s -- the block is off-limits" % (cls, ref))

    allowed = csp_hash(tree)
    cfg, _ = langlinks.load()
    homes = [l["top"]["home"] for l in cfg["languages"] if "home" in l.get("top", {})] or ["index.html"]
    for rel in homes:
        if not os.path.exists(os.path.join(tree, rel)):
            print("%-16s not built yet" % rel)
            continue
        s = read(rel)
        hs = script_hashes(s)
        ok = hs == [allowed]
        print("%-16s inline scripts %d, hash matches the Caddyfile: %s" % (rel, len(hs), ok))
        if not ok:
            problems.append("%s: inline script hashes %s, the CSP allows only %s" % (rel, hs, allowed))
        if rel != "index.html":
            for cls in ("abp", "abc"):
                a, b = skeleton(block(en, cls)), skeleton(block(s, cls))
                if a != b:
                    ta, tb = a[0].split("\n"), b[0].split("\n")
                    diff = next((i for i in range(min(len(ta), len(tb))) if ta[i] != tb[i]), min(len(ta), len(tb)))
                    problems.append("%s .%s: skeleton differs from English at tag %d: %.90r vs %.90r"
                                    % (rel, cls, diff, ta[diff] if diff < len(ta) else None,
                                       tb[diff] if diff < len(tb) else None))
                    if a[1] != b[1]:
                        problems.append("%s .%s: <style> differs from English" % (rel, cls))
                else:
                    print("%-16s .%s skeleton identical to English (%d tags)" % (rel, cls, len(a[0].split("\n"))))
    if problems:
        print("\n%d PROBLEMS:" % len(problems))
        for p in problems:
            print("  " + p)
        raise SystemExit(1)
    print("\nBLOCKS GUARD PASSED")


if __name__ == "__main__":
    a = sys.argv[1:]
    ref = None
    if "--ref" in a:
        ref = a[a.index("--ref") + 1]
        del a[a.index("--ref"):a.index("--ref") + 2]
    main(a[0], ref)
