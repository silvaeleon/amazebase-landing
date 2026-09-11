# Brief — rewriting decorative hero alt text

44 AmazeBase article hero images have alt text that inventories the picture:
colours, shapes, where things sit. Typical:

> "A blue line of stock crates running along a raised road that ends abruptly at
> a cliff edge, the remaining crates shown only as wireframes" — 25 words

That is the wrong job. These are **decorative marketing images**: abstract
artwork sitting under a headline. A screen-reader user gets 25 words of visual
inventory and learns nothing about the page. A search engine gets no term it
could ever match a query against.

Product screenshots and data figures elsewhere on the site keep their long
descriptions — a screen-reader user genuinely cannot see the numbers in a chart.
These 44 are not that.

## What to write instead

**8 to 14 words.** Say what the image *conveys about the article*, in the
article's own vocabulary. The reader should finish the alt knowing what the page
is about.

Good:

| | |
|---|---|
| Article | *Amazon Inventory Reorder Point: The Simple Formula Every Seller Should Know* |
| Before (25w) | A blue line of stock crates running along a raised road that ends abruptly at a cliff edge, the remaining crates shown only as wireframes |
| **After (12w)** | **Inventory running off a cliff edge when the reorder point is missed** |

| | |
|---|---|
| Article | *Advertising Debt: The Hidden Liability Almost Every Amazon Business Is Building* |
| Before (20w) | A lit house inside a glass dome, kept alive by blue cables running from a dark industrial generator behind it |
| **After (11w)** | **Sales kept alive entirely by advertising, like a house on a generator** |

## Rules

- **8–14 words.** Under 8 is usually too vague; over 14 and you are back to
  describing the picture.
- **No "image of", "picture of", "illustration showing".** Screen readers already
  announce it as an image.
- **Use the article's real vocabulary** — reorder point, ACoS, landed cost,
  quiebre de stock. Not because keywords are magic, but because that is what the
  picture is actually about.
- **Do not keyword-stuff.** "AmazeBase Amazon seller inventory software tool" is
  worse than the 25-word description it replaces. One natural sentence.
- **Do not invent claims.** The alt describes the artwork's meaning, not a
  product capability.
- **Keep the visual anchor if it carries the idea.** The cliff edge above is
  worth keeping; "blue", "amber", "glowing ring" almost never are.
- The **English and Spanish must say the same thing**, each written natively in
  its own language. The Spanish is not a translation of your English — write
  both from the article.
- Spanish register: **neutral Latin American, informal *tú*** where a verb form
  is needed at all. Accents as HTML entities (`&aacute; &eacute; &iacute;
  &oacute; &uacute; &ntilde;`), because that is how the rest of the file is
  written. English alt is plain ASCII.

## Input and output

`/home/claude/briefs/_alts.json` is a list of 44 objects:

```json
{"en_slug": "...", "es_slug": "...", "img": "hero-....webp",
 "en_title": "...", "es_title": "...",
 "en_alt": "<the long one>", "es_alt": "<the long one>"}
```

For the slugs you are given, write **one file** to
`/home/claude/altout/<en_slug>.json`:

```json
{"en_slug": "...", "en_alt": "...", "es_alt": "..."}
```

`en_alt` plain ASCII. `es_alt` with accents as entities. Nothing else in the
file. Do not print the alt text back in your reply — just say which files you
wrote and flag anything you were unsure about.
