"""
Generate graded severity findings from answer patterns.
Replaces binary Critical/Warning flags with scored findings (0–100).
"""
from __future__ import annotations
from scoring.config import FINDING_TEMPLATES, DATA_IMPACT_MULTIPLIERS
from scoring.severity import calculate_severity, get_severity_label


def _get_radio_answer_id(answers_by_id: dict, qid: str):
    a = answers_by_id.get(qid)
    if not a:
        return None
    if a.get("is_not_sure") or a.get("is_not_yet_implemented"):
        return "__unsure__"
    return a.get("answer_id")


def _get_radio_score(answers_by_id: dict, qid: str):
    a = answers_by_id.get(qid)
    if not a:
        return None
    return a.get("score")


def _get_selected(answers_by_id: dict, qid: str) -> list:
    a = answers_by_id.get(qid)
    if not a:
        return []
    return a.get("selected_option_ids") or []


def _make_finding(template_id: str, severity_score: float, related_qids: list[str], evidence_note: str) -> dict:
    t = FINDING_TEMPLATES[template_id]
    return {
        "id":                  template_id,
        "title":               t["title"],
        "severity_score":      round(severity_score, 1),
        "severity_label":      get_severity_label(severity_score),
        "related_question_ids": related_qids,
        "derived_variable":    t["derived_variable"],
        "evidence":            evidence_note,
        "consequence":         t["consequence"],
        "validation_step":     t["validation_step"],
    }


def generate_findings(answers_by_id: dict, pillar_scores: dict, construct_scores: dict, stage: str) -> list[dict]:
    findings = []
    q7_selected = _get_selected(answers_by_id, "q7")
    sensitive = any(s in q7_selected for s in ["pii", "financial", "hr", "regulated", "customer_data"])
    q7_multiplier = construct_scores.get("q7_impact_multiplier", 1.0)

    # Impact class for security-related findings: derived from data sensitivity
    sec_impact = max(0.5, 1.5 - q7_multiplier)   # higher multiplier = lower impact class

    # ── Security findings ────────────────────────────────────────────────
    q5_id = _get_radio_answer_id(answers_by_id, "q5")
    q5_score = _get_radio_score(answers_by_id, "q5") or 0

    if q5_id == "no_controls":
        sev = calculate_severity(0, 1.5, stage)
        findings.append(_make_finding(
            "no_tenant_isolation", sev, ["q5"],
            "Q05 → 'No controls in place — all users can reach all content'"
        ))
    elif q5_id == "system_prompt" and sensitive:
        sev = calculate_severity(20, sec_impact, stage)
        findings.append(_make_finding(
            "weak_isolation_sensitive_data", sev, ["q5", "q7"],
            "Q05 → 'Rely on model to respect system prompt' + sensitive data confirmed in scope (Q07)"
        ))

    q6_id = _get_radio_answer_id(answers_by_id, "q6")
    q6_score = _get_radio_score(answers_by_id, "q6") or 0

    if q6_id == "no_external_inputs":
        sev = calculate_severity(0, sec_impact, stage)
        findings.append(_make_finding(
            "no_injection_defense", sev, ["q6", "q7"],
            "Q06 → 'No — and the system accepts external inputs we don't fully control'"
        ))
    elif q6_id == "informal_mitigations" and sensitive:
        sev = calculate_severity(55, sec_impact * 0.8, stage)
        findings.append(_make_finding(
            "system_prompts_only_defense", sev, ["q6"],
            "Q06 → informal mitigations only with sensitive data in scope"
        ))

    # ── Tokenomics findings ───────────────────────────────────────────────
    q8_score = _get_radio_score(answers_by_id, "q8") or 0
    q9_score = _get_radio_score(answers_by_id, "q9") or 0
    q10_selected = _get_selected(answers_by_id, "q10")
    q10_has_controls = any(s != "none" for s in q10_selected)

    if q8_score <= 20 and q9_score <= 30:
        sev = calculate_severity(max(q8_score, q9_score), 1.0, stage)
        findings.append(_make_finding(
            "unmodeled_unit_economics", sev, ["q8", "q9"],
            "Q08 + Q09 → no per-task attribution, scale economics not modeled"
        ))

    if not q10_has_controls and stage in ("pilot", "production"):
        sev = calculate_severity(5, 1.0, stage)
        findings.append(_make_finding(
            "no_cost_controls", sev, ["q10"],
            "Q10 → no token budgets, rate limits, or model routing in place"
        ))
    elif q10_selected and "model_routing" not in q10_selected and stage == "production":
        sev = calculate_severity(35, 0.8, stage)
        findings.append(_make_finding(
            "token_gluttony_risk", sev, ["q10"],
            "Q10 → no model routing — single model handling all task types"
        ))

    # ── Reliability findings ──────────────────────────────────────────────
    q11_id  = _get_radio_answer_id(answers_by_id, "q11")
    q11_score = _get_radio_score(answers_by_id, "q11") or 0
    q12_id  = _get_radio_answer_id(answers_by_id, "q12")
    q12_score = _get_radio_score(answers_by_id, "q12") or 0

    if q11_id == "no_mechanism":
        sev = calculate_severity(0, 1.3, stage)
        findings.append(_make_finding(
            "no_failure_handling", sev, ["q11"],
            "Q11 → 'We don't have a mechanism for this yet'"
        ))
    elif q11_id == "passes_through" and sensitive:
        sev = calculate_severity(20, sec_impact, stage)
        findings.append(_make_finding(
            "failure_handling_mismatch", sev, ["q11", "q7"],
            "Q11 → outputs pass through undetected + sensitive data in scope"
        ))

    if q12_id == "no_observability":
        sev = calculate_severity(0, 1.1, stage)
        findings.append(_make_finding(
            "observability_gap", sev, ["q12"],
            "Q12 → 'No observability yet'"
        ))
    elif q12_id == "basic_logging" and stage == "production":
        sev = calculate_severity(20, 1.0, stage)
        findings.append(_make_finding(
            "observability_gap", sev, ["q12"],
            "Q12 → basic infrastructure logging only in a production system"
        ))

    # ── Process findings ──────────────────────────────────────────────────
    q1_score = _get_radio_score(answers_by_id, "q1") or 0
    q2_score = _get_radio_score(answers_by_id, "q2") or 0
    q3_score = _get_radio_score(answers_by_id, "q3") or 0

    if q1_score <= 35 and q2_score <= 35:
        sev = calculate_severity(min(q1_score, q2_score), 1.0, stage)
        findings.append(_make_finding(
            "automation_theater_risk", sev, ["q1", "q2"],
            "Q01 → high variability + Q02 → slow error detection"
        ))

    if q3_score >= 75:
        # High re-entry tax is a finding/opportunity, not purely a problem
        sev = min(40.0, calculate_severity(100 - q3_score, 0.8, stage))
        findings.append(_make_finding(
            "duplicate_entry_tax", sev, ["q3", "q4"],
            f"Q03 → significant cross-system re-entry burden identified"
        ))

    # ── Meta findings ─────────────────────────────────────────────────────
    evidence_confidence = construct_scores.get("evidence_confidence", 80)
    if evidence_confidence < 40:
        findings.append(_make_finding(
            "low_evidence_confidence",
            severity_score=45.0,
            related_qids=[],
            evidence_note=f"Evidence Confidence scored {round(evidence_confidence)}/100 — multiple uncertain or contradictory answers"
        ))

    nyi_count = sum(
        1 for a in answers_by_id.values()
        if (a or {}).get("is_not_yet_implemented")
    )
    if stage == "production" and nyi_count >= 2:
        findings.append(_make_finding(
            "production_controls_missing",
            severity_score=70.0,
            related_qids=[],
            evidence_note=f"Stage = Production + {nyi_count} controls marked 'not yet implemented'"
        ))

    return findings


