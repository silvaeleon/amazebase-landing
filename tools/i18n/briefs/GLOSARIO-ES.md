# Spanish glossary — AmazeBase Knowledge Hub

Read this before approving the pilot. Everything below is a **decision** that
will be applied identically to the remaining 48 articles, so a change here is
cheap now and expensive later.

Register: **neutral Latin American Spanish, informal *tú***. No *vosotros*, no
*ordenador*, no *coger*. Verbs in the *tú* form throughout (*puedes, revisa,
calcula*), which is what the English originals do in the second person.

---

## 1. The five decisions I made for you

These are the ones where reasonable people disagree. If you want any of them
changed, say which and I will re-run all three pilot pages before the other 48
start.

| # | Decision | What I chose | The alternative |
|---|---|---|---|
| 1 | **Numbers** | US formatting kept: `$30,000`, `$8.00`, `1,200 unidades` | European/RAE: `$30.000`, `$8,00`. Every figure on the site is USD and copied from US sources, so switching separators invites transcription errors. |
| 2 | **Percentages** | `25 %` with a non-breaking space (RAE style) | `25%` (US style). This one is cosmetic. |
| 3 | **"reorder point"** | **punto de reorden** | *punto de pedido* is the Spain term. *Reorden* is what LatAm Amazon sellers actually say. |
| 4 | **"lead time"** | **tiempo de reposición** (and *tiempo total de reposición* for the full chain) | Leaving *lead time* in English. Sellers use both; the Spanish reads better in a formula. |
| 5 | **Quotation marks** | `«…»` angle quotes | `"…"` curly quotes. Angle quotes are the Spanish convention and already render correctly in the dark theme. |

Decision 1 is now a **site-wide convention**, not a Spanish one: every number
in every language keeps US formatting — see `tools/i18n/README.md`, *Shared
conventions*. The row above stays as the record of how it was first decided.

---

## 2. Terms kept in English on purpose

These are how sellers actually talk. Translating them would make the articles
read as though written by someone who has never used Seller Central.

`ACOS` · `TACOS` · `ROAS` · `CPC` · `PPC` · `FBA` · `SKU` · `ASIN` ·
`Buy Box` · `listing` · `Seller Central` · `Business Reports` ·
`unit session percentage` · `Ledger` (the AmazeBase module name)

`Business Reports` and `unit session percentage` were added 2026-09-11 with
*¿Cuántos datos necesitas antes de cambiar una campaña?*. They are a Seller
Central section and one of its column headings: a reader hunting for that
column needs the string Amazon shows them, whatever language their Seller
Central is in. Same rule as `Seller Central` itself, with one addition — on
**first use only** the Spanish follows in brackets, so the reader learns what
it measures without losing the string: *la columna llamada unit session
percentage (porcentaje de sesiones por unidad)*. Later uses are bare.

"Advertising Cost of Sales" appears once, in plain text, where ACOS is
expanded in the lead of the ACOS article — as the English does. *(Corrected
2026-09-11: this line used to say "in italics … same as the English original
does". The English was never italic; the Spanish page alone wrapped it in
`<em>`, which is the one structural difference the gate found across all 51
Spanish pages. The page is fixed in the same commit.)*

---

## 3. The working vocabulary

| English | Spanish | Note |
|---|---|---|
| Amazon seller | vendedor de Amazon | |
| stockout | quiebre de stock | not *desabasto*, not *ruptura de stock* |
| overstock | sobrestock / exceso de inventario | |
| available inventory | inventario disponible | |
| reserved inventory | inventario reservado | |
| inbound inventory | inventario en tránsito | |
| days of supply | días de cobertura | |
| weeks of cover | semanas de cobertura | |
| sales velocity | velocidad de ventas | |
| average daily sales | ventas diarias promedio | |
| safety stock | stock de seguridad | |
| reorder point | punto de reorden | decision 3 |
| lead time | tiempo de reposición | decision 4 |
| purchase order | orden de compra | |
| to reorder / restock | reponer | *repone el producto que funciona* |
| supplier | proveedor | |
| manufacturing | fabricación | |
| supplier preparation | preparación del proveedor | |
| ocean freight | flete marítimo | |
| customs | aduana | |
| inland transport | transporte terrestre | |
| Amazon receiving | recepción en Amazon | |
| landed cost | costo puesto en destino | *costo*, not *coste* |
| cash flow | flujo de caja | |
| cash cycle | ciclo de efectivo | |
| cash floor | piso de efectivo | coined for this article; it is the author's coinage in English too |
| working capital | capital de trabajo | |
| capital allocation | asignación de capital | |
| margin | margen | |
| profit | utilidad | not *beneficio* (Spain) |
| revenue | ingresos | |
| payout | pago / ciclo de pagos de Amazon | |
| ad spend | inversión publicitaria | |
| bid | puja | |
| keyword | palabra clave | |
| search term | término de búsqueda | added 2026-09-11; what the shopper typed, as against the keyword you bid on |
| impressions | impresiones | added 2026-09-11 |
| negative keyword | palabra clave negativa | added 2026-09-11; the setting that stops a search term, not the decision to stop it |
| branded / generic campaign | campaña de marca / de palabras clave genéricas | |
| conversion rate | tasa de conversión | |
| organic ranking | posicionamiento orgánico | |
| incrementality | incrementalidad | |
| dashboard | panel | *dashboard* only where the English is talking about the software genre |
| spreadsheet | hoja de cálculo | |
| forecasting | pronóstico / pronosticar | |
| launch | lanzamiento | |
| efficiency metric / decision metric | métrica de eficiencia / métrica de decisión | the spine of the ACOS article |

