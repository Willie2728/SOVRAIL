# RUN158 — Buyer-Owned Savings Assumptions

## Customer Truth
The active SOVRAIL Base44 savings calculator opened with a very large preloaded call volume, vendor-set rates, and preset avoidable-work percentages. Even with disclaimers, that creates an avoidable trust problem: the buyer sees a savings result before supplying their own business evidence.

## Creative Strategy
**SOV-TXT-011 — If the model starts with our numbers, it is not your business case.**

Core message: no savings scenario should be preloaded. The buyer supplies the eligible traffic, current cost basis, proposed cost basis, avoidable-work assumptions, attribution method, and service-quality guardrail. Modeled delta remains separate from realized savings.

CTA: open the Buyer-Owned Savings Assumption Card, then define one bounded workflow and the evidence required before a second workflow is considered.

## Production Readiness
**SOV-DOC-006 — Buyer-Owned Savings Assumption Card**

The card asks for:
1. one bounded workflow;
2. eligible traffic volume and evidence source;
3. current fully loaded cost basis;
4. proposed SOVRAIL cost basis;
5. avoidable-work assumptions with evidence sources;
6. attribution method;
7. a non-cost service guardrail;
8. the expansion receipt required before workflow #2.

Base44 changes:
- savings-calculator defaults changed to zero instead of a preloaded scenario;
- headline and claims language changed to buyer-owned assumptions and designed-to language;
- `SavingsScopeSignal` now supports anonymous `session_id`, `content_variant`, runtime `environment`, and `measurement_eligible`;
- repeated copies of the same qualified savings scope are deduplicated per anonymous browser session with retry-safe release on telemetry failure;
- localhost/preview actions are excluded from eligible telemetry;
- `public/marketing/SOV-DOC-006-buyer-owned-savings-assumption-card.html` added.

Final Base44 build: exit 0.
Checkpoint: `6aa314964d18f09bd76a24c9`
Base44 checkpoint commit: `943886be425298af847cfdafae3dda74ab0a2d97`

The connected `Willie2728/SOVRAIL` repository is the Python/runtime repository; current Base44 `src/pages/Home.jsx` is not present there. Marketing content is durable here, but Base44↔GitHub application-source parity is not claimed.

## Distribution Queue
Not externally released. No social post, ad, email campaign, paid spend, or public savings claim is marked live.

## Analytics / Evaluation
Before RUN158 durable writes:
- `SavingsScopeSignal`: **0** records;
- `SavingsPilotRequest`: **0** records.

No conversion, savings, ROI, or payback result is inferred.

## Winner Library
No promotion. `winner=false` until measurement-eligible production evidence supports a decision.

## Claims boundary
A modeled delta is not realized or attributable savings. Savings should not be represented as product-caused until the agreed evidence sources reconcile the eligible workload and material costs, the attribution method supports the comparison, and the selected service-quality guardrail remains acceptable. This run does not establish SOVRAIL pricing, deployment readiness, security performance, customer savings, ROI, or payback.
