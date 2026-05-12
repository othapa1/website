from scoring.config import QUADRANT_COPY

QUADRANT_THRESHOLD = 75.0


def get_quadrant(automation_leverage: float, production_risk: float) -> dict:
    """
    Returns quadrant id, label, and body copy.
    Higher production_risk score = more production-ready (not more risky).
    """
    high_leverage = automation_leverage >= QUADRANT_THRESHOLD
    low_risk      = production_risk >= QUADRANT_THRESHOLD   # >= 75 = production-ready

    if high_leverage and low_risk:
        qid = "HIGH_LEVERAGE_LOW_RISK"
    elif high_leverage and not low_risk:
        qid = "HIGH_LEVERAGE_HIGH_RISK"
    elif not high_leverage and low_risk:
        qid = "LOW_LEVERAGE_LOW_RISK"
    else:
        qid = "LOW_LEVERAGE_HIGH_RISK"

    copy = QUADRANT_COPY[qid]
    return {"id": qid, "label": copy["label"], "body": copy["body"]}
