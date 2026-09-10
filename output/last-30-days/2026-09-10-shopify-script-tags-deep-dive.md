# Deep dive: "Will my store break on March 1?" — Shopify script-tag deadline audit

*Companion to the 2026-09-10 scan. Verified against shopify.dev docs and community threads via search; forum pages themselves were egress-blocked.*

## What is actually happening

- **ScriptTag** is the legacy way an app injects JavaScript into a storefront: the app calls the API once, and Shopify renders `<script src="https://app-domain/…?shop=store.myshopify.com">` into `{{ content_for_header }}` on every page (and optionally the order-status page). No theme edit, no merchant action, invisible in admin.
- **Replacement** (available since 2021): theme app extensions — *app embed blocks* the merchant toggles on in the theme editor (served from `cdn.shopify.com/extensions/…`), or *web pixels* for analytics/conversion scripts (no merchant action).
- **Timeline** (announced Aug 2026): from **Oct 1, 2026** `scriptTagCreate` / `scriptTagUpdate` return errors and REST ScriptTag rejects POST/PUT; from **Mar 1, 2027** Shopify stops injecting existing script tags. Any app feature that depends on one stops that day.
- **Scoping fact that creates the gap:** script tags are scoped to the app that created them. Another app can't list them, and the merchant has no admin page listing them. The only merchant-side way to see them is the storefront page source.
- **Oct 1 nuance:** existing tags keep working until March, but an app can't *re-create* one. So a merchant who uninstalls/reinstalls an affected app after Oct 1 gets a silent breakage immediately. Same for theme-switchers whose app "re-injects" on install.

## Who is affected

Apps that never migrated in five years: typically old, abandoned, or agency-built. Categories (not a claim about specific vendors): review widgets, chat/helpdesk widgets, popups/announcement bars, currency/geo converters, affiliate & referral tracking, session recording/heatmaps, upsell/cross-sell overlays, GDPR/cookie banners, loyalty widgets, custom tracking installed by a previous agency via a custom app. Merchants who've been on Shopify 4+ years and have changed agencies are the highest-risk profile.

## The self-check (non-technical, ~10 minutes)

1. Open the storefront homepage, a product page, and the cart page. Right-click → View Page Source (Chrome: `Ctrl/Cmd+U`).
2. `Ctrl/Cmd+F` for `<script` and walk the `<head>`.
3. Sort each external script into a bucket:
   - `cdn.shopify.com/extensions/…` → **app embed block — safe.**
   - `cdn.shopify.com/s/files/…/assets/…` → **theme asset — safe from this deadline** (may be a different legacy pattern; note it).
   - Anything under `web-pixels-manager` / sandboxed pixel → **safe.**
   - External domain (the app's own domain or a third-party CDN), especially with `?shop=yourstore.myshopify.com` on the URL, sitting in the head block near the Shopify boilerplate → **likely ScriptTag — flag it.**
4. Match each flagged domain to an installed app (Settings → Apps and sales channels). Unknown domain = likely a previous agency's custom app — highest risk.
5. Email each vendor the template below. Vendor says "we use app embeds / web pixels" → done. No reply in 10 days or "we're working on it" → shortlist a replacement app now, not in February.
6. Order-status page: place a test order and repeat step 2 on the thank-you page.

**Vendor email template**
> Subject: Script tag deprecation — is [App] affected?
> Hi — Shopify is retiring storefront script tags (no create/update after Oct 1, 2026; they stop running Mar 1, 2027). I'm auditing [store]. Does [App] currently inject a script tag on my storefront or order-status page? If yes, what's your migration date to app embed blocks / web pixels, and will I need to do anything in my theme editor? Thanks.

## Offer ladder

| Tier | Price | What they get | Who |
|------|-------|---------------|-----|
| Free | — | The self-check as a public post/thread + the email template | Everyone; lead-gen and SEO |
| Kit | **$29** | PDF/Notion: self-check with screenshots, the bucket rules above, a growing list of known app script domains → app names, the vendor email, a decision tree (analytics → web pixel; widget → app embed; abandoned → replacement app), "how to turn on an app embed" walkthrough | DIY merchants |
| Audit | **$149** | Adrian runs the check on the merchant's store (home/product/cart/thank-you), delivers a one-page report: flagged apps, vendor status, replacement recommendation, and sends the vendor emails on their behalf | Merchants who won't do it themselves |
| Agency | **$99/store, min 5** | Same audit across a client portfolio + a client-facing summary they can forward | Agencies with legacy client stores |
| Referral | 10–20% | Migration work handed to a partner Shopify dev | Only when something actually needs code |

Target math: 2–4 audits/mo, or ~10 kits + 1 audit, or one agency pack.

## Where the buyers are

- **r/shopify** (post the self-check as a value thread; link at the bottom).
- **Shopify Community** threads: "Shopify ScriptTag Deprecation" (community.shopify.com/t/…/203267), the dev-forum deprecation thread (community.shopify.dev/t/…/37108), "Shopify Scripts are ending — what is everyone using now?" (adjacent audience, already burned once).
- **Facebook groups** for Shopify store owners; **Shopify Partners** Slack/agency LinkedIn.
- **SEO:** "Shopify script tags March 2027 / which apps will break" currently returns only dev docs and one agency blog. A merchant-facing page can rank fast.
- **App vendors** still on ScriptTag need merchant-facing comms — offer the kit white-label.

## Timing waves

1. **Now → Oct 1:** agencies and proactive merchants. Angle: "reinstall after Oct 1 and it's already broken."
2. **Oct 1 → Dec:** first breakage stories from reinstalls/theme switches; vendors start emailing.
3. **Jan → Mar 1:** panic search. Have the SEO page and the kit already ranking.

## Risks and honest caveats

- Shopify may add an admin warning (they did for `checkout.liquid`). Mitigation: the *which vendor, what replacement* work still isn't in the admin.
- Well-run app vendors will email their merchants — that shrinks DIY demand but *creates* the "I got three scary emails, what do I do" audit demand.
- Urgency is low until February. Lead with the Oct 1 reinstall angle and sell to agencies first.
- The self-check is a heuristic, not proof; a flagged script must be confirmed with the vendor. Say so in the kit.
- Adjacent tools (Script Scan, SecureShop Scanner, Detectify, Store Health) detect scripts/apps generically; none found framing the deadline. Expect one of them to add a "March 2027" badge within months — the audit/service layer is the durable part.

## 7-day test

- Day 1–2: write the self-check post + email template; publish as a thread in r/shopify and reply in the two community threads.
- Day 2: one-page landing page: free post → $29 kit → $149 audit (Stripe link).
- Day 3: LinkedIn post aimed at agencies: "your legacy client stores have apps that die March 1 — here's the 10-minute check."
- Day 4–7: answer every reply personally; offer the audit.
- **Pass:** 25 people run the self-check (comments/DMs), 2 paid audits or 1 agency asking for portfolio pricing.
- **Fail:** <5 engaged replies → demand is later-wave; park until Oct 1 and re-post with the reinstall-breakage angle.
