"""
AWRA Phase 1 — Central scoring configuration.
All constants, multipliers, thresholds, and templates live here.
Never hardcode scoring logic in route handlers or report generators.
"""

SCORING_MODEL_VERSION = "awra-1.0.0"

# ── Pillar weights ─────────────────────────────────────────────────────────
PILLAR_WEIGHTS = {
    "process":     0.30,
    "security":    0.25,
    "tokenomics":  0.25,
    "reliability": 0.20,
}

# ── Unsure fallback scores (when user selects "Not sure") ──────────────────
UNSURE_FALLBACK = {
    "process":     45,
    "security":    50,
    "tokenomics":  30,
    "reliability": 30,
}

# ── Q4 workflow archetype multipliers ──────────────────────────────────────
# leverage: applied to automation_leverage construct
# economic: applied to economic_confidence construct
WORKFLOW_ARCHETYPE_MULTIPLIERS = {
    "document_processing":          {"leverage": 1.05, "economic": 0.95},
    "support_ticket_triage":        {"leverage": 1.10, "economic": 1.05},
    "internal_knowledge_retrieval": {"leverage": 1.00, "economic": 1.10},
    "data_entry_duplicate_entry":   {"leverage": 1.15, "economic": 1.10},
    "report_generation":            {"leverage": 1.00, "economic": 0.90},
    "compliance_evidence":          {"leverage": 0.90, "economic": 0.95},
    "sales_cs_handoffs":            {"leverage": 1.05, "economic": 1.00},
    "qa_test_generation":           {"leverage": 0.95, "economic": 1.00},
    "incident_summarization":       {"leverage": 1.00, "economic": 0.95},
    "invoice_ap_ar":                {"leverage": 1.10, "economic": 1.05},
    "onboarding_offboarding":       {"leverage": 0.95, "economic": 1.00},
    "meeting_notes":                {"leverage": 1.05, "economic": 0.90},
    "other":                        {"leverage": 1.00, "economic": 1.00},
}

# ── Q7 data sensitivity impact multipliers ─────────────────────────────────
# Applied to production_risk construct. Lower = more restrictive.
# When multiple categories selected, the minimum (strictest) value is used.
DATA_IMPACT_MULTIPLIERS = {
    "public_or_low_risk": 1.10,
    "internal_business":  1.00,
    "customer_data":      0.90,
    "pii":                0.80,
    "financial":          0.80,
    "hr":                 0.85,
    "regulated":          0.70,
    "none":               1.10,
}

# ── Workflow exposure by stage (used in severity calculation) ──────────────
WORKFLOW_EXPOSURE_BY_STAGE = {
    "pre_ai":     0.5,
    "pilot":      0.8,
    "production": 1.2,
}

# ── LotusNex production baseline (for Risk Radar) ─────────────────────────
# Labeled "LotusNex Production Baseline" — not an industry benchmark.
LOTUSNEX_BASELINE = {
    "process":     70,
    "security":    80,
    "tokenomics":  75,
    "reliability": 75,
}

# ── Composite score tier thresholds by stage ───────────────────────────────
# Production tightens thresholds — same controls create more risk when live.
COMPOSITE_TIER_THRESHOLDS = {
    "pre_ai": [
        (40,  "Critical Risk"),
        (60,  "Fragile Fit"),
        (70,  "Transitional"),
        (90,  "Production-Aware"),
        (101, "Production-Ready"),
    ],
    "pilot": [
        (40,  "Critical Risk"),
        (60,  "Fragile"),
        (80,  "Transitional"),
        (90,  "Production-Aware"),
        (101, "Production-Ready"),
    ],
    "production": [
        (40,  "Critical Risk"),
        (60,  "Fragile"),
        (70,  "Transitional"),
        (80,  "Fragile"),      # intentionally strict
        (90,  "Production-Aware"),
        (101, "Production-Ready"),
    ],
}

# ── Construct tier thresholds (shared across all four constructs) ──────────
CONSTRUCT_TIER_THRESHOLDS = [
    (40,  "Critical Risk"),
    (60,  "Fragile"),
    (75,  "Transitional"),
    (90,  "Production-Aware"),
    (101, "Production-Ready"),
]

# ── Severity label thresholds ──────────────────────────────────────────────
SEVERITY_THRESHOLDS = [
    (80, "Critical"),
    (60, "High"),
    (40, "Moderate"),
    (20, "Low"),
    (0,  "Note"),
]

# ── Efficiency dividend realization factors ────────────────────────────────
DIVIDEND_CONSERVATIVE = 0.50
DIVIDEND_EXPECTED     = 0.70
DIVIDEND_OPTIMISTIC   = 0.85