---

## 4. Site chrome

| English | Spanish |
|---|---|
| Knowledge Hub | Centro de Conocimiento |
| Join the Wait List | Únete a la lista de espera |
| Log in | Iniciar sesión |
| Product / Solutions / Pricing / Resources / Company | Producto / Soluciones / Precios / Recursos / Empresa |
| Beginners / Experienced sellers / Agencies | Principiantes / Vendedores con experiencia / Agencias |
| About / Contact / Privacy / Terms | Nosotros / Contacto / Privacidad / Términos |
| Advertising & PPC / Financials / Inventory | Publicidad y PPC / Finanzas / Inventario |
| Product Research / Simulations / Sales | Investigación de productos / Simulaciones / Ventas |
| Data & Sync / Security / AI Assistant — soon | Datos y sincronización / Seguridad / Asistente de IA — pronto |
| Skip to content | Saltar al contenido |
| min read | min de lectura |
| The fix / What to do *(callout label)* | Qué hacer |
| Podcast episode *(player label)* | Episodio de podcast · audio en inglés *(the audio stays in English; Leon, 2026-09-11)* |
| Step 01 | Paso 01 |
| What's in this guide / piece | Qué encontrarás en esta guía / en este artículo |
| Final thoughts | Para cerrar |
| Frequently asked | Preguntas frecuentes |
| Figures from this article's worked examples, not an industry survey. | Cifras de los ejemplos trabajados de este artículo, no de un estudio de mercado. |

**Note:** the Spanish nav labels link to pages that are still in English
(`/product.html`, `/solutions.html`, `/about.html`). That is normal for a
phased localisation, but it is a promise the site is not yet keeping. Say the
word and those five pages go in the next batch, ahead of the remaining
articles.

---

## 5. Slugs used in the pilot

| English | Spanish |
|---|---|
| `/articles/reorder-point.html` | `/es/articulos/punto-de-reorden.html` |
| `/articles/stop-optimizing-acos.html` | `/es/articulos/deja-de-optimizar-el-acos.html` |
| `/articles/first-product-succeeds-cash.html` | `/es/articulos/y-si-tu-primer-producto-funciona.html` |

Slugs are the Spanish title, lowercased, accents stripped, hyphenated. No
`el/la/los/las/de` are dropped — `y-si-tu-primer-producto-funciona` reads as a
sentence, which is what the English slugs do too.

---

## 6. Fixed callout labels

`gate.py` refuses a callout, rail or eyebrow label that is not one of these
strings. Until 2026-09-11 there was no such table for Spanish, and
`gate.load_labels("es")` looked for `GLOSSARIO-ES.md` with two S while this file
is `GLOSARIO-ES.md` with one — so the check found nothing and **passed vacuously
on all 51 Spanish pages**. Both are fixed in the same commit.

This table was **MEASURED, not translated**. Every row was read off the 51
shipped Spanish articles and paired with the English label its twin carries in
the same position, the same way the Portuguese table was built. The counts are
how many times the Spanish string occurs across every label class gate.py
checks (`fixbox-k`, `rail-k`, `label`, `lab`, `eyebrow`). Values are written with
raw accented characters, as the Portuguese table is: gate compares them against
the page's label after unescaping, so an entity here could never match.

A translated label that is not in this table is not wrong; it is unmeasured, and
it needs a decision.

