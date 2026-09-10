# Signal sources

All endpoints below are public and need no API key. Respect the rate limits — they're what keep these free.

Window: **30 days** for demand signal, **~90 days** for catalysts. Compute the cutoff timestamp once at the start of the run (`date -d '30 days ago' +%s`).

## 1. Reddit (public JSON)

No OAuth needed. Append `.json` to any listing or search URL. Always send a custom User-Agent and sleep 2s between calls — default UAs get 429'd.

```bash
UA="last-30-days-scan/1.0 (personal research)"

# Top of month for a subreddit
curl -s -A "$UA" "https://www.reddit.com/r/SaaS/top.json?t=month&limit=100"

# Search within a subreddit, last month, sorted by top
curl -s -A "$UA" "https://www.reddit.com/r/smallbusiness/search.json?q=%22is+there+a+tool%22&restrict_sr=1&t=month&sort=top&limit=50"
sleep 2
```

Fields to keep: `data.title`, `data.selftext` (first 300 chars), `data.score`, `data.num_comments`, `data.created_utc`, `data.permalink`, `data.author`.

**Default subreddits** (add focus-area subs on top):
`SaaS, Entrepreneur, smallbusiness, sidehustle, SideProject, indiehackers, startups, sales, marketing, b2bmarketing, coldemail, shopify, ecommerce, Notion, nocode, webdev, ClaudeAI, ChatGPTPro, artificial, productivity, freelance, Upwork`

**Query set** (run each against the top 5–8 subs for the focus area):
```
"is there a tool"
"is there an app"
"anyone know a tool"
"how do you all handle"
"I built a spreadsheet"
"I ended up building"
"wish there was"
"looking for a tool that"
"switched away from"
"just launched"
"changed their pricing"
"no longer works"
```

Reject: `[deleted]`, AutoModerator, score < 5, obvious vendor self-promo (new account + link in post).

## 2. Hacker News (Algolia API)

```bash
CUTOFF=$(date -d '30 days ago' +%s)

# Ask HN: tool requests
curl -s "https://hn.algolia.com/api/v1/search?query=%22is%20there%20a%20tool%22&tags=ask_hn&numericFilters=created_at_i%3E$CUTOFF&hitsPerPage=50"

# Show HN launches in the window (adjacent-launch waves)
curl -s "https://hn.algolia.com/api/v1/search_by_date?tags=show_hn&numericFilters=created_at_i%3E$CUTOFF,points%3E10&hitsPerPage=100"

# Keyword within window
curl -s "https://hn.algolia.com/api/v1/search?query=YOUR+TERM&numericFilters=created_at_i%3E$CUTOFF&hitsPerPage=50"
```

Fields: `title`, `url`, `points`, `num_comments`, `created_at`, `objectID` (thread = `https://news.ycombinator.com/item?id={objectID}`).

Useful Ask HN queries: `"what do you use for"`, `"how do you"`, `"is there a"`, `"recommend a"`, `"alternative to"`, `"annoyed"`, `"why is there no"`.

## 3. GitHub (recently created, high-star repos)

What developers are reaching for right now. Public search API, 10 req/min unauthenticated.

```bash
SINCE=$(date -d '30 days ago' +%Y-%m-%d)
curl -s "https://api.github.com/search/repositories?q=created:%3E$SINCE&sort=stars&order=desc&per_page=50"
# With topic filter:
curl -s "https://api.github.com/search/repositories?q=created:%3E$SINCE+topic:mcp&sort=stars&order=desc&per_page=30"
```

Also `https://github.com/trending?since=monthly` (HTML, fetch and skim). Note: some sandboxed environments block the search endpoint — if so, fall back to WebSearch `site:github.com "created" ...` or skip and record under "Sources not checked".

## 4. Launch feeds (adjacent-launch waves)

- **Product Hunt** — no free API. WebSearch: `site:producthunt.com [niche]` and skim the last 30 days; or fetch `https://www.producthunt.com/topics/[topic]`.
- **IndieHackers** — `https://www.indiehackers.com/products?sorting=newest` and the "Show IH" posts.
- **r/SideProject, r/SaaS "launched"** — covered by the Reddit queries above.
- **Gumroad / Lemon Squeezy Discover** — `https://discover.gumroad.com/` sorted by hot, filtered to the niche. Bestsellers = proof people pay for a shape of product.

Count launches per niche. 2–3 = early wave. 10+ = late.

## 5. Platform shifts (the "why now")

Check the changelogs of every platform in the focus area for the last ~90 days. Look for: new API, new capability, pricing change, policy change, deprecation, deadline.

| Platform | Where |
|----------|-------|
| Anthropic / Claude | docs.anthropic.com release notes, Claude Code changelog, MCP registry |
| OpenAI | platform.openai.com/docs/changelog |
| Shopify | shopify.dev/changelog |
| Stripe | stripe.com/docs/changelog |
| Notion | notion.so/releases, developers.notion.com/changelog |
| HubSpot | developers.hubspot.com/changelog |
| LinkedIn | LinkedIn Engineering + policy updates (WebSearch: `LinkedIn API changes [month year]`) |
| Google | Search Central blog (ranking/policy changes), Workspace updates |
| Meta | developers.facebook.com/blog |
| Apple / Chrome | App Store review guideline updates, Chrome extension Manifest changes |

WebSearch pattern: `"[platform]" (changelog OR "now available" OR deprecat* OR "pricing change") after:YYYY-MM-DD`.

A deprecation or price hike is often the best catalyst: it creates a dated pain for a known population who were already paying.

## 6. Paid-demand proof

People already paying humans for a repetitive task will pay a tool that does it.

- **Upwork / Fiverr** — WebSearch `site:upwork.com/freelance-jobs "[task]"` and count postings; note budgets.
- **Job boards** — a spike in "[task] specialist" postings means companies are hiring for a thing that could be a tool.
- **Google Trends** — `https://trends.google.com/trends/explore?date=today%203-m&q=[term]` — look at *Rising* related queries, not the main line. No API; fetch and read, or note as manual check.

## 7. Search-gap check (competition scan, run per cluster)

60 seconds per candidate:
```
"[idea phrase]" tool
"[idea phrase]" alternative
"[idea phrase]" site:producthunt.com
"best [idea phrase] tools"
```
- Zero dedicated results, only workarounds/forum threads → **Early = 5**
- 1–2 small indie tools → **Early = 4**
- A "best X tools" listicle exists → **Early ≤ 2**
- A G2/Capterra category exists → **Early = 1**

## Rate limits & etiquette

| Source | Limit | Practice |
|--------|-------|----------|
| Reddit JSON | ~60/min soft, aggressive 429s | 2s sleep, custom UA, ≤100 requests per run |
| HN Algolia | 10,000/hr | fine |
| GitHub search | 10/min unauthenticated | 6s sleep between calls |
| Everything else | — | WebFetch once, don't crawl |

If a source is unreachable, don't retry more than once. Record it under **Sources not checked** in the report.