# ── Quadrant display copy ──────────────────────────────────────────────────
QUADRANT_COPY = {
    "HIGH_LEVERAGE_LOW_RISK": {
        "label": "Pilot recommended",
        "body":  "Strong workflow fit with manageable production risk. The value case is clear — the next step is validating it at controlled scale.",
    },
    "HIGH_LEVERAGE_HIGH_RISK": {
        "label": "Architecture review required",
        "body":  "The value is real, but the systems intended to carry it need hardening before automation compounds the risk.",
    },
    "LOW_LEVERAGE_LOW_RISK": {
        "label": "Process discovery recommended",
        "body":  "Clarify the workflow scope and automation fit before committing to a build. The architecture is safer than the process is ready.",
    },
    "LOW_LEVERAGE_HIGH_RISK": {
        "label": "De-prioritize this workflow",
        "body":  "Neither leverage nor safety currently justify investment here. Address process fit and architecture gaps before revisiting.",
    },
}

# ── Stage-specific roadmaps ────────────────────────────────────────────────
ROADMAPS = {
    "pre_ai": [
        {
            "phase": "Validate",
            "title": "Process Validation",
            "description": "Confirm which workflows have sufficient consistency and volume to justify automation. Map error rates, exception paths, and data sources.",
        },
        {
            "phase": "Design",
            "title": "Architecture Design",
            "description": "Define the system boundaries, data contracts, access controls, and failure handling before writing production code.",
        },
        {
            "phase": "Build",
            "title": "Pilot Build",
            "description": "Build a scoped pilot on the highest-fit workflow. Evaluate against real data with defined success criteria before expanding.",
        },
        {
            "phase": "Harden",
            "title": "Production Hardening",
            "description": "Add observability, cost controls, guardrails, and runbooks. Hand off with documentation your team can operate.",
        },
    ],
    "pilot": [
        {
            "phase": "Stabilize",
            "title": "Immediate Stabilization",
            "description": "Address the critical and high-severity findings first. Close the gaps that will cause incidents when the system goes live at scale.",
        },
        {
            "phase": "Harden",
            "title": "Production Hardening",
            "description": "Add observability, approval gates, cost telemetry, and deterministic failure handling. Validate against real workflow data before full deployment.",
        },
        {
            "phase": "Scale",
            "title": "Scale Optimization",
            "description": "Extend to additional workflows, implement model routing, and optimize unit economics once production controls are validated.",
        },
    ],
    "production": [
        {
            "phase": "Remediate",
            "title": "Critical Risk Remediation",
            "description": "Address critical findings as production incidents. Access controls, failure handling, and cost overruns cannot wait for a sprint cycle.",
        },
        {
            "phase": "Harden",
            "title": "Hardening Sprint",
            "description": "Close the high and moderate findings systematically. Establish baselines for observability, cost telemetry, and retrieval quality.",
        },
        {
            "phase": "Improve",
            "title": "Continuous Improvement",
            "description": "Implement regression testing, model routing, and automation expansion once the production baseline is stable.",
        },
    ],
}

# ── CTA copy by segment and stage ─────────────────────────────────────────
CTA_COPY = {
    "A_HIGH_URGENCY": {
        "heading": "These findings need an architect, not a deck.",
        "body":    "Your results show production-critical gaps that compound the longer they run. A 30-minute engineer-to-engineer review covers your specific flags — no pitch, no generic roadmap.",
        "button":  "Request the Architecture Review →",
        "url":     "https://lotusnex.com/contact.html",
    },
    "B_MEDIUM_URGENCY": {
        "heading": "The value case is real. The gaps are closeable.",
        "body":    "Your Efficiency Dividend is within reach, but a few architectural decisions will determine whether the automation creates leverage or creates new problems. Let's walk through them.",
        "button":  "Book a 30-Minute Review →",
        "url":     "https://lotusnex.com/contact.html",
    },
    "C_WORKFLOW_DISCOVERY": {
        "heading": "Clarify the process before committing to a build.",
        "body":    "Your results suggest the workflows need scoping before architecture decisions are made. A process discovery session maps which workflows are genuinely ready — and which would be automation theater.",
        "button":  "Start a Process Discovery →",
        "url":     "https://lotusnex.com/contact.html",
    },
    "D_NURTURE": {
        "heading": "Get a walkthrough of your results.",
        "body":    "A 30-minute review of your Workflow Readiness Score and Efficiency Dividend — specific to your answers, not a generic overview.",
        "button":  "Request a Results Walkthrough →",
        "url":     "https://lotusnex.com/contact.html",
    },
}

