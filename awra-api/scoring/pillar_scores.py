"""
Calculate per-pillar scores from normalized answers.

Q4 and Q7 are excluded from pillar averaging — they produce multipliers instead.
Q10 (checkbox) is scored by count of selected non-null controls.
"""
from __future__ import annotations
import math
from scoring.config import PILLAR_WEIGHTS, UNSURE_FALLBACK
from scoring.questions import QUESTIONS, QUESTION_BY_ID

# Questions excluded from pillar averaging (handled as multipliers or special cases)
MULTIPLIER_QUESTIONS = {"q4", "q7"}


def _score_q10(selected_ids: list[str]) -> float:
    """Q10: scored by count of meaningful controls selected (excludes 'none')."""
    controls = [s for s in selected_ids if s != "none"]
    count = len(controls)
    if count == 0:
        return 5
    if count == 1:
        return 35
    if count == 2:
        return 65
    return 100


def get_question_score(q: dict, answer, stage: str):
    """
    Returns numeric score 0–100 for a single question given the answer and stage.
    Returns None if the question has no answer or is not applicable.
    """
    if answer is None:
        return None

    qid = q["id"]

    # Special handling for checkbox questions
    if q["type"] == "checkbox":
        selected = answer.get("selected_option_ids") or []
        if not selected:
            return None
        if qid == "q10":
            return _score_q10(selected)
        # Q4, Q7: handled as multipliers — return None to exclude from pillar averaging
        return None

    # Radio questions
    if answer.get("is_not_sure") or answer.get("is_not_yet_implemented"):
        return float(UNSURE_FALLBACK.get(q["pillar"], 40))

    answer_id = answer.get("answer_id")
    if not answer_id:
        return None

    for opt in q["options"]:
        if opt["id"] == answer_id:
            score = opt["score_by_stage"].get(stage)
            if score is None:
                # Not applicable for this stage — treat as unsure fallback
                return float(UNSURE_FALLBACK.get(q["pillar"], 40))
            return float(score)

    return None


def calculate_pillar_scores(answers_by_id: dict, stage: str) -> dict:
    """
    Returns {pillar: score} where score is 0–100 (float).
    Pillars without any scoreable answers default to 50.
    """
    pillar_scores_raw: dict[str, list[float]] = {p: [] for p in PILLAR_WEIGHTS}

    for q in QUESTIONS:
        qid = q["id"]
        pillar = q["pillar"]

        if qid in MULTIPLIER_QUESTIONS:
            continue  # Q4, Q7 — handled separately

        answer = answers_by_id.get(qid)
        score = get_question_score(q, answer, stage)
        if score is not None:
            pillar_scores_raw[pillar].append(score)

    return {
        pillar: (
            round(sum(scores) / len(scores), 2) if scores else 50.0
        )
        for pillar, scores in pillar_scores_raw.items()
    }
