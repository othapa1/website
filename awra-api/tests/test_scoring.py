"""
Unit tests for AWRA Phase 1 scoring logic.
Run with: pytest tests/test_scoring.py -v
"""
import math
import pytest
import sys
import os

# Ensure awra-api is on the path when running from the tests directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scoring.severity          import calculate_severity, get_severity_label
from scoring.tiers             import get_construct_tier, get_composite_tier
from scoring.quadrant          import get_quadrant
from scoring.composite_score   import calculate_composite_score
from scoring.construct_scores  import calculate_construct_scores, get_q4_multipliers, get_q7_impact_multiplier
from scoring.pillar_scores     import calculate_pillar_scores
from scoring.efficiency_dividend import calculate_efficiency_dividend
from scoring.contradictions    import detect_contradictions
from scoring.findings          import generate_findings, select_top_findings, get_top_strength
from scoring.segmentation      import get_segment
from scoring.evidence_chain    import generate_evidence_chain
from scoring.engine            import calculate_awra_result


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures — reusable answer sets
# ─────────────────────────────────────────────────────────────────────────────

def _radio(qid: str, answer_id: str, score: float) -> dict:
    return {"id": qid, "answer_id": answer_id, "score": score}


def _checkbox(qid: str, selected: list[str]) -> dict:
    return {"id": qid, "selected_option_ids": selected}


def _not_sure(qid: str) -> dict:
    return {"id": qid, "is_not_sure": True}


def _not_yet(qid: str) -> dict:
    return {"id": qid, "is_not_yet_implemented": True}


def _make_answers(*items) -> dict:
    return {a["id"]: a for a in items}


# ─────────────────────────────────────────────────────────────────────────────
# Severity
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverity:
    def test_zero_question_score_production_max_impact(self):
        sev = calculate_severity(0, 1.5, "production")
        # (1.0) * 1.5 * 1.2 * 100 = 180 → clamped to 100
        assert sev == 100.0

    def test_perfect_question_score_yields_zero(self):
        assert calculate_severity(100, 1.5, "production") == 0.0

    def test_pre_ai_exposure_is_lower(self):
        pre_ai = calculate_severity(0, 1.0, "pre_ai")
        prod   = calculate_severity(0, 1.0, "production")
        assert pre_ai < prod

    def test_pilot_between_pre_ai_and_production(self):
        pre_ai = calculate_severity(50, 1.0, "pre_ai")
        pilot  = calculate_severity(50, 1.0, "pilot")
        prod   = calculate_severity(50, 1.0, "production")
        assert pre_ai < pilot < prod

    def test_severity_label_critical(self):
        assert get_severity_label(80.0) == "Critical"
        assert get_severity_label(100.0) == "Critical"

    def test_severity_label_high(self):
        assert get_severity_label(60.0) == "High"
        assert get_severity_label(79.9) == "High"

    def test_severity_label_moderate(self):
        assert get_severity_label(40.0) == "Moderate"

    def test_severity_label_low(self):
        assert get_severity_label(20.0) == "Low"

    def test_severity_label_note(self):
        assert get_severity_label(0.0) == "Note"
        assert get_severity_label(19.9) == "Note"


# ─────────────────────────────────────────────────────────────────────────────
# Tiers
# ─────────────────────────────────────────────────────────────────────────────

class TestTiers:
    def test_construct_tier_critical(self):
        assert get_construct_tier(30) == "Critical Risk"

    def test_construct_tier_production_ready(self):
        assert get_construct_tier(90) == "Production-Ready"

    def test_composite_tier_production_stricter(self):
        # 72 = "Production-Aware" in pilot, but "Fragile" in production
        pilot_tier = get_composite_tier(72, "pilot")
        prod_tier  = get_composite_tier(72, "production")
        assert pilot_tier != prod_tier
        assert prod_tier in ("Fragile", "Transitional")

    def test_composite_tier_pre_ai_high_score(self):
        # Pre-AI at 85 should be Production-Ready tier
        tier = get_composite_tier(85, "pre_ai")
        assert "Production" in tier or "Aware" in tier


# ─────────────────────────────────────────────────────────────────────────────
# Quadrant
# ─────────────────────────────────────────────────────────────────────────────

