from scoring.config import CONSTRUCT_TIER_THRESHOLDS, COMPOSITE_TIER_THRESHOLDS


def get_construct_tier(score: float) -> str:
    for threshold, label in CONSTRUCT_TIER_THRESHOLDS:
        if score < threshold:
            return label
    return "Production-Ready"


def get_composite_tier(score: float, stage: str) -> str:
    thresholds = COMPOSITE_TIER_THRESHOLDS.get(stage, COMPOSITE_TIER_THRESHOLDS["pilot"])
    for threshold, label in thresholds:
        if score < threshold:
            return label
    return "Production-Ready"
