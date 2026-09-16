# Execution Governor release checklist

Before merging/deploying the governor integration:

- Run the complete pytest suite in a clean environment.
- Confirm database migration is non-destructive against an existing SOVRAIL database.
- Create a scoped key with `usage` permission and verify governor job creation.
- Submit progress, failure, and credit receipts and verify persistence after process restart.
- Verify 60/75/85/90 percent budget transitions and protected reserve behavior.
- Verify two repeated no-progress/failure receipts cause selective escalation.
- Verify successful progress de-escalates to the default cheap tier.
- Verify stopped jobs cannot be treated as authorized autonomous execution by the external runner.
- Verify audit records contain governor creation/decision events without secrets.
- Verify Codex adapter uses authoritative credit telemetry and supported model identifiers.
- Verify end-to-end runner honors execute/checkpoint/stop decisions before enabling production autonomy.

Do not label the governor production-live until these checks pass in the deployed environment.
