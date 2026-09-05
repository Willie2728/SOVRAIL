# SOVRAIL Growth Run 13 — Every API Call Needs a Passport and a Budget

## Product-grounded thesis

SOVRAIL already implements the primitives that make this message credible:

- scoped WCL-issued credentials;
- expiration and revocation;
- optional signed requests;
- per-asset rate limits and daily ceilings;
- upstream budget ceilings;
- local-first routing with optional paid-provider fallback;
- circuit breakers, idempotency and exact-result caching;
- provider abstraction and tamper-evident audit records.

## Campaign hook

**Every API call should have a passport and a budget.**

Supporting line:

**Know who is calling, what they are allowed to do, where the request can go, and how much it can spend.**

## 30-second B2B script

Open on three WCL applications, each containing different provider keys and different retry logic.

Voiceover: “The fastest way to lose control of an AI stack is to let every app manage providers, secrets, retries and spend on its own.”

The provider keys disappear from the individual apps and move behind one SOVRAIL boundary.

On-screen sequence:
`WCL credential → scope check → budget/rate check → route → provider/local execution → audit record`

Voiceover: “SOVRAIL gives each asset a scoped credential, applies usage and budget rules, then routes approved work through one controlled service boundary.”

Final frame: **SOVRAIL — one governed runtime between your products and the providers they use.**

CTA: **Review the integration architecture.**

## Qualified buyer

- AI product teams running multiple model/provider integrations;
- internal platforms managing many AI-enabled applications;
- teams that need provider abstraction, spend controls, auditability and local-first options.

## Claims boundary

SOVRAIL does not bypass provider authorization, commercial billing, rate limits or terms. Paid upstream requests still require valid provider accounts/credentials and remain subject to provider pricing.

## Status

Prompt Ready only. No media rendered or published in Run 13.