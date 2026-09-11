# -*- coding: utf-8 -*-
"""
Google Analytics 4 on every live page, and the check that it can report.

GA4 property G-M8R4ZTFM6H, added 2026-09-11 ("Install manually" -- there is no
CMS). Google's snippet is NOT pasted as-is: its inline <script> would need a
second CSP hash. Instead every page carries, right after its viewport meta,

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-...">
    <script src="/js/analytics.js">

and js/analytics.js holds the init lines. An external file is already
allowed by script-src 'self', so the Caddyfile keeps its ONE hash.

That file also carries the Consent Mode v2 defaults -- ads storage denied
everywhere, analytics storage denied in the EEA, the UK and Switzerland and
granted elsewhere -- and configures Google Ads AW-11127271562, whose
"Waitlist signup" conversion js/waitlist.js fires. --check compares the file
to INIT_JS below byte for byte, so edit THIS file, never js/analytics.js.

The Caddyfile CSP must name Google's origins, or the browser refuses the
tag, its script or its beacons. All three failures are silent: the tag is
present in the page source either way, and a blocked beacon shows only in the
console. So --check asserts the policy as well as the pages.

Live pages are the same set tools/build_favicon.py links: every tracked .html
outside _*, index-*, editor, graphify-out/ and assets/ (assets/src/frame.html
is an image source file, not a page).

    python tools/analytics.py                  # insert where missing, write js/analytics.js
    python tools/analytics.py --check          # assert everything; writes nothing, exits 1 on a problem
    python tools/analytics.py --check --ref X  # the same, against commit X instead of the working tree

--ref is what the pre-push hook uses, so it checks exactly the commit being
deployed rather than whatever is on disk.
"""

import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GA_ID = "G-M8R4ZTFM6H"
VIEWPORT = '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
TAG_GTAG = '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n' % GA_ID
TAG_INIT = '<script src="/js/analytics.js"></script>\n'
TAGS = TAG_GTAG + TAG_INIT

# The whole of js/analytics.js. It is longer than Google's four init lines
# because it also sets the Consent Mode v2 defaults and configures the Ads
# account; --check compares the file to this byte for byte, so change it
# HERE and re-run, never by editing js/analytics.js.
INIT_JS = """/* ==========================================================================
   FILE: js/analytics.js -- WRITTEN BY tools/analytics.py. Edit that, not this:
   `python tools/analytics.py --check` compares this file byte for byte and
   the pre-push hook fails if they differ.

   Every page loads gtag.js and then this file. The config lines live in a
   file rather than inline because the CSP carries exactly one sha256 hash and
   we are keeping it that way -- see tools/analytics.py for the whole story.

   CONSENT
   Consent Mode v2 defaults are set below, before any measurement command.
   gtag.js processes the dataLayer queue in order, so it sees consent first
   whichever of the two scripts finishes loading first. Advertising storage is
   denied everywhere. Analytics storage is denied in the EEA, the UK and
   Switzerland -- those visits are still counted, cookielessly and modelled --
   and granted everywhere else. There is no cookie banner on the site; if one
   is added it calls gtag('consent', 'update', ...) on accept and nothing here
   changes.

   WHAT IS CONFIGURED
       G-M8R4ZTFM6H     Google Analytics 4, property "amazebase.pro"
       AW-11127271562   Google Ads, for the "Waitlist signup" conversion that
                        js/waitlist.js fires once the server accepts a signup
========================================================================== */
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

gtag('consent', 'default', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'granted',
  wait_for_update: 500
});
gtag('consent', 'default', {
  region: ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU',
           'IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES',
           'SE','IS','LI','NO','GB','CH'],
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'denied',
  wait_for_update: 500
});
gtag('set', 'url_passthrough', true);
gtag('set', 'ads_data_redaction', true);

gtag('js', new Date());
gtag('config', 'G-M8R4ZTFM6H');
gtag('config', 'AW-11127271562');
"""

# Every origin GA4 needs, by directive. Remove one and the tag still sits in
# every page while the browser refuses it.
CSP_NEEDS = {
    "script-src": ["https://www.googletagmanager.com",
                   "https://www.googleadservices.com",
                   "https://googleads.g.doubleclick.net"],
    "connect-src": ["https://*.google-analytics.com", "https://*.analytics.google.com",
                    "https://*.googletagmanager.com",
                    "https://www.googleadservices.com",
                    "https://googleads.g.doubleclick.net", "https://www.google.com"],
    "img-src": ["https://*.google-analytics.com", "https://*.googletagmanager.com",
                "https://www.googleadservices.com",
                "https://googleads.g.doubleclick.net", "https://www.google.com"],
    # Ads writes a hidden iframe to doubleclick to join a click to a
    # conversion. default-src 'self' would otherwise refuse it and the
    # conversion would be attributed to nobody.
    "frame-src": ["https://td.doubleclick.net", "https://googleads.g.doubleclick.net"],
}

