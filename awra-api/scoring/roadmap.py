"""
Stage-specific recommended roadmap — 3–4 phases depending on stage.
Returns the roadmap from config for the given stage.
"""
from scoring.config import ROADMAPS


def get_roadmap(stage: str) -> list[dict]:
    """
    Returns a list of roadmap phase dicts for the given stage.
    Falls back to pilot if stage not found.
    Each dict: { phase, title, description, actions: [str] }
    """
    return ROADMAPS.get(stage, ROADMAPS["pilot"])
