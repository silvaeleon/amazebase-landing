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
   Nothing is granted by default. A first-time visitor is measured with every
   storage type DENIED, which under Consent Mode means Google counts the visit
   but writes no cookie and keeps no identifier, until they answer the banner
   in js/consent.js. That file is loaded at the bottom of this one.

   A RETURNING visitor's stored answer is read below and becomes the DEFAULT,
   not an update. This matters: an update arriving after the config commands
   would leave the first page view of every session measured under the wrong
   consent state. Reading it here closes that gap.

   WHAT IS CONFIGURED
       G-M8R4ZTFM6H     Google Analytics 4, property "amazebase.pro"
       AW-11127271562   Google Ads, for the "Waitlist signup" conversion that
                        js/waitlist.js fires once the server accepts a signup
========================================================================== */
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

var abConsent = null;
try {
  var abRaw = window.localStorage.getItem('ab_consent_v1');
  if (abRaw) {
    var abSaved = JSON.parse(abRaw);
    if (abSaved && typeof abSaved.analytics === 'boolean'
        && typeof abSaved.ads === 'boolean' && abSaved.at
        && (Date.now() - abSaved.at) < 31536000000) {
      abConsent = abSaved;
    }
  }
} catch (e) {
  abConsent = null;
}

gtag('consent', 'default', {
  analytics_storage:  abConsent && abConsent.analytics ? 'granted' : 'denied',
  ad_storage:         abConsent && abConsent.ads ? 'granted' : 'denied',
  ad_user_data:       abConsent && abConsent.ads ? 'granted' : 'denied',
  ad_personalization: abConsent && abConsent.ads ? 'granted' : 'denied',
  wait_for_update: 500
});

gtag('set', 'url_passthrough', true);
gtag('set', 'ads_data_redaction', true);

gtag('js', new Date());
gtag('config', 'G-M8R4ZTFM6H');
gtag('config', 'AW-11127271562');

