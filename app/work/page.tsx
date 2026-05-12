import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Work',
  description: 'Representative engineering patterns in production AI systems, retrieval infrastructure, platform modernization, and DevSecOps delivery.',
  openGraph: {
    url: 'https://lotusnex.com/work',
    title: 'Work • LotusNex',
    description: 'Representative engineering patterns in production AI systems, retrieval infrastructure, platform modernization, and DevSecOps delivery.',
  },
  twitter: {
    title: 'Work • LotusNex',
    description: 'Representative engineering patterns in production AI systems, retrieval infrastructure, platform modernization, and DevSecOps delivery.',
  },
}

export default function WorkPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">Delivery patterns</p>
          <h1>Delivery patterns</h1>
          <p className="lede">
            Described at the architecture level. Client details are not disclosed. Each pattern reflects a real system — scoped, built, hardened, and handed off in production.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container vignette-grid">

          <div className="vignette" id="data-entry">
            <div className="vignette-header">
              <div className="vignette-tags">
                <span className="vtag discipline">Process Automation</span>
                <span className="vtag">Operations Workflow</span>
                <span className="vtag">~8 weeks</span>
              </div>
              <h2>Automated document data-entry pipeline for a high-volume accounting firm</h2>
            </div>
            <p className="vignette-context">
              A professional services firm processing high volumes of client financial documents faced a persistent manual bottleneck. Staff were transcribing structured data from incoming documents — invoices, statements, and tax filings — into internal systems by hand. The work was repetitive and rule-bounded, but error-prone and scaling with headcount rather than revenue. An architecture review confirmed process fit and data readiness before any build commitment. The goal was to automate extraction and entry end-to-end, with validation gates before any data reached the system of record.
            </p>
            <hr className="vignette-divider" />
            <div className="vignette-details">
              <div className="vignette-detail-block">
                <h4>Architecture approach</h4>
                <ul>
                  <li>Document intake pipeline with format normalization across PDF, scanned, and digital-native inputs</li>
                  <li>Structured extraction with schema-grounded LLM output and per-field confidence scoring</li>
                  <li>Human review routing for low-confidence extractions — clear UI for review, approval, and correction</li>
                  <li>Write pipeline with dry-run mode, diff preview, and rollback on validation failure</li>
                </ul>
              </div>
              <div className="vignette-detail-block">
                <h4>Production properties</h4>
                <ul>
                  <li>End-to-end audit trail from document receipt to system write</li>
                  <li>Validation layer catches format drift before extraction failures propagate</li>
                  <li>Human review queue with SLA visibility and exception reporting</li>
                  <li>Cost telemetry per document type with budget controls and alert thresholds</li>
                </ul>
              </div>
            </div>
            <div className="vignette-outcome">
              <strong>Delivery outcome</strong>
              Pipeline shipped to production with extraction validated against a held-out document sample and the human review queue operational from day one. The validation layer caught format drift across three document variants before any failures reached the system of record. Operations staff reallocated from manual transcription to exception handling and advisory work.
            </div>
          </div>

          <div className="vignette" id="rag">
            <div className="vignette-header">
              <div className="vignette-tags">
                <span className="vtag discipline">Retrieval Infrastructure</span>
                <span className="vtag">B2B SaaS</span>
                <span className="vtag">~10 weeks</span>
              </div>
              <h2>Permission-aware retrieval in multi-tenant systems</h2>
            </div>
            <p className="vignette-context">
              A B2B SaaS platform serving regulated-industry clients needed internal knowledge retrieval exposed to end users across multiple tenants. The client came with an existing retrieval prototype. An architecture review identified access control at the query layer — not retrieval quality — as the critical production risk before go-live. Documents carried role and tenant-level permissions that a standard RAG implementation would not respect. Post-filtering was insufficient: it couldn&apos;t prevent cross-tenant context from influencing generated responses. The system had to enforce boundaries at the index query layer, before any content reached the model.
            </p>
            <hr className="vignette-divider" />
            <div className="vignette-details">
              <div className="vignette-detail-block">
                <h4>Architecture approach</h4>
                <ul>
                  <li>Ingestion pipeline with document normalization and permission metadata extraction at ingest time</li>
                  <li>Chunking strategy tuned to document structure and role-relevant content boundaries</li>
                  <li>RBAC-aware retrieval with identity-layer integration — access enforced at query, not filtered after</li>
                  <li>Offline evaluation harness with recall/precision baselines and adversarial query regression suite</li>
                </ul>
              </div>
              <div className="vignette-detail-block">
                <h4>Production properties</h4>
                <ul>
                  <li>Tenant isolation enforced at index query time — zero cross-tenant document exposure</li>
                  <li>Retrieval audit trail aligned to compliance and data access requirements</li>
                  <li>Monitoring for recall drift and retrieval latency across tenant partitions</li>
                  <li>Runbooks and ownership documentation delivered at handoff</li>
                </ul>
              </div>
            </div>
            <div className="vignette-outcome">
              <strong>Delivery outcome</strong>
              The system shipped to production with permission boundaries validated under adversarial query testing and evaluation baselines established. Internal teams assumed full ownership with the ability to maintain and extend the retrieval pipeline without external support.
            </div>
          </div>

          <div className="vignette" id="agent">
            <div className="vignette-header">
              <div className="vignette-tags">
                <span className="vtag discipline">Agent Orchestration</span>
                <span className="vtag">B2B SaaS</span>
                <span className="vtag">~12 weeks</span>
              </div>
              <h2>Agentic workflow with human approval gates for an operations team</h2>
            </div>
            <p className="vignette-context">
              An operations team managing high-volume, multi-step workflows across several internal tools wanted to automate a class of repetitive decisions — while retaining human review for actions above a defined risk threshold. A workflow discovery scoped the automation boundary before architecture work began — defining what the agent could execute autonomously, what required approval, and what had to fail deterministically rather than degrade silently.
            </p>
            <hr className="vignette-divider" />
            <div className="vignette-details">
              <div className="vignette-detail-block">
                <h4>Architecture approach</h4>
                <ul>
                  <li>Orchestration loop with explicit tool boundary definitions and least-privilege permissioning</li>
                  <li>Risk-tiered approval flow: auto-execute, human-in-loop, and hard-stop tiers</li>
                  <li>Tool-call logging and trace spans for full auditability</li>
                  <li>Evaluation test set covering edge cases, adversarial inputs, and boundary conditions</li>
                </ul>
              </div>
              <div className="vignette-detail-block">
                <h4>Production properties</h4>
                <ul>
                  <li>Deterministic fallbacks for all failure modes — no silent degradation</li>
                  <li>Cost telemetry and per-workflow token budgets</li>
                  <li>Escalation path with clear notification and override mechanics</li>
                  <li>Regression checks integrated into CI pipeline</li>
                </ul>
              </div>
            </div>
            <div className="vignette-outcome">
              <strong>Delivery outcome</strong>
              Agentic system deployed with approval gates validated against real workflow data, cost controls active from day one, and operations team trained on override and monitoring procedures.
            </div>
          </div>

          <div className="vignette" id="lead-gen">
            <div className="vignette-header">
              <div className="vignette-tags">
                <span className="vtag discipline">Agent Orchestration</span>
                <span className="vtag">B2B SaaS</span>
                <span className="vtag">~12 weeks</span>
              </div>
              <h2>Automated lead research and CRM enrichment system for a B2B SaaS sales team</h2>
            </div>
            <p className="vignette-context">
              A B2B SaaS sales team was spending significant SDR time on manual prospect research — ICP qualification, company enrichment, contact data entry, and CRM hygiene. An architecture review scoped the research and enrichment loop before build began, defining what the agent could automate fully versus what required human approval before any CRM write or outreach trigger. The research loop was repetitive but judgment-dependent: some enrichment could be fully automated, but outreach decisions required human review.
            </p>
            <hr className="vignette-divider" />
            <div className="vignette-details">
              <div className="vignette-detail-block">
                <h4>Architecture approach</h4>
                <ul>
                  <li>Orchestration loop covering prospect discovery, enrichment from multiple data sources, and ICP scoring</li>
                  <li>Tool integrations with research APIs, enrichment providers, and CRM write endpoints — all with least-privilege permissions</li>
                  <li>Human approval gate before CRM write and before outreach action triggers</li>
                  <li>Completeness and confidence scoring with graceful degradation when external sources fail</li>
                </ul>
              </div>
              <div className="vignette-detail-block">
                <h4>Production properties</h4>
                <ul>
                  <li>All enrichment actions logged with source attribution for auditability</li>
                  <li>Idempotent CRM writes with duplicate detection and merge conflict handling</li>
                  <li>Per-prospect and per-source cost telemetry with budget controls</li>
                  <li>Runbooks for common failure modes — API downtime, low-confidence bulk batches, CRM rate limits</li>
                </ul>
              </div>
            </div>
            <div className="vignette-outcome">
              <strong>Delivery outcome</strong>
              System deployed with CRM write gates validated against a live prospect sample and cost telemetry active from day one. Source attribution logging confirmed enrichment provenance on every record. Sales team trained on review procedures, confidence thresholds, and override paths. No post-handoff support required.
            </div>
          </div>

          <div className="vignette" id="platform-reliability">
            <div className="vignette-header">
              <div className="vignette-tags">
                <span className="vtag discipline">Platform &amp; Reliability</span>
                <span className="vtag">B2B SaaS</span>
                <span className="vtag">~8 weeks</span>
              </div>
              <h2>Production observability and deployment infrastructure for an AI system with no visibility</h2>
            </div>
            <p className="vignette-context">
              A team had shipped an AI-powered feature to production but had no alerting, no per-workflow cost visibility, and a deployment process that required manual steps with no rollback capability. The first time quality degraded, it was reported by a customer — not surfaced by the system. An architecture review confirmed the gap: the AI system was live but the operational infrastructure that should have surrounded it from day one was absent.
            </p>
            <hr className="vignette-divider" />
            <div className="vignette-details">
              <div className="vignette-detail-block">
                <h4>Architecture approach</h4>
                <ul>
                  <li>Full-stack observability with structured logging, distributed traces, and per-workflow latency and error-rate dashboards</li>
                  <li>Alerting on model response quality signals, token spend anomalies, and downstream system failures — with runbooks attached to each alert</li>
                  <li>CI/CD pipeline with automated regression checks against a held-out evaluation set and one-command rollback capability</li>
                  <li>Per-workflow cost telemetry with budget alert thresholds before spend reaches critical levels</li>
                </ul>
              </div>
              <div className="vignette-detail-block">
                <h4>Production properties</h4>
                <ul>
                  <li>Incidents surface in dashboards with runbooks — not in customer reports</li>
                  <li>Deployments are automated, regression-tested, and reversible</li>
                  <li>Per-workflow spend is visible and bounded before scale</li>
                  <li>Team owns the full operational stack at handoff with no external dependency</li>
                </ul>
              </div>
            </div>
            <div className="vignette-outcome">
              <strong>Delivery outcome</strong>
              Observability infrastructure operational in the first week. First degradation alert fired and was resolved internally before any user reported an issue. Deployment pipeline adopted by the team with automated regression checks running on every merge. Cost telemetry active across all workflows with budget controls in place.
            </div>
          </div>

          <div className="vignette" id="security-hardening">
            <div className="vignette-header">
              <div className="vignette-tags">
                <span className="vtag discipline">AI Security &amp; Hardening</span>
                <span className="vtag">B2B SaaS</span>
                <span className="vtag">~6 weeks</span>
              </div>
              <h2>Adversarial testing and access control hardening for a multi-tenant AI system</h2>
            </div>
            <p className="vignette-context">
              A team had built an AI assistant handling customer and internal data across multiple tenants. The system had never been tested adversarially — no prompt injection testing, no cross-tenant access validation, no review of how data sensitivity was handled at the retrieval layer. A Workflow Discovery assessment surfaced critical and high-severity security findings. The engagement scope was to test, document, and close the gaps before the system was exposed to a broader user base.
            </p>
            <hr className="vignette-divider" />
            <div className="vignette-details">
              <div className="vignette-detail-block">
                <h4>Architecture approach</h4>
                <ul>
                  <li>Adversarial test suite covering direct prompt injection, instruction override attempts, and indirect injection via retrieved documents</li>
                  <li>Access control review at the query layer — validating that tenant boundaries held under adversarial retrieval queries, not just standard usage</li>
                  <li>Data sensitivity mapping — tracing PII, financial, and customer data flows through the AI stack to identify unguarded exposure points</li>
                  <li>Remediation implementation for all critical findings with regression tests to prevent recurrence</li>
                </ul>
              </div>
              <div className="vignette-detail-block">
                <h4>Production properties</h4>
                <ul>
                  <li>All critical and high-severity findings resolved and verified via retesting before broader rollout</li>
                  <li>Adversarial test suite integrated into CI pipeline for ongoing regression</li>
                  <li>Access control validated at query time — not via model instructions that can be overridden</li>
                  <li>Findings report and remediation log delivered as part of handoff documentation</li>
                </ul>
              </div>
            </div>
            <div className="vignette-outcome">
              <strong>Delivery outcome</strong>
              All critical findings closed before broader user exposure. Remediation verified via retesting across the full adversarial suite. Findings report used internally to align stakeholders on ongoing security posture. Adversarial test suite adopted into the team&apos;s CI pipeline.
            </div>
          </div>

        </div>
      </section>
    </>
  )
}
