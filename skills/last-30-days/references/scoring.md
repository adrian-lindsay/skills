# Scoring rubric & money archetypes

## The four axes (1–5 each)

### Early — how empty is the field?

| Score | Condition |
|-------|-----------|
| 5 | No dedicated product. Only workarounds, forum threads, "is there a tool" posts |
| 4 | 1–2 tiny indie tools, no traction signal (no reviews, no listicle mentions) |
| 3 | A few small tools; none owns the niche; nobody has clearly nailed it |
| 2 | A "best X tools" listicle exists; 5+ entrants |
| 1 | Funded leader, G2 category, or a platform already ships it natively |

### Timing — how strong and recent is the catalyst?

| Score | Condition |
|-------|-----------|
| 5 | Dated catalyst in last 30 days (new API, deprecation, price hike, policy, deadline) with people already reacting to it |
| 4 | Catalyst in last 90 days, reaction building |
| 3 | A slow trend (new capability getting cheaper) with a visible 30-day uptick in complaints/launches |
| 2 | Evergreen pain, but a fresh wave of adjacent launches suggests something shifted |
| 1 | No reason this is more urgent or more possible now than a year ago |

### Ease — build + reach first 10 customers in ≤2 weeks, solo

| Score | Condition |
|-------|-----------|
| 5 | Weekend build with AI assistance; first customers are the people in the source threads; no integrations beyond one API |
| 4 | 1–2 weeks; one or two integrations; distribution channel obvious |
| 3 | 2–4 weeks; needs a data source or scraping that's fragile; distribution needs some cold outreach |
| 2 | Needs sales calls, an approval (app store review, partner program), or ongoing manual ops |
| 1 | Two-sided marketplace, hardware, compliance, or content library that takes months to build |

### $ fit — is $250–500/mo plausible?

| Score | Condition |
|-------|-----------|
| 5 | People in the threads say "I'd pay for this" *or* are already paying a human / a clunky tool for it; clear price anchor |
| 4 | Adjacent tools charge; audience is businesses (not hobbyists) |
| 3 | Willingness to pay is plausible but unstated; audience mixed |
| 2 | Audience expects free (consumers, students, open-source devs) but a pro tier is conceivable |
| 1 | Free is the norm and any paid version will be undercut by a free clone within weeks |

## Kill checks (any one → Rejected)

- **Two-sided** — needs both supply and demand to show up (marketplace, community, job board).
- **Hardware / inventory / shipping.**
- **Regulatory** — medical, legal, financial advice, KYC, tax filing, anything needing a license.
- **Enterprise sales** — buyer is a procurement process, not a person with a credit card.
- **Platform absorption** — the host platform will obviously ship this natively within months (e.g. a thin wrapper on a feature the platform has already announced). Flag as *Watching* only if there's a differentiated angle.
- **Single-source signal** — all evidence traces to one loud person or one thread.
- **Already on Exclusions** from Step 0.

## Overall score

`Overall = (Timing × 1.5) + (Early × 1.25) + (Ease × 1.25) + ($ fit × 1.0)` → max 25.

- **≥ 19** — Shortlist. Run the 7-day test.
- **15–18** — Shortlist if nothing scores higher; otherwise Watching with the weakest axis named.
- **< 15** — Watching or Rejected.

Timing is weighted highest on purpose: the whole point of a 30-day scan is to catch things *because* of when they're happening. An evergreen idea with a great score on everything else belongs in a different process.

## $250–500/mo archetypes (with the math)

Pick the archetype at scoring time — it forces the "simplest paid version" to be concrete.

| Archetype | Shape | Math to $250–500 | Build time | Best when |
|-----------|-------|------------------|------------|-----------|
| **Micro-SaaS** | Single-feature web app, monthly sub | 10–25 users × $19–49 | 1–2 wks | Recurring pain, business buyer |
| **Browser extension** | Chrome/Firefox ext, one-time or sub | 15–30 × $15–29 one-time/mo, or 10 × $39/yr sub | 2–5 days | Pain lives inside a specific web app (LinkedIn, Gmail, Notion, Shopify admin) |
| **Template / kit** | Notion/Sheets/Airtable/Claude-prompt pack | 10–20 sales/mo × $19–39 | 2–4 days | The workaround people describe *is* a spreadsheet — sell the good version |
| **Paid directory / list** | Curated dataset of X, paid listings or paid access | 5–10 listings × $49/mo, or 20 × $19 access | 1 wk + upkeep | New category with no map yet (early-wave signal) |
| **Niche data / API** | Scraped or compiled data behind a simple API or CSV sub | 5–10 × $29–49 | 1–2 wks | Devs in the threads asking "where do I get X data" |
| **Productized service** | Fixed-scope, fixed-price done-for-you (often the concierge MVP for a future tool) | 2–4 clients × $125–250 | 0 days | Fastest validation; run it manually before building |
| **Micro-newsletter / alert** | Paid alerts on a specific change (price changes, new listings, policy updates) | 25–50 × $9–12 | 3–5 days | Catalyst is a recurring change people need to track |
| **One-time tool** | Single-purpose utility, one-time $ | 20–30 × $15–25 | 2–5 days | Pain is acute but infrequent (migration, export, cleanup) |

Rule of thumb: if the simplest paid version needs a free tier to work, it's not a $500/mo idea — it's a $50k/mo idea being dressed down. Prefer shapes where the *first* customer pays.
