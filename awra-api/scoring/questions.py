"""
AWRA Phase 1 — Question definitions.
Each question carries stage-specific wording, answer options with per-stage scores,
and evidence/consequence/validation templates used to build the Evidence Chain.
"""

# score_by_stage: None means "Not applicable" for that stage (maps to NA option shown in UI)
# Questions with unsure=True in an option use fallback scores from config.UNSURE_FALLBACK

QUESTIONS = [

    # ── Q1: Workflow consistency ──────────────────────────────────────────
    {
        "id": "q1",
        "pillar": "process",
        "derived_variable": "Process-Consistency Score",
        "wording": {
            "pre_ai":     "How consistent are the workflows you're considering automating?",
            "pilot":      "How consistent are the workflows you've started automating?",
            "production": "How consistent are the workflows currently running in production?",
        },
        "type": "radio",
        "options": [
            {
                "id": "very_consistent",
                "label": "Very consistent — nearly identical each time, minimal judgment required.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "mostly_consistent",
                "label": "Mostly consistent with occasional exceptions that need human review.",
                "score_by_stage": {"pre_ai": 75, "pilot": 75, "production": 75},
            },
            {
                "id": "frequently_varies",
                "label": "Frequently varies — the right output depends on context and judgment.",
                "score_by_stage": {"pre_ai": 35, "pilot": 35, "production": 35},
            },
            {
                "id": "highly_variable",
                "label": "Highly variable — most instances require significant human judgment.",
                "score_by_stage": {"pre_ai": 10, "pilot": 10, "production": 10},
            },
            {
                "id": "not_sure",
                "label": "Not sure.",
                "score_by_stage": {"pre_ai": None, "pilot": None, "production": None},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates the consistency level of the target workflows.",
        "consequence_template": "High variability reduces automation leverage and increases the risk that automated outputs require as much human review as the original manual process.",
        "validation_step_template": "Document a representative sample of 20+ workflow instances. Measure variance in inputs, logic paths, and outputs before committing to automation.",
    },

    # ── Q2: Error detection speed ─────────────────────────────────────────
    {
        "id": "q2",
        "pillar": "process",
        "derived_variable": "Error-Detection Latency",
        "wording": {
            "pre_ai":     "When a manual process produces a wrong output today, how quickly does someone catch it?",
            "pilot":      "When your automated system produces a wrong output, how quickly is it caught?",
            "production": "When your production system produces a wrong output, how quickly is it caught?",
        },
        "type": "radio",
        "options": [
            {
                "id": "same_day",
                "label": "Same day — there is a clear check before the output leaves the team.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "within_week",
                "label": "Within a week — someone downstream usually notices.",
                "score_by_stage": {"pre_ai": 70, "pilot": 70, "production": 70},
            },
            {
                "id": "days_later",
                "label": "We often find out through downstream effects, days later.",
                "score_by_stage": {"pre_ai": 35, "pilot": 35, "production": 35},
            },
            {
                "id": "rarely",
                "label": "Rarely — unless a customer or external party reports it.",
                "score_by_stage": {"pre_ai": 10, "pilot": 10, "production": 10},
            },
            {
                "id": "not_sure",
                "label": "Not sure.",
                "score_by_stage": {"pre_ai": None, "pilot": None, "production": None},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates how quickly errors in the target workflow are detected.",
        "consequence_template": "Slow error detection amplifies the blast radius of incorrect automated outputs — errors accumulate before anyone catches them.",
        "validation_step_template": "Define error detection SLAs before automating. Build exception queues and alerting before shipping to production.",
    },

    # ── Q3: Data re-entry across systems ──────────────────────────────────
    {
        "id": "q3",
        "pillar": "process",
        "derived_variable": "Duplicate-Entry Tax",
        "wording": {
            "pre_ai":     "How much of the manual work involves re-entering the same data across multiple systems?",
            "pilot":      "Before automation, how much of the manual work involved re-entering data across systems?",
            "production": "How much residual cross-system re-entry work remains outside the automated workflow?",
        },
        "type": "radio",
        "options": [
            {
                "id": "more_than_half",
                "label": "More than half — the same information gets entered in 2+ systems routinely.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "significant",
                "label": "A significant portion — this happens daily for our team.",
                "score_by_stage": {"pre_ai": 75, "pilot": 75, "production": 75},
            },
            {
                "id": "occasionally",
                "label": "Occasionally — maybe a few times per week.",
                "score_by_stage": {"pre_ai": 40, "pilot": 40, "production": 40},
            },
            {
                "id": "rarely",
                "label": "Rarely — most workflows are contained in a single system.",
                "score_by_stage": {"pre_ai": 20, "pilot": 20, "production": 20},
            },
            {
                "id": "not_sure",
                "label": "Not sure.",
                "score_by_stage": {"pre_ai": None, "pilot": None, "production": None},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response quantifies the cross-system data re-entry burden in the target workflow.",
        "consequence_template": "High duplicate-entry tax indicates strong automation leverage — but only if the target systems have stable, accessible APIs.",
        "validation_step_template": "Map every system the data touches. Confirm stable API access or export capabilities for each before designing the automation pipeline.",
    },

    # ── Q4: Workflow archetypes (multiplier — not directly scored) ─────────
    {
        "id": "q4",
        "pillar": "process",
        "derived_variable": "Workflow-Archetype Multiplier",
        "wording": {
            "pre_ai":     "Which types of workflows are you hoping to automate?",
            "pilot":      "Which workflow types are you automating?",
            "production": "Which workflow types are currently automated in production?",
        },
        "type": "checkbox",
        "options": [
            {"id": "document_processing",          "label": "Document processing — invoices, contracts, or reports"},
            {"id": "support_ticket_triage",        "label": "Customer support and ticket triage"},
            {"id": "internal_knowledge_retrieval", "label": "Internal knowledge retrieval and Q&A"},
            {"id": "data_entry_duplicate_entry",   "label": "Data entry and cross-system re-entry"},
            {"id": "report_generation",            "label": "Report generation and analytics prep"},
            {"id": "compliance_evidence",          "label": "Compliance evidence gathering and audit prep"},
            {"id": "sales_cs_handoffs",            "label": "Sales and customer success handoffs"},
            {"id": "qa_test_generation",           "label": "QA and test case generation"},
            {"id": "incident_summarization",       "label": "Incident summarization and post-mortem prep"},
            {"id": "invoice_ap_ar",                "label": "Invoice processing and AP/AR workflows"},
            {"id": "onboarding_offboarding",       "label": "Employee or customer onboarding/offboarding"},
            {"id": "meeting_notes",                "label": "Meeting notes and action item extraction"},
            {"id": "other",                        "label": "Something else — still figuring it out"},
        ],
        "evidence_template": "The selected workflow archetypes determine automation leverage and economic confidence multipliers.",
        "consequence_template": "Archetype selection affects how much leverage is realistically achievable and how confident the Efficiency Dividend estimate should be.",
        "validation_step_template": "For each selected archetype, validate process consistency (Q1) and data accessibility (Q3) before committing to a build.",
    },

    # ── Q5: Access control enforcement ────────────────────────────────────
    {
        "id": "q5",
        "pillar": "security",
        "derived_variable": "Tenant-Isolation Score",
        "wording": {
            "pre_ai":     "If you built AI for these workflows, would different users need to see different data?",
            "pilot":      "When your AI returns information to a user, does it enforce which records that user is allowed to see?",
            "production": "When your AI returns information to a user, does it enforce which records that user is allowed to see?",
        },
        "type": "radio",
        "options": [
            {
                "id": "enforced_tested",
                "label": "Yes — enforced at query time with controls we have tested.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "mostly_filtered",
                "label": "Mostly — we filter results, but have not tested edge cases formally.",
                "score_by_stage": {"pre_ai": 60, "pilot": 60, "production": 60},
            },
            {
                "id": "system_prompt",
                "label": "We rely on the model to respect the context set in the system prompt.",
                "score_by_stage": {"pre_ai": 20, "pilot": 20, "production": 20},
            },
            {
                "id": "no_controls",
                "label": "No controls in place — all users can reach all content.",
                "score_by_stage": {"pre_ai": 0, "pilot": 0, "production": 0},
            },
            {
                "id": "not_applicable",
                "label": "Not applicable — single-tenant, single-user, or no AI in production yet.",
                "score_by_stage": {"pre_ai": 65, "pilot": 65, "production": 65},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates how access control is enforced at retrieval or query time.",
        "consequence_template": "Insufficient access control in multi-user systems creates data leakage risk. System-prompt-based controls fail under adversarial inputs.",
        "validation_step_template": "Validate access enforcement at the query layer — not via model instructions. Run adversarial queries that attempt cross-user data retrieval.",
    },

    # ── Q6: Prompt injection defense ──────────────────────────────────────
    {
        "id": "q6",
        "pillar": "security",
        "derived_variable": "Adversarial-Resilience Score",
        "wording": {
            "pre_ai":     "If you built AI for these workflows, would the AI need to take actions in other systems on behalf of users?",
            "pilot":      "How do you defend against prompt injection and attempts by users to override the system's instructions?",
            "production": "How do you defend against prompt injection and attempts by users to override the system's instructions?",
        },
        "type": "radio",
        "options": [
            {
                "id": "adversarially_tested",
                "label": "Yes — we have run adversarial testing or red-teamed it.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "informal_mitigations",
                "label": "We have thought about it and have some informal mitigations.",
                "score_by_stage": {"pre_ai": 55, "pilot": 55, "production": 55},
            },
            {
                "id": "on_the_list",
                "label": "No — it is on our list but we have not gotten to it.",
                "score_by_stage": {"pre_ai": 20, "pilot": 20, "production": 20},
            },
            {
                "id": "no_external_inputs",
                "label": "No — and the system accepts external inputs we do not fully control.",
                "score_by_stage": {"pre_ai": 0, "pilot": 0, "production": 0},
            },
            {
                "id": "not_applicable",
                "label": "Not applicable — no external users interact with the system directly.",
                "score_by_stage": {"pre_ai": 65, "pilot": 65, "production": 65},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates the level of adversarial hardening against prompt injection and instruction override.",
        "consequence_template": "Weak injection defenses expose the system to manipulation — especially when the AI has access to tools, documents, or customer data.",
        "validation_step_template": "Run adversarial test cases including indirect prompt injection. Review tool permissions, output validation, and content isolation.",
    },

    # ── Q7: Data sensitivity (multiplier — not directly scored) ───────────
    {
        "id": "q7",
        "pillar": "security",
        "derived_variable": "Data-Sensitivity Impact Multiplier",
        "wording": {
            "pre_ai":     "What types of data would the AI need to access to automate these workflows?",
            "pilot":      "What types of data does your AI system access or process?",
            "production": "What types of data does your AI system access or process?",
        },
        "type": "checkbox",
        "options": [
            {"id": "public_or_low_risk", "label": "Public or low-risk data — no sensitivity concerns"},
            {"id": "internal_business",  "label": "Internal business data — non-customer, non-regulated"},
            {"id": "customer_data",      "label": "Customer data — names, emails, IDs, contact details"},
            {"id": "pii",                "label": "PII — personal identifiable information beyond basic contact"},
            {"id": "financial",          "label": "Financial records — invoices, transactions, revenue data"},
            {"id": "hr",                 "label": "HR or employee records"},
            {"id": "regulated",          "label": "Regulated data — HIPAA, SOC 2, GDPR, or similar"},
            {"id": "none",               "label": "None of the above — or no AI in production yet"},
        ],
        "evidence_template": "The selected data categories determine the impact multiplier applied to Production Risk.",
        "consequence_template": "Higher data sensitivity requires stricter access controls, more rigorous injection testing, and compliance-aligned audit trails.",
        "validation_step_template": "For each data category in scope, confirm access controls, audit trail requirements, and regulatory obligations before building.",
    },

    # ── Q8: Per-task cost attribution ─────────────────────────────────────
    {
        "id": "q8",
        "pillar": "tokenomics",
        "derived_variable": "Cost-Attribution Depth",
        "wording": {
            "pre_ai":     "Do you have a cost model for what each automated workflow would cost to run?",
            "pilot":      "Do you know what each automated task or workflow costs in tokens or compute?",
            "production": "Do you know what each automated task or workflow costs in tokens or compute?",
        },
        "type": "radio",
        "options": [
            {
                "id": "per_workflow_attribution",
                "label": "Yes — we track cost per workflow or task with clear attribution.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "overall_spend",
                "label": "We have overall AI spend but not per-task or per-workflow breakdowns.",
                "score_by_stage": {"pre_ai": 55, "pilot": 55, "production": 55},
            },
            {
                "id": "monthly_bill",
                "label": "We know the monthly bill, but not what is driving it.",
                "score_by_stage": {"pre_ai": 20, "pilot": 20, "production": 20},
            },
            {
                "id": "no_tracking",
                "label": "No cost tracking at all yet.",
                "score_by_stage": {"pre_ai": 5, "pilot": 5, "production": 5},
            },
            {
                "id": "not_sure",
                "label": "Not sure.",
                "score_by_stage": {"pre_ai": None, "pilot": None, "production": None},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates the depth of cost visibility at the per-task or per-workflow level.",
        "consequence_template": "Without per-task attribution, cost drivers are invisible and budget overruns will surface as incidents rather than metrics.",
        "validation_step_template": "Instrument per-task token spend before scaling. Add budget controls and alert thresholds at the workflow level.",
    },

    # ── Q9: Scale economics validation ────────────────────────────────────
    {
        "id": "q9",
        "pillar": "tokenomics",
        "derived_variable": "Unit-Economics Confidence",
        "wording": {
            "pre_ai":     "If your usage 10×'d, do you have a model for what that would cost?",
            "pilot":      "If your usage 10×'d tomorrow, would your current AI cost structure stay within acceptable unit economics?",
            "production": "If your usage 10×'d tomorrow, would your current AI cost structure stay within acceptable unit economics?",
        },
        "type": "radio",
        "options": [
            {
                "id": "modeled_holds",
                "label": "Yes — we have modeled cost at scale and it holds.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "probably",
                "label": "Probably — we have thought about it but have not formally modeled it.",
                "score_by_stage": {"pre_ai": 65, "pilot": 65, "production": 65},
            },
            {
                "id": "uncertain",
                "label": "Uncertain — we have not stress-tested the economics.",
                "score_by_stage": {"pre_ai": 30, "pilot": 30, "production": 30},
            },
            {
                "id": "would_spiral",
                "label": "No — costs would almost certainly spiral without architectural changes.",
                "score_by_stage": {"pre_ai": 5, "pilot": 5, "production": 5},
            },
            {
                "id": "not_sure",
                "label": "Not sure.",
                "score_by_stage": {"pre_ai": None, "pilot": None, "production": None},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates whether unit economics have been validated for production scale.",
        "consequence_template": "Unmodeled scale economics create budget exposure. Cost structures that appear acceptable at current volume frequently fail at 10× without architectural changes.",
        "validation_step_template": "Model cost at 5× and 10× current volume. Validate that model routing, caching, and token budgets hold at scale before committing to growth.",
    },

    # ── Q10: Cost control mechanisms (checkbox) ───────────────────────────
    {
        "id": "q10",
        "pillar": "tokenomics",
        "derived_variable": "Cost-Control Coverage",
        "wording": {
            "pre_ai":     "Which cost control mechanisms do you plan to implement?",
            "pilot":      "Which cost control mechanisms do you currently have in place?",
            "production": "Which cost control mechanisms do you currently have in place?",
        },
        "type": "checkbox",
        "options": [
            {"id": "token_budgets",  "label": "Token budgets or spend caps per workflow or user"},
            {"id": "rate_limits",    "label": "Rate limits at the API or application layer"},
            {"id": "model_routing",  "label": "Model routing — different models for different task types"},
            {"id": "none",           "label": "None — spend is uncapped at the workflow level"},
        ],
        "evidence_template": "The selected controls indicate coverage of token spend, rate limiting, and model routing.",
        "consequence_template": "Missing cost controls leave spend uncapped. A single runaway workflow or prompt pattern can spike costs without alerting.",
        "validation_step_template": "Implement all three: token budgets, rate limits, and model routing by task type. Validate each before scaling.",
    },

    # ── Q11: Failure handling ─────────────────────────────────────────────
    {
        "id": "q11",
        "pillar": "reliability",
        "derived_variable": "Failure-Containment Score",
        "wording": {
            "pre_ai":     "If the AI produces a wrong or uncertain answer, what should happen?",
            "pilot":      "What happens when your AI system returns a wrong or low-confidence answer?",
            "production": "What happens when your AI system returns a wrong or low-confidence answer?",
        },
        "type": "radio",
        "options": [
            {
                "id": "human_review_queue",
                "label": "A guardrail catches it and routes to a human review queue.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "log_and_handle",
                "label": "We log it and handle it manually after the fact.",
                "score_by_stage": {"pre_ai": 55, "pilot": 55, "production": 55},
            },
            {
                "id": "passes_through",
                "label": "The output goes through — we usually find out later when something breaks.",
                "score_by_stage": {"pre_ai": 20, "pilot": 20, "production": 20},
            },
            {
                "id": "no_mechanism",
                "label": "We do not have a mechanism for this yet.",
                "score_by_stage": {"pre_ai": 0, "pilot": 0, "production": 0},
            },
            {
                "id": "not_sure",
                "label": "Not sure / No AI in production yet.",
                "score_by_stage": {"pre_ai": None, "pilot": None, "production": None},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates whether failure handling is defined and enforced before outputs reach downstream systems.",
        "consequence_template": "No failure handling means wrong outputs propagate downstream — into customer-facing systems, compliance records, or dependent workflows — without interception.",
        "validation_step_template": "Define failure modes before shipping. Implement confidence thresholds, human review queues, and deterministic fallbacks for every output type.",
    },

    # ── Q12: Production observability ─────────────────────────────────────
    {
        "id": "q12",
        "pillar": "reliability",
        "derived_variable": "Observability Coverage",
        "wording": {
            "pre_ai":     "How would you know if the automated system started producing wrong outputs?",
            "pilot":      "Do you have observability in place — dashboards or alerts that tell you when the AI system is degrading?",
            "production": "Do you have observability in place — dashboards or alerts that tell you when the AI system is degrading?",
        },
        "type": "radio",
        "options": [
            {
                "id": "active_alerting",
                "label": "Yes — active alerting with defined response runbooks.",
                "score_by_stage": {"pre_ai": 100, "pilot": 100, "production": 100},
            },
            {
                "id": "logging_no_alerting",
                "label": "Logging in place, but no active monitoring or alerting.",
                "score_by_stage": {"pre_ai": 55, "pilot": 55, "production": 55},
            },
            {
                "id": "basic_logging",
                "label": "Basic infrastructure error logging only.",
                "score_by_stage": {"pre_ai": 20, "pilot": 20, "production": 20},
            },
            {
                "id": "no_observability",
                "label": "No observability yet.",
                "score_by_stage": {"pre_ai": 0, "pilot": 0, "production": 0},
            },
            {
                "id": "not_sure",
                "label": "Not sure / No AI in production yet.",
                "score_by_stage": {"pre_ai": None, "pilot": None, "production": None},
                "unsure": True,
            },
        ],
        "evidence_template": "Your response indicates the visibility you have into system degradation and output quality in production.",
        "consequence_template": "No observability means system degradation is invisible until it surfaces as a downstream complaint, data failure, or customer incident.",
        "validation_step_template": "Instrument active alerting with runbooks before go-live. Set up recall drift monitoring for retrieval systems and output-quality sampling for generation systems.",
    },
]

# Quick lookup by id
QUESTION_BY_ID = {q["id"]: q for q in QUESTIONS}
