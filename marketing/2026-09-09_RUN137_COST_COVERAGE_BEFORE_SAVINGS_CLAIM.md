# RUN137 — SOVRAIL AI
## SOV-TXT-009 / SOV-DOC-004 — Cost Coverage Before a Savings Claim

### Customer Truth
An observed request count is useful evidence, but it is not the same thing as fully loaded observed cost. A cost comparison becomes commercially credible only when the customer baseline, the compared workload, and the material cost sources are all defined clearly enough to reconcile.

### Creative Strategy
**Hook:** Do not sell a savings percentage before you know what the receipt actually covers.

**Deployable copy:**
> API savings are easy to model and harder to prove. Start with one comparable workload. Record the customer baseline. Observe the SOVRAIL request volume. Reconcile the provider, gateway, compute, network, support, and fixed-cost sources that materially belong in the comparison. Then show the buyer the receipt and the gaps. If cost coverage is incomplete, call it a modeled comparison—not verified savings.

**CTA:** Bring one API or middleware workload and define the baseline + cost boundary before discussing ROI.

### Production Readiness
The SOVRAIL README was updated during RUN137 to distinguish observed usage from fully loaded observed cost, label savings output as a modeled comparison until cost coverage/workload comparability are established, and document that the current legacy runtime field `verified_window_savings` should not be used as proof of verified customer savings while upstream/provider costs may be absent from the usage log.

### Distribution Queue
Text/document asset is ready for owned-site or sales-enablement use. No external post, ad, email, or campaign is claimed live.

### Analytics / Evaluation
No customer savings result is inferred. A future evaluation should compare a bounded, materially comparable workload and reconcile material cost sources to actual billing/usage evidence before promotion to a quantified proof point.

### Winner Library
No winner. There is no attributable distribution/performance sample for SOV-TXT-009.

### Build Liaison
The runtime endpoint currently returns a field named `verified_window_savings`, while the inspected request paths can write `cost_micros=0` when upstream/provider billing has not been reconciled. Runtime naming/semantics remain an engineering blocker to resolve before that field is used in customer-facing proof.

### Claims Boundary
SOVRAIL can record scoped request usage and model comparisons from supplied assumptions. That does not establish a customer's fully loaded savings, future savings, ROI, or payback without reconciled cost coverage and comparable workload evidence.
