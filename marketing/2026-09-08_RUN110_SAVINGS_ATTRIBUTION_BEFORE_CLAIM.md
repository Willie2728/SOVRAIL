# RUN110 — SOVRAIL Savings Attribution Before Claim

**Asset ID:** SOV-TXT-103  
**Status:** Production-ready; unpublished; untested against a live customer workload.

## Customer truth

A before/after cost delta is not automatically caused by SOVRAIL. A credible enterprise savings claim needs a bounded workload, baseline evidence, a buyer-agreed attribution method, and an inspectable receipt that separates product effects from traffic, pricing, seasonality, or provider changes.

## Creative strategy

**Hook:** A savings receipt needs more than a before/after delta.  
**CTA:** Define the baseline, attribution method, and receipt before the call.

The qualified pilot flow now asks buyers to choose an attribution approach before contact: matched period, normalized baseline, holdout/shadow comparison, provider-invoice reconciliation, or “not decided yet.” The last option is intentionally allowed as a readiness gap, but the copy says it must be resolved before claiming attributable savings.

## Production readiness

Base44 app: `Saurell Insight` (current SOVRAIL commercial UI)  
Changed file: `src/pages/Home.jsx`

Changes include:
- attribution method added to `SavingsPilotRequest` and anonymous `SavingsScopeSignal`;
- copied One-Workflow Savings Evidence Brief now carries the attribution method;
- fixed “two-week pilot / 30-day baseline” language replaced by buyer-defined bounded measurement planning;
- before/after language explicitly disclaims causality without an agreed attribution method.

Build verification: `npm run build` exited 0.  
Base44 checkpoint: `6aa08c1aa44e385cd0146717`  
Base44 checkpoint commit: `e1b5280cda2bd70118591a80405b570024ab601f`

## Analytics / evaluation

RUN110 baseline readback: 0 `SavingsScopeSignal` records and 0 `SavingsPilotRequest` records. Empty telemetry is not interpreted as zero demand. A future savings claim requires measured eligible workload data and the agreed attribution method; modeled calculator output is not realized savings.

## Distribution / winner library

Queue for owned enterprise product surfaces only until authenticated external distribution and analytics receipts exist. No post, ad, email, pilot, deployment, realized savings, revenue, ROI, or winner is claimed by this record.