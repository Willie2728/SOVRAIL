# SOVRAIL AI
## API Gateway Intelligence — Sovereign API Runtime & Integration Layer v2.1

SOVRAIL is the Wilkerson Collective-controlled service boundary between WCL assets and local or third-party APIs. Assets receive SOVRAIL keys and call one stable interface. Provider secrets stay server-side. Local inference can be preferred; paid upstreams remain optional and still require valid provider accounts/credentials.

### Core capabilities

1. Scoped WCL-controlled credentials (`sov_...`) with scopes, expiration and revocation.
2. Optional signed requests to reduce tampering and replay risk.
3. Per-asset rate limits, daily request ceilings and upstream budget ceilings.
4. Local-first routing with optional OpenAI and Anthropic fallback.
5. Circuit breakers and failover when providers are unhealthy.
6. Idempotency to avoid accidental duplicate paid work.
7. Exact-result caching for safe reusable responses.
8. Provider abstraction so consuming apps do not need provider-specific code.
9. Constrained Tavus proxying rather than an unsafe arbitrary URL proxy.
10. Tamper-evident audit records.
11. Usage telemetry for future WCL dashboards.
12. Automated scaffolding for future WCL assets.

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
  -d '{"name":"aurelis","scopes":["chat","usage"],"rpm":120,"daily_limit":5000}'
```

Call SOVRAIL:

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H 'x-sovrail-key: sov_YOUR_ASSET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"provider":"auto","messages":[{"role":"user","content":"Hello"}]}'
```

### Repeated integration

```bash
python scripts/integrate.py /path/to/new-wcl-asset
```

The consuming asset should know only its SOVRAIL URL and its scoped SOVRAIL credential. Do not scatter OpenAI, Anthropic, Tavus or other provider keys across individual products.

### SWARMER + SOVRAIL + KAMERON

**SWARMER** decides whether a capability/provider/tool is trusted and permitted. **SOVRAIL** decides how an approved request is authenticated, budgeted, cached, routed and executed. **KAMERON** preserves trusted task state so interrupted work can resume.

### Production hardening path

SQLite is intentionally retained for a portable single-node package. For multi-instance deployment, move shared state to PostgreSQL/Redis, terminate TLS at trusted ingress, use managed secret storage, rotate master/upstream credentials, export audit/metrics data, and keep SOVRAIL behind SWARMER policy/security inspection where available.

### Economic boundary

SOVRAIL can reduce commercial API usage through local execution, caching, duplicate prevention, budgets and provider selection. It does not bypass third-party authorization or billing. Any request actually executed by a paid provider remains subject to that provider's terms and pricing.
