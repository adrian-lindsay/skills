---
name: last-30-days
description: >
  Scan the last 30 days of public signal (Reddit, Hacker News, GitHub, Product Hunt, platform changelogs, job/freelance boards) to spot emerging micro-business ideas that are early to market, well-timed, and easy enough for one person to ship — targeting $250–500/month. Returns a ranked shortlist with evidence, a "why now" catalyst, the simplest paid version, and a 7-day validation test.

  Trigger this skill whenever Adrian says things like: "run last 30 days", "what's emerging this month", "scan for new business ideas", "find me a $500/mo idea", "what should I build next", "what's early right now", "what changed in the last month I could build on", "any new gaps in [space]", or wants a recurring idea-spotting pass. Do NOT trigger for evaluating an idea he already has (use identify-game-structure or beachhead-segment), or for marketing an existing product (use marketing-ideas).
---

# Last 30 Days

A recurring scan that finds small, well-timed business ideas from what people complained about, asked for, launched, or were forced to change **in the last 30 days**. Not a brainstorm — every idea must be traceable to dated evidence.

## The filter

Every candidate has to pass three gates before it gets scored:

| Gate | Pass condition | Fail examples |
|------|----------------|---------------|
| **Early** | No dedicated product with real traction yet. People are using workarounds (spreadsheets, Zapier chains, manual work) or asking "is there a tool for…" | Category has a funded leader, a "top 10 tools for X" listicle, or a G2 category |
| **Right time** | A concrete catalyst in the last ~90 days: new API/platform feature, policy or pricing change, deadline, new capability that just became cheap, a wave of adjacent launches | Evergreen pain with no reason it's more solvable/urgent now than a year ago |
| **Not super hard** | One person can ship v1 in ≤2 weeks with AI-assisted build, and the first 10 customers are reachable from the exact threads where the signal came from | Needs a marketplace (two-sided), hardware, regulatory approval, enterprise sales, inventory, or a partnership to exist |

The money target is **$250–500/mo**. That is ~10–25 paying users at $19–49/mo, or ~10–20 sales/mo of a $29 digital product, or 2–4 productized-service clients. Think micro-SaaS, extension, template pack, paid directory, niche dataset/API, or a productized service — not a startup. See `references/scoring.md` for the archetypes and the math.

## Workflow

### Step 0: Set the aperture

Ask (or reuse from the last run if Adrian says "same as last time"):
- **Focus area** — open scan, or narrowed (e.g. "GTM/sales tooling", "AI agents", "Shopify", "creators")? Default: open scan weighted toward what he can distribute to (GTM, marketing, B2B SaaS, Claude Code / AI tooling).
- **Unfair advantages** — audience, sites, skills, existing code. Default assumptions: thegtmstack.io + its tool database, LinkedIn presence, ships with Claude Code, deep GTM domain knowledge.
- **Time budget** — hours/week available. Default: evenings + weekends, ~8 hrs/week.
- **Exclusions** — anything he's already tried, or won't do (e.g. no content-only businesses, no consulting).

Then check for prior runs in `output/last-30-days/`. If any exist, read the most recent one — its **Watching** list is your first set of leads to re-check, and its **Rejected** list tells you what not to re-surface.

### Step 1: Pull raw signal (30-day window, dated)

Collect from as many of these as the environment allows. Exact queries, endpoints, and rate limits are in `references/sources.md`. Run `scripts/scan.py` first if network access permits — it pulls Reddit + HN in one pass and dumps JSON to work from; use WebSearch/WebFetch for the rest.

1. **Complaint & request clusters** — Reddit (r/SaaS, r/Entrepreneur, r/smallbusiness, r/sales, r/marketing, r/shopify, r/Notion, r/ClaudeAI, r/ChatGPTPro, r/webdev, r/nocode, focus-area subs), Ask HN, "is there a tool that", "how do you all handle", "I built a spreadsheet to".
2. **Platform shifts** — changelogs / "now available" / API launches / pricing & policy changes from the platforms in the focus area (Claude, OpenAI, Shopify, Stripe, Notion, HubSpot, LinkedIn, Meta, Google, Apple, Chrome). Each one is a potential "why now."
3. **Adjacent-launch waves** — Show HN, Product Hunt, IndieHackers, r/SideProject launches in the last 30 days. 2–3 tiny launches in the same niche = validated demand, still early. 10+ = late.
4. **Search & repo demand** — GitHub repos created in the last 30 days sorted by stars (what devs are reaching for), Google Trends "rising" queries in the focus area, Chrome Web Store / App Store gaps.
5. **Paid-demand proof** — Upwork/Fiverr/job-board posts asking for a repetitive task in the niche (people already paying humans = will pay a tool), Gumroad/Lemon Squeezy bestsellers.

