"""
Phase 1 contradiction detection — 5 rules.
Each triggered rule reduces Evidence Confidence by 15 and produces a ReflectionPrompt.
"""
from __future__ import annotations


def detect_contradictions(answers_by_id: dict, stage: str) -> list[dict]:
    """
    Returns list of triggered contradiction dicts:
    {id, title, body, related_question_ids, evidence_confidence_penalty}
    """
    contradictions = []

    def get_radio_score(qid: str):
        a = answers_by_id.get(qid)
        if not a or a.get("is_not_sure") or a.get("is_not_yet_implemented"):
            return None
        return a.get("score")

    def get_selected(qid: str) -> list[str]:
        a = answers_by_id.get(qid)
        if not a:
            return []
        return a.get("selected_option_ids") or []

    q1 = get_radio_score("q1")
    q2 = get_radio_score("q2")
    q3 = get_radio_score("q3")
    q4_selected = get_selected("q4")
    q9 = get_radio_score("q9")
    q10_selected = get_selected("q10")
    q11 = get_radio_score("q11")

    # Count "not yet implemented" answers (used for Rule 3)
    nyi_count = sum(
        1 for a in answers_by_id.values()
        if (a or {}).get("is_not_yet_implemented")
    )

    # Rule 1: Consistent inputs, low-bound logic
    if q1 is not None and q2 is not None and q1 >= 75 and q2 <= 40:
        contradictions.append({
            "id": "structured_inputs_unbound_logic",
            "title": "Structured inputs, unbound logic",
            "body": "Your inputs are highly consistent but errors are caught slowly — this usually means the workflow logic is more complex than it appears. The automation scope may need tighter bounding before it is reliable.",
            "related_question_ids": ["q1", "q2"],
            "evidence_confidence_penalty": 15,
        })

    # Rule 2: Minimal re-entry but large workflow inventory
    if q3 is not None and q3 >= 90 and len(q4_selected) >= 3:
        contradictions.append({
            "id": "low_reentry_large_inventory",
            "title": "Few integration gaps, many manual workflows",
            "body": "You reported minimal cross-system re-entry but identified multiple manual workflow categories. The hours may be coming from process logic and judgment calls rather than data movement — which is harder to automate reliably.",
            "related_question_ids": ["q3", "q4"],
            "evidence_confidence_penalty": 15,
        })

    # Rule 3: Production stage + multiple not-yet-implemented
    if stage == "production" and nyi_count >= 2:
        contradictions.append({
            "id": "production_with_missing_controls",
            "title": "Production stage with key controls not yet implemented",
            "body": "You selected Production but indicated several controls are not yet in place. Controls that are acceptable gaps in a prototype become production incidents when the system is live and handling real users.",
            "related_question_ids": [],
            "evidence_confidence_penalty": 15,
        })

    # Rule 4: No failure handling with high-stakes work
    # High stakes proxied by q11 answer being the 0-score option
    if q11 is not None and q11 == 0:
        q7_selected = get_selected("q7")
        high_stakes = any(s in q7_selected for s in ["pii", "financial", "hr", "regulated"])
        if high_stakes:
            contradictions.append({
                "id": "no_failure_handling_high_stakes",
                "title": "No failure handling with significant-consequence work",
                "body": "Your AI handles sensitive data but has no defined failure handling. When the system produces a wrong output, there is no mechanism to catch it before it reaches a downstream record or decision.",
                "related_question_ids": ["q11", "q7"],
                "evidence_confidence_penalty": 15,
            })

    # Rule 5: No cost controls but high cost confidence
    q10_has_controls = any(s != "none" for s in q10_selected)
    q10_score = 0 if not q10_has_controls else None  # approximate
    if q9 is not None and q9 >= 90 and not q10_has_controls:
        contradictions.append({
            "id": "high_cost_confidence_no_controls",
            "title": "Strong cost confidence with no enforcement mechanisms",
            "body": "You reported strong confidence that costs would hold at 10× scale, but no token budgets, rate limits, or model routing are in place. Cost discipline without mechanisms is an assumption, not a control.",
            "related_question_ids": ["q9", "q10"],
            "evidence_confidence_penalty": 15,
        })

    return contradictions
