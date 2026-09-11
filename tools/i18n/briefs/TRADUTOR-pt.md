# Translator brief — AmazeBase Knowledge Hub, English → Brazilian Portuguese

You are translating marketing/educational articles for **AmazeBase**, an
analytics product for Amazon sellers. The English is deliberately written: short
sentences, concrete numbers, a dry confident voice that never oversells. Match
that voice. A translation that reads like a translation has failed.

**Translate from the English brief only.** Do not open anything under `es/` or
any Spanish file, even to "check a term". Spanish is not closer to the source;
it is one more step away from it, and several Spanish rulings are deliberately
wrong for Portuguese (see `GLOSSARIO-PT.md` §1).

The approved decisions are in `tools/i18n/briefs/GLOSSARIO-PT.md`. Read it
first. This brief repeats what you need; if the two ever disagree, the glossary
wins and you should say so in your reply.

## Register — decided, not negotiable

**Brazilian Portuguese, *você*, friendly and professional.**

- *você / seu / sua*; verbs in the *você* form: *você pode, você tem, confira,
  calcule, revise, use*.
- Never *tu*, never *o senhor / a senhora*, never *vós*.
- Brazilian, not European, word choice and grammar: *equipe* not *equipa*,
  *tela* not *ecrã*, *celular* not *telemóvel*, *fato* not *facto*, *registro*
  not *registo*, *usuário* not *utilizador*, *contato* not *contacto*,
  *estou fazendo* not *estou a fazer*.
- Write *para*, not *pra*; avoid *a gente* — the voice is plain, not slangy.
- **Percentages: `25%`, no space.** Not `25 %`.
- **Quotes: curly double quotes** `&ldquo; &rdquo;`, and `&lsquo; &rsquo;`
  inside them. Never `«…»`, never straight `"` in text.
- **Numbers keep US formatting**: `$30,000`, `$8.00`, `1,200 unidades`. Never
  `$30.000`, never `US$`. This is a decided rule — do not "fix" it.
- Dates are written the Brazilian way, lowercase month: `14 de julho de 2026`.
  The `datetime="…"` attribute never changes.
- Multipliers stay as written: `4.2x`.

## Terminology — use exactly these

| English | Portuguese |
|---|---|
| Amazon seller | vendedor da Amazon |
| inventory | estoque (never *inventário* for stock on hand) |
| stockout | ruptura de estoque; *ficar sem estoque* as the verb |
| overstock | excesso de estoque |
| available / reserved / inbound inventory | estoque disponível / reservado / em trânsito |
| days of supply | dias de cobertura |
| weeks of cover | semanas de cobertura |
| sales velocity | velocidade de vendas |
| average daily sales | vendas médias diárias |
| safety stock | estoque de segurança |
| reorder point | **ponto de reposição** (never *ponto de pedido*) |
| lead time | **lead time**, in English, masculine (*o lead time*, *lead time total*) |
| purchase order | pedido de compra |
| to reorder / restock | repor |
| supplier | fornecedor |
| manufacturing / freight / customs | fabricação / frete / alfândega |
| ocean freight | frete marítimo |
| supplier preparation | preparação do fornecedor |
| inland transport | transporte terrestre |
| Amazon receiving | recebimento na Amazon |
| landed cost | **imported product:** custo total de importação · **domestic, or not said:** custo total por unidade — *(landed cost)* in brackets on first use. Use *importação* only if the article's product is imported (overseas supplier, freight, duty, customs). |
| cash flow | fluxo de caixa |
| cash cycle | ciclo de caixa |
| cash floor | piso de caixa |
| working capital | capital de giro |
| capital allocation | alocação de capital |
| margin / profit / revenue | margem / lucro / faturamento — **but** *faturamento* is GROSS revenue: where the English means revenue after returns or refunds ("net revenue", "net sales", "after returns") write **receita líquida**. Decide each occurrence; the gate refuses *faturamento* where the English says net revenue. |
| break-even | ponto de equilíbrio |
| payout | repasse |
| ad spend | gasto com anúncios |
| bid | lance |
| keyword / search term | palavra-chave / termo de pesquisa |
| placement | posicionamento |
| organic ranking | ranqueamento orgânico |
| dayparting | programação por horário |
| branded campaign | campanha de marca |
| conversion rate | taxa de conversão |
| incrementality | incrementalidade |
| to negate (a keyword) | negativar |
| dashboard | painel |
| spreadsheet | planilha |
| forecasting | previsão / prever |
| launch | lançamento |
| portfolio | portfólio |
| momentum | tração / impulso (by sense) |
| compounding | efeito composto |
| moat | vantagem competitiva |
| optionality | opcionalidade |
| trade-off | trade-off / concessão (by sense) |
| warehouse | armazém |
| storage fees | taxas de armazenagem |
| shrinkage | perdas |
| overheads | despesas gerais |
| settlement | liquidação |