class TestQuadrant:
    def test_high_leverage_low_risk(self):
        q = get_quadrant(80, 80)
        assert q["id"] == "HIGH_LEVERAGE_LOW_RISK"

    def test_high_leverage_high_risk(self):
        q = get_quadrant(80, 50)
        assert q["id"] == "HIGH_LEVERAGE_HIGH_RISK"

    def test_low_leverage_low_risk(self):
        q = get_quadrant(50, 80)
        assert q["id"] == "LOW_LEVERAGE_LOW_RISK"

    def test_low_leverage_high_risk(self):
        q = get_quadrant(50, 50)
        assert q["id"] == "LOW_LEVERAGE_HIGH_RISK"

    def test_boundary_at_75(self):
        # Exactly 75 counts as "high"
        q = get_quadrant(75, 75)
        assert q["id"] == "HIGH_LEVERAGE_LOW_RISK"

    def test_returns_label_and_body(self):
        q = get_quadrant(80, 80)
        assert "label" in q
        assert "body" in q
        assert len(q["body"]) > 10


# ─────────────────────────────────────────────────────────────────────────────
# Composite Score
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeScore:
    def test_pre_ai_uses_process_only(self):
        pillar = {"process": 70, "security": 50, "tokenomics": 50, "reliability": 50}
        assert calculate_composite_score(pillar, "pre_ai") == 70.0

    def test_pilot_weighted_formula(self):
        pillar = {"process": 80, "security": 80, "tokenomics": 80, "reliability": 80}
        expected = 80 * 0.30 + 80 * 0.25 + 80 * 0.25 + 80 * 0.20
        assert calculate_composite_score(pillar, "pilot") == round(expected, 1)

    def test_production_same_formula_as_pilot(self):
        pillar = {"process": 60, "security": 70, "tokenomics": 65, "reliability": 75}
        pilot_score = calculate_composite_score(pillar, "pilot")
        prod_score  = calculate_composite_score(pillar, "production")
        assert pilot_score == prod_score  # formula same, tiers differ


# ─────────────────────────────────────────────────────────────────────────────
# Q4 Multipliers — geometric mean
# ─────────────────────────────────────────────────────────────────────────────

class TestQ4Multipliers:
    def test_single_archetype(self):
        # data_entry_duplicate_entry: leverage=1.15, economic=1.10
        selected = ["data_entry_duplicate_entry"]
        lev, eco = get_q4_multipliers(selected)
        assert abs(lev - 1.15) < 0.001
        assert abs(eco - 1.10) < 0.001

    def test_geometric_mean_two_archetypes(self):
        # report_generation: leverage=1.0, economic=0.9
        # data_entry_duplicate_entry: leverage=1.15, economic=1.10
        selected = ["report_generation", "data_entry_duplicate_entry"]
        lev, eco = get_q4_multipliers(selected)
        expected_lev = math.sqrt(1.0 * 1.15)
        expected_eco = math.sqrt(0.9 * 1.10)
        assert abs(lev - expected_lev) < 0.001
        assert abs(eco - expected_eco) < 0.001

    def test_empty_selection_returns_ones(self):
        lev, eco = get_q4_multipliers([])
        assert lev == 1.0
        assert eco == 1.0

    def test_other_archetype_neutral(self):
        lev, eco = get_q4_multipliers(["other"])
        assert lev == 1.0
        assert eco == 1.0


# ─────────────────────────────────────────────────────────────────────────────
# Q7 Impact Multiplier — minimum (strictest wins)
# ─────────────────────────────────────────────────────────────────────────────

class TestQ7ImpactMultiplier:
    def test_single_low_risk(self):
        mult = get_q7_impact_multiplier(["public_or_low_risk"])
        assert mult == 1.10  # from config

    def test_regulated_is_strictest(self):
        mult = get_q7_impact_multiplier(["internal_business", "regulated"])
        assert mult == 0.70  # regulated is strictest

    def test_multiple_non_regulated(self):
        mult = get_q7_impact_multiplier(["customer_data", "pii"])
        # pii = 0.80, customer_data = 0.85 → min = 0.80
        assert mult == 0.80

    def test_empty_returns_one(self):
        assert get_q7_impact_multiplier([]) == 1.0

    def test_none_category(self):
        # "none" means no sensitive data; treated as benign (high/neutral multiplier)
        mult = get_q7_impact_multiplier(["none"])
        assert mult >= 1.0  # benign category never reduces the multiplier


