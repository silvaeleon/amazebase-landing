# Portuguese glossary — AmazeBase Knowledge Hub

**What is approved and what is not.** The register, §1 (the six decisions) and
§5 (the slug rule and slugs) were approved by Leon on 2026-09-10. §2, §3 and §4
were approved with the pilot on 2026-09-11, with the two conditions written
into §3 (*faturamento*, *landed cost*). §6 and §7 were reviewed by Leon on 2026-09-11; rows that follow from
a ruling rather than being ruled on directly say so. Everything here is applied identically to all 51 articles.

Register: **Brazilian Portuguese, *você***, friendly and professional. Verbs in
the *você* form (*você pode, confira, calcule, revise*), which is what the
English does in the second person. Never *tu*, never *o senhor*, never *vós*,
and no European-Portuguese forms (*equipa, ecrã, telemóvel, facto, registo,
utilizador, contacto*, *estou a fazer*).

URLs: `/pt/` · hub `/pt/recursos.html` · articles `/pt/artigos/` · chrome
`/pt/produto.html`, `solucoes`, `sobre`, `contato`. Tagged plain **`pt`**
(`<html lang="pt">`, `hreflang="pt"`) so a reader in Portugal gets this version
rather than falling through to English. `og:locale` is `pt_BR`, because that is
the variety it is written in.

---

## 1. The six decisions

**Read this table against `GLOSARIO-ES.md` before "harmonising" anything.**
Four of these six — **rows 2, 3, 4 and 5** — deliberately differ from the
Spanish rulings; row 6 matches Spanish, and row 1 matches because it is shared. They differ
because Portuguese is not Spanish, not because one glossary is out of date. A
later pass that sees `25 %` in one file and `25%` in the other and makes them
agree is making one of them wrong.

| # | Decision | Portuguese | Alternative considered | Against Spanish |
|---|---|---|---|---|
| 1 | **Numbers** | US formatting for every number, money and counts: `$30,000`, `$8.00`, `1,200 unidades`. `$`, never `US$`. | Brazilian `$30.000`, `$8,00`. | **A site-wide convention, not a Portuguese row** — see `tools/i18n/README.md`, *Shared conventions*, including the accepted cost for unit counts. Matches Spanish because every language inherits it. |
| 2 | **Percentages and quotes** | `25%`, no space. Curly double quotes `“…”` (`&ldquo;…&rdquo;`), single `‘…’` inside them. | `25 %` with a space; angle quotes `«…»`. | **DELIBERATE DIVERGENCE.** Spanish ships `25 %` and `«…»`. Both are Spanish (RAE) conventions; Brazilian usage writes `25%` and uses curly quotes, and angle quotes read as foreign there. |
| 3 | **"reorder point"** | **ponto de reposição** | *ponto de pedido*, the textbook term. | **DELIBERATE DIVERGENCE.** Spanish chose *punto de reorden*. In Portuguese the textbook *ponto de pedido* collides with *pedido* meaning a customer order in Seller Central, and *reposição* pairs with *repor*, the verb for restocking. |
| 4 | **"lead time"** | **lead time**, kept in English (masculine: *o lead time*; *lead time total* for the whole chain). | *prazo de reposição*. | **DELIBERATE DIVERGENCE.** Spanish translated it, *tiempo de reposición*. Brazilian logistics says *lead time* as-is, and *prazo de reposição* next to *ponto de reposição* in one formula is a tongue-twister and easy to misread. |
| 5 | **"stockout"** | **ruptura de estoque**; *ficar sem estoque* as the verb. | *falta de estoque*, plainer. | **DELIBERATE DIVERGENCE.** Spanish avoided *ruptura de stock* because it is the Spain term and chose LatAm *quiebre de stock*. In Brazil *ruptura* is the standard retail trade term. Same root word, opposite regional status. |
| 6 | **"listing"** | **listing**, kept in English. *Página do produto* where the English means the page itself. | *anúncio*, which is what Amazon Brazil calls it. | **Matches Spanish.** *Anúncio* also means "ad", and the PPC articles put both in one sentence — "the ad sends traffic to the listing" — which stops meaning anything if both words are *anúncio*. |

---

## 2. Terms kept in English on purpose

