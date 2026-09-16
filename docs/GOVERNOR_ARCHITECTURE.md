# Job-level governance architecture

SOVRAIL separates vendor-neutral governance from provider-specific execution.

`Objective -> Governor Job -> Budget/Progress Decision -> Execution Adapter -> Model/Tool -> Progress Receipt -> Governor`

The governor owns economic policy, progress policy, escalation/de-escalation, checkpoints, and autonomous stop conditions. The adapter owns provider authentication, concrete model identifiers, execution, and authoritative usage telemetry. This separation lets SOVRAIL govern Codex or another agent runner without hard-coding one vendor into the core.

## Verified progress

Progress is based on objective evidence rather than conversational activity. Current receipts accept changed source files, changed tests, passing tests, durable state changes, and deployment changes. Status commentary alone is zero progress.

## Economic policy

The default policy starts with the cheapest permitted tier. It becomes progressively more conservative as the declared budget is consumed and stops before the protected reserve is spent. Escalation is triggered by repeated no-progress or repeated failure evidence; verified success returns the job to the cheap default tier.

## Auditability

Job creation and governor decisions are written to SOVRAIL's audit path. Execution receipts are retained as job events so an operator can reconstruct why a tier change or stop decision occurred.
