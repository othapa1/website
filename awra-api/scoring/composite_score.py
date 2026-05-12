from scoring.config import PILLAR_WEIGHTS


def calculate_composite_score(pillar_scores: dict, stage: str) -> float:
    """
    Pre-AI: process pillar only.
    Pilot / Production: full weighted formula.
    """
    if stage == "pre_ai":
        return round(pillar_scores["process"], 1)

    total = sum(
        pillar_scores[p] * w
        for p, w in PILLAR_WEIGHTS.items()
    )
    return round(total, 1)