`ACOS` `ACoS` `TACOS` `TACoS` `ROAS` `CPC` `PPC` `FBA` `AWD` `3PL` `SKU`
`ASIN` `TAM` `ROI` `LTV` `P&L` `Buy Box` `listing` `lead time` `bulksheet` `trade-off`
`flywheel` `Seller Central` `Campaign Manager` `Amazon` and the Amazon ad
products `Sponsored Products / Brands / Display`. AmazeBase module names stay
exactly as they appear (`Ledger`).

"Advertising Cost of Sales" appears once in the English, in the lead of the
ACOS article, in **plain text**. `GLOSARIO-ES.md` says it is italic "same as the
English original does"; measured on 2026-09-10, it is not, and the Spanish page
is the only one on the site that wraps it in `<em>`. Keep it plain: the
Portuguese adds no emphasis the English does not have.

---

## 3. The working vocabulary

| English | Portuguese | Note |
|---|---|---|
| Amazon seller | vendedor da Amazon | |
| inventory | estoque | never *inventário* for stock on hand |
| stockout | ruptura de estoque / ficar sem estoque | decision 5 |
| overstock | excesso de estoque | |
| available / reserved / inbound inventory | estoque disponível / reservado / em trânsito | |
| days of supply | dias de cobertura | |
| weeks of cover | semanas de cobertura | |
| sales velocity | velocidade de vendas | |
| average daily sales | vendas médias diárias | |
| safety stock | estoque de segurança | |
| reorder point | ponto de reposição | decision 3 |
| lead time | lead time | decision 4 |
| purchase order | pedido de compra | the fixed phrase is unambiguous; bare *pedido* is not |
| to reorder / restock | repor | *repor o produto que vende* |
| supplier | fornecedor | |
| manufacturing | fabricação | |
| supplier preparation | preparação do fornecedor | |
| ocean freight | frete marítimo | |
| customs | alfândega | |
| inland transport | transporte terrestre | |
| Amazon receiving | recebimento na Amazon | |
| landed cost | **imported goods:** custo total de importação · **sourced domestically, or not said:** custo total por unidade | *(landed cost)* in brackets on first use. **Scoped:** *importação* is only right when the article's product is imported (overseas supplier, freight, customs). A domestic product has no importação; use *custo total por unidade* — everything paid to get one unit into Amazon's warehouse. |
| cash flow | fluxo de caixa | |
| cash cycle | ciclo de caixa | |
| cash floor | piso de caixa | the author's coinage in English too |
| working capital | capital de giro | the Brazilian term; not *capital de trabalho* |
| capital allocation | alocação de capital | |
| customer lifetime value | **LTV** — *valor vitalício do cliente (LTV)* on first use in an article, *LTV* after | decided 2026-09-11 on market usage (Brazilian sellers say LTV; *valor vitalício do cliente* is the established written form), NOT on which form the translators used most |
| margin / profit / revenue | margem / lucro / faturamento | **Condition:** *faturamento* is GROSS revenue. Wherever the English means revenue after returns or refunds — "net revenue", "net sales", "after returns" — it is **receita líquida**, never *faturamento*. Check each occurrence; do not map the word globally. The gate refuses *faturamento* in a text node whose English says net revenue. *Receita* where the English is doing accounting. |
| break-even | ponto de equilíbrio | |
| payout | repasse | what Brazilian marketplaces call it |
| ad spend | gasto com anúncios | neutral, as *spend* is; not *investimento* |
| bid | lance | Amazon Ads Brazil's own word |
| keyword / search term | palavra-chave / termo de pesquisa | |
| placement | posicionamento | |
| organic ranking | ranqueamento orgânico | keeps it apart from *posicionamento* |
| dayparting | programação por horário | |
| branded campaign | campanha de marca | |
| conversion rate | taxa de conversão | |
| incrementality | incrementalidade | |
| to negate (a keyword) | negativar | |
| dashboard | painel | *dashboard* only for the software genre |
| spreadsheet | planilha | |
| forecasting | previsão / prever | |
| launch | lançamento | |
| portfolio | portfólio | |
| momentum | tração / impulso | by sense |
| compounding | efeito composto | |
| moat | diferencial | changed 2026-09-11: *vantagem competitiva* is reserved for "competitive advantage" (33 uses in the English); the two are different live terms |
| optionality | opcionalidade | |
| trade-off | trade-off | kept in English, as the label *O trade-off*; *A contrapartida* is the Portuguese on record |
| warehouse | armazém | |
| storage fees | taxas de armazenagem | |
| shrinkage | perdas | |
| overheads | despesas gerais | |
| settlement | liquidação | |

