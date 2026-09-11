# -*- coding: utf-8 -*-
"""
Restore the chart series colours the drafts defined and publish.py dropped.

publish.py strips the drafts' own :root blocks (they carry a light palette the
site must not inherit). Three drafts also defined their chart series colours
there, so those pages ship referencing variables that either do not exist
(--s1-fill, --s2-fill, --accent-fill) or resolve to the SITE's spacing scale
(--s1: 8px, --s2: 16px). A stroke of "8px" is invalid, so the data lines and
legend swatches render as nothing.

The values below are the drafts' own dark-mode values, copied verbatim from
_drafts/*.html. Nothing here is invented. The series names are changed to
--ser-a / --ser-b so they can never collide with the spacing scale again.
"""
import io, os, re, sys

SRC = "/mnt/user-data/uploads/amazebase-landing"
OUT = "/home/claude/esout"

# slug -> (definitions to add, {old var -> new var} to rewrite inside .art-diagram)
JOBS = {
    "first-product-succeeds-cash": (
        "  --ser-a:#9F7BF2;  --ser-b:#12A594;\n"
        "  --ser-a-fill:rgba(159,123,242,.13);  --ser-b-fill:rgba(18,165,148,.13);",
        {"--s1-fill": "--ser-a-fill", "--s2-fill": "--ser-b-fill",
         "--s1": "--ser-a", "--s2": "--ser-b"}),
    "supplier-payment-schedules-margins": (
        "  --ser-a:#9F7BF2;  --ser-b:#12A594;\n"
        "  --ser-a-fill:rgba(159,123,242,.15);  --ser-b-fill:rgba(18,165,148,.15);",
        {"--s1-fill": "--ser-a-fill", "--s2-fill": "--ser-b-fill",
         "--s1": "--ser-a", "--s2": "--ser-b"}),
    "fba-reorder-date-velocity": (
        "  --accent-fill:rgba(173,143,245,.16);",
        {}),
}

BLOCK = ("\n/* Chart series colours. These live on .art-diagram rather than :root so\n"
         "   they cannot shadow the site's --s1..--s8 spacing scale. Values are the\n"
         "   draft's own dark-mode series colours. */\n"
         ".art-diagram{\n%s\n}\n")


def load(rel):
    p = os.path.join(OUT, rel)
    return io.open(p if os.path.exists(p) else os.path.join(SRC, rel), encoding="utf-8").read()


def save(rel, s):
    p = os.path.join(OUT, rel)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def patch(s, defs, rename, tag):
    assert ".art-diagram{\n  --ser" not in s and "--accent-fill:" not in s, "already patched " + tag
    # rewrite only inside the figure, never in the page's spacing CSS
    i = s.index('<figure class="art-diagram">')
    j = s.index("</figure>", i) + len("</figure>")
    fig = s[i:j]
    total = 0
    for old, new in rename.items():                 # longest keys first (dict order above)
        n = fig.count("var(%s)" % old)
        total += n
        fig = fig.replace("var(%s)" % old, "var(%s)" % new)
    assert not rename or total >= 6, "%s: only %d series vars rewritten" % (tag, total)
    s = s[:i] + fig + s[j:]

    k = s.index("</style>")
    s = s[:k] + BLOCK % defs + s[k:]

    # postflight: nothing in the figure references an undefined or spacing var
    i = s.index('<figure class="art-diagram">')
    j = s.index("</figure>", i)
    used = set(re.findall(r"var\((--[a-zA-Z0-9_-]+)", s[i:j]))
    bad = [v for v in used if re.match(r"^--s\d+$", v)]
    assert not bad, "%s: spacing var still used as a colour: %s" % (tag, bad)
    css = s[s.index("<style"):s.index("</style>")]
    site = set(re.findall(r"(--[a-zA-Z0-9_-]+)\s*:",
                          io.open(SRC + "/css/variables.css", encoding="utf-8").read()))
    local = set(re.findall(r"(--[a-zA-Z0-9_-]+)\s*:", css))
    undef = sorted(v for v in used if v not in local and v not in site)
    assert not undef, "%s: still undefined %s" % (tag, undef)
    return s


for slug, (defs, rename) in JOBS.items():
    rel = "articles/%s.html" % slug
    save(rel, patch(load(rel), defs, rename, slug))
    print("chart fixed", rel)

# the Spanish mirror carries the same figure markup
rel = "es/articulos/y-si-tu-primer-producto-funciona.html"
defs, rename = JOBS["first-product-succeeds-cash"]
save(rel, patch(load(rel), defs, rename, "es-mirror"))
print("chart fixed", rel)
