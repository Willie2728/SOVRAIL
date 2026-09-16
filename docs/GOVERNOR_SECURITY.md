# Governor security and trust boundaries

- Governor jobs are scoped to the authenticated SOVRAIL key hash; one client cannot retrieve another client's job through the governor API.
- Job/event endpoints require the existing `usage` scope. Production deployments may introduce a dedicated `governor` scope in a later migration.
- The external execution adapter is an untrusted reporter until its receipts are backed by authoritative provider telemetry and repository/test evidence. Do not use self-reported credits for billing.
- `stop` is an authorization boundary for autonomous execution. The adapter must refuse additional autonomous spend after receiving it.
- Never include provider secrets, API keys, source credentials, or raw authentication headers in execution events or audit payloads.
- Failure fingerprints should describe the failure class without embedding secrets or sensitive source content.
- Production rollout must validate restart persistence, concurrent updates, and replay/idempotency behavior before multiple workers mutate the same job.
