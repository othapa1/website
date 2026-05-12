"""
Per-question Evidence Chain — one structured item per answered question.

Each item surfaces:
  - what the respondent selected
  - what that implies (the derived variable)
  - what happens if no action is taken (consequence)
  - what a reviewer should check to verify (validation step)
"""
from __future__ import annotations
from scoring.questions import QUESTION_BY_ID


def _get_answer_label(question: dict, answer: dict) -> str:
    """Return the human-readable label for what was selected."""
    if answer.get("is_not_sure"):
        return "Not sure / unclear"
    if answer.get("is_not_yet_implemented"):
        return "Not yet implemented"

    qtype = question.get("type", "radio")

    if qtype == "radio":
        aid = answer.get("answer_id")
        for opt in question.get("options", []):
            if opt["id"] == aid:
                return opt["label"]
        return aid or "Unknown"

    if qtype == "checkbox":
        selected = answer.get("selected_option_ids") or []
        labels = []
        for opt in question.get("options", []):
            if opt["id"] in selected:
                labels.append(opt["label"])
        return ", ".join(labels) if labels else "None selected"

    return str(answer.get("answer_id", ""))


def _interpolate(template: str, answer_label: str) -> str:
    return template.replace("{answer}", answer_label)


def generate_evidence_chain(answers_by_id: dict, stage: str) -> list:
    """
    Returns one evidence-chain item per question that was answered.
    Questions not present in answers_by_id are skipped.
    Items are ordered by question number (q1 … q12).
    """
    chain = []
    ordered_ids = [f"q{i}" for i in range(1, 13)]

    for qid in ordered_ids:
        answer = answers_by_id.get(qid)
        if answer is None:
            continue

        question = QUESTION_BY_ID.get(qid)
        if not question:
            continue

        answer_label = _get_answer_label(question, answer)
        score        = answer.get("score")

        # Wording is stage-specific; fall back to pilot if stage key missing
        wording_key = stage if stage in ("pre_ai", "pilot", "production") else "pilot"
        wording = (
            question.get("wording", {}).get(wording_key)
            or question.get("wording", {}).get("pilot", "")
        )

        evidence_text    = _interpolate(question.get("evidence_template", "{answer}"), answer_label)
        consequence_text = question.get("consequence_template", "")
        validation_text  = question.get("validation_step_template", "")

        chain.append({
            "question_id":            qid,
            "question_wording":       wording,
            "answer_label":           answer_label,
            "score":                  round(score, 1) if score is not None else None,
            "derived_variable":       question.get("derived_variable", ""),
            "evidence":               evidence_text,
            "consequence":            consequence_text,
            "validation_step":        validation_text,
            "is_not_sure":            bool(answer.get("is_not_sure")),
            "is_not_yet_implemented": bool(answer.get("is_not_yet_implemented")),
        })

    return chain
