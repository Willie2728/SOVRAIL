# SOVRAIL AI OS - Agent Identity and Authority Integration

SOVRAIL AI OS is the execution-authority layer of the WCL Autonomous Trust Fabric.

Every consequential agent request should be attributable to an Agent Identification Number (AIN) and a current Agent Operating Credential (AOC). The credential defines owner/operator, delegation lineage, permitted providers, APIs, tools and resources, financial ceilings, rate limits, network scope, credential authority, expiration and lifecycle status.

Rules: reject suspended, revoked, retired or expired credentials; enforce least privilege; prevent child agents exceeding parent authority; force re-attestation after material fingerprint, permission, runtime, dependency, publisher or ownership changes; create signed receipts for consequential external effects; route unauthorized effects to AI SWARMER OS; permit high-risk execution to require SWARMER clearance.

SOVRAIL retains provider abstraction, quotas, budgets, caching controls, failover and intent/context/effect/outcome assurance while adding verifiable agent authority as its execution envelope.

Identity -> Authority -> Execution -> Enforcement -> Recovery.