(function () {
  var s = document.createElement('script');
  s.src = '/js/consent.js';
  s.defer = true;
  (document.head || document.documentElement).appendChild(s);
})();
"""

# Every origin GA4 needs, by directive. Remove one and the tag still sits in
# every page while the browser refuses it.
CSP_NEEDS = {
    "script-src": ["https://www.googletagmanager.com",
                   "https://www.googleadservices.com",
                   "https://googleads.g.doubleclick.net",
                   # Microsoft Clarity, loaded by js/consent.js on an analytics yes
                   "https://www.clarity.ms"],
    # pagead2.googlesyndication.com was NOT in the first version of this policy
    # and the Ads tag calls it on every page load (ccm/collect). Seen live on
    # 2026-09-12.
    "connect-src": ["https://*.google-analytics.com", "https://*.analytics.google.com",
                    "https://*.googletagmanager.com",
                    "https://www.googleadservices.com",
                    "https://googleads.g.doubleclick.net", "https://www.google.com",
                    "https://pagead2.googlesyndication.com",
                    "https://*.clarity.ms", "https://c.bing.com"],
    "img-src": ["https://*.google-analytics.com", "https://*.googletagmanager.com",
                "https://www.googleadservices.com",
                "https://googleads.g.doubleclick.net", "https://www.google.com",
                "https://pagead2.googlesyndication.com"],
    # Ads writes a hidden iframe to doubleclick to join a click to a
    # conversion. default-src 'self' would otherwise refuse it and the
    # conversion would be attributed to nobody.
    "frame-src": ["https://td.doubleclick.net", "https://googleads.g.doubleclick.net"],
}

# 180 on 2026-09-12 (178 on 2026-09-11). A floor, not an exact count, so adding
# a page never breaks the check -- but a page set that silently shrank (a
# changed exclusion, a failed git call) cannot pass by checking nothing. Raise
# it as the site grows, or it keeps passing a set that shrank to an older size.
MIN_PAGES = 180


def strip_js_comments(src):
    """`src` with its comments removed and its string literals left alone.

    The abc- guard in check() reads the result of this, not the file itself.
    js/consent.js's header comment names that prefix half a dozen times, on
    purpose, to record why it must never come back; a guard that matched
    those would be permanently red, and a permanently red guard gets deleted.
    Comments are prose ABOUT the code. Only what survives this is code.

    String-aware, because "https://www.clarity.ms/tag/" is not a comment.
    The file carries no regular-expression literals, so a "/" outside a
    string is read here as a division sign. If one ever appears, this wants
    a real tokeniser rather than a wider pattern.
    """
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'`":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith("//", i):
            i = src.find("\n", i)
            if i < 0:
                break
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


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
        """File content with CRLF folded to LF.

        Line endings are a property of the checkout, not of the content. git
        stores LF; a clone on a machine with core.autocrlf=true writes CRLF to
        disk. Without this fold the two halves of this class disagreed: the
        git-ref half read LF from the object store, the working-tree half read
        whatever the checkout happened to have. Every assertion below is
        written against \\n -- the byte-for-byte compare with INIT_JS, the tag
        patterns, the CSP parse -- so on such a clone all 180 pages and
        js/analytics.js failed at once, in the one shape that looks like
        catastrophe and is actually nothing (2026-09-12).

        A check that passes here and fails on a colleague's laptop teaches
        people to ignore it, which is worse than not having it.
        """
        if self.ref:
            r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (self.ref, rel)], capture_output=True)
            if r.returncode != 0:
                return None
            return r.stdout.decode("utf-8").replace("\r\n", "\n")
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            return None
        return io.open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")

    def pages(self):
        """Live pages that must carry the tag.

        google<hex>.html is Google Search Console's ownership file. It is a
        one-line text file Google fetches directly, not a page anyone reads,
        and tagging it would make this check fail forever. Search Console
        stops trusting the site if it is deleted, so it stays in the repo.
        """
        return sorted(p for p in self.files if p.endswith(".html")
                      and not re.match(r"(_|index-|editor|graphify-out/|assets/|google[0-9a-f]{16}\.html$)", p))


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

    cjs = tree.read("js/consent.js")
    print("js/consent.js %s" % ("present" if cjs else "MISSING"))
    if not cjs:
        problems.append("js/consent.js is missing -- js/analytics.js loads it, so the "
                        "cookie banner would 404 on every page")
    else:
        # Three independent faults, deliberately not chained. The first version
        # of this was an elif ladder, in which an abc- regression would have
        # hidden a missing Clarity id in the same run: you would have fixed the
        # first, pushed, and learned about the second one push later.

        # The banner injects its CSS globally, so a class it shares with the
        # site restyles the site. abc- is the homepage comparison block and it
        # already owns abc-card, abc-bar, abc-title, abc-body, abc-btn,
        # abc-link and a dozen more; shipping the banner under that prefix on
        # 2026-09-12 set the two homepage comparison cards to opacity 0 in
        # production, and restyled abc-link's seven uses besides.
        #
        # Matched against the code with comments stripped, not against the two
        # spellings the file happened to use ('"abc-' and "'.abc-"). Those are
        # what a rewrite would have been LIKELY to contain, which is a weaker
        # thing to assert than what it must not contain at all: 'abc-btn' in
        # single quotes, in a class list, in a template literal or inside a
        # querySelector all went through. The banner's classes are abconsent-.
        if "abc-" in strip_js_comments(cjs):
            problems.append("js/consent.js uses the abc- prefix somewhere in its code. "
                            "That prefix belongs to the site's homepage comparison "
                            "block -- the banner's injected styles would silently "
                            "restyle it. Use abconsent-.")
        if "yh4nta35du" not in cjs:
            problems.append("js/consent.js no longer carries the Microsoft Clarity project "
                            "id yh4nta35du -- Clarity would silently stop recording")
        if "ab_consent_v1" not in cjs:
            problems.append("js/consent.js does not use the ab_consent_v1 storage key that "
                            "js/analytics.js reads -- the two would disagree about consent")

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