**Keep in English, untranslated:** `ACOS` `ACoS` `TACOS` `TACoS` `ROAS` `CPC`
`PPC` `FBA` `AWD` `3PL` `SKU` `ASIN` `TAM` `ROI` `P&L` `Buy Box` `listing`
`lead time` `bulksheet` `flywheel` `Seller Central` `Campaign Manager`
`Amazon`, and *Sponsored Products / Brands / Display*. AmazeBase module names
stay as they appear (`Ledger`). `listing` stays English because *anúncio* also
means "ad"; where the English means the product page itself, *página do
produto* is fine.

**Category eyebrows** lose the ampersand: *PPC & Advertising* → *Publicidade e
PPC*, *Profit & Finances* → *Lucro e finanças*, *Inventory* → *Estoque*,
*Inventory Planning* → *Planejamento de estoque*, *Growth Playbook* → *Guia de
crescimento*, *Product Research* → *Pesquisa de produtos*, *Tools & Tutorials*
→ *Ferramentas e tutoriais*. Example labels *Alpha/Beta* become *Alfa/Beta*.

**Fixed labels — exact strings, enforced.** Callout labels (the short
headings in `fixbox-k`, `rail-k`, `label`, `lab`, `eyebrow` and `player-kind`
elements — "The fix", "The point", "Related reading"…) recur across dozens of
articles and must read identically in every one. **Open
`GLOSSARIO-PT.md` §6 and use its Portuguese string exactly** whenever the
English label matches a row: "The point" is *O que importa*, never *A questão*
or *O ponto*. The gate refuses any variant. The same table fixes *Passo 01*,
*N min de leitura*, the table-of-contents heading, *Para fechar*, *Perguntas
frequentes* and the figures note. A label that is NOT in the table is yours to
translate naturally.

**Other chrome strings inside your regions:** Join the Wait List → *Entre na
lista de espera*; Knowledge Hub → *Central de Conhecimento*; rail `aria-label`
"Key figures from this article" → *Números-chave deste artigo*.

**Numbers and their units:** type a normal space between a number and its unit
(*6 meses*, *1,200 unidades*); a later step joins them with a non-breaking
space so they never wrap apart. Do not abbreviate a unit to save width
(*4 semanas*, not *4 sem.*).

## The absolute rules about markup

You are translating **text nodes only**. The HTML around them must come back
**byte-for-byte identical in structure**. A build gate compares the ordered
sequence of every tag and its `id`, `class`, `href`, `src`, `style`, `width`,
`height`, `points`, `d`, `viewBox`, `colspan`, `scope`, `datetime` attributes.
If anything differs, the article is rejected and has to be redone.

**Do:**
- Translate text between tags.
- Translate the *value* of `alt="…"` and `aria-label="…"` attributes.
- Write accented characters as HTML entities, because the surrounding files
  do: `&aacute; &acirc; &atilde; &agrave; &ccedil; &eacute; &ecirc; &iacute;
  &oacute; &ocirc; &otilde; &uacute;` and the capitals `&Aacute; &Acirc;
  &Atilde; &Agrave; &Ccedil; &Eacute; &Ecirc; &Iacute; &Oacute; &Ocirc;
  &Otilde; &Uacute;`, plus `&ldquo; &rdquo; &lsquo; &rsquo; &mdash;`.

**Never:**
- Add, remove, reorder, merge or split ANY tag — including `<b>`, `<em>`,
  `<strong>`, `<br>`, `<li>`, `<span>`. If the English wraps three words in
  `<b>`, the Portuguese wraps its equivalent words in `<b>` — same tag, same
  place in the sequence.
- Change any `id`, any `href`, any `class`, any inline `style`, any SVG
  coordinate, any `width`/`height`. **Leave every `href` exactly as it is,
  including links to other articles** — they are rewritten to the Portuguese
  pages later, in a separate step, once every Portuguese slug exists.
- Change any number, figure, currency amount, percentage or date value.
- Translate an SVG `points`/`d` attribute — only plain-language labels rendered
  as `<text>` content are translated.

**`<pre>` blocks — decide by what the block IS, not by its tag:**
- **Literal code** — anything a reader would copy and run or paste: commands,
  JSON, config, a formula in a programming syntax. Never translated;
  byte-identical. (There is none in this corpus today; the rule is here for
  when there is.)
- **Worked sums written in words** that sit in `<pre>` only to line up — *stock
  lasts 50 days*, *cash floor = one full reorder…*. **Translate the words.**
  Keep every digit, operator (`= + × ÷ ≈ ~ − / %`), currency symbol and bracket
  exactly where it is, in the same order. Keep **the same number of lines** —
  never wrap a long line onto a new one. Where the English lines values up in a
  column (the `=` signs, or the numbers after a gap of spaces), line the
  Portuguese up too by adjusting the spaces: labels get longer in Portuguese, so
  the column moves right, and every line in it moves with it. The gate compares
  the numbers and operators of each `<pre>` with the English, its line count,
  and its columns, and refuses any difference.
- Add explanatory notes, translator comments, or emphasis the English does not
  have.

HTML comments inside the body may be translated or left as they are — they are
not rendered.

## Alt text for the hero image

