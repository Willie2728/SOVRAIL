"""SOVRAIL execution governor.

Cost-aware policy engine for agentic/coding workloads.  It tracks a job budget,
selects the cheapest permitted model tier, detects no-progress/retry loops,
creates checkpoints, and escalates only the blocked subtask.

Provider adapters remain responsible for translating model tiers into concrete
provider/model identifiers and reporting actual usage cost back to this module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import hashlib
import json


class ModelTier(str, Enum):
    LUNA_LIGHT = "luna-light"
    LUNA_MEDIUM = "luna-medium"
    TERRA = "terra"
    SOL = "sol"


MODEL_ORDER = [ModelTier.LUNA_LIGHT, ModelTier.LUNA_MEDIUM, ModelTier.TERRA, ModelTier.SOL]


@dataclass
class GovernorPolicy:
    total_budget: float = 100.0
    conserve_at: float = 0.60
    essential_only_at: float = 0.75
    checkpoint_at: float = 0.85
    autonomous_stop_at: float = 0.90
    protected_reserve: float = 10.0
    max_same_failure: int = 2
    max_no_progress: int = 2
    default_tier: ModelTier = ModelTier.LUNA_LIGHT


@dataclass
class ProgressReceipt:
    changed_files: int = 0
    tests_changed: int = 0
    tests_passed: int = 0
    state_changes: int = 0
    deployment_changes: int = 0
    fingerprint: Optional[str] = None

    @property
    def verified_progress(self) -> int:
        return self.changed_files + self.tests_changed + self.tests_passed + self.state_changes + self.deployment_changes

    def ensure_fingerprint(self) -> str:
        if self.fingerprint:
            return self.fingerprint
        payload = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()


@dataclass
class ExecutionState:
    objective: str
    spent: float = 0.0
    tier: ModelTier = ModelTier.LUNA_LIGHT
    same_failure_count: int = 0
    no_progress_count: int = 0
    last_failure: Optional[str] = None
    last_progress_fingerprint: Optional[str] = None
    checkpoints: list[dict] = field(default_factory=list)


class ExecutionGovernor:
    """Deterministic governor; callers persist ExecutionState between turns."""

    def __init__(self, policy: GovernorPolicy | None = None):
        self.policy = policy or GovernorPolicy()

    def new_job(self, objective: str) -> ExecutionState:
        return ExecutionState(objective=objective, tier=self.policy.default_tier)

    def record_cost(self, state: ExecutionState, credits: float) -> None:
        state.spent += max(0.0, credits)

    def budget_ratio(self, state: ExecutionState) -> float:
        return state.spent / self.policy.total_budget if self.policy.total_budget else 1.0

    def mode(self, state: ExecutionState) -> str:
        ratio = self.budget_ratio(state)
        if ratio >= self.policy.autonomous_stop_at or self.remaining(state) <= self.policy.protected_reserve:
            return "stop"
        if ratio >= self.policy.checkpoint_at:
            return "checkpoint"
        if ratio >= self.policy.essential_only_at:
            return "essential-only"
        if ratio >= self.policy.conserve_at:
            return "conserve"
        return "normal"

    def remaining(self, state: ExecutionState) -> float:
        return max(0.0, self.policy.total_budget - state.spent)

    def may_execute(self, state: ExecutionState) -> bool:
        return self.mode(state) != "stop"

    def record_progress(self, state: ExecutionState, receipt: ProgressReceipt) -> None:
        fp = receipt.ensure_fingerprint()
        if receipt.verified_progress <= 0 or fp == state.last_progress_fingerprint:
            state.no_progress_count += 1
        else:
            state.no_progress_count = 0
            state.same_failure_count = 0
            # Successful work de-escalates to the cheapest tier.
            state.tier = self.policy.default_tier
        state.last_progress_fingerprint = fp

    def record_failure(self, state: ExecutionState, failure: str) -> None:
        normalized = failure.strip().lower()
        if normalized == (state.last_failure or ""):
            state.same_failure_count += 1
        else:
            state.same_failure_count = 1
            state.last_failure = normalized

    def should_reroute(self, state: ExecutionState) -> bool:
        return state.no_progress_count >= self.policy.max_no_progress or state.same_failure_count >= self.policy.max_same_failure

    def escalate(self, state: ExecutionState) -> ModelTier:
        idx = MODEL_ORDER.index(state.tier)
        if idx < len(MODEL_ORDER) - 1:
            state.tier = MODEL_ORDER[idx + 1]
        state.no_progress_count = 0
        state.same_failure_count = 0
        return state.tier

    def checkpoint(self, state: ExecutionState, label: str, receipt: ProgressReceipt | None = None) -> dict:
        item = {
            "label": label,
            "spent": state.spent,
            "remaining": self.remaining(state),
            "tier": state.tier.value,
            "mode": self.mode(state),
            "progress": receipt.__dict__ if receipt else None,
        }
        state.checkpoints.append(item)
        return item

    def decision(self, state: ExecutionState) -> dict:
        if not self.may_execute(state):
            action = "stop"
        elif self.should_reroute(state):
            action = "escalate"
        elif self.mode(state) == "checkpoint":
            action = "checkpoint"
        else:
            action = "execute"
        return {
            "action": action,
            "model_tier": state.tier.value,
            "budget_mode": self.mode(state),
            "spent": state.spent,
            "remaining": self.remaining(state),
            "no_progress_count": state.no_progress_count,
            "same_failure_count": state.same_failure_count,
        }
