title: When Should You Negate a Keyword?
slug: when-to-negate-a-keyword
summary: There are two different reasons to stop spending on a search term, and treating them as one reason causes two opposite mistakes.
categories: PPC & Advertising
hero_alt: A search term judged first on relevance, then on whether enough clicks exist
reading_time: 7

A negative keyword tells Amazon to stop showing your ad for a particular search term. Sellers call this negating a keyword, and the verdict Negate means exactly that.

Beginners ask how bad a search term has to be before they negate it. The question hides a problem: there are two reasons to stop spending on a search term, and they need different evidence.

The first is relevance. The term describes something you do not sell, so no number of clicks will make it convert. Block it today.

The second is performance. The term is genuinely your product but has not produced sales. That is a question about evidence, and it needs enough clicks before the silence means anything.

Collapse the two and you make both mistakes at once: you wait on terms that were never going to work, and you cut relevant terms long before you had a result.

## What's in this guide
- Where do the search term numbers come from?
- How do I decide whether a search term is relevant to my product?
- How many clicks do I need before zero sales means something?
- Should I negate my main keywords when their ACOS is high?
- Should I negate, pause, or lower the bid?
- Should the negative go on the ad group or the campaign?
- What is the difference between negative exact and negative phrase?

## Where do the search term numbers come from?

Every decision below rests on one report: the Sponsored Products search term report, in the reporting section of Campaign Manager. For a date range you choose, it lists each shopper search your ads appeared for, with its impressions, clicks, spend and orders.

It holds only ad-attributed activity: clicks your ads received, and orders Amazon credits to one of those clicks within the attribution window, which is seven days after the click for sellers. Organic sales are not in it.

Orders are counted against the day of the click, not the day of the purchase, so the most recent days always look worse than they are. Let them settle for a few days before judging them.

[[The trap]]
Do not use unit session percentage from your Business Reports as the conversion rate behind an advertising decision. Its denominator is all sessions, organic visits included, and ad clicks usually convert worse. The number reads high, your click threshold comes out short, and you cut terms early — the exact mistake you were trying to avoid. Use the ad conversion rate instead: ad-attributed orders divided by clicks, from Campaign Manager.

## How do I decide whether a search term is relevant to my product?

Relevance is a yes or no question, and you can answer it with no performance data.

[[The test]]
Read the search term and ask: if a shopper typed this and my product was the first result, would that shopper have found what they wanted? If the honest answer is no, the term is irrelevant. Negate it now. Clicks do not enter into it.

Irrelevant terms are usually obvious: a different product category, a size or color you do not offer, a brand that is not yours, an accessory rather than the product itself. A seller of a digital kitchen scale will find "baby scale" in the report.

This is the only case where acting quickly costs you nothing.

[[FIGURE: Two gates before a negative keyword, relevance first, then enough clicks to judge]]

## How many clicks do I need before zero sales means something?

Once a term passes the relevance test, "no sales yet" is a sample size question, not a verdict. A term with few clicks and no orders is not failing. It is untested.

[[The rule]]
Assume an ad conversion rate of 10%, meaning one order for every ten clicks. At that rate, a perfectly normal search term still produces zero orders after 22 clicks less than 10% of the time. Below roughly 20 clicks you usually have no result at all, only a short run of misses, which is what nine clicks in ten are even on a term that works.

[[The risk]]
The 10% is a planning assumption, not your number: your real ad conversion rate comes from Campaign Manager, and in the first weeks you will not have enough ad-attributed orders to compute it. The assumption errs in the dangerous direction. If your true rate is below 10% — common for a new listing with few reviews — 22 clicks is not enough, and cutting there cuts healthy terms. Halve the rate and you roughly double the clicks needed: at 5%, about 45. When in doubt, wait longer on a relevant term, never shorter.

## Should I negate my main keywords when their ACOS is high?

No. This is the most expensive mistake a beginner makes with negative keywords, because a high ACOS on a high-volume term looks exactly like a problem a negative keyword would solve.

