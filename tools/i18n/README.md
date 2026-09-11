# tools/i18n — adding a language to amazebase.pro

Read this before translating anything. It is written for the session that adds
Portuguese, and for the three after that.

The site is English and Spanish today: 51 articles and 5 top-level pages in
each, 112 pages carrying a language switcher. Spanish took one full session.
The parts of that session worth keeping are in here.

---

## The one rule

**Anything that names every language is generated, never authored.**

Two lists on every page name every other language: the `<link rel="alternate">`
block in the head and the switcher menu in the nav. Author them by hand and
adding language N means editing every page of languages 1 through N-1 — 112
pages for Portuguese, then 168 for French, 224 for Italian, 280 for German.
784 page edits, and every one of them a chance for a single page to disagree
with the others about which languages exist.

Both failure modes are silent. A search engine that finds an inconsistent
alternates cluster may discard the whole cluster; a stale switcher row is a 404
sitting in the navigation. The page still renders. Nothing errors. You find out
from Search Console months later.

So `langlinks.py` regenerates both lists on **every page in every language**
from `languages.json`. Adding a language is a manifest entry, a slug map, and
one run.

---

## Adding a language, in order

### 1. Regenerate the briefs

```bash
python3 tools/i18n/reextract.py . -o /tmp/briefs --compare /tmp/briefs-last
```

One JSON per English article: title, meta, breadcrumb, keywords, `<header>`,
hero, `<main>`, rail, CTA. This is what a translator receives.

**Briefs are derived and are not committed.** A committed brief goes stale the
moment an article is edited and it goes stale silently — the file still parses
and the translator still gets something plausible. This has already happened
once: the Spanish briefs were extracted before `e6c841f` and still held the
20–25 word hero alts that commit replaced. Handed on unchanged they would have
put the discarded alt text back on the site, one language at a time.

`--compare` names every field that moved since a previous extraction. Anything
outside `hero`, `hero_alt` and `og_img_alt` means an article changed under you.

### 2. Write the register and glossary, and get them approved

This is the step that decides whether the language reads native, and it is the
only step that genuinely needs Leon. Copy `briefs/TRANSLATOR-es.md` to
`TRANSLATOR-<code>.md` and rewrite the language-specific half:

- **Register.** Spanish settled on neutral Latin American, informal *tú*.
  Portuguese has the same decision to make and a sharper one — Brazil or
  Portugal, *você* or *tu*. Brazilian is almost certainly right for Amazon
  sellers, but say so and get a yes rather than assuming.
- **The glossary.** `briefs/GLOSARIO-ES.md` is the model: a table of the calls
  where reasonable translators disagree, each with the alternative and the
  reason. Five decisions was the right size. Get them approved **before** the
  bulk run, not after — Spanish did the pilot first for exactly this reason.
- **Number and punctuation conventions.** Spanish kept US separators
  (`$30,000`) because every figure is USD copied from US sources. German and
  Portuguese conventions differ from Spanish; decide explicitly.

Then translate **three articles as a pilot** and have them approved before the
other 48 start.

### 3. Translate from the English briefs — never from another translation

Subagents take 2–3 articles each and return JSON. Do not hand a Portuguese
translator the Spanish page because it is "closer". Error compounds through a
relay, and the Spanish already contains judgement calls that were right for
Spanish and are not automatically right for Portuguese.

Translators are told to leave every `href` alone so the gate can compare them.
Cross-article links are rewritten afterwards in a separate deterministic pass,
once every slug in the new language exists. **Do not merge those two steps.**

### 4. Gate every translation before it reaches a page

`es-2026/gate.py` is the working example. It refuses a translation whose
structural skeleton, anchor ids, hrefs or figures differ from the English, or
that still contains English stopwords.

**Calibrate the gate on known-good work first.** The Spanish gate was run
against the three approved pilot pages and passed at 418 elements identical
before any of the 48 went through it. That is what made a later failure mean
something rather than look like noise.

### 5. Build the pages

`es-2026/` holds the Spanish run verbatim as a worked example: `common.py` and
`build_articles.py` for articles, `chrome_common.py` and `build_chrome.py` for
the five top-level pages, `build_hub.py` and `hubjs.py` for the hub.

`build_articles.py` assembles by replacing regions *inside* the English wrap
block rather than rebuilding the page, so each page's own quirks survive.

### 6. Update the hub data

`data/resources.json` is the whole Knowledge Hub. For a new language:

- **51 new entries**, each with `language`, `url`, and `translationOf` pointing
  at the English `id`.
- **25 taxonomy labels** — `label_<code>` on 6 categories, 7 formats, 2 levels
  and each row of `languages`, plus `label_one_<code>` on all 7 formats.
- Thumbnails and heroes are derived from the **slug in `url`, never `id`**.
  Seven entries have an `id` that differs from their filename.

`js/hub.js` puts every user-facing string through `T()`, which falls back to
the English literal. Adding a language is one column in `STR`. A hub is
**scoped** to its own language — `SCOPE` filters everything the page counts,
tiles, searches and features, and is never offered as a clearable filter.

