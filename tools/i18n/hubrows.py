# -*- coding: utf-8 -*-
"""
Make a translated Knowledge Hub row, and check every translated row that exists.

THE BUG THIS EXISTS TO PREVENT
------------------------------
The Spanish rows in data/resources.json were made by copying a NAMED LIST of
fields from each English entry. `category` was on the list. `categories` -- the
multi-tile field hub.js reads FIRST -- was not. So 12 Spanish rows lost it: 7
whose English source has only `categories` sat under no tile at all, and 5 kept
the first tile and silently lost the second. Nothing errored. The hub listed
them; it just could not find them from a tile.

A list of names is only as complete as the author's memory on the day it was
written, and it fails silently on the one field nobody thought of. So nothing
here enumerates what to COPY. A translated row starts as a copy of the WHOLE
English entry, and only the fields in LOCAL are replaced. A field added to the
English entries next month travels into every language without anyone editing
this file.

LOCAL is the opposite list: the fields that are allowed to differ. It was
MEASURED, not guessed -- on 2026-09-10 the 51 Spanish rows differed from their
English source in exactly these six keys, plus `translationOf`, and in nothing
else. Adding to it is a decision; it makes a field stop being checked.

THE CHECK
---------
For every row with a `translationOf`, its key set must equal its English
source's key set (plus `translationOf`), and every key outside LOCAL must hold
an IDENTICAL value. It compares whole key sets, so it catches the dropped field
nobody has named yet, and it can fail for the reason it exists: run against the
tree before the fix, it reports those 12 rows.

    python tools/i18n/hubrows.py . --check
"""

import copy, io, json, os, re, sys

# The only fields a translation may change. Measured 2026-09-10 across all 51
# Spanish rows -- see the module docstring before adding anything here.
LOCAL = ("id", "title", "summary", "url", "topics", "language")
LINK = "translationOf"
SOURCE_LANG = "en"


def translated_row(en, **local):
    """A translated row: the whole English entry, with only LOCAL replaced.

    Every LOCAL field must be given, and nothing outside LOCAL may be -- a
    translator's row cannot quietly carry its own taxonomy."""
    stray = sorted(set(local) - set(LOCAL))
    assert not stray, "not a language-specific field, refusing to override: %s" % stray
    missing = [k for k in LOCAL if k not in local]
    assert not missing, "a translated row needs every LOCAL field; missing: %s" % missing
    assert en.get("language") == SOURCE_LANG, "source is not an English entry: %s" % en.get("id")
    row = copy.deepcopy(en)
    for k in LOCAL:
        row[k] = copy.deepcopy(local[k])
    row.pop(LINK, None)
    row[LINK] = en["id"]
    return row


def english_row(data, id, title, summary, categories, level, topics, minutes, published,
                format="article", author="AmazeBase", **extra):
    """A new ENGLISH row. `categories` must be a LIST of hub category ids, even
    for one value: it is the field hub.js reads FIRST, and the 12-row Spanish
    defect came from it being dropped. `category` (the older single field)
    is set to its first entry, as the rows that carry both have it."""
    assert isinstance(categories, list) and categories, "categories must be a non-empty LIST: %r" % (categories,)
    known = set(c["id"] for c in data["categories"])
    assert set(categories) <= known, "unknown category ids %s (known: %s)" % (sorted(set(categories) - known), sorted(known))
    assert level in set(l["id"] for l in data["levels"]), "unknown level %r" % level
    assert format in set(f["id"] for f in data["formats"]), "unknown format %r" % format
    row = {"id": id, "title": title, "summary": summary, "category": categories[0],
           "categories": list(categories), "format": format, "level": level, "language": SOURCE_LANG,
           "author": author, "published": published, "minutes": int(minutes),
           "url": "articles/%s.html" % id, "topics": list(topics)}
    row.update(extra)
    return row


def check(data):
    """Returns (checked, problems). Empty problems means every translated row
    carries exactly its English source's taxonomy."""
    rows = data["resources"]
    source = dict((r["id"], r) for r in rows if r.get("language") == SOURCE_LANG)
    problems, checked = [], 0

    # `categories`, where a row has it, is the field hub.js reads first: it must be a list
    for r in rows:
        if "categories" in r and not (isinstance(r["categories"], list) and r["categories"]):
            problems.append("%s: categories is %r, must be a non-empty list" % (r.get("id"), r["categories"]))

    for r in rows:
        if r.get("language") == SOURCE_LANG:
            continue
        rid = r.get("id")
        if LINK not in r:
            # A translation with no link is never compared, which is exactly
            # where a dropped field would hide. Refuse it rather than skip it.
            problems.append("%s: language %s but no %s, so nothing checks it"
                            % (rid, r.get("language"), LINK))
            continue
        en = source.get(r[LINK])
        if en is None:
            problems.append("%s: %s points at %r, which is not an English entry"
                            % (rid, LINK, r[LINK]))
            continue
        checked += 1
        want, have = set(en), set(r) - {LINK}
        for k in sorted(want - have):
            problems.append("%s: missing %r (English has %s)"
                            % (rid, k, json.dumps(en[k], ensure_ascii=False)))
        for k in sorted(have - want):
            problems.append("%s: has %r, which its English source does not" % (rid, k))
        for k in sorted(want & have):
            if k not in LOCAL and en[k] != r[k]:
                problems.append("%s: %r is %s, English says %s"
                                % (rid, k, json.dumps(r[k], ensure_ascii=False),
                                   json.dumps(en[k], ensure_ascii=False)))
    return checked, problems