### Worked sums in `<pre>`

A `<pre>` is split by what it IS, not by its tag. **Literal code** — anything a
reader would copy and run or paste: commands, JSON, config, formulas in a
programming syntax — is never translated and stays byte-identical. **Worked
sums in prose** that sit in `<pre>` for alignment are translated: the words
change; every digit, operator and currency symbol stays in place. Measured
2026-09-11: all 19 `<pre>` blocks in the corpus (6 articles) are worked sums;
none is code. The gate compares the ordered numbers and operators of each
`<pre>` with the English and refuses any difference, and refuses a block whose
columns no longer line up where the English lines them up (9 of the 19 align).

### A number and its unit do not split

A non-breaking space joins a number to its unit word — `6&nbsp;meses`,
`4&nbsp;semanas`, `1,200&nbsp;unidades`, `5&nbsp;min` — so a line can never
wrap between them. `normalise_pt.py` applies it mechanically to every
translation; translators may type a plain space.

---

## 4. Site chrome

| English | Portuguese |
|---|---|
| Knowledge Hub | Central de Conhecimento |
| Join the Wait List | Entre na lista de espera |
| Log in | Entrar |
| Product / Solutions / Pricing / Resources / Company | Produto / Soluções / Preços / Recursos / Empresa |
| Beginners / Experienced sellers / Agencies | Iniciantes / Vendedores experientes / Agências |
| About / Contact / Privacy / Terms | Sobre / Contato / Privacidade / Termos |
| Advertising & PPC / Financials / Inventory | Publicidade e PPC / Finanças / Estoque |
| Product Research / Simulations / Sales | Pesquisa de produtos / Simulações / Vendas |
| Data & Sync / Security / AI Assistant — soon | Dados e sincronização / Segurança / Assistente de IA — em breve |
| The operating system for Amazon sellers. Everything connected, everything in sync. | O sistema operacional para vendedores da Amazon. Tudo conectado, tudo sincronizado. |
| All rights reserved. | Todos os direitos reservados. |
| Skip to content | Pular para o conteúdo |
| Primary *(nav label)* / AmazeBase home / Open menu | Principal / Página inicial da AmazeBase / Abrir menu |
| Home *(breadcrumb)* | Início |
| min read | min de leitura |
| The fix *(callout label)* | O que fazer |
| Step 01 | Passo 01 |
| What's in this guide / piece | O que você vai encontrar neste guia / neste artigo |
| Final thoughts | Para fechar |
| Frequently asked | Perguntas frequentes |
| Worked example | Exemplo prático |
| Key figures from this article *(rail label)* | Números-chave deste artigo |
| Figures from this article's worked examples, not an industry survey. | Números dos exemplos deste artigo, não de uma pesquisa de mercado. |

Category eyebrows lose the ampersand: *PPC & Advertising* → *Publicidade e
PPC*, *Profit & Finances* → *Lucro e finanças*, *Inventory* → *Estoque*,
*Inventory Planning* → *Planejamento de estoque*, *Growth Playbook* → *Guia de
crescimento*, *Product Research* → *Pesquisa de produtos*, *Tools & Tutorials*
→ *Ferramentas e tutoriais*.

Pricing, the brand mark, Privacy and Terms point at the English pages — there
is no Portuguese homepage, pricing, privacy or terms, by decision.

---

## 5. Slugs

The Portuguese title, lowercased, accents stripped (`ç`→`c`, `ã`→`a`,
`é`→`e`), hyphenated, taken from the title's most distinctive clause.

**At most 50 characters AND at most 7 words. The build refuses a slug that
breaks either cap; it never truncates one.** Both caps, because each alone
fails in the other direction: the Spanish rule knew only words and let a
56-character slug through, and a character-only rule would pass an
eleven-word slug of short words. A silently shortened slug is a broken URL
that still builds, so the answer to a long slug is a human choosing a shorter
clause.