For every item, capture: **source URL, date, verbatim quote (≤2 sentences), and engagement (upvotes/comments/stars)**. No undated or unlinked signal makes it into the report.

**Stop conditions:** 40–80 raw items, or 2 passes over each source. Don't exhaustively crawl — this is a monthly radar, not a research project.

### Step 2: Cluster into candidate ideas

Group raw items into candidates. A candidate needs **≥3 independent signals** (different authors, ideally different sources) *or* 1 platform-shift catalyst + 2 demand signals.

For each cluster write one line: *"[who] can't [do what] because [why], since [catalyst/date]."* If you can't fill in "since," it's probably evergreen — demote to Watching unless it's obviously early.

Aim for 8–15 clusters before scoring. Discard obvious duplicates of known products immediately (do a 60-second competitor check: search `"[idea]" tool`, `[idea] alternative`, and Product Hunt).

### Step 3: Score

Score each cluster 1–5 on the four axes in `references/scoring.md`:

- **Early** — how empty is the field?
- **Timing** — how strong and recent is the catalyst?
- **Ease** — build + first-10-customer distribution in ≤2 weeks solo?
- **$ fit** — is $250–500/mo plausible, with evidence people pay for adjacent things?

Then apply the **kill checks** (two-sided marketplace, hardware, regulatory, enterprise sales, platform-absorption risk where the host platform will obviously ship this natively within months, single-source signal that could be one loud person). Any kill check → Rejected with the reason stated.

Overall = weighted: Timing ×1.5, Early ×1.25, Ease ×1.25, $ fit ×1. Rank descending.

### Step 4: Build the shortlist

For the **top 3–5**, write a full card (format in `examples/sample-report.md`):

- **Idea** — one sentence, plain.
- **Evidence** — 3–5 dated, linked quotes.
- **Why now** — the catalyst, with date.
- **Simplest paid version** — exact product, price, who pays, which archetype.
- **First 10 customers** — the actual threads/subreddits/people to go back to, and the message to post.
- **Competition** — what exists, why it's not "done," platform-absorption risk.
- **7-day validation test** — the cheapest experiment that produces a yes/no (landing page + the threads above; a $X pre-order; a manual/concierge version for 3 people; a Chrome extension MVP). Define the pass threshold up front (e.g. "5 emails or 1 paid pre-order").
- **Scores** — the four numbers + overall.

Then two short lists:
- **Watching** — interesting but missing a gate. State what would need to change (e.g. "needs a catalyst", "needs a second independent signal").
- **Rejected** — one line each with the kill reason, so they don't come back next month.

### Step 5: Save and diff

Write the report to `output/last-30-days/YYYY-MM-DD.md` (create the folder if needed; `./output/` relative to the current project unless Adrian says otherwise).

If a prior run exists, add a **Since last scan** section at the top: which Watching items matured, which shortlisted ideas got competitors (now Late), and what's net-new. This is how the skill compounds — month over month, the diff matters more than any single scan.

## Rules

- **Evidence or it doesn't exist.** Every claim about demand links to a dated source. No "people are increasingly…" without a URL.
- **Recency is hard.** Signal older than 30 days is context, not evidence. Catalysts can go back ~90 days.
- **Bias toward boring.** A $29 template solving a fresh pain beats an "AI platform." Ideas that require a pitch deck fail the Ease gate.
- **Distribution is part of the idea.** If the first 10 customers aren't reachable from the source threads or Adrian's existing audience, score Ease ≤2.
- **Say when it's thin.** If a scan turns up nothing that clears all three gates, say so and ship a Watching list. A thin month is a real finding; a padded shortlist is not.
- **No fabricated quotes, counts, or URLs.** If a source was unreachable, list it under "Sources not checked" in the report.

## Output

1. The ranked report (chat + saved file).
2. One-line recommendation: which single idea to run the 7-day test on this week, and why.
3. A reminder of what to bring to next month's run (results of the test, anything to add to Exclusions).
