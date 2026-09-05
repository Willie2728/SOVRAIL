# SOVRAIL AI — Growth Run 18

## Campaign: Your App Should Not Know Your Provider Secrets

**Hook:** Your product should know one integration contract — not every provider secret.

### Customer truth

WCL software increasingly depends on multiple AI and service providers. Scattering provider-specific keys and SDK assumptions across every app creates avoidable operational surface area: credential sprawl, duplicated integration code, uneven budgets, harder provider changes, and fragmented audit trails.

SOVRAIL's current v2.1 architecture is built around the opposite boundary: consuming apps receive scoped WCL-controlled SOVRAIL credentials and call one stable interface; upstream provider secrets remain server-side. The gateway can apply per-asset limits, budget ceilings, local-first routing, optional provider fallbacks, circuit breakers, idempotency, safe caching, provider abstraction, and audit records.

### Deployable LinkedIn copy

**Your app should not know your OpenAI key. Or your Anthropic key. Or the next provider key you add six months from now.**

SOVRAIL AI gives each WCL asset one scoped credential and one stable service boundary. Provider secrets stay server-side. Approved requests can be budgeted, cached, routed local-first, failed over when configured, and written into an audit trail without forcing every consuming app to carry provider-specific integration logic.

That is the wedge: fewer secret copies, fewer provider assumptions, one governed runtime boundary.

SOVRAIL does not bypass provider authorization, billing, limits, or terms. Any request actually executed by a commercial provider remains subject to that provider's account and pricing.

**CTA:** Use SOVRAIL as the default API boundary for the next WCL integration.

### Creative brief

Five-frame carousel:
1. APP A → OpenAI key / Anthropic key / Tavus key / vendor SDKs.
2. Headline: **Secret sprawl is architecture debt.**
3. Replace the fan-out with APP → scoped `sov_...` key → SOVRAIL.
4. Show policies around the gateway: scope, budget, cache, route, failover, audit.
5. End: **One integration contract. Provider choice stays behind the boundary.**

### Claims boundary

Do not claim SOVRAIL eliminates breaches, guarantees availability, provides free third-party API usage, bypasses provider billing, or is production-hardened for multi-instance deployment without the documented PostgreSQL/Redis, TLS, managed-secret, rotation, and observability hardening work.

Status: **Prompt Ready; no media rendered; not published.**