# 178 on 2026-09-11. A floor, not an exact count, so adding a page never breaks
# the check -- but a page set that silently shrank (a changed exclusion, a
# failed git call) cannot pass by checking nothing.
MIN_PAGES = 178


class Tree:
    """The working tree, or one commit read through git cat-file."""

    def __init__(self, ref=None):
        self.ref = ref
        if ref:
            ls = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", ref],
                                capture_output=True, text=True, check=True).stdout
        else:
            ls = subprocess.run(["git", "-C", ROOT, "ls-files"],
                                capture_output=True, text=True, check=True).stdout
        self.files = set(ls.split("\n")) - {""}

    def read(self, rel):
        if self.ref:
            r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (self.ref, rel)], capture_output=True)
            return r.stdout.decode("utf-8") if r.returncode == 0 else None
        p = os.path.join(ROOT, rel)
        return io.open(p, encoding="utf-8", newline="").read() if os.path.exists(p) else None

    def pages(self):
        return sorted(p for p in self.files if p.endswith(".html")
                      and not re.match(r"(_|index-|editor|graphify-out/|assets/)", p))


def csp_directives(caddyfile):
    m = re.findall(r'Content-Security-Policy "([^"]*)"', caddyfile)
    assert len(m) == 1, "expected one Content-Security-Policy header in the Caddyfile, found %d" % len(m)
    out = {}
    for part in m[0].split(";"):
        words = part.split()
        if words:
            assert words[0] not in out, "CSP names %s twice" % words[0]
            out[words[0]] = words[1:]
    return out


def page_problems(rel, s):
    head = s[:s.find("</head>")] if "</head>" in s else ""
    p = []
    n_gtag = s.count("googletagmanager.com/gtag/js")
    n_init = s.count("/js/analytics.js")
    if n_gtag != 1:
        p.append("%s: %d gtag.js tags (want exactly 1)" % (rel, n_gtag))
    if n_init != 1:
        p.append("%s: %d /js/analytics.js tags (want exactly 1)" % (rel, n_init))
    if n_gtag == 1 and n_init == 1 and head.count(TAGS) != 1:
        p.append("%s: the two tags are not the expected pair inside <head> (wrong id or attributes?)" % rel)
    return p


def check(tree):
    problems = []
    pages = tree.pages()
    carrying = 0
    for rel in pages:
        pp = page_problems(rel, tree.read(rel))
        problems += pp
        carrying += not pp
    print("live pages %d, carrying exactly one of each tag %d" % (len(pages), carrying))
    if len(pages) < MIN_PAGES:
        problems.append("only %d live pages found, fewer than the floor of %d -- is the page set wrong?"
                        % (len(pages), MIN_PAGES))

    js = tree.read("js/analytics.js")
    print("js/analytics.js %s" % ("matches" if js == INIT_JS else "MISSING" if js is None else "DIFFERS"))
    if js != INIT_JS:
        problems.append("js/analytics.js is %s" % ("missing" if js is None else "not Google's init lines for %s" % GA_ID))

    csp = csp_directives(tree.read("Caddyfile"))
    for d, origins in CSP_NEEDS.items():
        missing = [o for o in origins if o not in csp.get(d, [])]
        print("CSP %-12s %s" % (d, "has all %d GA origins" % len(origins) if not missing else "MISSING %s" % missing))
        if missing:
            problems.append("Caddyfile CSP %s lacks %s" % (d, " ".join(missing)))
    hashes = [w for w in csp.get("script-src", []) if w.startswith("'sha256-")]
    print("CSP script-src hashes %d (want 1)" % len(hashes))
    if len(hashes) != 1:
        problems.append("CSP script-src carries %d sha256 hashes, want 1" % len(hashes))

    if problems:
        print("\n%d PROBLEMS:" % len(problems))
        for x in problems:
            print("  " + x)
        return 1
    print("\nANALYTICS CHECK PASSED")
    return 0


def install(tree):
    changed = []
    for rel in tree.pages():
        s = tree.read(rel)
        assert "\r" not in s, rel
        if TAGS in s:
            continue
        assert "googletagmanager" not in s and "/js/analytics.js" not in s, \
            "%s carries part of a GA tag already; fix it by hand" % rel
        assert s.count(VIEWPORT) == 1, "%s: expected one viewport meta" % rel
        s = s.replace(VIEWPORT, VIEWPORT + TAGS, 1)
        io.open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="").write(s)
        changed.append(rel)
    js = os.path.join(ROOT, "js", "analytics.js")
    if not os.path.exists(js) or io.open(js, encoding="utf-8", newline="").read() != INIT_JS:
        io.open(js, "w", encoding="utf-8", newline="").write(INIT_JS)
        changed.append("js/analytics.js")
    print("tagged %d files" % len(changed))


if __name__ == "__main__":
    a = sys.argv[1:]
    ref = a[a.index("--ref") + 1] if "--ref" in a else None
    t = Tree(ref)
    if "--check" in a:
        sys.exit(check(t))
    assert not ref, "--ref only makes sense with --check"
    install(t)
    sys.exit(check(Tree()))
