"""
AWRA scoring engine — orchestrates all sub-modules and returns AwraResult.

Entry point: calculate_awra_result(session: DiagnosticSession) -> AwraResult
"""
from scoring.config          import SCORING_MODEL_VERSION, LOTUSNEX_BASELINE
from scoring.pillar_scores   import calculate_pillar_scores
from scoring.construct_scores import calculate_construct_scores
from scoring.composite_score  import calculate_composite_score
from scoring.tiers            import get_composite_tier, get_construct_tier
from scoring.quadrant         import get_quadrant
from scoring.findings         import generate_findings, select_top_findings, get_top_strength
from scoring.contradictions   import detect_contradictions
from scoring.evidence_chain   import generate_evidence_chain
from scoring.evidence_matrix  import generate_evidence_matrix
from scoring.efficiency_dividend import calculate_efficiency_dividend
from scoring.roadmap          import get_roadmap
from scoring.cta              import get_cta
from scoring.segmentation     import get_segment


# ── helpers ──────────────────────────────────────────────────────────────────

def _count_not_sure(answers_by_id: dict) -> int:
    return sum(
        1 for a in answers_by_id.values()
        if (a or {}).get("is_not_sure")
    )


def _optional_confidence_bonus(intake: dict, calculator_inputs: dict) -> int:
    """
    +10 if monthly AI volume provided, +10 if SLA / uptime SLO provided.
    These are soft signals that the respondent has thought more carefully.
    """
    bonus = 0
    if calculator_inputs.get("monthly_ai_volume") or intake.get("monthly_ai_volume"):
        bonus += 10
    if calculator_inputs.get("sla_target") or intake.get("sla_target"):
        bonus += 10
    return bonus


# ── main orchestrator ─────────────────────────────────────────────────────────

