title:        How Much Data Do You Need Before You Change a Campaign?
slug:         how-much-data-before-changing-a-campaign
summary:      Zero sales on a keyword means nothing until you have enough clicks. Here is how many, and how to count them correctly.
categories:   PPC & Advertising
hero_alt: Clicks filling a chamber until they cross a threshold and move a gauge
reading_time: 7

Most new sellers change their campaigns too early. They see a keyword with clicks and no sales, decide it is a bad keyword, and turn it off. A week later they do the same thing to another keyword. After a month they have changed so many things that nothing in the account can be explained.

The cause is almost never impatience about time. It is impatience about data. Three days is not too short a wait because three days is short; it is too short because three days has not produced enough clicks to tell you anything.

This guide gives you a number: how many clicks a keyword needs before "no sales" is real evidence, where that number comes from, and how to work out your own.

## What's in this guide

- Why a keyword with no sales is not automatically a bad keyword
- How many clicks you need before zero sales means something
- How to find your own ad conversion rate in the advertising console
- Why your campaign total is not the number that matters
- How long it takes to collect enough clicks
- What to do while you wait

## Why does a keyword with no sales not mean the keyword is bad?

Your ad conversion rate is the share of ad clicks that turn into ad-attributed orders. If your ad conversion rate is 10%, then on average one click in ten becomes a sale. That average is the only thing 10% promises. It does not promise that the tenth click will be a sale.

With a 10% ad conversion rate, a run of clicks with no sale is completely ordinary. Nine clicks in a row with nothing is the expected experience some of the time, not a sign that anything is broken.

You can calculate how ordinary. For each click, the chance of no sale is 90%. For eight clicks in a row with no sale, multiply 0.90 by itself once per click.

Clicks so far | 8
Sales so far | 0
Chance of no sale on any one click | 90%
Chance of no sale across all 8 clicks | 43%

[[The problem]]
A keyword that is performing exactly as expected will show you zero sales after eight clicks roughly four times out of ten. If eight clicks is enough to make you turn a keyword off, you will turn off good keywords about 43% of the time.

## How many clicks do you need before zero sales means something?

You need enough clicks that a run of zeros becomes unlikely rather than ordinary. A workable standard is to wait until the chance of seeing zero sales from a normally performing keyword drops below 10%.

At that point, one of two things is true: either the keyword really is underperforming, or you have been unlucky in a way that happens less than one time in ten. That is a reasonable basis for a decision.

The number of clicks that takes depends entirely on your ad conversion rate. The lower your ad conversion rate, the longer a run of zeros can be before it means anything.

| Your ad conversion rate | Clicks with no sale before zero is meaningful |
|---|---|
| 20% | 11 |
| 15% | 15 |
| 10% | 22 |
| 8% | 28 |
| 5% | 45 |
| 3% | 76 |

[[The rule]]
If you do not know your ad conversion rate yet, use 22 clicks. It assumes a 10% ad conversion rate, which is a reasonable planning number for a product that is converting normally. Below 22 clicks on a single keyword, you do not have a result. You have a gap in the data.

Notice what the table does to the common advice that 10 clicks is enough. Ten clicks does not clear the threshold at any ad conversion rate in the table: even the 20% row asks for 11. For a product converting at 5%, acting on 10 clicks means acting on roughly a fifth of the evidence you need.

## How do you find your own ad conversion rate?

Your ad conversion rate is ad-attributed orders divided by clicks. It comes from the advertising console, not from Seller Central.

In Campaign Manager, set a date range of at least 30 days and read two columns for the ASIN you are advertising: clicks, and ad-attributed orders. Divide the second by the first. The console also displays a conversion rate column calculated the same way, but column names change over time, so the division is the version that will always work.

Clicks in the last 30 days | 640
Ad-attributed orders in the same period | 51
Ad conversion rate, 51 divided by 640 | 8.0%
Row to use from the table above | 28 clicks

[[The distinction]]
Do not use unit session percentage from Seller Central Business Reports for this. That figure divides orders by sessions on your listing, and it counts organic visits alongside ad clicks. It answers a different question — how well your listing converts overall. The threshold in this guide needs how well your ads convert, which is a different number on a different denominator.

Take the rate at account or campaign level, not from the keyword you are about to judge. A single keyword does not have enough clicks to produce a reliable rate, which is the reason you are reading this guide. The rate comes from the larger pool of clicks; the threshold then gets applied to the individual keyword.

One caution about the date range. Ad-attributed orders are [[SEE: how-amazon-ads-bills-you | counted after the click]], so the most recent days in any window are still filling in. End your date range about a week before today, or the rate you calculate will come out too low.

If the ASIN has no advertising history at all, you have no measured rate. Use 10% as a planning assumption, take the 22-click row, and replace it with a measured figure once the campaign has a few hundred clicks behind it.

## Why is your campaign total not the number that matters?

This is the mistake that survives even after sellers learn the click threshold. They check the campaign, see hundreds of clicks, and conclude they have plenty of data. Then they make decisions about individual keywords using a number that belongs to the campaign.

A campaign total tells you nothing about any keyword inside it. Clicks are never spread evenly. One keyword usually takes a large share of the spend while several others sit on two or three clicks each.

[[The trap]]
A campaign with 1,200 clicks can easily contain eight keywords that have fewer than 22 clicks each. The campaign has enough data. The keywords do not. Decisions get made at the keyword level, so the count that matters is the keyword count.

Download your search term report and read the click column keyword by keyword. Any keyword below your threshold is not ready for a decision, whatever the campaign total says.

[[FIGURE: One campaign total split unevenly across keywords, most below the decision threshold]]

