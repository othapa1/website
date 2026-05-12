"""
Evidence Matrix — five-column table built from top findings.

Columns:
  Input Answers      – which questions drove this finding + what was selected
  Derived Variable   – the construct or metric being measured
  Consequence        – what happens if not addressed
  Severity           – score + label
  Validation Step    – what a reviewer should verify

Used in PDF Page 2 and optionally surfaced in the result screen.
"""
from scoring.questions import QUESTION_BY_ID


def _answer_summary(qid: str, answers_by_id: dict) -> str:
    question = QUESTION_BY_ID.get(qid)
    answer   = answers_by_id.get(qid)
    if not question or not answer:
        return f"{qid.upper()}: (no answer)"

    if answer.get("is_not_sure"):
        return f"{qid.upper()}: Not sure"
    if answer.get("is_not_yet_implemented"):
        return f"{qid.upper()}: Not yet implemented"

    qtype = question.get("type", "radio")

    if qtype == "radio":
        aid = answer.get("answer_id")
        for opt in question.get("options", []):
            if opt["id"] == aid:
                # Truncate long labels to keep table cells readable
                label = opt["label"]
                return f"{qid.upper()}: {label[:80]}{'…' if len(label) > 80 else ''}"
        return f"{qid.upper()}: {aid}"

    if qtype == "checkbox":
        selected = answer.get("selected_option_ids") or []
        labels = []
        for opt in question.get("options", []):
            if opt["id"] in selected:
                labels.append(opt["label"])
        joined = ", ".join(labels) if labels else "None"
        return f"{qid.upper()}: {joined[:80]}{'…' if len(joined) > 80 else ''}"

    return f"{qid.upper()}: {answer.get('answer_id', '')}"


def generate_evidence_matrix(top_findings: list[dict], answers_by_id: dict) -> list[dict]:
    """
    Returns one matrix row per top finding.
    Each row is a dict with keys matching the five column names.
    """
    rows = []
    for finding in top_findings:
        related = finding.get("related_question_ids") or []
        input_answers = "; ".join(
            _answer_summary(qid, answers_by_id) for qid in related
        ) if related else "Derived from overall pattern"

        rows.append({
            "input_answers":    input_answers,
            "derived_variable": finding.get("derived_variable", ""),
            "consequence":      finding.get("consequence", ""),
            "severity_score":   finding.get("severity_score"),
            "severity_label":   finding.get("severity_label", ""),
            "validation_step":  finding.get("validation_step", ""),
            # Pass through for template convenience
            "finding_title":    finding.get("title", ""),
            "finding_id":       finding.get("id", ""),
        })

    return rows