Accent-stripping makes *é* (is) and *e* (and) the same letter, so
`publicidade-e-decisao-de-estoque` reads "advertising AND inventory decision"
where the title says "IS". That is fine: a slug is an identifier, not a
sentence, and Spanish has the same property. **Do not "fix" it by putting
accents back into filenames.**

| English | Portuguese | chars | words |
|---|---|---|---|
| `reorder-point` | `ponto-de-reposicao` | 18 | 3 |
| `stop-optimizing-acos` | `pare-de-otimizar-o-acos` | 23 | 5 |
| `first-product-succeeds-cash` | `e-se-seu-primeiro-produto-der-certo` | 35 | 7 |
| `advertising-is-inventory` | `publicidade-e-decisao-de-estoque` | 32 | 5 |
| `risk-research` | `pesquisa-de-produto-e-pesquisa-de-risco` | 39 | 7 |

The first three are the pilot. The last two are the two longest Spanish slugs,
kept here as the stress cases for the caps.

---

## 6. Fixed labels

These are exact strings, enforced. `gate.py` reads this table: when an English
callout label (classes `fixbox-k`, `rail-k`, `label`, `lab`, `eyebrow`,
`player-kind`) matches a row, the Portuguese must be that string exactly, and
`normalise_pt.py` writes it in. Rows starting `re:` are patterns that apply
anywhere in the article. To change a label: edit its row here, then run
normalise and rebuild; every article follows.

Rows were chosen from the English corpus by frequency: every label that recurs
in two or more articles, plus Leon's nine. Context-dependent words (*Assumed*,
*Scheduled*, *Format* in a table) are deliberately left out: their gender
agreement in Portuguese depends on what they label.