def select_top_findings(findings: list[dict]) -> list[dict]:
    """
    All findings with severity ≥ 60, ranked by severity (max 5).
    Padded with highest remaining findings if result is under 3.
    """
    high    = sorted([f for f in findings if f["severity_score"] >= 60], key=lambda f: -f["severity_score"])
    low     = sorted([f for f in findings if f["severity_score"] < 60],  key=lambda f: -f["severity_score"])

    if len(high) >= 3:
        return high[:5]

    combined = high + low
    return combined[:3]


def get_top_strength(pillar_scores: dict, construct_scores: dict) -> dict:
    """Returns the highest-scoring pillar as the top strength."""
    pillar_labels = {
        "process":     "Process Fit",
        "security":    "Security & Isolation",
        "tokenomics":  "Cost & Economics",
        "reliability": "Reliability & Architecture",
    }
    pillar_descriptions = {
        "process":     "Your target workflows show strong consistency and automation potential.",
        "security":    "Your access controls and security posture are well-positioned for production.",
        "tokenomics":  "Your cost attribution and economic controls are production-grade.",
        "reliability": "Your failure handling and observability are strong production foundations.",
    }
    best_pillar = max(pillar_scores, key=lambda p: pillar_scores[p])
    return {
        "pillar":      best_pillar,
        "label":       pillar_labels[best_pillar],
        "score":       pillar_scores[best_pillar],
        "description": pillar_descriptions[best_pillar],
    }