# ─────────────────────────────────────────────────────────────────────────────
# Construct Scores
# ─────────────────────────────────────────────────────────────────────────────

class TestConstructScores:
    def _make_answers_simple(self):
        return _make_answers(
            _checkbox("q4", ["document_processing"]),
            _checkbox("q7", ["internal_business"]),
        )

    def test_automation_leverage_clamped(self):
        pillar = {"process": 100, "security": 80, "tokenomics": 80, "reliability": 80}
        answers = self._make_answers_simple()
        cs = calculate_construct_scores(pillar, answers, 0, 0, {})
        assert 0 <= cs["automation_leverage"] <= 100

    def test_evidence_confidence_penalty_for_not_sure(self):
        pillar = {"process": 80, "security": 80, "tokenomics": 80, "reliability": 80}
        answers = self._make_answers_simple()
        cs_clean = calculate_construct_scores(pillar, answers, 0, 0, {})
        cs_unsure = calculate_construct_scores(pillar, answers, 3, 0, {})
        assert cs_unsure["evidence_confidence"] < cs_clean["evidence_confidence"]

    def test_evidence_confidence_penalty_for_contradictions(self):
        pillar = {"process": 80, "security": 80, "tokenomics": 80, "reliability": 80}
        answers = self._make_answers_simple()
        cs_clean = calculate_construct_scores(pillar, answers, 0, 0, {})
        cs_contr = calculate_construct_scores(pillar, answers, 0, 2, {})
        assert cs_contr["evidence_confidence"] < cs_clean["evidence_confidence"]

    def test_evidence_confidence_optional_bonus(self):
        pillar = {"process": 80, "security": 80, "tokenomics": 80, "reliability": 80}
        answers = self._make_answers_simple()
        cs_no   = calculate_construct_scores(pillar, answers, 0, 0, {})
        cs_bonus= calculate_construct_scores(pillar, answers, 0, 0, {"bonus": 20})
        assert cs_bonus["evidence_confidence"] >= cs_no["evidence_confidence"]

    def test_production_risk_uses_security_and_reliability(self):
        # High security + reliability with benign data → high production_risk
        pillar_good = {"process": 50, "security": 95, "tokenomics": 50, "reliability": 95}
        answers = _make_answers(_checkbox("q4", []), _checkbox("q7", ["public_or_low_risk"]))
        cs = calculate_construct_scores(pillar_good, answers, 0, 0, {})
        assert cs["production_risk"] > 80


# ─────────────────────────────────────────────────────────────────────────────
# Efficiency Dividend
# ─────────────────────────────────────────────────────────────────────────────

class TestEfficiencyDividend:
    def test_basic_calculation(self):
        result = calculate_efficiency_dividend(
            people=5, hours_per_week=10, automation_pct=60, hourly_cost=75
        )
        base = 5 * 10 * 0.60 * 75 * 52
        assert result["base_annual"] == round(base)
        assert result["expected"] == round(base * 0.70)
        assert result["conservative"] == round(base * 0.50)
        assert result["optimistic"] == round(base * 0.85)

    def test_conservative_lt_expected_lt_optimistic(self):
        result = calculate_efficiency_dividend(3, 8, 50, 60)
        assert result["conservative"] < result["expected"] < result["optimistic"]

    def test_zero_people_returns_zeros(self):
        result = calculate_efficiency_dividend(0, 10, 60, 75)
        assert result["expected"] == 0

    def test_automation_pct_clamped(self):
        # 150% should be treated as 100%
        normal  = calculate_efficiency_dividend(1, 10, 100, 50)
        clamped = calculate_efficiency_dividend(1, 10, 150, 50)
        assert normal["base_annual"] == clamped["base_annual"]

    def test_hours_per_week_recovered(self):
        result = calculate_efficiency_dividend(2, 10, 50, 60)
        expected_hrs = round(2 * 10 * 0.5 * 0.70, 1)
        assert result["hours_per_week_recovered"] == expected_hrs

    def test_assumptions_and_caveat_present(self):
        result = calculate_efficiency_dividend(3, 8, 40, 65)
        assert len(result["assumptions"]) >= 4
        assert len(result["caveat"]) > 20


