# -*- coding: utf-8 -*-
"""
No committed text file carries a CR byte.

Line endings are a property of the checkout, not of the content. git stores
what you commit; what lands on disk is then converted by core.autocrlf, which
is true by default on Windows. So the only place the invariant can be stated
without lying is the object store, and that is what this reads: the blobs in a
commit, through git cat-file, never the working tree. A clone whose files are
all CRLF on disk passes this, correctly.

WHY IT EXISTS
Until 2026-09-12 this was enforced by accident. tools/analytics.py compared
js/analytics.js byte for byte against a \\n literal and matched its tag
patterns against \\n, so a CRLF file failed. That was real coverage, and it was
also the thing that made a fresh clone on a core.autocrlf=true machine report
181 problems -- every page plus analytics.js -- which looks like catastrophe
and means nothing. Folding CRLF to LF in that reader fixed the false alarm and
removed the coverage with it. This is the coverage put back in the one place
it cannot false-alarm, because a checkout conversion cannot reach a blob.

It matters because CRLF in committed content is not cosmetic here. It breaks
the CSP sha256 hash (the browser hashes bytes, and the Caddyfile carries
exactly one hash), it breaks js/analytics.js's byte-for-byte identity, and it
is invisible in a diff and in the browser.

Twice on 2026-09-12 a routine git operation on a Windows clone rewrote LF
files to CRLF in the working tree. That is fine and expected. What is not fine
is committing them, and that is what this refuses.

    python tools/eol.py [--ref <sha>]      # default: HEAD

BINARY
A blob holding a NUL byte is binary and is skipped -- git's own heuristic. The
count of text blobs searched is printed, so a scope that silently shrinks is
visible rather than passing by checking nothing.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 335 text blobs of 554 at 7092ffb (the rest are images and fonts). A floor,
# not an exact count: adding files never breaks this, but a scope that
# collapsed (a changed git call, a tree read as empty, every blob suddenly
# looking binary) cannot pass by searching nothing.
MIN_TEXT_BLOBS = 330


def tree(ref):
    """[(sha, path)] for every blob in `ref`. -z so paths are raw, not quoted."""
    out = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "-z", ref],
                         capture_output=True, check=True).stdout
    entries = []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, kind, sha = meta.split(b" ")
        if kind == b"blob":
            entries.append((sha.decode(), path.decode("utf-8", "replace")))
    return entries


def contents(shas):
    """Every blob's bytes, in one git call rather than one per file."""
    p = subprocess.Popen(["git", "-C", ROOT, "cat-file", "--batch"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = p.communicate(("\n".join(shas) + "\n").encode())[0]
    blobs, i = [], 0
    while i < len(out):
        nl = out.index(b"\n", i)
        size = int(out[i:nl].split(b" ")[2])
        blobs.append(out[nl + 1:nl + 1 + size])
        i = nl + 1 + size + 1          # the trailing newline cat-file adds
    return blobs


def check(ref="HEAD"):
    entries = tree(ref)
    bodies = contents([sha for sha, _ in entries])
    assert len(bodies) == len(entries), "cat-file returned %d blobs for %d entries" % (
        len(bodies), len(entries))

    text = [(path, body) for (_, path), body in zip(entries, bodies) if b"\0" not in body]
    bad = sorted(path for path, body in text if b"\r" in body)
    print("%s: %d blobs, %d text, %d with a CR byte" % (ref, len(entries), len(text), len(bad)))

    problems = []
    if len(text) < MIN_TEXT_BLOBS:
        problems.append("only %d text blobs searched, fewer than the floor of %d -- "
                        "is the tree read wrong?" % (len(text), MIN_TEXT_BLOBS))
    for path in bad:
        problems.append("%s is committed with CR bytes; commit it with LF endings" % path)
    return problems


if __name__ == "__main__":
    ref = "HEAD"
    if "--ref" in sys.argv:
        ref = sys.argv[sys.argv.index("--ref") + 1]
    problems = check(ref)
    if problems:
        print("\nEOL CHECK FAILED")
        for p in problems:
            print("  %s" % p)
        print("\n  A CRLF file breaks the CSP sha256 hash and js/analytics.js's identity,")
        print("  and shows up in neither the diff nor the browser. To fix one file:")
        print("      python -c \"import io;p='PATH';s=io.open(p,'rb').read().replace(b'\\\\r\\\\n',b'\\\\n');io.open(p,'wb').write(s)\"")
        raise SystemExit(1)
    print("\nEOL CHECK PASSED")
