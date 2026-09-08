# SOVRAIL AI
## Sovereign API Execution, Cost Control & Integration Layer v2.3

SOVRAIL is the Wilkerson Collective-controlled execution boundary between applications, AI agents, MCP tools and third-party or internal APIs. Consuming assets receive scoped SOVRAIL credentials and call one stable interface. Provider secrets stay server-side.

### What SOVRAIL is designed to do

SOVRAIL moves API orchestration out of individual app platforms and into a controlled execution layer. This can reduce platform-side integration cost, centralize credentials, enforce budgets and create a measurable record of what the infrastructure actually cost to run.

The enterprise value proposition is simple: **measure the customer's current API/middleware execution cost, run approved traffic through SOVRAIL, and produce a before/after savings receipt backed by observed SOVRAIL usage.**

### Core capabilities

1. Scoped WCL-controlled credentials (`sov_...`) with scopes, expiration and revocation.
2. Optional signed requests to reduce tampering and replay risk.
3. Per-asset rate limits, daily request ceilings and upstream budget ceilings.
4. Provider abstraction so consuming apps do not need provider-specific code.
5. Circuit breakers and failover when providers are unhealthy.
6. Idempotency to avoid accidental duplicate paid work.
7. Exact-result caching for safe reusable responses.
8. Constrained third-party proxying rather than unsafe arbitrary URL proxying.
9. Tamper-evident audit records.
10. Usage telemetry for dashboards and enterprise reporting.
11. Automated scaffolding for future WCL assets.
12. Savings estimation and observed-usage savings receipts.

### Enterprise Savings Engine

SOVRAIL now exposes two economic measurement paths:

- `POST /v1/savings/estimate` — models expected savings from customer-supplied baseline pricing and traffic assumptions.
- `POST /v1/savings/receipt` — compares customer-supplied baseline pricing with **actual SOVRAIL usage recorded for a scoped key** over a 1–30 day window.

The receipt returns:

- baseline calls for the selected window
- observed SOVRAIL calls
- observed average latency
- baseline execution cost
- observed SOVRAIL execution cost
- verified savings for the measured window
- annualized savings run rate

This is intentionally designed for pilots with mid-market and enterprise customers that need quantifiable ROI rather than an abstract platform claim.

### Enterprise deployment model

```text
Applications / AI Agents / MCP Clients
                 |
                 v
              SOVRAIL
        -------------------
        Auth | Policy | Cost
        Usage | Audit | ROI
        -------------------
          |      |      |
          v      v      v
       APIs   SaaS   Internal Services
```

SOVRAIL does not need to replace the customer's applications. It becomes the execution and control layer between those applications and downstream services.

### Start locally

```bash
cp .env.example .env
# Set a strong SOVRAIL_MASTER_KEY and optional upstream credentials/models
docker compose up --build
```

Create an asset key:

```bash
curl -X POST http://localhost:8080/admin/keys \
  -H 'Authorization: Bearer YOUR_MASTER_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"name":"enterprise-pilot","scopes":["chat","usage"],"rpm":120,"daily_limit":5000}'
```

Call SOVRAIL:

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H 'x-sovrail-key: sov_YOUR_ASSET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"provider":"auto","messages":[{"role":"user","content":"Hello"}]}'
```

Generate an observed savings receipt:

```bash
curl -X POST http://localhost:8080/v1/savings/receipt \
  -H 'x-sovrail-key: sov_YOUR_ASSET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "baseline_monthly_calls": 100000000,
    "baseline_gateway_cost_per_million": 1.25,
    "sovrail_gateway_cost_per_million": 0.30,
    "window_days": 30,
    "label": "Enterprise Pilot"
  }'
```

### SWARMER + SOVRAIL + KAMERON

**SWARMER** decides whether a capability/provider/tool is trusted and permitted. **SOVRAIL** decides how an approved request is authenticated, budgeted, executed and measured. **KAMERON** preserves trusted task state so interrupted work can resume.

### Production hardening path

SQLite is intentionally retained for a portable single-node package. For multi-instance enterprise deployment, move shared state to PostgreSQL/Redis, terminate TLS at trusted ingress, use managed secret storage, rotate master/upstream credentials, export audit/metrics data, add tenant isolation and SSO/RBAC, and keep SOVRAIL behind SWARMER policy/security inspection where available.

### Economic boundary

SOVRAIL's enterprise thesis is not that every API becomes free. Its measurable claim is narrower and defensible: **where a customer currently pays an application platform, gateway or middleware layer to execute and orchestrate API traffic, SOVRAIL can move that work onto a controlled execution layer and quantify whether that displacement reduces cost.**