def calculate_awra_result(session: dict) -> dict:
    """
    session keys:
      intake            – dict (name, company, email, role, etc.)
      stage             – "pre_ai" | "pilot" | "production"
      answers           – list[dict] — each dict has id + answer fields
      calculator_inputs – dict (people, hours_per_week, automation_pct, hourly_cost)

    Returns a complete AwraResult dict.
    """
    stage             = session.get("stage", "pilot")
    intake            = session.get("intake", {})
    raw_answers       = session.get("answers", [])
    calculator_inputs = session.get("calculator_inputs") or session.get("calculatorInputs") or {}

    # Normalise answers into a lookup dict keyed by question id
    answers_by_id: dict = {}
    for a in raw_answers:
        qid = a.get("id") or a.get("question_id")
        if qid:
            answers_by_id[qid] = a

    # ── Step 1: pillar scores ────────────────────────────────────────────────
    pillar_scores = calculate_pillar_scores(answers_by_id, stage)

    # ── Step 2: contradictions (needed for evidence_confidence) ──────────────
    contradictions = detect_contradictions(answers_by_id, stage)
    contradiction_count = len(contradictions)

    # ── Step 3: construct scores ─────────────────────────────────────────────
    not_sure_count = _count_not_sure(answers_by_id)
    optional_bonus = _optional_confidence_bonus(intake, calculator_inputs)

    construct_scores = calculate_construct_scores(
        pillar_scores       = pillar_scores,
        answers_by_id       = answers_by_id,
        not_sure_count      = not_sure_count,
        contradiction_count = contradiction_count,
        optional_inputs     = {"bonus": optional_bonus},
    )

    automation_leverage  = construct_scores["automation_leverage"]
    production_risk      = construct_scores["production_risk"]
    economic_confidence  = construct_scores["economic_confidence"]
    evidence_confidence  = construct_scores["evidence_confidence"]

    # ── Step 4: composite score + tiers ─────────────────────────────────────
    composite_score = calculate_composite_score(pillar_scores, stage)
    composite_tier  = get_composite_tier(composite_score, stage)

    construct_tiers = {
        "automation_leverage":  get_construct_tier(automation_leverage),
        "production_risk":      get_construct_tier(production_risk),
        "economic_confidence":  get_construct_tier(economic_confidence),
        "evidence_confidence":  get_construct_tier(evidence_confidence),
    }

    # ── Step 5: quadrant ─────────────────────────────────────────────────────
    quadrant = get_quadrant(automation_leverage, production_risk)

    # ── Step 6: findings ─────────────────────────────────────────────────────
    all_findings  = generate_findings(answers_by_id, pillar_scores, construct_scores, stage)
    top_findings  = select_top_findings(all_findings)
    top_strength  = get_top_strength(pillar_scores, construct_scores)

    # ── Step 7: evidence chain + matrix ─────────────────────────────────────
    evidence_chain  = generate_evidence_chain(answers_by_id, stage)
    evidence_matrix = generate_evidence_matrix(top_findings, answers_by_id)

    # ── Step 8: efficiency dividend ──────────────────────────────────────────
    people          = float(calculator_inputs.get("people", 0) or 0)
    hours_per_week  = float(calculator_inputs.get("hours_per_week", 0) or calculator_inputs.get("hoursPerWeek", 0) or 0)
    automation_pct  = float(calculator_inputs.get("automation_pct", 0) or calculator_inputs.get("automationPct", 0) or 0)
    hourly_cost     = float(calculator_inputs.get("hourly_cost", 0) or calculator_inputs.get("hourlyCost", 0) or 0)

    dividend = calculate_efficiency_dividend(people, hours_per_week, automation_pct, hourly_cost)

    # ── Step 9: roadmap + CTA ────────────────────────────────────────────────
    roadmap = get_roadmap(stage)

    segment = get_segment(
        findings           = top_findings,
        quadrant_id        = quadrant["id"],
        expected_dividend  = dividend["expected"],
        composite_score    = composite_score,
        stage              = stage,
        evidence_confidence = evidence_confidence,
    )

    cta = get_cta(segment)

    # ── Step 10: pillar gap vs LotusNex baseline ─────────────────────────────
    pillar_gaps = {
        pillar: round(score - LOTUSNEX_BASELINE.get(pillar, 75), 1)
        for pillar, score in pillar_scores.items()
    }

    # ── Assemble result ───────────────────────────────────────────────────────
    return {
        "scoring_model_version": SCORING_MODEL_VERSION,
        "stage": stage,

        # Core scores
        "composite_score": composite_score,
        "composite_tier":  composite_tier,
        "pillar_scores":   {k: round(v, 1) for k, v in pillar_scores.items()},
        "pillar_gaps":     pillar_gaps,

        # Construct scores
        "construct_scores": {
            "automation_leverage":  round(automation_leverage, 1),
            "production_risk":      round(production_risk, 1),
            "economic_confidence":  round(economic_confidence, 1),
            "evidence_confidence":  round(evidence_confidence, 1),
        },
        "construct_tiers": construct_tiers,

        # Multipliers (for CRM / debugging)
        "q4_leverage_multiplier":  round(construct_scores.get("q4_leverage_multiplier", 1.0), 3),
        "q4_economic_multiplier":  round(construct_scores.get("q4_economic_multiplier", 1.0), 3),
        "q7_impact_multiplier":    round(construct_scores.get("q7_impact_multiplier", 1.0), 3),

        # Quadrant
        "quadrant": quadrant,

        # Findings
        "findings":       top_findings,
        "all_findings":   all_findings,
        "top_strength":   top_strength,

        # Contradictions / reflection prompts
        "contradictions":      contradictions,
        "contradiction_count": contradiction_count,

        # Evidence
        "evidence_chain":  evidence_chain,
        "evidence_matrix": evidence_matrix,

        # Dividend
        "efficiency_dividend": dividend,

        # Roadmap + CTA
        "roadmap":  roadmap,
        "segment":  segment,
        "cta":      cta,

        # Meta
        "not_sure_count":  not_sure_count,
        "lotusnex_baseline": LOTUSNEX_BASELINE,

        # Pass intake through (for PDF header / CRM)
        "intake": intake,
    }
