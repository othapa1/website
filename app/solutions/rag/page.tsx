import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Knowledge Retrieval',
  description: 'Permission-aware ingestion, indexing, retrieval, and evaluation-driven quality for knowledge systems that must enforce access boundaries in production.',
  openGraph: {
    url: 'https://lotusnex.com/solutions/rag',
    title: 'Knowledge Retrieval • LotusNex',
    description: 'Permission-aware ingestion, indexing, retrieval, and evaluation-driven quality for knowledge systems that must enforce access boundaries in production.',
  },
  twitter: {
    title: 'Knowledge Retrieval • LotusNex',
    description: 'Permission-aware ingestion, indexing, retrieval, and evaluation-driven quality for knowledge systems that must enforce access boundaries in production.',
  },
}

export default function KnowledgeRetrievalPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">Knowledge retrieval</p>
          <h1>Not a vector search layer bolted onto a prompt.</h1>
          <p className="lede">
            If retrieval is already in use, the risk isn&apos;t retrieval — it&apos;s access control and correctness under real conditions. Systems fail in production not because retrieval is hard, but because access boundaries and quality measurement are treated as afterthoughts.
          </p>
          <p>We design retrieval as a permission-aware system from the start — access enforced at query time, quality measured continuously, degradation surfaced before users notice it.</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="pov">
            <h3>The common failure mode isn&apos;t bad retrieval. It&apos;s invisible retrieval.</h3>
            <p style={{ marginBottom: 0 }}>Access control handled with post-retrieval filtering. Retrieval quality guessed rather than measured. No alerting when the system degrades. These gaps matter most in multi-tenant systems and regulated environments — exactly where retrieval systems are most valuable and most exposed.</p>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="grid-2" style={{ marginBottom: 20 }}>
            <div className="card">
              <h3>What we build</h3>
              <ul>
                <li>Ingestion pipelines with structured metadata and permission extraction at ingest time</li>
                <li>Chunking strategies aligned to document structure and role-relevant boundaries</li>
                <li>RBAC-aware retrieval integrated with identity systems — access enforced at query, not filtered after</li>
                <li>Evaluation harnesses with recall/precision baselines and adversarial query regression</li>
              </ul>
            </div>
            <div className="card">
              <h3>Production properties</h3>
              <ul>
                <li>Tenant and role-based access enforced at query time — zero cross-tenant document exposure</li>
                <li>Retrieval audit trail aligned to compliance and data access requirements</li>
                <li>Monitoring for recall drift and latency across tenant partitions</li>
                <li>Runbooks and ownership documentation delivered at handoff</li>
              </ul>
            </div>
          </div>

          <div className="pov" style={{ marginTop: 28 }}>
            <h3>What this architecture guarantees — by design.</h3>
            <p style={{ marginBottom: 12 }}>These aren&apos;t outcome projections. They&apos;re properties of how the system is built:</p>
            <ul style={{ marginBottom: 0 }}>
              <li><strong>Zero cross-tenant document exposure</strong> — access is enforced at the query layer against your identity system, not filtered after retrieval where gaps can slip through</li>
              <li><strong>Retrieval quality is measurable, not assumed</strong> — evaluation harnesses with recall and precision baselines mean you know when the system degrades, not just when users complain</li>
              <li><strong>Latency is observable under real load</strong> — monitoring across tenant partitions surfaces p95 drift before it becomes a support issue</li>
              <li><strong>Your team owns it at handoff</strong> — runbooks, ownership documentation, and regression checks in CI mean no dependency on us to keep it running</li>
            </ul>
          </div>

          <div className="pov" style={{ marginTop: 16 }}>
            <h3>Your ROI depends on your knowledge workflows, not ours.</h3>
            <p style={{ marginBottom: 0 }}>The business case for retrieval is driven by how much time your team spends searching for answers that should already be findable — support triage, document review, internal Q&amp;A. The Workflow Discovery maps that time, scores your data readiness, and produces your specific <strong>Efficiency Dividend</strong>. <Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>Calculate yours →</Link></p>
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="card">
            <h3>Without this architecture</h3>
            <ul>
              <li>Sensitive data exposed across tenants when access control relies on post-filtering</li>
              <li>Retrieval quality degrades over time without recall baselines to detect it</li>
              <li>No visibility into latency, drift, or failure modes at the retrieval layer</li>
              <li>Compliance exposure when retrieval decisions can&apos;t be audited</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="section cta-band">
        <div className="container">
          <h2>Find out if your knowledge workflows are ready — and where the architecture needs hardening first.</h2>
          <p className="lede">The Workflow Discovery scores your data readiness, access control maturity, and retrieval quality posture across your existing workflows. 12 questions. Results immediately.</p>
          <p className="sublede">No commitment required. Findings are confidential.</p>
          <div className="hero-actions">
            <Link className="button primary" href="/discovery#start-audit">Start the Discovery →</Link>
            <Link className="button" href="/work#rag">See a retrieval architecture pattern →</Link>
          </div>
        </div>
      </section>
    </>
  )
}
