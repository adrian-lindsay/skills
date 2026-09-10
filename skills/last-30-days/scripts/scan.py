#!/usr/bin/env python3
"""Pull 30-day demand signal from Reddit and Hacker News into one JSON file.

No API keys. Standard library only.

    python3 scan.py --out signal.json
    python3 scan.py --subs SaaS,sales,shopify --days 30 --out signal.json
    python3 scan.py --queries '"is there a tool","wish there was"' --no-hn

Output: a JSON list of items, each:
  {source, sub_or_tag, title, text, score, comments, created (ISO date), url, author, query}

Sorted by score descending. Feed this into Step 2 (clustering) of the skill.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

UA = "last-30-days-scan/1.0 (personal research)"

DEFAULT_SUBS = [
    "SaaS", "Entrepreneur", "smallbusiness", "sidehustle", "SideProject",
    "indiehackers", "startups", "sales", "marketing", "b2bmarketing",
    "shopify", "Notion", "nocode", "webdev", "ClaudeAI", "productivity",
]

DEFAULT_QUERIES = [
    '"is there a tool"',
    '"is there an app"',
    '"anyone know a tool"',
    '"how do you all handle"',
    '"I built a spreadsheet"',
    '"wish there was"',
    '"looking for a tool that"',
    '"changed their pricing"',
    '"no longer works"',
]

HN_ASK_QUERIES = [
    "is there a tool", "what do you use for", "why is there no",
    "recommend a", "alternative to",
]


def get_json(url, sleep=0.0, retries=1):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.load(r)
            if sleep:
                time.sleep(sleep)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                time.sleep(10)
                continue
            print(f"  ! {e.code} {url}", file=sys.stderr)
            return None
        except Exception as e:  # network blocked, timeout, bad JSON
            print(f"  ! {type(e).__name__} {url}", file=sys.stderr)
            return None
    return None


def iso(ts):
    return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()


# ---------------------------------------------------------------- Reddit

def reddit_items(data, cutoff_ts, query, sub):
    out = []
    if not data:
        return out
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        created = d.get("created_utc", 0)
        if created < cutoff_ts:
            continue
        if d.get("author") in ("AutoModerator", "[deleted]"):
            continue
        if d.get("score", 0) < 5:
            continue
        text = (d.get("selftext") or "")[:300].replace("\n", " ")
        out.append({
            "source": "reddit",
            "sub_or_tag": f"r/{d.get('subreddit', sub)}",
            "title": d.get("title", ""),
            "text": text,
            "score": d.get("score", 0),
            "comments": d.get("num_comments", 0),
            "created": iso(created),
            "url": "https://www.reddit.com" + d.get("permalink", ""),
            "author": d.get("author", ""),
            "query": query,
        })
    return out


def scan_reddit(subs, queries, cutoff_ts, sleep):
    items = []
    for sub in subs:
        print(f"reddit r/{sub}: top/month", file=sys.stderr)
        url = f"https://www.reddit.com/r/{sub}/top.json?t=month&limit=100"
        items += reddit_items(get_json(url, sleep), cutoff_ts, "top:month", sub)
        for q in queries:
            print(f"reddit r/{sub}: {q}", file=sys.stderr)
            url = (f"https://www.reddit.com/r/{sub}/search.json?"
                   f"q={urllib.parse.quote(q)}&restrict_sr=1&t=month&sort=top&limit=50")
            items += reddit_items(get_json(url, sleep), cutoff_ts, q, sub)
    return items


# ------------------------------------------------------------ Hacker News

def hn_items(data, tag, query):
    out = []
    if not data:
        return out
    for h in data.get("hits", []):
        oid = h.get("objectID")
        out.append({
            "source": "hn",
            "sub_or_tag": tag,
            "title": h.get("title") or "",
            "text": (h.get("story_text") or "")[:300].replace("\n", " "),
            "score": h.get("points") or 0,
            "comments": h.get("num_comments") or 0,
            "created": (h.get("created_at") or "")[:10],
            "url": f"https://news.ycombinator.com/item?id={oid}",
            "author": h.get("author", ""),
            "query": query,
        })
    return out


def scan_hn(cutoff_ts):
    items = []
    base = "https://hn.algolia.com/api/v1/"
    for q in HN_ASK_QUERIES:
        print(f"hn ask_hn: {q}", file=sys.stderr)
        url = (f"{base}search?query={urllib.parse.quote(q)}&tags=ask_hn"
               f"&numericFilters=created_at_i%3E{cutoff_ts}&hitsPerPage=50")
        items += hn_items(get_json(url), "ask_hn", q)
    print("hn show_hn: launches", file=sys.stderr)
    url = (f"{base}search_by_date?tags=show_hn"
           f"&numericFilters=created_at_i%3E{cutoff_ts},points%3E10&hitsPerPage=100")
    items += hn_items(get_json(url), "show_hn", "launches")
    return items


# ------------------------------------------------------------------ main

def dedupe(items):
    seen, out = set(), []
    for it in items:
        if it["url"] in seen:
            continue
        seen.add(it["url"])
        out.append(it)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subs", default=",".join(DEFAULT_SUBS), help="comma-separated subreddits")
    ap.add_argument("--queries", default=None, help="comma-separated Reddit search queries (quote phrases)")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--sleep", type=float, default=2.0, help="seconds between Reddit calls")
    ap.add_argument("--no-reddit", action="store_true")
    ap.add_argument("--no-hn", action="store_true")
    ap.add_argument("--out", default="signal.json")
    args = ap.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    cutoff_ts = int(cutoff.timestamp())
    subs = [s.strip() for s in args.subs.split(",") if s.strip()]
    queries = ([q.strip() for q in args.queries.split(",") if q.strip()]
               if args.queries else DEFAULT_QUERIES)

    items = []
    if not args.no_reddit:
        items += scan_reddit(subs, queries, cutoff_ts, args.sleep)
    if not args.no_hn:
        items += scan_hn(cutoff_ts)

    items = dedupe(items)
    items.sort(key=lambda x: x["score"], reverse=True)

    with open(args.out, "w") as f:
        json.dump(items, f, indent=1)

    by_src = {}
    for it in items:
        by_src[it["source"]] = by_src.get(it["source"], 0) + 1
    print(f"\n{len(items)} items since {cutoff.date()} → {args.out}  {by_src}", file=sys.stderr)


if __name__ == "__main__":
    main()
