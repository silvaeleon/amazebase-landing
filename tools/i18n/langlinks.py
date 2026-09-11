# -*- coding: utf-8 -*-
"""
Regenerate every page's language cross-links from one manifest.

THE PROBLEM THIS EXISTS TO PREVENT
----------------------------------
Each translated page carries two lists that name every other language: the
<link rel="alternate" hreflang> block in the head, and the switcher menu in the
nav. Add a language by hand and you must edit every page of every language that
already shipped. Today that is 112 pages. Add Portuguese by hand and it is 168
before French, 224 before Italian, 280 before German -- 784 page edits, each one
an opportunity for one page to disagree with the others about what exists.

Search engines read a disagreement as a broken cluster and may ignore the
alternates entirely, and a stale switcher row is a 404 in the nav. Both failures
are silent: the page renders, nothing errors, and you find out from analytics.

So the lists are not authored. They are generated, here, from languages.json
plus one slug map per language, and regenerated for EVERY page in EVERY language
on every run. Adding a language is a manifest entry, a slug map, and one run.

WHAT IT REWRITES, AND NOTHING ELSE
----------------------------------
  1. the run of <link rel="alternate" ...> lines in the head
  2. the chip inside the .lang-btn (the current language's code)
  3. the run of <a> lines inside <div class="nav-drop lang-drop">

It does not touch the canonical, <html lang>, og:locale, or any content. Those
belong to the page builder. This script has one job.

CALIBRATION
-----------
Run with --check against the current tree first. With the manifest describing
the languages that already ship, the output must be BYTE-IDENTICAL to what is
on disk. If it cannot reproduce what already works, it must not be trusted to
generate what comes next. See --check in main().
"""

import io, os, re, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------- the manifest

def load(cfg_dir=None):
    d = cfg_dir or HERE
    cfg = json.load(io.open(os.path.join(d, "languages.json"), encoding="utf-8"))
    slugs = {}
    for lang in cfg["languages"]:
        c = lang["code"]
        p = os.path.join(d, "slugs", c + ".json")
        if os.path.exists(p):
            slugs[c] = json.load(io.open(p, encoding="utf-8"))
        else:
            # English is the source language: its slugs map to themselves.
            slugs[c] = None
    return cfg, slugs


def groups(cfg, slugs, en_slugs):
    """Every set of pages that are the same page in different languages.

    Returns {path -> {code: path}}, keyed by EVERY member path, so a page can
    look itself up by its own location without knowing which language it is."""
    out = {}

    def add(members):
        for p in members.values():
            out[p] = members

    for key in cfg["languages"][0]["top"]:
        members = {}
        for lang in cfg["languages"]:
            if key in lang.get("top", {}):
                members[lang["code"]] = lang["top"][key]
        add(members)

    for en in en_slugs:
        members = {}
        for lang in cfg["languages"]:
            c = lang["code"]
            m = slugs.get(c)
            local = en if m is None else m.get(en)
            if local:
                members[c] = "%s/%s.html" % (lang["articles"], local)
        add(members)

    return out


# ----------------------------------------------------------------- the blocks

def alt_block(cfg, members):
    """The <link rel=alternate> run, in manifest order, x-default last."""
    site = cfg["site"].rstrip("/")
    lines = []
    for lang in cfg["languages"]:
        c = lang["code"]
        if c in members:
            lines.append('<link rel="alternate" hreflang="%s" href="%s/%s">'
                         % (c, site, members[c]))
    xd = cfg["x_default"]
    if xd in members:
        lines.append('<link rel="alternate" hreflang="x-default" href="%s/%s">'
                     % (site, members[xd]))
    return "\n".join(lines)


def menu_block(cfg, members, current, indent="        "):
    """The switcher rows. Root-absolute hrefs -- a relative one under /es/
    resolves inside /es/ and 404s, which is the trap that broke the hero."""
    lines = []
    for lang in cfg["languages"]:
        c = lang["code"]
        if c not in members:
            continue
        cur = ' aria-current="true"' if c == current else ""
        lines.append('%s<a href="/%s" hreflang="%s" lang="%s"%s>'
                     '<span class="lc">%s</span>%s</a>'
                     % (indent, members[c], c, c, cur, lang["chip"], lang["label"]))
    return "\n".join(lines)


# ------------------------------------------------------------------- rewriting

ALT_RUN = re.compile(r'(?:^<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n)+',
                     re.M)
MENU_RUN = re.compile(r'(<div class="nav-drop lang-drop">\n)'
                      r'((?:[ \t]*<a href="[^"]*" hreflang="[^"]*"[^>]*>.*?</a>\n)+)'
                      r'([ \t]*</div>)')
CHIP = re.compile(r'(<button class="lang-btn"[^>]*>\n[ \t]*)([A-Za-z-]+)( <svg class="chev")')


