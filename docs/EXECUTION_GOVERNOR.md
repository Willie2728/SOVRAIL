# SOVRAIL Execution Governor

SOVRAIL 2.4 introduces durable job-level execution governance.

## Purpose

The governor optimizes an entire agentic job against an explicit budget rather than treating every model call independently. It starts at the cheapest permitted tier, measures verified progress, detects repeated failures/no-progress loops, escalates only when needed, de-escalates after successful progress, checkpoints near the budget boundary, and preserves a protected reserve.

## API flow

1. `POST /v1/governor/jobs` creates a governed objective with a total budget.
2. The caller executes the recommended model tier.
3. After an execution batch, `POST /v1/governor/jobs/{job_id}/events` reports credits consumed plus objective progress (changed files, tests, state/deployment changes) and any failure.
4. SOVRAIL returns the next decision: execute, checkpoint, or stop, plus the recommended tier.
5. `GET /v1/governor/jobs/{job_id}` returns durable state and execution receipts.

## Default policy

- Luna Light: default execution tier.
- Luna Medium: first escalation.
- Terra: harder blocked work.
- Sol: exceptional unresolved work.
- 60% budget: conserve.
- 75%: essential-only.
- 85%: checkpoint.
- 90% or protected reserve boundary: stop autonomous spending.
- Successful verified progress de-escalates to Luna Light.
- Repeated identical failures or repeated no-progress receipts trigger escalation.

## Integration boundary

SOVRAIL exposes and persists the governor decisions. A Codex/agent adapter must report actual credit consumption and verified progress and honor the returned model tier/action. Provider-specific model identifiers and Codex session control belong in that adapter; SOVRAIL deliberately keeps the policy engine vendor-independent.