**Before you copy the gaps forward:** 7 English articles and their 7 Spanish
counterparts have no `category`, so they list but sit under no tile. Fixing
that is a content decision for Leon, and it is much cheaper now than after it
has been replicated into four more languages.

### 7. Run langlinks.py

Append to `languages.json`, add `slugs/<code>.json` mapping every English
article slug to the local one, then:

```bash
python3 tools/i18n/langlinks.py . --check   # see what would change
python3 tools/i18n/langlinks.py .           # write it
```

It rewrites the alternates block, the switcher chip and the switcher menu on
every page in every language. It refuses to run if a slug map has holes,
because a hole means those pages would quietly drop the new language from their
alternates and nothing would look wrong.

**It must be a no-op before you add anything.** Run `--check` against the
current tree with the current manifest first: byte-identical on all pages, or
the generator does not reproduce what already ships and must not be trusted to
generate what comes next.

### 8. Verify before it ships

The sandbox cannot reach amazebase.pro, and `WebFetch` can but strips JSON-LD —
so structured data has to be checked **before** it goes out. Serve the tree
locally and drive it with Playwright.

---

## Traps that have already cost a commit

**Relative paths under a language directory.** The top-level English pages
reference their CSS, JS and each other with relative paths. Copied under
`/es/` those resolve to `/es/css/base.css` and 404, and the page renders as
unstyled text. Every translated copy is rewritten root-absolute and the rewrite
is asserted at build time.

The URL-carrying attributes are **`href`, `src`, `srcset`, `imagesrcset` and
`poster`**. A rewriter that knows only the first two looks like it works and
asserts clean — that is exactly how the hero on `/es/recursos.html` shipped
404ing. Note also that a `<picture>` commits to the first `<source>` whose type
the browser supports and does **not** fall back to the `<img>` beneath it, so a
single missed attribute kills the image outright. Assert on each candidate
inside a srcset list, not on the attribute as a whole.

**Narrowing a check past the thing it was checking for.** The Spanish
builder's postflight was scoped to the body so English comments inside the
shared stylesheet would not trip it. `<title>`, every `<meta>` and the whole
JSON-LD graph live in the *head*, so `/es/recursos.html` shipped declaring
itself to be the English hub, with an English name and 44 English articles in
`hasPart`, and the check passed. When you narrow a check to avoid a false
positive, say out loud what is now unchecked.

**Asserting a convention the existing pages do not follow.** Two postflights
during the alt-text pass flagged raw accents in HTML comments and raw em dashes
in attribute values. Both are inherited from the English pages and both are
fine. Check what the good pages actually do before asserting on it.

**Alt text.** The 44 decorative hero images say what the image *means* in 8–14
words (`briefs/ALTS.md`). Product screenshots and data figures — `sol-*`,
`product-*`, `about-*`, `feat-*` — deliberately keep long descriptions, because
a screen-reader user cannot otherwise reach the numbers inside them. Do not
"tidy" those. Each language writes its own alts from its own article rather
than translating the English ones.

**Number formatting in translated bodies.** `gate.py` compares the ordered list
of figures in the English and the translation and warns on a mismatch. A comma
is a thousands separator only when digits follow it — that regex is
`\d+(?:,\d{3})*(?:\.\d+)?`, and it is narrow on purpose.

---

## What is in here

| | |
|---|---|
| `languages.json` | The manifest. One entry per language: code, label, switcher chip, articles directory, and the path of each top-level page. Order here is the order in the head and in the switcher. |
| `slugs/<code>.json` | English article slug → that language's slug. |
| `langlinks.py` | Regenerates the alternates block, switcher chip and switcher menu on every page. `--check` for a dry run, `--cfg DIR` to point at a different manifest. |
| `reextract.py` | Extracts one brief per English article. `--compare` diffs against a previous extraction. |
| `pipeline.py` | `brief()`, `skeleton()`, `skeleton_diff()`, `check()`. The structural fingerprint is the ordered sequence of every tag with its `id/class/href/src/style/points/d/viewBox/...`. |
| `briefs/TRANSLATOR-es.md` | The Spanish translator brief. Copy and rewrite the language half. |
| `briefs/GLOSARIO-ES.md` | The five Spanish judgement calls Leon approved, with alternatives. The model for the next language's glossary. |
| `briefs/ALTS.md` | The alt-text brief. Language-neutral. |
| `es-2026/` | The Spanish run verbatim — every build script as it was actually used. A worked example, not a library. Paths in it are absolute to the session that ran it. |

Briefs themselves are not committed. Regenerate them; it takes two seconds.

One naming rule, learned the hard way: **`.gitignore` ignores `_*` everywhere
in this repo.** These two documents were originally `_TRANSLATOR.es.md` and
`_ALTS.md`, and git silently declined to track either — the two files here that
cannot be regenerated from anything. Do not give a file in this folder a
leading underscore.