<!-- FIXED-LABELS:START -->
| English | Portuguese | Status |
|---|---|---|
| The parallel | O paralelo | approved 2026-09-11 |
| The real issue | O verdadeiro problema | approved 2026-09-11 |
| The point | O que importa | approved 2026-09-11 |
| The blind spot | O ponto cego | approved 2026-09-11 |
| The gap | A lacuna | approved 2026-09-11 |
| The reframe | Outro ângulo | approved 2026-09-11 |
| The question | A pergunta | approved 2026-09-11 |
| The risk | O risco | approved 2026-09-11 |
| Ask these instead | Pergunte assim | approved 2026-09-11 — the review first supplied "Try this instead → Faça assim", a label the corpus does not contain; "Faça" (do) would have replaced "ask". Kept as a record that a reviewer can invent a source string. |
| The fix | O que fazer | approved (§4) |
| Worked example | Exemplo prático | approved (§4) |
| PPC & Advertising | Publicidade e PPC | approved (§4) |
| Product Research | Pesquisa de produtos | approved (§4) |
| Growth Playbook | Guia de crescimento | approved (§4) |
| Inventory Planning | Planejamento de estoque | approved (§4) |
| Profit & Finances | Lucro e finanças | approved (§4) |
| Inventory & Cash Flow | Estoque e fluxo de caixa | approved (§4) |
| Tools & Tutorials | Ferramentas e tutoriais | approved (§4) |
| `re:^Step (\d+)$` | `Passo \1` | approved (§4) |
| `re:^(\d+) min read$` | `\1 min de leitura` | approved (§4) |
| `re:^What’s in this guide$` | `O que você vai encontrar neste guia` | approved (§4) |
| `re:^What’s in this piece$` | `O que você vai encontrar neste artigo` | approved (§4) |
| `re:^Final thoughts$` | `Para fechar` | approved (§4) |
| `re:^Frequently asked$` | `Perguntas frequentes` | approved (§4) |
| `re:^Figures from this article’s worked examples, not an industry survey\.$` | `Números dos exemplos deste artigo, não de uma pesquisa de mercado.` | approved (§4) |
| Related reading | Leitura relacionada | approved 2026-09-11 |
| The shift | A virada | approved 2026-09-11 |
| The distinction | A distinção | approved 2026-09-11 |
| The diagnosis | O diagnóstico | approved 2026-09-11 |
| The difference | A diferença | approved 2026-09-11 |
| The principle | O princípio | approved 2026-09-11 |
| The discipline | A disciplina | approved 2026-09-11 |
| The consequence | A consequência | approved 2026-09-11 |
| The rule | A regra | approved 2026-09-11 |
| The standard | O critério | approved 2026-09-11 — was O padrão until 2026-09-11; changed so it no longer collides with The pattern |
| The pattern | O padrão | approved 2026-09-11 — found in the bulk run |
| The test | O teste | approved 2026-09-11 |
| The better test | Um teste melhor | approved 2026-09-11 — O teste melhor reads as a botched superlative |
| The better question | Uma pergunta melhor | extends the ruling on The better test (same construction); 5 uses |
| The better one | Uma pergunta melhor | extends the same ruling; the one use pairs with The usual question |
| The through-line | O fio condutor | approved 2026-09-11 |
| Why | O porquê | approved 2026-09-11 — the noun; cannot be mis-accented, matches every other row's shape |
| The asymmetry | A assimetria | approved 2026-09-11 |
| The balance | O equilíbrio | approved 2026-09-11 |
| The limit | O limite | approved 2026-09-11 |
| The objective | O objetivo | approved 2026-09-11 |
| The premise | A premissa | approved 2026-09-11 |
| The problem | O problema | approved 2026-09-11 |
| The trade | O trade-off | approved 2026-09-11 — every use means what you give up; A troca is a swap. Alternative on record: A contrapartida |
| The trade nobody votes on | O trade-off que ninguém põe em votação | follows The trade |
| The trap | A armadilha | approved 2026-09-11 |
| The uncomfortable part | A parte incômoda | approved 2026-09-11 |
| The mismatch | O descompasso | approved 2026-09-11 |
| The claim | A afirmação | approved 2026-09-11 |
| The confusion | A confusão | approved 2026-09-11 |
| The moat | O diferencial | approved 2026-09-11 — NOT A vantagem competitiva: "competitive advantage" is its own live term (33 uses) and keeps that phrase |
| What to prize | O que valorizar | approved 2026-09-11 |
| The usual question | A pergunta de sempre | approved 2026-09-11 |
| Traditional research asks | A pesquisa tradicional pergunta | approved 2026-09-11 |
| The business question | A pergunta de negócio | approved 2026-09-11 |
| Podcast episode | Episódio de podcast · áudio em inglês | approved 2026-09-11 — Leon: the three podcast pages play the English audio, and the player says so; a Portuguese page must not play English silently |
| The long tail | A cauda longa | approved 2026-09-11 — a distribution, not time (O longo prazo was wrong) |
| Scheduled | Programado | approved 2026-09-11 — bulk run had Agendado and Programado; Programado matches its series Comprometido / Programado / A vencer |
| Operating Systems | Sistemas operacionais | approved 2026-09-11 — found in the bulk run |
| `re:^Figures from this article’s own worked example, not an industry survey\.$` | `Números do próprio exemplo deste artigo, não de uma pesquisa de mercado.` | approved 2026-09-11 — 7 articles; the approved pilot's wording, parallel to the approved plural |
| `re:^Examples from this article, not an industry survey\.$` | `Exemplos deste artigo, não de uma pesquisa de mercado.` | approved 2026-09-11 — found in the bulk run |
<!-- FIXED-LABELS:END -->

---

## 7. Settled vocabulary

Where parallel translators produced more than one Portuguese form for the same
English term, the forms on the left are replaced by the one on the right —
`normalise_pt.py` rewrites them, and `gate.py` refuses them from then on, so a
re-translation cannot bring a variant back. Measured across all 51 articles on
2026-09-11. Matching is case-insensitive; a capital at the start is kept.

<!-- VOCAB-SETTLE:START -->
| Variant | Settled form | Why |
|---|---|---|
| falta de estoque | ruptura de estoque | decision 5; 2 stray uses against 61 of ruptura |
| valor do cliente ao longo do tempo | valor vitalício do cliente | customer lifetime value: settled 2026-09-11 on market usage, not on the majority count (§3); first use per article carries (LTV), later uses are LTV |
| valor do tempo de vida do cliente | valor vitalício do cliente | as above |
| valor do ciclo de vida do cliente | valor vitalício do cliente | as above |
| capital de trabalho | capital de giro | §3; 0 uses today, guarded |
| ponto de pedido | ponto de reposição | decision 3; 0 uses today, guarded |
<!-- VOCAB-SETTLE:END -->
