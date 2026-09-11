# Translator addendum: homepage, privacy policy, terms of service

This addendum is for the three pages Leon added on 2026-09-11. Read your
language's brief first: `TRADUTOR-pt.md` or `TRANSLATOR-es.md`. Also read its
glossary: `GLOSSARIO-PT.md` or `GLOSARIO-ES.md`. Every rule there applies. It
covers register, terminology, the absolute markup rules, entities, `<pre>` and
"faithful over helpful". This file only adds what is specific to these pages.

## Placeholders: `@@T12@@`

The homepage's `main` holds 29 placeholders. Each one stands in for an
embedded image, a `<script>` or `<style>` body, or a long SVG path. The
builder restores the originals byte-for-byte. It refuses any translation that
loses one, repeats one or invents one.

Copy each placeholder exactly where it is. Never translate it, split it or
move it. Privacy and terms have none.

## The homepage (`home`)

- **Pricing stays in US dollars** (Leon). Keep every price, figure and
  percentage exactly as written: `$`, US number format, the same order.
  Translate only the words around them, such as "/month" and "per seat".
- **The two self-contained blocks** are the 7-module pipeline (`.abp`) and
  the "too many tools vs AmazeBase" comparison (`.abc`). Translate their text
  like everything else. Leave every tag, class and attribute exactly as it is.
  Their layout is measured from the text, so short labels stay short.
- **Module names:** use the words the shipped product page already uses in
  your language. That is `pt/produto.html` or `es/producto.html`, including
  its header menu, which lists Advertising & PPC, Financials, Inventory,
  Product Research and the rest. One name per module across the site.
- **Plan names stay as they are:** *Pro*, *Enterprise*. They are product
  names, like the module name *Ledger*.
- **Third-party names stay as they are:** Seller Central, Excel, Helium 10,
  Google Sheets, Amazon and the lowercase "amazon" logo text. The gate accepts
  an identical text node that has no English function word in it.
- **`features`** is a list of 8 short English phrases. They go into the
  page's structured data (JSON-LD). Return a list of 8 translations, in the
  same order, as plain text with real accented characters, not entities.
- There is **no `crumb`** for the homepage. Return `"crumb": null`.

## Privacy policy and terms of service (`privacy`, `terms`)

These are legal documents. Translate them **faithfully and completely**.

- **No summarising, no simplifying, no improving, no omissions.** Every
  sentence and every clause stays, with its meaning and its conditions. If a
  sentence is long in English, it may be long in your language.
- **Keep the site's register.** Portuguese uses *você*. Spanish uses the
  informal *tú*, the site-wide decision; do not switch to *usted*. Legal
  precision does not need a formal pronoun.
- **Defined terms are consistent.** When the English defines a term in
  quotes, such as ("the Platform", "Services", "we", "us"), choose one
  translation and use exactly that everywhere in both documents: for example
  *la Plataforma* / *a Plataforma*. Keep the definition's quotes, using
  `&ldquo; &rdquo;`.
- **Names, entities and places:** keep *Silbros Trading LLC* and
  *AmazeBase* exactly. Translate the legal form in prose ("a New Mexico
  limited liability company" becomes *una sociedad de responsabilidad
  limitada de Nuevo México* / *uma sociedade de responsabilidade limitada do
  Novo México*), but never inside the company name. Do not localise the law:
  governing law, courts and jurisdictions stay what the English says.
- **Emails, URLs and the street address** stay identical. The country line of
  a postal address is translated (*Estados Unidos*), as the shipped contact
  pages do. Both legal translators kept "United States", following an earlier
  version of this line, and it was corrected after the gate.
- **Dates:** write them in your language (*6 de agosto de 2026*). Never
  change a `datetime="…"` attribute. Every number stays in the same order:
  the gate compares them.
- **Do NOT add the "this is a translation" note.** The builder inserts it
  after the gate has passed.
- There is no `features` list. Return `"features": null`.

## What you produce

This is the same shape as your brief's "What you produce", with these fields:

```json
{
  "slug": "home | privacy | terms",
  "pt_slug": "…"   (or "es_slug"),
  "main": "<main …> … </main>",
  "title": "…", "desc": "…", "og_title": "…", "og_desc": "…", "og_img_alt": "…",
  "crumb": "… or null",
  "features": ["…"] or null,
  "cta": null, "article_head": null, "rail": null, "hero_alt": null,
  "ld_headline": null, "ld_desc": null, "keywords": []
}
```

The slug is given to you. Use it exactly.

- `title`, `desc`, `og_*` go into HTML attributes, so use entities, not raw
  accented characters.
- `crumb` and `features` go into JSON-LD, so use plain text with real accents.

Run the gate until it reports 0 problems:

```
python tools/i18n/gate.py <lang> <slug> --brief <brief.json> --content <your file>
```

Then run the builder's strict check. It compares every tag and every
attribute except alt, title, aria-label and placeholder, and it also checks
the placeholders:

```
python tools/i18n/home_legal.py strict <brief.json> <your file>
```
