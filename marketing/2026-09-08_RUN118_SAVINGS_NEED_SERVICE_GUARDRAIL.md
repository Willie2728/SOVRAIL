# SOVRAIL RUN118 — Savings Need a Service-Quality Guardrail

**Asset:** SOV-TXT-104  
**Customer Truth:** Savings do not count if service quality degrades.

## Creative strategy

SOVRAIL already asks a buyer to define baseline evidence, an attribution method and a success receipt before sharing contact. RUN118 adds the missing non-cost condition: what must remain acceptable while the workflow gets cheaper?

**Hook:** A cheaper workflow is not a win if reliability gets worse.

**Body:** Before calling a cost delta a win, predeclare one service-quality guardrail: latency budget, error-rate ceiling, reliability/availability SLO, output-quality threshold, human-rework ceiling, or explicitly unresolved. Then measure the savings and the guardrail together.

**CTA:** Name one service-quality guardrail before you claim savings.

## Production readiness

`SavingsScopeSignal` and `SavingsPilotRequest` now require a structured `quality_guardrail`. The no-contact savings brief includes it, the contact gate requires it, and the decision rule now says savings should not be represented as attributable realized savings unless the required receipt and attribution method support the claim **and the selected service-quality guardrail remains acceptable**.

This change does not claim that SOVRAIL currently meets any SLO, latency target, error-rate ceiling, output-quality threshold or rework target. It is a buyer-defined evaluation criterion.

## Analytics / evaluation

Verified RUN118 baseline before change: **0 SavingsScopeSignal records and 0 SavingsPilotRequest records**. No realized savings, causality, reliability improvement, service-quality result, pilot acceptance, deployment or ROI is inferred from build success or empty telemetry.

## Distribution state

No RUN118 post, ad, email or video is claimed published. External attributable distribution remains blocked until a connected destination returns a provider/publication receipt.