If the brief's `hero_alt` is not null, write **one new alt of 8 to 14 words**
saying what the image *means for this article*, in this article's Portuguese
vocabulary — not a translation of the English alt, and not a description of
colours and shapes. No "imagem de" / "ilustração mostrando". Keep a visual
anchor only if it carries the idea (the cliff edge in the reorder-point image
does). Put the **same string** in `hero_alt` and `og_img_alt`: the `<img alt>`,
`og:image:alt` and `twitter:image:alt` describe the same picture and move
together. If `hero_alt` is null, both are null. The full brief is
`tools/i18n/briefs/ALTS.md`.

## Top-level pages (product, solutions, about, contact, the hub)

Same rules, plus:

- **Screenshot and data-figure alts are translated IN FULL.** `product-*`,
  `sol-*`, `about-*` and `feat-*` images carry real numbers a screen-reader user
  cannot otherwise reach; the 8–14 word rule is for decorative article heroes
  only. Every figure stays.
- **The waitlist dialog** (translated once, on product): translate the text,
  aria-labels, placeholders, optgroup labels and option texts; add the seven
  `data-msg-*` attributes to the opening `<dialog>` tag (`js/waitlist.js` reads
  them). Never change a `name`, `id`, `for`, `value` or `data-waitlist-*`
  attribute, and never touch the hidden honeypot inputs `company_website` and
  `referral_code` — renaming one disables the bot trap silently. The HTML
  comment above them stays in English, verbatim: it is developer documentation.
- **Postal addresses, names and codes stay identical** — the gate allows an
  identical text node when it carries no English function word.
- **Faithful over helpful.** Where the English does something a Portuguese
  reader may find odd (Brazil grouped under "North America", following Amazon's
  own region naming), translate it faithfully and raise it; do not fix the
  meaning in translation.

## What you produce

For **each** slug you are given:

1. Read the brief JSON at the path you are given. It has: `main` (the whole
   `<main>…</main>` block), `title`, `desc`, `og_title`, `og_desc`,
   `og_img_alt`, `ld_headline`, `ld_desc`, `crumb`, `keywords`, `hero_alt`,
   `article_head`, `back_link`, `rail`, `cta`, `words`.

2. Write **one file**, UTF-8, to the output path you are given, containing
   exactly this shape:

```json
{
  "slug": "<english slug>",
  "pt_slug": "<portuguese-url-slug>",
  "main": "<main id=\"main\" class=\"article\"> … </main>",
  "article_head": "<header class=\"article-head\"> … </header>",
  "rail": "<aside class=\"rail\" …> … </aside>",
  "cta": "<aside class=\"cta\"> … </aside>",
  "hero_alt": "…",
  "og_img_alt": "…",
  "title": "…",
  "desc": "…",
  "og_title": "…",
  "og_desc": "…",
  "ld_headline": "…",
  "ld_desc": "…",
  "crumb": "…",
  "keywords": ["…", "…"]
}
```

- `rail` and `cta` are `null` if the brief's are `null`. Same for `hero_alt`
  and `og_img_alt`.
- `pt_slug`: if you were given one, use it exactly. Otherwise take the most
  distinctive clause of the Portuguese title, lowercase, strip accents
  (`ç`→`c`, `ã`→`a`, `é`→`e`), spaces to hyphens, no punctuation. **At most 50
  characters AND at most 7 words** — the build refuses anything longer and
  does not shorten it for you. Do not put accents back into a slug.
- `ld_headline`, `ld_desc`, `crumb` and `keywords` go into JSON-LD, so write
  them as **plain text with real accented characters**, not HTML entities.
- `title`, `desc`, `og_*`, `hero_alt` end up inside HTML attributes — entities
  there, no raw accented characters.
- The file must be valid JSON. HTML inside it has its double quotes escaped as
  `\"` and newlines as `\n`. The easy way to get this right is to write the
  fragments with a short Python script that builds the dict and calls
  `json.dump(..., ensure_ascii=False, indent=1)` — then load the file back to
  prove it parses.

3. Run the gate on your file and fix anything it reports:

```
python tools/i18n/gate.py pt <slug> --brief <brief.json> --content <your file>
```

Do not print the article content back in your reply. Your reply should be a
few lines: which slug you wrote, the gate's last line, and any term or sentence
you were unsure about.

## Worked example

English:

```html
  <div class="fixbox">
    <span class="fixbox-k">The fix</span>
    <p>If your sales are growing quickly, don&rsquo;t rely on a 90-day average.
       Use the most recent 30 days &mdash; or even the last two weeks &mdash; to
       better reflect current demand.</p>
  </div>
```

Portuguese:

```html
  <div class="fixbox">
    <span class="fixbox-k">O que fazer</span>
    <p>Se as suas vendas est&atilde;o crescendo r&aacute;pido, n&atilde;o confie
       numa m&eacute;dia de 90 dias. Use os &uacute;ltimos 30 dias &mdash; ou
       at&eacute; as duas &uacute;ltimas semanas &mdash; para refletir melhor a
       demanda atual.</p>
  </div>
```

Same tags, same classes, same order, same numbers. Only the words changed.