<!-- FIXED-LABELS:START -->
| English | Spanish | Status |
|---|---|---|
| What to do | Qué hacer | measured 2026-09-11 — 50 uses of the Spanish, 49 of them paired with this English; the most settled label on the site |
| The fix | Qué hacer | measured 2026-09-11 — the English label was "The fix" before it became "What to do"; both render the same Spanish |
| What to do about it | Qué hacer | measured 2026-09-11 — 1 of the 50 "Qué hacer" labels pairs with this longer English, which still shortens to the same Spanish |
| Related reading | Lecturas relacionadas | measured 2026-09-11 — 24 uses. The SINGULAR "Lectura relacionada" is also correct and has 11 uses: it is used when exactly one article is linked. A number agreement, not a conflict. |
| The reframe | El replanteo | measured 2026-09-11 — 9 uses. "El replanteamiento" has 2 and is the same word lengthened; settle on the shorter. |
| The distinction | La distinción | measured 2026-09-11 — 8 uses |
| The point | El punto | measured 2026-09-11 — 8 uses |
| The shift | El cambio | measured 2026-09-11 — 8 uses |
| The trap | La trampa | measured 2026-09-11 — 7 uses |
| The usual question | La pregunta de siempre | measured 2026-09-11 — 7 uses |
| The question | La pregunta | measured 2026-09-11 — 7 uses |
| The discipline | La disciplina | measured 2026-09-11 — 7 uses |
| The difference | La diferencia | measured 2026-09-11 — 6 uses |
| The principle | El principio | measured 2026-09-11 — 6 uses |
| The parallel | El paralelo | measured 2026-09-11 — 5 uses |
| The test | La prueba | measured 2026-09-11 — 5 uses |
| The diagnosis | El diagnóstico | measured 2026-09-11 — 5 uses |
| The asymmetry | La asimetría | measured 2026-09-11 — 5 uses |
| The rule | La regla | measured 2026-09-11 — 5 uses |
| The gap | La brecha | measured 2026-09-11 — 4 uses. "El hueco" has 1; brecha is the measured majority and the word the inventory articles already use. |
| The mismatch | El desajuste | measured 2026-09-11 — 4 uses |
| The blind spot | El punto ciego | measured 2026-09-11 — 4 uses |
| The premise | La premisa | measured 2026-09-11 — 4 uses |
| The better question | La mejor pregunta | measured 2026-09-11 — 5 uses of the Spanish, 4 of them paired with this English; the 5th pairs with "The better one", exactly as the Portuguese table records |
| The consequence | La consecuencia | measured 2026-09-11 — 3 uses |
| The problem | El problema | measured 2026-09-11 — 3 uses |
| The through-line | El hilo conductor | measured 2026-09-11 — 3 uses |
| Worked example | Ejemplo práctico | **proposed 2026-09-11, NOT approved** — zero precedent in the Spanish corpus: "Worked example" occurs in only two English articles and neither had a Spanish twin. Portuguese has "Exemplo prático" approved (PT §6). Needs Leon's yes before it is fixed. |
| PPC & Advertising | Publicidad y PPC | measured 2026-09-11 — 12 eyebrows; matches label_es in data/resources.json |
| Product Research | Investigación de productos | measured 2026-09-11 — 11 eyebrows |
| Growth Playbook | Manual de crecimiento | measured 2026-09-11 — 9 eyebrows |
| Inventory Planning | Planificación de inventario | measured 2026-09-11 — 7 eyebrows |
| Profit & Finances | Utilidad y finanzas | measured 2026-09-11 — 6 eyebrows |
| Tools & Tutorials | Herramientas y tutoriales | measured 2026-09-11 — 1 eyebrow |
| Podcast episode | Episodio de podcast · audio en inglés | measured 2026-09-11 — 3 uses; the three podcast pages play the English audio and the player says so (Leon, 2026-09-11) |
| `re:^Step (\d+)$` | `Paso ` | §4 |
| `re:^(\d+) min read$` | ` min de lectura` | §4 |
| `re:^What’s in this guide$` | `Qué encontrarás en esta guía` | §4 |
| `re:^What’s in this piece$` | `Qué encontrarás en este artículo` | §4 |
| `re:^Final thoughts$` | `Para cerrar` | §4 |
| `re:^Frequently asked$` | `Preguntas frecuentes` | §4 |
| `re:^Figures from this article’s worked examples, not an industry survey\.$` | `Cifras de los ejemplos trabajados de este artículo, no de un estudio de mercado.` | §4 |
<!-- FIXED-LABELS:END -->

### Not in this table on purpose

The corpus holds roughly 340 further labels ("La aritmética silenciosa", "El
impuesto que nadie declara") that occur once each, in one article, as part of
that article's own argument. They are prose, not chrome, and fixing them would
turn a writer's sentence into a lookup. Only labels that repeat belong here.