[[The diagnosis]]
If a search term is central to what you sell, a poor result is a conversion problem, not a targeting problem. The traffic is correct; something after the click is failing — price, main image, reviews, or a listing that does not make the benefit obvious. A negative keyword fixes none of those. It removes the sales you were still winning and the organic ranking they were feeding.

[[Worked example]]
A seller of digital kitchen scales runs a 30-day search term report. The first term, "digital kitchen scale", is precisely the product:

Clicks in the date range | 240
Spend | $180.00
Ad-attributed orders | 6
Ad sales from those orders | $144.00
ACOS (spend divided by ad sales) | 125%
Ad conversion rate (orders divided by clicks) | 2.5%
Orders expected at a 10% ad conversion rate (240 × 10%) | 24

The second term, "baby scale", is a product this seller does not offer:

Clicks in the date range | 14
Spend | $10.50
Ad-attributed orders | 0

The instinct is to negate the first term and wait on the second. Both are backwards. The first is relevant and past 22 clicks, so its number is real: 6 orders where 24 were expected is a 2.5% ad conversion rate, a listing problem, and negating it would remove the six orders a month you still get. The second fails the relevance test, so its click count does not matter.

## Should I negate, pause, or lower the bid?

These three actions get used interchangeably, and they are not interchangeable.

| Action | Effect on the term | Its past data | How far it reaches |
|---|---|---|---|
| Lower the bid | Still shows, at a price you choose; usually fewer clicks | Kept, still accumulating | The keyword or target you changed |
| Pause the keyword or target | Stops showing; can be set active again later | Kept, stops accumulating | That keyword or target, in that ad group |
| Add a negative keyword | Blocked from matching your ad until you remove it | Kept, stops accumulating | The ad group or campaign you added it to |

Choose by the reason, not by the size of the number.

[[What to do]]
1. Lower the bid when the term converts, but not at the price you are paying. This keeps a relevant, high-ACOS term alive at a cost you can afford.
2. Pause when you want the term stopped for now but might want it back.
3. Negate when you never want to pay for that search term again, which means it failed the relevance test.

Pausing stops one keyword, not the search term, which can still reach you through another keyword or campaign. Only a negative keyword blocks the search term itself.

## Should the negative go on the ad group or the campaign?

A negative keyword added at ad group level applies to that ad group only. Added at campaign level, it applies to every ad group in that campaign.

Neither reaches any other campaign. If you block a term in your automatic campaign and it still triggers your manual campaign, you have not blocked it: each campaign carries its own list.

[[The limit]]
A negative blocks the term at exactly the level you added it, and nowhere else. To stop a search term across your account, add it in every campaign that can match it. The search term report tells you which campaign produced the clicks.

## What is the difference between negative exact and negative phrase?

One match type blocks a single search term; the other blocks a whole family of them.

- Negative exact blocks only that search term itself, plus close variations such as plurals. "Kitchen scale" as a negative exact does not block "digital kitchen scale", which is a different search term.
- Negative phrase blocks any search term containing those words in that order, plus close variations. "Kitchen scale" as a negative phrase blocks "digital kitchen scale", "kitchen scale for coffee", and everything else with that sequence inside it.

[[The risk]]
Negative phrase is how sellers accidentally block their own main terms. A phrase negative on a short, central word removes every longer search term built on top of it, including the ones producing your sales, and it shows up as a quiet drop in impressions rather than an error. Use negative exact unless you mean to remove a whole family of terms, such as an unrelated brand name.

## Frequently asked

**Can I undo a negative keyword?**
You remove one by archiving it in Campaign Manager, and archiving cannot be reversed. You can add the same word again later as a new negative keyword, but the original entry does not come back.

**What about dozens of search terms with only one or two clicks each?**
Individually they will never accumulate enough clicks to judge, but together they spend real money. Negate the ones that are not your product, because relevance needs no clicks. For the rest, treat their total as a price problem and lower the bid on the keyword generating them.

## Final thoughts