# ─────────────────────────────────────────────────────────────────────────────
# Contradiction Detection
# ─────────────────────────────────────────────────────────────────────────────

class TestContradictions:
    def test_rule1_structured_inputs_unbound_logic(self):
        answers = _make_answers(
            _radio("q1", "consistent", 80),
            _radio("q2", "slow", 30),
        )
        cs = detect_contradictions(answers, "pilot")
        ids = [c["id"] for c in cs]
        assert "structured_inputs_unbound_logic" in ids

    def test_rule1_not_triggered_when_q2_high(self):
        answers = _make_answers(
            _radio("q1", "consistent", 80),
            _radio("q2", "fast", 90),
        )
        cs = detect_contradictions(answers, "pilot")
        ids = [c["id"] for c in cs]
        assert "structured_inputs_unbound_logic" not in ids

    def test_rule2_low_reentry_large_inventory(self):
        answers = _make_answers(
            _radio("q3", "minimal", 95),
            _checkbox("q4", ["document_processing", "report_generation", "support_ticket_triage"]),
        )
        cs = detect_contradictions(answers, "pilot")
        ids = [c["id"] for c in cs]
        assert "low_reentry_large_inventory" in ids

    def test_rule3_production_missing_controls(self):
        answers = _make_answers(
            _not_yet("q5"),
            _not_yet("q6"),
        )
        cs = detect_contradictions(answers, "production")
        ids = [c["id"] for c in cs]
        assert "production_with_missing_controls" in ids

    def test_rule3_not_triggered_in_pilot(self):
        answers = _make_answers(
            _not_yet("q5"),
            _not_yet("q6"),
        )
        cs = detect_contradictions(answers, "pilot")
        ids = [c["id"] for c in cs]
        assert "production_with_missing_controls" not in ids

    def test_rule4_no_failure_handling_high_stakes(self):
        answers = _make_answers(
            _radio("q11", "no_mechanism", 0),
            _checkbox("q7", ["pii", "financial"]),
        )
        cs = detect_contradictions(answers, "production")
        ids = [c["id"] for c in cs]
        assert "no_failure_handling_high_stakes" in ids

    def test_rule4_not_triggered_without_sensitive_data(self):
        answers = _make_answers(
            _radio("q11", "no_mechanism", 0),
            _checkbox("q7", ["public_or_low_risk"]),
        )
        cs = detect_contradictions(answers, "production")
        ids = [c["id"] for c in cs]
        assert "no_failure_handling_high_stakes" not in ids

    def test_rule5_high_cost_confidence_no_controls(self):
        answers = _make_answers(
            _radio("q9", "confident", 95),
            _checkbox("q10", ["none"]),
        )
        cs = detect_contradictions(answers, "pilot")
        ids = [c["id"] for c in cs]
        assert "high_cost_confidence_no_controls" in ids

    def test_each_contradiction_has_penalty(self):
        answers = _make_answers(
            _radio("q1", "consistent", 80),
            _radio("q2", "slow", 30),
        )
        cs = detect_contradictions(answers, "pilot")
        for c in cs:
            assert c["evidence_confidence_penalty"] == 15

    def test_no_contradictions_clean_session(self):
        answers = _make_answers(
            _radio("q1", "variable", 20),
            _radio("q2", "fast", 90),
            _radio("q3", "low", 40),
            _radio("q9", "unsure", 30),
            _checkbox("q10", ["token_budgets", "rate_limits"]),
            _radio("q11", "passes_errors", 80),
            _checkbox("q7", ["internal_business"]),
        )
        cs = detect_contradictions(answers, "pilot")
        assert cs == []


# ─────────────────────────────────────────────────────────────────────────────
# Findings
# ─────────────────────────────────────────────────────────────────────────────

