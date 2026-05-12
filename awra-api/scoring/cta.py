"""
Adaptive Call-to-Action — driven by segment (A/B/C/D).
Returns heading, body copy, and button label from config.
"""
from scoring.config import CTA_COPY


def get_cta(segment: str) -> dict:
    """
    Returns CTA dict: { heading, body, button_label, segment }
    Falls back to D_NURTURE if segment not recognised.
    """
    copy = CTA_COPY.get(segment, CTA_COPY["D_NURTURE"])
    return {
        "heading":      copy["heading"],
        "body":         copy["body"],
        "button_label": copy.get("button_label") or copy.get("button", "Book the Review →"),
        "url":          copy.get("url", "https://lotusnex.com/contact.html"),
        "segment":      segment,
    }
