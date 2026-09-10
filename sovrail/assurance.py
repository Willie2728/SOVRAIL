from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Literal

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/v1/assurance", tags=["assurance"])

_ATTESTATIONS: dict[str, dict[str, Any]] = {}


def _stable_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()


class IntentAttestation(BaseModel):
    actor_id: str
    agent_id: str
    objective: str
    authority_scope: list[str] = []
    max_cost: float | None = Field(None, ge=0)
    expires_at: int | None = None
    approval_evidence: dict[str, Any] = {}


class ContextAttestation(BaseModel):
    agent_id: str
    sources: list[dict[str, Any]]
    authoritative_state_version: str | None = None
    ttl_seconds: int | None = Field(None, ge=0)
    policy_version: str | None = None


class EffectObservation(BaseModel):
    agent_id: str
    action_id: str
    system: str
    resource: str
    before_state: Any = None
    after_state: Any = None
    authorized_effect: bool = False
    external_write: bool = False
    evidence: dict[str, Any] = {}


class OutcomeAttestation(BaseModel):
    agent_id: str
    objective: str
    expected_state: Any
    observed_state: Any
    systems_checked: list[str] = []
    exactly_once: bool = True
    reconciled: bool = True
    recovery_required: bool = False
    evidence: dict[str, Any] = {}


class CacheDecision(BaseModel):
    risk: Literal["low", "medium", "high", "critical"] = "low"
    tenant: str
    authorization_scope_hash: str
    state_version: str | None = None
    cached_state_version: str | None = None
    freshness_seconds: int = Field(0, ge=0)
    ttl_seconds: int = Field(0, ge=0)
    similarity: float = Field(1.0, ge=0, le=1)


def _record(kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    created_at = int(time.time())
    canonical = {"kind": kind, "payload": payload, "created_at": created_at}
    attestation_id = f"att_{_stable_hash(canonical)[:24]}"
    record = {**canonical, "attestation_id": attestation_id, "evidence_hash": _stable_hash(canonical)}
    _ATTESTATIONS[attestation_id] = record
    return record


def _require_master(authorization: str | None) -> None:
    # Secure-main intentionally reuses the existing deployment's master-key contract.
    from .config import settings
    if not settings.master_key or authorization != f"Bearer {settings.master_key}":
        raise HTTPException(401, "Master authorization required")


@router.post("/intent")
def attest_intent(body: IntentAttestation, authorization: str | None = Header(None)):
    _require_master(authorization)
    if body.expires_at and body.expires_at <= int(time.time()):
        raise HTTPException(409, "Intent authorization already expired")
    return _record("intent", body.model_dump())


@router.post("/context")
def attest_context(body: ContextAttestation, authorization: str | None = Header(None)):
    _require_master(authorization)
    stale = any(bool(s.get("stale")) for s in body.sources)
    result = _record("context", {**body.model_dump(), "stale_source_detected": stale})
    result["decision"] = "review" if stale else "allow"
    return result


@router.post("/effect")
def observe_effect(body: EffectObservation, authorization: str | None = Header(None)):
    _require_master(authorization)
    changed = body.before_state != body.after_state or body.external_write
    unauthorized_change = changed and not body.authorized_effect
    result = _record("effect", {**body.model_dump(), "state_changed": changed, "unauthorized_change": unauthorized_change})
    result["decision"] = "block_and_contain" if unauthorized_change else "allow"
    return result


@router.post("/outcome")
def attest_outcome(body: OutcomeAttestation, authorization: str | None = Header(None)):
    _require_master(authorization)
    matched = body.expected_state == body.observed_state
    verified = matched and body.exactly_once and body.reconciled and not body.recovery_required
    result = _record("outcome", {**body.model_dump(), "state_match": matched, "verified": verified})
    result["decision"] = "verified" if verified else "reconcile_or_recover"
    return result


@router.post("/cache-decision")
def cache_decision(body: CacheDecision, authorization: str | None = Header(None)):
    _require_master(authorization)
    stale = body.ttl_seconds == 0 or body.freshness_seconds > body.ttl_seconds
    state_drift = bool(body.state_version and body.cached_state_version and body.state_version != body.cached_state_version)
    if body.risk in {"high", "critical"}:
        decision = "CACHE_FORBIDDEN"
    elif stale or state_drift or body.similarity < 0.95:
        decision = "CACHE_VERIFY"
    else:
        decision = "CACHE_ALLOWED"
    return _record("cache", {**body.model_dump(), "stale": stale, "state_drift": state_drift, "decision": decision})


@router.get("/{attestation_id}")
def get_attestation(attestation_id: str, authorization: str | None = Header(None)):
    _require_master(authorization)
    record = _ATTESTATIONS.get(attestation_id)
    if not record:
        raise HTTPException(404, "Unknown attestation")
    return record