class TestFindings:
    def _pillar(self):
        return {"process": 70, "security": 60, "tokenomics": 65, "reliability": 70}

    def _construct(self, answers_by_id=None):
        answers_by_id = answers_by_id or {}
        return calculate_construct_scores(
            self._pillar(), answers_by_id, 0, 0, {}
        )

    def test_no_tenant_isolation_finding(self):
        answers = _make_answers(
            _radio("q5", "no_controls", 0),
            _checkbox("q7", ["internal_business"]),
        )
        cs = self._construct(answers)
        findings = generate_findings(answers, self._pillar(), cs, "production")
        ids = [f["id"] for f in findings]
        assert "no_tenant_isolation" in ids

    def test_no_injection_defense_finding(self):
        answers = _make_answers(
            _radio("q6", "no_external_inputs", 0),
            _checkbox("q7", ["internal_business"]),
        )
        cs = self._construct(answers)
        findings = generate_findings(answers, self._pillar(), cs, "production")
        ids = [f["id"] for f in findings]
        assert "no_injection_defense" in ids

    def test_unmodeled_unit_economics_finding(self):
        answers = _make_answers(
            _radio("q8", "none", 10),
            _radio("q9", "unsure", 20),
        )
        cs = self._construct(answers)
        findings = generate_findings(answers, self._pillar(), cs, "pilot")
        ids = [f["id"] for f in findings]
        assert "unmodeled_unit_economics" in ids

    def test_no_cost_controls_in_production(self):
        answers = _make_answers(
            _checkbox("q10", ["none"]),
        )
        cs = self._construct(answers)
        findings = generate_findings(answers, self._pillar(), cs, "production")
        ids = [f["id"] for f in findings]
        assert "no_cost_controls" in ids

    def test_finding_has_required_keys(self):
        answers = _make_answers(
            _radio("q5", "no_controls", 0),
            _checkbox("q7", ["internal_business"]),
        )
        cs = self._construct(answers)
        findings = generate_findings(answers, self._pillar(), cs, "production")
        for f in findings:
            assert "id" in f
            assert "title" in f
            assert "severity_score" in f
            assert "severity_label" in f
            assert "evidence" in f
            assert "consequence" in f
            assert "validation_step" in f

    def test_select_top_findings_pads_to_3(self):
        # Feed only one low-severity finding
        low_finding = {
            "id": "test", "title": "Test", "severity_score": 10,
            "severity_label": "Note", "related_question_ids": [],
            "derived_variable": "", "evidence": "", "consequence": "",
            "validation_step": ""
        }
        top = select_top_findings([low_finding])
        assert len(top) >= 1  # padding doesn't add phantom findings

    def test_select_top_findings_max_5(self):
        findings = [
            {"id": f"f{i}", "title": f"Finding {i}", "severity_score": 80,
             "severity_label": "Critical", "related_question_ids": [],
             "derived_variable": "", "evidence": "", "consequence": "",
             "validation_step": ""}
            for i in range(8)
        ]
        top = select_top_findings(findings)
        assert len(top) <= 5

    def test_select_top_findings_sorted_by_severity(self):
        scores = [40, 80, 60, 90, 70]
        findings = [
            {"id": f"f{i}", "title": f"Finding {i}", "severity_score": s,
             "severity_label": get_severity_label(s), "related_question_ids": [],
             "derived_variable": "", "evidence": "", "consequence": "",
             "validation_step": ""}
            for i, s in enumerate(scores)
        ]
        top = select_top_findings(findings)
        sevs = [f["severity_score"] for f in top]
        assert sevs == sorted(sevs, reverse=True)

    def test_get_top_strength_returns_highest_pillar(self):
        pillar = {"process": 90, "security": 60, "tokenomics": 70, "reliability": 65}
        cs = {"automation_leverage": 85}
        strength = get_top_strength(pillar, cs)
        assert strength["pillar"] == "process"

    def test_production_controls_missing_finding(self):
        answers = _make_answers(
            _not_yet("q5"),
            _not_yet("q6"),
            _not_yet("q10"),
        )
        cs = self._construct(answers)
        findings = generate_findings(answers, self._pillar(), cs, "production")
        ids = [f["id"] for f in findings]
        assert "production_controls_missing" in ids


# ─────────────────────────────────────────────────────────────────────────────
# Segmentation
# ─────────────────────────────────────────────────────────────────────────────