Ask the relevance question first and the evidence question second, and most negative keyword decisions answer themselves. Terms that describe a product you do not sell go immediately, whatever their click count. Terms that describe your product stay until you have enough clicks to know something.

The costliest error is the quiet one: negating a main keyword because its ACOS looked frightening. That term was the sale you were trying to win. Lower the bid, fix what happens after the click, and keep it running.

Figures from this article's worked examples, not an industry survey.

## Sources

- Clicks, spend and orders for an individual search term — Campaign Manager > reporting section > Sponsored Products search term report > columns "Customer Search Term", "Clicks", "Spend", and the ad-attributed orders column — covers ad-attributed activity only, for the chosen date range, with orders counted against the click date within the attribution window — matches the claim: yes.
- Exact on-screen label of the ad-attributed orders column — historically "7 Day Total Orders (#)" in the downloaded file for sellers, shown as an orders column in the current console — covers ad-attributed orders within the seven-day seller attribution window — matches the claim: uncertain because Amazon has renamed reporting columns more than once; the body therefore names the report and the population but prints no exact orders column label. Verify against a live account before shipping.
- Menu path to the search term report — Campaign Manager reporting section, report type "Search term" — covers Sponsored Products campaigns — matches the claim: uncertain because the console's navigation labels ("Measurement and reporting", "Sponsored ads reports") have changed across versions and by marketplace; the body deliberately says "the reporting section of Campaign Manager" rather than a precise menu chain.
- Sponsored Products attribution window of seven days after the click for sellers — Amazon Ads reporting definitions; vendors use a 14-day window — covers ad-attributed orders only — matches the claim: yes, and the article states the seller figure explicitly.
- Recent days still filling in — reporting data appears within roughly 48 hours and continues to settle for a few days as orders are attributed back to the click date — matches the claim: yes, and the article avoids naming a precise settling period.
- Ad conversion rate (ad-attributed orders divided by clicks) — Campaign Manager — covers ad traffic only — matches the claim: yes.
- Unit session percentage — Seller Central > Business Reports — covers units ordered divided by ALL sessions, organic included — matches the claim: no; it appears in the article only as a warning never to use it for an advertising decision.
- Negative exact blocks the search term itself and close variations; negative phrase blocks any search term containing that sequence of words, plus close variations — Amazon Ads targeting guidance for Sponsored Products — matches the claim: yes.
- Negative keywords apply at ad group level or campaign level, and do not reach other campaigns — Amazon Ads targeting guidance — matches the claim: yes.
- Removing a negative keyword is done by archiving, which is not reversible — Campaign Manager behavior — matches the claim: uncertain because this is documented in third-party guidance rather than a current Amazon help page; the article's wording stays at the safe part of the claim, that archiving cannot be reversed and the word can be re-added.
- The 22-click standard at a 10% ad conversion rate, and roughly 45 clicks at 5% — derived arithmetic, not measured data — covers an illustrative calculation only — matches the claim: yes, and the article labels the 10% a planning assumption and carries the illustrative-figures line.

## New terms

- ad conversion rate — ad-attributed orders divided by clicks, from Campaign Manager. Defined by the first article in this set; this article leans on it heavily, so translators must keep it clearly distinct from listing conversion rate. Nearest everyday English: how often an ad click turns into a sale.
- ad-attributed order — an order Amazon credits to an ad click within the attribution window. Defined by the first article in this set; used here to describe what the search term report contains.
- negative keyword — an instruction that stops a search term from triggering your ad, applied at ad group or campaign level. Nearest everyday English: a blocked search word.
- negative exact / negative phrase — the two match types of a negative keyword. Keep "exact" and "phrase" aligned with however the positive match types are already translated in this hub, because sellers read them as a pair.
- relevance test — the name used here for the yes-or-no question of whether a search term describes a product you sell. Nearest everyday English: is this shopper looking for my product at all.
- attribution window — the period after a click during which Amazon credits an order to that click. Nearest everyday English: how long an ad click keeps getting credit for a sale.
- close variations — plurals and minor spelling differences that Amazon treats as the same term when matching.
