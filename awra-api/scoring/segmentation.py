"""
Lead segmentation — A/B/C/D — drives CTA copy and CRM routing.

  A_HIGH_URGENCY      – critical finding OR high-leverage / high-risk quadrant
                         OR large dividend OR production system with low score
  B_MEDIUM_URGENCY    – solid dividend OR pilot stage with mid-range score
  C_WORKFLOW_DISCOVERY – low leverage + production-ready quadrant + low evidence confidence
                         (they need better workflow definition before AI)
  D_NURTURE           – everything else
"""


def get_segment(
    findings: list[dict],
    quadrant_id: str,
    expected_dividend: float,
    composite_score: float,
    stage: str,
    evidence_confidence: float,
) -> str:
    has_critical = any(f.get("severity_label") == "Critical" for f in findings)

    if (
        has_critical
        or quadrant_id == "HIGH_LEVERAGE_HIGH_RISK"
        or expected_dividend >= 100_000
        or (stage == "production" and composite_score < 60)
    ):
        return "A_HIGH_URGENCY"

    if expected_dividend >= 25_000 or (stage == "pilot" and 60 <= composite_score <= 74):
        return "B_MEDIUM_URGENCY"

    if (
        quadrant_id == "LOW_LEVERAGE_LOW_RISK"
        and evidence_confidence < 40
    ):
        return "C_WORKFLOW_DISCOVERY"

    return "D_NURTURE"