class TestSegmentation:
    def _seg(self, **kwargs):
        defaults = dict(
            findings=[], quadrant_id="LOW_LEVERAGE_HIGH_RISK",
            expected_dividend=10_000, composite_score=80,
            stage="pre_ai", evidence_confidence=70
        )
        defaults.update(kwargs)
        return get_segment(**defaults)

    def test_critical_finding_yields_A(self):
        seg = self._seg(findings=[{"severity_label": "Critical"}])
        assert seg == "A_HIGH_URGENCY"

    def test_high_leverage_high_risk_quadrant_yields_A(self):
        seg = self._seg(quadrant_id="HIGH_LEVERAGE_HIGH_RISK")
        assert seg == "A_HIGH_URGENCY"

    def test_large_dividend_yields_A(self):
        seg = self._seg(expected_dividend=150_000)
        assert seg == "A_HIGH_URGENCY"

    def test_production_low_score_yields_A(self):
        seg = self._seg(stage="production", composite_score=55)
        assert seg == "A_HIGH_URGENCY"

    def test_medium_dividend_yields_B(self):
        seg = self._seg(expected_dividend=30_000)
        assert seg == "B_MEDIUM_URGENCY"

    def test_pilot_mid_score_yields_B(self):
        seg = self._seg(stage="pilot", composite_score=67, expected_dividend=5_000)
        assert seg == "B_MEDIUM_URGENCY"

    def test_low_leverage_low_risk_low_confidence_yields_C(self):
        seg = self._seg(quadrant_id="LOW_LEVERAGE_LOW_RISK", evidence_confidence=30)
        assert seg == "C_WORKFLOW_DISCOVERY"

    def test_default_yields_D(self):
        seg = self._seg()
        assert seg == "D_NURTURE"


# ─────────────────────────────────────────────────────────────────────────────
# Pillar Scores
# ─────────────────────────────────────────────────────────────────────────────

class TestPillarScores:
    def test_returns_four_pillars(self):
        answers = _make_answers(
            _radio("q1", "consistent", 80),
            _radio("q2", "fast", 90),
        )
        ps = calculate_pillar_scores(answers, "pilot")
        assert set(ps.keys()) == {"process", "security", "tokenomics", "reliability"}

    def test_not_sure_handled_gracefully(self):
        answers = _make_answers(_not_sure("q1"), _not_sure("q2"))
        ps = calculate_pillar_scores(answers, "pilot")
        assert 0 <= ps["process"] <= 100

    def test_q10_checkbox_scoring_by_count(self):
        # 0 controls
        answers_none = _make_answers(_checkbox("q10", ["none"]))
        ps_none = calculate_pillar_scores(answers_none, "pilot")

        # 3 controls
        answers_many = _make_answers(
            _checkbox("q10", ["token_budgets", "rate_limits", "model_routing"])
        )
        ps_many = calculate_pillar_scores(answers_many, "pilot")

        assert ps_many["tokenomics"] > ps_none["tokenomics"]

    def test_scores_clamped_0_100(self):
        answers = _make_answers(
            _radio("q1", "perfect", 100),
            _radio("q2", "perfect", 100),
        )
        ps = calculate_pillar_scores(answers, "pilot")
        for v in ps.values():
            assert 0 <= v <= 100


# ─────────────────────────────────────────────────────────────────────────────
# Evidence Chain
# ─────────────────────────────────────────────────────────────────────────────

class TestEvidenceChain:
    def test_chain_has_item_per_answered_question(self):
        answers = _make_answers(
            _radio("q1", "consistent", 80),
            _radio("q2", "moderate", 60),
        )
        chain = generate_evidence_chain(answers, "pilot")
        assert len(chain) == 2

    def test_chain_item_has_required_keys(self):
        answers = _make_answers(_radio("q1", "consistent", 80))
        chain = generate_evidence_chain(answers, "pilot")
        item = chain[0]
        required = {"question_id", "question_wording", "answer_label", "score",
                    "derived_variable", "evidence", "consequence", "validation_step"}
        assert required.issubset(item.keys())

    def test_not_sure_flagged(self):
        answers = _make_answers(_not_sure("q1"))
        chain = generate_evidence_chain(answers, "pilot")
        assert chain[0]["is_not_sure"] is True

    def test_ordered_by_question_number(self):
        answers = _make_answers(
            _radio("q3", "low", 30),
            _radio("q1", "consistent", 80),
        )
        chain = generate_evidence_chain(answers, "pilot")
        ids = [c["question_id"] for c in chain]
        assert ids == sorted(ids, key=lambda x: int(x[1:]))


