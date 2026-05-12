"""
Efficiency Dividend — three-point range: Conservative / Expected / Optimistic.

Inputs come from the calculator section of the diagnostic:
  people          – number of people doing the work
  hours_per_week  – average hours each person spends on the targeted workflows
  automation_pct  – what percentage of that time could be automated (0–100)
  hourly_cost     – fully-loaded hourly cost (salary + benefits + overhead)

The base estimate uses the same 70 % realisation factor as the previous single-point
output so that existing prospects see consistent numbers.  Conservative and Optimistic
bracket it symmetrically-ish without overstating.
"""
from scoring.config import (
    DIVIDEND_CONSERVATIVE,
    DIVIDEND_EXPECTED,
    DIVIDEND_OPTIMISTIC,
)


def calculate_efficiency_dividend(
    people: float,
    hours_per_week: float,
    automation_pct: float,
    hourly_cost: float,
) -> dict:
    """
    Returns a dict with:
      base_annual      – gross automatable hours × cost (pre-realisation)
      conservative     – base × 0.50
      expected         – base × 0.70  (matches legacy single-point estimate)
      optimistic       – base × 0.85
      hours_per_week_recovered – expected hrs/wk recovered across the team
      weeks_to_break_even      – None (requires implementation cost input — Phase 2)
      assumptions              – list of human-readable assumption strings
      caveat                   – standard disclaimer string
    """
    # Guard: all inputs must be positive
    people        = max(0.0, float(people))
    hours_per_week = max(0.0, float(hours_per_week))
    automation_pct = max(0.0, min(100.0, float(automation_pct)))
    hourly_cost   = max(0.0, float(hourly_cost))

    annual_hours_available = people * hours_per_week * 52.0
    automatable_hours      = annual_hours_available * (automation_pct / 100.0)
    base_annual            = automatable_hours * hourly_cost

    conservative = round(base_annual * DIVIDEND_CONSERVATIVE)
    expected     = round(base_annual * DIVIDEND_EXPECTED)
    optimistic   = round(base_annual * DIVIDEND_OPTIMISTIC)

    # Weekly time recovered (expected scenario)
    hours_per_week_recovered = round(
        people * hours_per_week * (automation_pct / 100.0) * DIVIDEND_EXPECTED, 1
    )

    assumptions = [
        f"{int(people)} {'person' if people == 1 else 'people'} × "
        f"{hours_per_week} hrs/week on targeted workflows",
        f"{int(automation_pct)}% of that time estimated as automatable",
        f"${hourly_cost:,.0f}/hr fully-loaded cost (salary + benefits + overhead)",
        "Realisation factors: Conservative 50%, Expected 70%, Optimistic 85%",
        "Annual projection based on 52 working weeks",
        "No implementation or ongoing AI operating costs deducted",
    ]

    caveat = (
        "This is a directional estimate, not a guarantee. "
        "Realised savings depend on workflow complexity, change management, "
        "model reliability, and integration depth. "
        "A discovery engagement will produce a tighter, evidence-backed projection."
    )

    return {
        "base_annual":             round(base_annual),
        "conservative":            conservative,
        "expected":                expected,
        "optimistic":              optimistic,
        "hours_per_week_recovered": hours_per_week_recovered,
        "weeks_to_break_even":     None,
        "assumptions":             assumptions,
        "caveat":                  caveat,
    }
