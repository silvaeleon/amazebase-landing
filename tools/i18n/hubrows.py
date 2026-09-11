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

import copy, io, json, os, sys

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


def check(data):
    """Returns (checked, problems). Empty problems means every translated row
    carries exactly its English source's taxonomy."""
    rows = data["resources"]
    source = dict((r["id"], r) for r in rows if r.get("language") == SOURCE_LANG)
    problems, checked = [], 0

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
    if problems:
        print("\nCHECK FAILED: %d problems" % len(problems))
        for p in problems:
            print("  " + p)
        raise SystemExit(1)
    print("\nCHECK PASSED: every translated row carries its English source's taxonomy exactly.")