def rewrite(s, cfg, members, current):
    """Returns the new text. Raises if an anchor is missing or not unique."""
    n_alt = len(ALT_RUN.findall(s))
    assert n_alt == 1, "expected exactly 1 alternates run, found %d" % n_alt
    s = ALT_RUN.sub(lambda m: alt_block(cfg, members) + "\n", s, count=1)

    mm = MENU_RUN.search(s)
    assert mm, "no lang-drop menu found"
    assert len(MENU_RUN.findall(s)) == 1, "more than one lang-drop menu"
    indent = re.match(r"[ \t]*", mm.group(2)).group(0) or "        "
    s = MENU_RUN.sub(lambda m: m.group(1) + menu_block(cfg, members, current, indent)
                     + "\n" + m.group(3), s, count=1)

    chip = dict((l["code"], l["chip"]) for l in cfg["languages"])[current]
    n_chip = len(CHIP.findall(s))
    assert n_chip == 1, "expected exactly 1 lang-btn chip, found %d" % n_chip
    s = CHIP.sub(lambda m: m.group(1) + chip + m.group(3), s, count=1)
    return s


# ----------------------------------------------------------------------- main

def page_lang(cfg, path, members):
    for c, p in members.items():
        if p == path:
            return c
    return None


def run(tree, cfg_dir=None, check=False, verbose=True):
    cfg, slugs = load(cfg_dir)
    en_dir = cfg["languages"][0]["articles"]
    en_slugs = sorted(os.path.basename(p)[:-5]
                      for p in glob.glob(os.path.join(tree, en_dir, "*.html")))
    g = groups(cfg, slugs, en_slugs)

    skip = set(cfg.get("no_switcher", []))
    changed, same, missing, problems = [], [], [], []

    # A slug map with holes fails SILENTLY: the pages it forgot simply omit that
    # language from their alternates and switcher, render fine, error nowhere,
    # and are found months later in Search Console. So check coverage up front.
    top_keys = set(cfg["languages"][0]["top"])
    for lang in cfg["languages"]:
        c = lang["code"]
        m = slugs.get(c)
        if m is not None:
            gaps = [s for s in en_slugs if s not in m]
            if gaps:
                problems.append(
                    "slugs/%s.json is missing %d of %d article slugs -- those "
                    "pages would silently drop %s from their alternates: %s"
                    % (c, len(gaps), len(en_slugs), c.upper(),
                       ", ".join(gaps[:6]) + (" ..." if len(gaps) > 6 else "")))
            extra = [s for s in m if s not in en_slugs]
            if extra:
                problems.append(
                    "slugs/%s.json names %d article slugs that do not exist in "
                    "English: %s" % (c, len(extra), ", ".join(sorted(extra)[:6])))
        gaps = sorted(top_keys - set(lang.get("top", {})))
        if gaps and c != cfg["languages"][0]["code"]:
            print("  note: %s has no %s page yet" % (c, "/".join(gaps)))

    # every page that carries a switcher must be in a group, and vice versa
    on_disk = set()
    for p in glob.glob(os.path.join(tree, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, tree).replace(os.sep, "/")
        s = io.open(p, encoding="utf-8").read()
        if 'class="nav-drop lang-drop"' not in s:
            if rel in g and rel not in skip:
                problems.append("%s is in a translation group but has no switcher" % rel)
            continue
        on_disk.add(rel)
        if rel not in g:
            problems.append("%s has a switcher but is in no translation group "
                            "(unknown page, or a slug map is out of date)" % rel)
            continue
        members = g[rel]
        cur = page_lang(cfg, rel, members)
        try:
            new = rewrite(s, cfg, members, cur)
        except AssertionError as e:
            problems.append("%s: %s" % (rel, e))
            continue
        if new == s:
            same.append(rel)
        else:
            changed.append(rel)
            if not check:
                io.open(p, "w", encoding="utf-8", newline="").write(new)

    for path in sorted(g):
        if path not in on_disk and path not in skip:
            missing.append(path)

    if verbose:
        print("%d pages carry a switcher" % len(on_disk))
        print("  unchanged: %d" % len(same))
        print("  rewritten: %d" % len(changed))
        for r in changed[:12]:
            print("      %s" % r)
        if len(changed) > 12:
            print("      ... and %d more" % (len(changed) - 12))
        if missing:
            print("  %d group members do not exist on disk yet "
                  "(expected while a language is being built):" % len(missing))
            for r in missing[:8]:
                print("      %s" % r)

    if problems:
        print("\n%d PROBLEMS:" % len(problems))
        for p_ in problems:
            print("  " + p_)
        raise SystemExit(1)

    return changed, same, missing


if __name__ == "__main__":
    argv = sys.argv[1:]
    check = "--check" in argv
    cfg_dir = None
    if "--cfg" in argv:
        cfg_dir = argv[argv.index("--cfg") + 1]
        argv = argv[:argv.index("--cfg")] + argv[argv.index("--cfg") + 2:]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        raise SystemExit("usage: langlinks.py <site-root> [--cfg DIR] [--check]")
    tree = args[0]
    changed, same, missing = run(tree, cfg_dir=cfg_dir, check=check)

    if check:
        if changed:
            print("\nCHECK FAILED: %d pages would change." % len(changed))
            print("With the manifest describing only languages that already ship,")
            print("this must be a no-op. A difference means the generator does not")
            print("reproduce the markup that is live, so it cannot be trusted to")
            print("generate the next language's.")
            raise SystemExit(1)
        print("\nCHECK PASSED: byte-identical on all %d pages." % len(same))
