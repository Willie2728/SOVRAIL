"""Source-backed Wisdom Guide framework routing for SOVRAIL assurance.

These entries are advisory lenses based on publicly documented areas of work.
They are not simulations, quotations, endorsements, or claims that the named
people advised Wilkerson Collective Labs.
"""
from __future__ import annotations

from typing import Any

_GUIDES = (
    {
        "name": "Bruce Schneier",
        "title": "Security Engineering & Trust Guide",
        "triggers": ("security", "trust", "threat", "adversarial", "attack", "unauthorized", "privacy", "effect"),
        "lens": "Threat-model incentives and failure modes, minimize implicit trust, and design for resilience when controls fail.",
    },
    {
        "name": "Ron Ross",
        "title": "Cyber Risk & Controls Guide",
        "triggers": ("risk", "control", "authorization", "attestation", "monitor", "assurance", "context", "policy"),
        "lens": "Tie risk decisions to explicit controls, authorization boundaries, evidence, continuous monitoring, and recoverable system states.",
    },
    {
        "name": "Marietje Schaake",
        "title": "Technology Governance & Democracy Guide",
        "triggers": ("governance", "accountability", "authority", "policy", "transparency", "oversight", "tenant", "public"),
        "lens": "Make technology power accountable through transparent authority, reviewable decisions, institutional oversight, and clear rights boundaries.",
    },
    {
        "name": "Geoffrey Hinton",
        "title": "AI Foundations & Critical-Risk Guide",
        "triggers": ("ai", "agent", "model", "autonomy", "autonomous", "learning", "objective"),
        "lens": "Separate demonstrated capability from speculation, constrain unnecessary autonomy and privilege, and preserve monitoring and human override.",
    },
    {
        "name": "Fei-Fei Li",
        "title": "Human-Centered AI & Vision Guide",
        "triggers": ("human", "user", "deployment", "oversight", "impact", "context", "objective"),
        "lens": "Evaluate AI in its real human context, preserve meaningful human agency, and test performance and harms against the actual deployment environment.",
    },
)

_DISCLOSURE = (
    "Wisdom Guides are source-backed framework references only; SOVRAIL does not "
    "impersonate named people, fabricate quotations, or imply endorsement."
)


def relevant_lenses(*values: Any, limit: int = 4) -> dict[str, Any]:
    """Return deterministic advisory lenses relevant to an assurance record."""
    text = " ".join(str(value) for value in values if value is not None).lower()
    selected = [guide for guide in _GUIDES if any(trigger in text for trigger in guide["triggers"])]
    if not selected:
        selected = [_GUIDES[0], _GUIDES[1]]
    selected = selected[: max(1, limit)]
    return {
        "mode": "framework_reference",
        "guides": [
            {"name": guide["name"], "title": guide["title"], "lens": guide["lens"]}
            for guide in selected
        ],
        "disclosure": _DISCLOSURE,
    }
