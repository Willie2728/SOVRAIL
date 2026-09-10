# RUN144 — SOVRAIL AI

## Customer Truth
Observed request count is not the same thing as fully loaded observed cost. The current SOVRAIL runtime can log upstream request cost as zero, while `/v1/savings/receipt` still exposes a legacy field named `verified_window_savings`. Until workload comparability and material cost sources are reconciled, that number must not be sold as verified customer savings.

## Creative Strategy
**SOV-TXT-010 — “Name the missing cost source before you name the savings number.”**

Qualified economic conversations should start with a cost-coverage receipt rather than an ROI headline. The buyer should be able to see which inputs are customer-supplied, which SOVRAIL values are observed, which material cost categories are reconciled, and which remain missing.

## Production Readiness
**SOV-DOC-005 — Coverage Gap Receipt**

Before a savings number is used in sales or marketing, record:
1. baseline workload definition and comparison window;
2. SOVRAIL workload comparability status;
3. provider/API billing coverage;
4. gateway or middleware cost coverage;
5. compute/network cost coverage where material;
6. support/operations and fixed-cost coverage where material;
7. source/receipt for each reconciled cost category;
8. unresolved cost categories;
9. evidence state: `modeled_partial_cost` until the material boundary is reconciled.

The existing README already states this boundary. This RUN144 asset makes it a buyer-facing qualification rule; it does not change the runtime response schema.

## Distribution Queue
Owned GitHub sales-enablement artifact only. No external post, ad, email campaign, or paid distribution is claimed.

## Analytics / Evaluation
The economic success criterion is not “lower number returned by the endpoint.” It is a comparable workload plus a cost-coverage record sufficient for a buyer to audit the comparison. No customer savings, ROI, payback, or conversion lift is verified in this run.

## Winner Library
No winner promoted. This asset remains a challenger until a real, attributable customer evaluation produces a reconciled receipt.

## Build Liaison
GitHub issue #1 remains open because runtime semantics are not fully reconciled: the API still returns the legacy `verified_window_savings` field, request paths can write `cost_micros=0`, and the current test file does not include savings-receipt coverage tests. Do not use that runtime field as customer-facing verified proof until the issue is resolved.

No production deployment or customer economics are claimed.