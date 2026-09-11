# -*- coding: utf-8 -*-
"""
Extract one JSON brief per English article -- everything a translator needs.

    python3 tools/i18n/reextract.py <site-root> [-o OUTDIR] [--compare DIR]

Briefs are DERIVED, never committed. That is deliberate. A committed brief goes
stale the moment an article is edited, and it goes stale silently: the file
still parses, the translator still gets a title and a <main>, and the language
built from it disagrees with the English page in ways nobody notices.

That is not hypothetical. The briefs used for Spanish were extracted before the
alt-text rewrite in e6c841f, so they still carried the old 20-25 word picture
descriptions. Handed to a Portuguese translator unchanged, they would have put
the discarded alts back on the site one language at a time, with English and
Portuguese describing the same image differently.

So: regenerate before every language. It takes about two seconds.

--compare DIR diffs against a previous extraction and names every field that
moved, which is how the staleness above was found.
"""

import io, os, re, sys, json, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline

ALT_FIELDS = {"hero_alt", "og_img_alt", "hero"}   # hero embeds the alt string

REQUIRED = ("title", "desc", "og_title", "og_desc", "main",
            "article_head", "back_link")


def extract(tree, out, compare=None, verbose=True):
    pipeline.SRC = tree
    if not os.path.isdir(out):
        os.makedirs(out)

    slugs = sorted(os.path.basename(p)[:-5]
                   for p in glob.glob(os.path.join(tree, "articles", "*.html")))
    if verbose:
        print("%d English articles in %s" % (len(slugs), tree))

    moved, unexpected, no_prior = {}, [], []

    for sl in slugs:
        b = pipeline.brief(sl)
        io.open(os.path.join(out, sl + ".json"), "w",
                encoding="utf-8", newline="\n").write(
            json.dumps(b, ensure_ascii=False, indent=1))

        if not compare:
            continue
        old_p = os.path.join(compare, sl + ".json")
        if not os.path.exists(old_p):
            no_prior.append(sl)
            continue
        o = json.load(io.open(old_p, encoding="utf-8"))
        for k in sorted(set(b) | set(o)):
            if b.get(k) != o.get(k):
                moved[k] = moved.get(k, 0) + 1
                if k not in ALT_FIELDS:
                    unexpected.append(
                        "%s: field %r changed since the last extraction\n"
                        "    WAS %.110r\n    NOW %.110r" % (sl, k, o.get(k), b.get(k)))

    if compare and verbose:
        print("\nfields that moved since %s:" % compare)
        for k in sorted(moved, key=lambda x: -moved[x]):
            print("  %-14s %3d articles" % (k, moved[k]))
        if no_prior:
            print("  (%d articles had no previous brief: %s)"
                  % (len(no_prior), ", ".join(no_prior)))

    # ---- postflight: a brief that is missing a field fails at translate time,
    # which is the expensive place to find out.
    bad = list(unexpected)
    heroes = 0
    for p in sorted(glob.glob(os.path.join(out, "*.json"))):
        d = json.load(io.open(p, encoding="utf-8"))
        sl = d["slug"]
        for k in REQUIRED:
            if not d.get(k):
                bad.append("%s: brief is missing %r" % (sl, k))
        if d.get("hero"):
            heroes += 1
            am = re.search(r'alt="([^"]*)"', d["hero"])
            alt = am.group(1) if am else ""
            w = len(alt.split())
            # The alt policy from e6c841f: decorative hero art says what the
            # image MEANS in 8-14 words. Anything longer has drifted back to
            # describing the picture; see tools/i18n/briefs/_ALTS.md.
            if not (8 <= w <= 15):
                bad.append("%s: hero alt is %d words, expected 8-15: %.60s"
                           % (sl, w, alt))
            if d.get("og_img_alt") and d["og_img_alt"] != alt:
                bad.append("%s: og:image:alt disagrees with the hero alt\n"
                           "    hero %r\n    og   %r" % (sl, alt, d["og_img_alt"]))

    if bad:
        print("\n%d PROBLEMS:" % len(bad))
        for b_ in bad:
            print("  " + b_)
        raise SystemExit(1)

    if verbose:
        print("\npostflight clean: %d briefs written to %s "
              "(%d with a hero image, %d with an empty slot)"
              % (len(slugs), out, heroes, len(slugs) - heroes))
    return slugs


if __name__ == "__main__":
    argv = sys.argv[1:]

    def opt(flag, default=None):
        if flag in argv:
            i = argv.index(flag)
            v = argv[i + 1]
            del argv[i:i + 2]
            return v
        return default

    out = opt("-o", "briefs")
    compare = opt("--compare")
    args = [a for a in argv if not a.startswith("-")]
    if not args:
        raise SystemExit(__doc__.strip().split("\n")[2].strip())
    extract(args[0], out, compare)
