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

---

## 2. Terms kept in English on purpose

These are how sellers actually talk. Translating them would make the articles
read as though written by someone who has never used Seller Central.

`ACOS` · `TACOS` · `ROAS` · `CPC` · `PPC` · `FBA` · `SKU` · `ASIN` ·
`Buy Box` · `listing` · `Seller Central` · `Ledger` (the AmazeBase module name)

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
| The fix *(callout label)* | Qué hacer |
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