## How long does it take to collect enough clicks?

Long enough that it is worth planning for. Here is the arithmetic for a small launch budget on a campaign with ten keywords.

Daily ad spend | $12.00
Average CPC | $0.60
Clicks per day across the campaign | 20
Keywords in the campaign | 10
Average clicks per keyword per day | 2
Clicks needed on one keyword | 22
Days until one keyword reaches that number | 11

[[Worked example]]
At $12.00 per day and a $0.60 CPC, the campaign buys 20 clicks per day. Spread across 10 keywords that is 2 clicks per keyword per day, so a single keyword takes 11 days to reach 22 clicks. The even split is a simplification used to keep the example readable; in a real campaign the spread is uneven, which means your slowest keywords take longer than 11 days, not less.

Two things follow from this arithmetic, and both are more useful than any bidding tip.

The first is that fewer keywords per campaign produce usable data faster. The same $12.00 spread across 4 keywords gives each one 5 clicks per day and a decision in 5 days instead of 11. You are not buying more data by narrowing the campaign; you are concentrating it where you can read it.

The second is that [[SEE: daily-budget-runs-out-by-midday | cutting your budget when results look bad]] makes the problem worse. A smaller budget buys fewer clicks, which means a longer wait before you know anything, during which you keep spending.

## What should you do while you wait?

Waiting does not mean doing nothing. It means not changing the thing you are measuring.

[[What to do]]
1. Write down the date you launched each campaign and the click threshold you are using for it.
2. Check the search term report weekly, not daily, and look only at the click column to see which keywords are approaching the threshold.
3. Act on keywords that have crossed the threshold. Leave the rest alone, including the ones that look terrible.
4. Work on the parts of the listing that do not disturb the measurement: supplier questions, images awaiting replacement, stock planning.
5. Record every change you do make, with the date. A change you cannot date is a change you cannot evaluate.

There is one exception to leaving campaigns alone. If a keyword has no impressions at all, waiting will not help, because no data is being collected in the first place. Impressions are the number of times your ad was displayed, and zero impressions is [[SEE: not-showing-not-indexed-not-selling | a different problem with different causes]].

## Frequently asked

**Does this apply to spend as well as clicks?**
Use clicks. Spend is a poor substitute because it mixes two different things: how many chances a keyword had to convert, and what each chance cost. A keyword that has spent $40.00 at a $4.00 CPC has had 10 chances, not 40.

**What if a keyword has clicks and sales, but a bad ACOS?**
That is a different decision and the threshold does not apply in the same way. Once a keyword has produced sales you are no longer asking whether it can convert; you are asking whether it converts profitably, which is [[SEE: acos-tacos-and-your-margin | a question about your margin]].

**Should I use 22 clicks for negative keywords too?**
The same evidence standard applies, with one addition: relevance. A search term that is clearly unrelated to your product can be excluded immediately, because you are not making a statistical judgement, you are making [[SEE: when-to-negate-a-keyword | a relevance judgement]].

**My product converts at 25%. Can I decide faster?**
Yes. Higher ad conversion rates need fewer clicks, because a run of zeros becomes unlikely sooner. Extend the table using the same standard and you will find 25% needs 9 clicks.

**How was the click threshold calculated?**
Start by assuming the keyword converts at your ad conversion rate. Each click then has a chance of producing no sale equal to 100% minus that rate, and the chance that a whole run of clicks produces nothing is that figure multiplied by itself once per click. At a 10% ad conversion rate, a run of 21 clicks with no sale happens to a perfectly normal keyword 10.9% of the time, and a run of 22 clicks happens 9.8% of the time. The threshold is the first click count where that figure falls below 10%, which is the point where zero stops being an ordinary result and starts being evidence. Every row of the table is the same calculation at a different rate.

The choice of 10% as the cutoff is a convention, not a law of the platform. A stricter standard — waiting until the chance falls below 5% — would ask for 29 clicks instead of 22 at a 10% ad conversion rate. The looser standard is used here because it is reachable on a small launch budget while still being far more evidence than the eight or ten clicks most sellers act on.

## Final thoughts

The question "how long should I wait?" has no answer, because time is not what you are collecting. Clicks are. Two campaigns launched on the same day can be four days apart in evidence, depending on budget and keyword count.

Replacing the question with "how many clicks does this keyword have?" changes what you do every week. It tells you which decisions are ready to make and which are not yet decisions at all. It also tells you something uncomfortable but useful early on: that a very small budget spread across many keywords does not buy slow learning, it buys no learning.

Figures from this article's worked examples, not an industry survey.

## New terms

- ad conversion rate — ad-attributed orders divided by clicks. Everyday phrase: how often an ad click turns into a sale. Must stay distinct from listing conversion rate throughout; they have different denominators.
- ad-attributed order — an order Amazon credits to an ad click within the attribution window. Everyday phrase: a sale the ad gets credit for.
- unit session percentage — the Seller Central Business Reports column that divides units ordered by listing sessions. Everyday phrase: the share of listing visits that ended in an order. Appears in this article only as the metric readers are told not to use for advertising decisions, so the contrast with ad conversion rate must survive translation.
- impressions — the number of times an ad was displayed, whether or not anyone clicked. Everyday phrase: how many times the ad was shown.
- negative keyword — a search term you tell Amazon not to show your ad for. Everyday phrase: a blocked search term. Related to the verdict Negate, but the verdict is a decision and this is the setting that carries it out.
- No new callout labels were needed. All callouts in this article use approved labels: The problem, The rule, The distinction, The trap, Worked example, What to do.