# ── Finding templates ──────────────────────────────────────────────────────
# Each template is matched against answer patterns in findings.py.
# Severity is calculated dynamically; templates provide the copy.
FINDING_TEMPLATES = {
    "no_tenant_isolation": {
        "title": "No tenant data isolation",
        "derived_variable": "Tenant-Isolation Score",
        "consequence": "All users can access all content. For any multi-user or multi-tenant deployment, automation built on top of this exposes records across users at scale.",
        "validation_step": "Enforce access controls at the query layer — not via system prompt. Validate with adversarial queries that attempt cross-tenant retrieval.",
    },
    "weak_isolation_sensitive_data": {
        "title": "Access control relies on the model, not the system",
        "derived_variable": "Tenant-Isolation Score",
        "consequence": "Sensitive data is in scope and access is enforced via system prompt. Model-level controls fail under adversarial inputs and cannot be audited — a known path to data leakage.",
        "validation_step": "Move access enforcement to the retrieval layer. Test with adversarial prompts designed to bypass system prompt constraints.",
    },
    "no_injection_defense": {
        "title": "No prompt injection defense",
        "derived_variable": "Adversarial-Resilience Score",
        "consequence": "The system accepts external inputs but has no injection defenses. Users familiar with these techniques can manipulate the system into returning restricted content or executing unintended actions.",
        "validation_step": "Run adversarial test cases including indirect prompt injection. Review tool permissions and output validation.",
    },
    "system_prompts_only_defense": {
        "title": "Injection defense relies on instruction hierarchy only",
        "derived_variable": "Adversarial-Resilience Score",
        "consequence": "System-prompt-only defenses are insufficient for production systems handling sensitive data. Instruction hierarchy can be overridden by sufficiently adversarial inputs.",
        "validation_step": "Add layered defenses: tool permission scoping, retrieval filtering, output validation, and adversarial test cases.",
    },
    "unmodeled_unit_economics": {
        "title": "Cost model not validated for production scale",
        "derived_variable": "Unit-Economics Confidence",
        "consequence": "No per-task cost attribution combined with unmodeled scale economics. Cost structure is unknown until it becomes a budget incident.",
        "validation_step": "Instrument per-task token spend. Model cost at 10× current volume before scaling.",
    },
    "no_cost_controls": {
        "title": "No token budgets or cost controls",
        "derived_variable": "Cost-Control Coverage",
        "consequence": "Spend is uncapped at the workflow level. A single runaway workflow or prompt pattern can spike costs without any alerting mechanism.",
        "validation_step": "Implement per-workflow token budgets, rate limits, and model routing by task type.",
    },
    "token_gluttony_risk": {
        "title": "Token gluttony risk — flagship model routing all tasks",
        "derived_variable": "Model-Routing Efficiency",
        "consequence": "Using a high-cost model for all task types, including simple classification and extraction, erodes unit economics at scale.",
        "validation_step": "Implement policy-based model routing. Route high-frequency, low-complexity tasks to smaller models.",
    },
    "no_failure_handling": {
        "title": "No failure handling — wrong outputs pass through undetected",
        "derived_variable": "Failure-Containment Score",
        "consequence": "When the system produces a wrong or low-confidence answer, nothing catches it. Failures propagate downstream — into customer outputs, compliance records, or dependent workflows.",
        "validation_step": "Define failure modes before shipping. Implement confidence thresholds, human review queues, and deterministic fallbacks.",
    },
    "failure_handling_mismatch": {
        "title": "Failure handling does not match the stakes of this workflow",
        "derived_variable": "Failure-Containment Score",
        "consequence": "The failure handling in place is insufficient for the data sensitivity and consequence level of this workflow. Partial controls create false confidence.",
        "validation_step": "Map failure modes explicitly to consequence levels. High-stakes outputs require guardrails, not just logging.",
    },
    "observability_gap": {
        "title": "Observability gap — system degradation is invisible",
        "derived_variable": "Observability Coverage",
        "consequence": "No active monitoring means degradation is invisible until it surfaces as a downstream complaint or data failure. Silent failures are the hardest to diagnose.",
        "validation_step": "Instrument active alerting with defined response runbooks. Set up recall drift monitoring for retrieval systems.",
    },
    "automation_theater_risk": {
        "title": "Automation Theater risk",
        "derived_variable": "Process-Fit Score",
        "consequence": "High variability combined with slow error detection means incorrect automated outputs may circulate for days. Automation here risks shifting cost from manual work to manual error correction.",
        "validation_step": "Validate process consistency before committing to a build. Define error detection SLAs and build exception handling first.",
    },
    "duplicate_entry_tax": {
        "title": "Duplicate-Entry Tax — measurable hours lost to cross-system re-entry",
        "derived_variable": "Automation-Leverage Coefficient",
        "consequence": "Significant staff hours are consumed by re-entering the same data across multiple systems. This is a high-leverage automation target — but only if the architecture is ready to carry it.",
        "validation_step": "Map the data flow between systems. Validate that the target systems have stable APIs before building extraction pipelines.",
    },
    "low_evidence_confidence": {
        "title": "Low Evidence Confidence — results carry significant uncertainty",
        "derived_variable": "Evidence-Confidence Score",
        "consequence": "Multiple 'Not sure' answers and/or contradictions in the response pattern reduce the reliability of the diagnostic. Results should be treated as directional, not definitive.",
        "validation_step": "Review the Reflection Prompts section. Consider completing the optional confidence inputs for a higher-confidence assessment.",
    },
    "production_controls_missing": {
        "title": "Production-stage system missing critical production controls",
        "derived_variable": "Production-Readiness Gap",
        "consequence": "You selected Production stage but key controls are not yet in place. Controls that are acceptable gaps in a prototype become production incidents when the system is live.",
        "validation_step": "Treat each missing control as a production incident, not a backlog item. Prioritize by consequence severity.",
    },
}
