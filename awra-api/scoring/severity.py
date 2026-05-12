from scoring.config import SEVERITY_THRESHOLDS, WORKFLOW_EXPOSURE_BY_STAGE


def get_severity_label(score: float) -> str:
    for threshold, label in SEVERITY_THRESHOLDS:
        if score >= threshold:
            return label
    return "Note"


def calculate_severity(
    question_score: float,
    impact_class: float,
    stage: str,
) -> float:
    """
    severity = control_weakness × impact_class × workflow_exposure × 100
    Clamped to 0–100.
    """
    control_weakness  = (100.0 - question_score) / 100.0
    workflow_exposure = WORKFLOW_EXPOSURE_BY_STAGE.get(stage, 0.8)
    raw = control_weakness * impact_class * workflow_exposure * 100.0
    return round(max(0.0, min(100.0, raw)), 1)
