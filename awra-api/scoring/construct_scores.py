"""
Calculate the four AWRA construct scores.

Automation Leverage   = process × Q4 leverage multiplier
Production Risk       = (security×0.55 + reliability×0.45) × Q7 impact multiplier
Economic Confidence   = tokenomics × Q4 economic multiplier
Evidence Confidence   = 80 - (not_sure×10) - (contradiction×15) + optional_bonus
"""
from __future__ import annotations
import math
from scoring.config import (
    WORKFLOW_ARCHETYPE_MULTIPLIERS,
    DATA_IMPACT_MULTIPLIERS,
)


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def _geometric_mean(values: list) -> float:
    if not values:
        return 1.0
    product = math.prod(values)
    return product ** (1.0 / len(values))


def get_q4_multipliers(selected_ids: list) -> tuple:
    """
    Accepts a list of selected archetype IDs.
    Returns (leverage_multiplier, economic_multiplier) as a tuple.
    Geometric mean across all known archetypes; defaults to (1.0, 1.0).
    """
    known = [s for s in selected_ids if s in WORKFLOW_ARCHETYPE_MULTIPLIERS]
    if not known:
        return (1.0, 1.0)

    leverage_vals = [WORKFLOW_ARCHETYPE_MULTIPLIERS[s]["leverage"] for s in known]
    economic_vals = [WORKFLOW_ARCHETYPE_MULTIPLIERS[s]["economic"] for s in known]

    return (
        _geometric_mean(leverage_vals),
        _geometric_mean(economic_vals),
    )


def get_q7_impact_multiplier(selected_ids: list) -> float:
    """
    Accepts a list of selected data sensitivity category IDs.
    Returns the minimum (strictest) impact multiplier.
    Defaults to 1.0 if nothing meaningful is selected.
    """
    known = [s for s in selected_ids if s in DATA_IMPACT_MULTIPLIERS]
    if not known:
        return 1.0
    return min(DATA_IMPACT_MULTIPLIERS[s] for s in known)


def _get_q4_from_answers(answers_by_id: dict) -> tuple:
    answer = answers_by_id.get("q4")
    selected = (answer or {}).get("selected_option_ids") or []
    return get_q4_multipliers(selected)


def _get_q7_from_answers(answers_by_id: dict) -> float:
    answer = answers_by_id.get("q7")
    selected = (answer or {}).get("selected_option_ids") or []
    return get_q7_impact_multiplier(selected)


def get_optional_confidence_bonus(optional_inputs) -> int:
    if not optional_inputs:
        return 0
    # Support raw bonus value passed directly from engine
    if isinstance(optional_inputs, dict) and "bonus" in optional_inputs:
        return int(optional_inputs["bonus"])
    has_volume = optional_inputs.get("monthly_workflow_volume") is not None
    has_sla    = bool(optional_inputs.get("current_sla_or_turnaround_time"))
    if has_volume and has_sla:
        return 20
    if has_volume or has_sla:
        return 10
    return 0


def calculate_construct_scores(
    pillar_scores: dict,
    answers_by_id: dict,
    not_sure_count: int,
    contradiction_count: int,
    optional_inputs=None,
) -> dict:
    """
    Returns a flat dict:
      automation_leverage, production_risk, economic_confidence, evidence_confidence,
      q4_leverage_multiplier, q4_economic_multiplier, q7_impact_multiplier,
      q7_impact_multiplier (float scalar, for engine)
    """
    q4_lev, q4_eco = _get_q4_from_answers(answers_by_id)
    q7             = _get_q7_from_answers(answers_by_id)
    optional_bonus = get_optional_confidence_bonus(optional_inputs)

    automation_leverage = _clamp(pillar_scores["process"] * q4_lev)
    production_risk     = _clamp(
        (pillar_scores["security"] * 0.55 + pillar_scores["reliability"] * 0.45) * q7
    )
    economic_confidence = _clamp(pillar_scores["tokenomics"] * q4_eco)
    evidence_confidence = _clamp(
        80
        - (not_sure_count * 10)
        - (contradiction_count * 15)
        + optional_bonus
    )

    return {
        "automation_leverage":   round(automation_leverage, 1),
        "production_risk":       round(production_risk, 1),
        "economic_confidence":   round(economic_confidence, 1),
        "evidence_confidence":   round(evidence_confidence, 1),
        "q4_leverage_multiplier": round(q4_lev, 3),
        "q4_economic_multiplier": round(q4_eco, 3),
        "q7_impact_multiplier":   round(q7, 3),
    }