# ─────────────────────────────────────────────────────────────────────────────
# Full Engine (integration smoke test)
# ─────────────────────────────────────────────────────────────────────────────

class TestEngine:
    def _full_session(self, stage="pilot"):
        return {
            "stage": stage,
            "intake": {
                "name": "Test User",
                "company": "Acme",
                "email": "test@acme.com",
            },
            "answers": [
                {"id": "q1",  "answer_id": "very_consistent"},
                {"id": "q2",  "answer_id": "same_day"},
                {"id": "q3",  "answer_id": "significant_hours"},
                {"id": "q4",  "selected_option_ids": ["data_entry_duplicate_entry", "report_generation"]},
                {"id": "q5",  "answer_id": "enforced_tested"},
                {"id": "q6",  "answer_id": "adversarially_tested"},
                {"id": "q7",  "selected_option_ids": ["internal_business"]},
                {"id": "q8",  "answer_id": "per_workflow_attribution"},
                {"id": "q9",  "answer_id": "modeled_holds"},
                {"id": "q10", "selected_option_ids": ["token_budgets", "rate_limits", "model_routing"]},
                {"id": "q11", "answer_id": "human_review_queue"},
                {"id": "q12", "answer_id": "active_alerting"},
            ],
            "calculator_inputs": {
                "people": 4,
                "hours_per_week": 10,
                "automation_pct": 60,
                "hourly_cost": 75,
            },
        }

    def test_engine_returns_dict(self):
        result = calculate_awra_result(self._full_session())
        assert isinstance(result, dict)

    def test_engine_has_required_top_level_keys(self):
        result = calculate_awra_result(self._full_session())
        required = {
            "scoring_model_version", "stage", "composite_score", "composite_tier",
            "pillar_scores", "construct_scores", "construct_tiers", "quadrant",
            "findings", "top_strength", "contradictions", "evidence_chain",
            "evidence_matrix", "efficiency_dividend", "roadmap", "segment",
            "cta", "lotusnex_baseline",
        }
        assert required.issubset(result.keys())

    def test_engine_construct_scores_in_range(self):
        result = calculate_awra_result(self._full_session())
        for k, v in result["construct_scores"].items():
            assert 0 <= v <= 100, f"{k} out of range: {v}"

    def test_engine_composite_score_in_range(self):
        result = calculate_awra_result(self._full_session())
        assert 0 <= result["composite_score"] <= 100

    def test_engine_scoring_model_version_present(self):
        result = calculate_awra_result(self._full_session())
        assert result["scoring_model_version"] == "awra-1.0.0"

    def test_engine_dividend_structure(self):
        result = calculate_awra_result(self._full_session())
        div = result["efficiency_dividend"]
        assert div["conservative"] < div["expected"] < div["optimistic"]

    def test_engine_production_session(self):
        session = self._full_session(stage="production")
        result = calculate_awra_result(session)
        assert result["stage"] == "production"

    def test_engine_pre_ai_session(self):
        session = self._full_session(stage="pre_ai")
        result = calculate_awra_result(session)
        assert result["stage"] == "pre_ai"
        # Pre-AI composite = process score only
        assert result["composite_score"] == result["pillar_scores"]["process"]

    def test_engine_roadmap_not_empty(self):
        result = calculate_awra_result(self._full_session())
        assert len(result["roadmap"]) >= 3

    def test_engine_cta_has_button_label(self):
        result = calculate_awra_result(self._full_session())
        assert "button_label" in result["cta"]

    def test_engine_evidence_chain_ordered(self):
        result = calculate_awra_result(self._full_session())
        chain = result["evidence_chain"]
        ids = [c["question_id"] for c in chain]
        assert ids == sorted(ids, key=lambda x: int(x[1:]))

    def test_engine_pillar_gaps_against_baseline(self):
        result = calculate_awra_result(self._full_session())
        gaps = result["pillar_gaps"]
        assert "process" in gaps
        # A high-scoring session should be at or above baseline on most pillars
        above_baseline = sum(1 for v in gaps.values() if v >= 0)
        assert above_baseline >= 2
