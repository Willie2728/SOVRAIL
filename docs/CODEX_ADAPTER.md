# Codex Adapter Contract

A Codex runner integrates with SOVRAIL's vendor-independent execution governor as follows.

- Create one governor job per objective and declare the maximum credit budget.
- Before each implementation batch, read the governor decision and honor `stop`/`checkpoint` immediately.
- Map `luna-light`, `luna-medium`, `terra`, and `sol` to the model/effort identifiers exposed by the active Codex environment.
- Execute related implementation work as a batch rather than repeatedly prompting for status.
- Report actual credits consumed after each batch. Never estimate credits when authoritative telemetry is available.
- Produce a progress receipt from objective evidence: repository file changes, test changes/passes, durable state changes, or deployment changes.
- Report a normalized failure fingerprint when blocked so repeated failures can be detected.
- If SOVRAIL escalates a blocked subtask, use the recommended tier only for that work. Successful verified progress returns execution to the cheapest default tier.
- Do not represent status commentary, planning text, or repeated repository reads as verified implementation progress.

This contract intentionally does not embed private Codex APIs or invent model identifiers. The concrete runner must use the supported Codex interface available in its deployment environment.