def hubs(root, data):
    """Every language's hub page lists exactly that language's rows.

    THE BUG THIS EXISTS TO PREVENT
    ------------------------------
    A hub carries the corpus TWICE outside hub.js: the no-JS card list between
    the SEO:HUB-FALLBACK markers, and the CollectionPage `hasPart` in the
    JSON-LD. Both are generated -- but seo.py regenerates only the ENGLISH hub,
    and each translated hub has its own generator that has to be run by hand.
    So three batches running shipped with the Spanish and Portuguese hubs a
    release behind the data: 51 against 52, then 52 against 61, then 61 against
    62. A reader with JavaScript saw the new articles because hub.js builds the
    list from resources.json; a crawler, and a reader without JavaScript, saw
    the stale one.

    It kept coming back because nothing caught it. verify_top_pt.py checks the
    Portuguese hub and no equivalent exists for Spanish, so the Spanish hub was
    unchecked in every batch. This compares both lists, in every language, to
    the rows in data/resources.json -- the file all three are generated from.
    """
    cfg = json.load(io.open(os.path.join(root, "tools", "i18n", "languages.json"), encoding="utf-8"))
    site = cfg["site"].rstrip("/") + "/"
    problems, checked = [], 0
    for lang in cfg["languages"]:
        code, rel = lang["code"], lang["top"]["resources"]
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            problems.append("%s: %s does not exist" % (code, rel))
            continue
        want = sorted(r["url"].lstrip("/") for r in data["resources"] if r.get("language") == code)
        s = io.open(p, encoding="utf-8").read()
        cards = sorted(h.lstrip("/") for h in re.findall(r'<a class="hub-row" href="([^"]+)"', s))
        # Each card's picture, too. The same staleness hid here on 2026-09-13:
        # 18 rows gained a `thumb` and the generated cards would have kept none
        # until each hub was regenerated. A card lists its thumb or nothing,
        # so the card's picture must be exactly its row's.
        row_thumb = dict((r["url"].lstrip("/"), r.get("thumb")) for r in data["resources"]
                         if r.get("language") == code)
        for href, body in re.findall(r'<a class="hub-row" href="([^"]+)">(.*?)</a>', s, re.S):
            img = re.search(r'<span class="hub-row-thumb"><img src="([^"]+)"', body)
            have_t, want_t = img.group(1).lstrip("/") if img else None, row_thumb.get(href.lstrip("/"))
            if href.lstrip("/") in row_thumb and have_t != want_t:
                problems.append("%s (%s): card %s shows %s, its row's thumb is %s"
                                % (rel, code, href, have_t, want_t))
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
        cp = [n for n in json.loads(m.group(1))["@graph"]
              if n.get("@type") == "CollectionPage"] if m else []
        parts = sorted(x["url"].split(site, 1)[-1] for x in cp[0].get("hasPart", [])) if cp else None
        checked += 1
        for what, have in (("no-JS card list", cards), ("CollectionPage hasPart", parts)):
            if have is None:
                problems.append("%s (%s): no CollectionPage in the JSON-LD" % (rel, code))
            elif have != want:
                miss, extra = sorted(set(want) - set(have)), sorted(set(have) - set(want))
                problems.append(
                    "%s (%s): the %s has %d entries, data/resources.json has %d %s rows.%s%s"
                    % (rel, code, what, len(have), len(want), code,
                       "\n      missing: %s" % ", ".join(miss[:4]) if miss else "",
                       "\n      not in the data: %s" % ", ".join(extra[:4]) if extra else ""))
    return checked, problems


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or "--check" not in sys.argv:
        raise SystemExit("usage: hubrows.py <site-root> --check")
    path = os.path.join(args[0], "data", "resources.json")
    data = json.load(io.open(path, encoding="utf-8"))
    checked, problems = check(data)
    n = len(data["resources"])
    print("%d entries, %d English, %d translations checked against their English source"
          % (n, sum(1 for r in data["resources"] if r.get("language") == SOURCE_LANG), checked))
    n_hubs, hub_problems = hubs(args[0], data)
    problems += hub_problems
    print("%d hub pages checked against the rows they are generated from" % n_hubs)
    if problems:
        print("\nCHECK FAILED: %d problems" % len(problems))
        for p in problems:
            print("  " + p)
        raise SystemExit(1)
    print("\nCHECK PASSED: every translated row carries its English source's taxonomy exactly,\n"
          "and every language's hub lists exactly that language's rows, each card with its row's thumb.")
