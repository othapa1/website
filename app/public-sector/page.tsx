import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Public Sector',
  description: 'LotusNex supports selective federal and public sector programs requiring secure, auditable, production-grade AI systems engineering and platform delivery.',
  openGraph: {
    url: 'https://lotusnex.com/public-sector',
    title: 'Public Sector • LotusNex',
    description: 'LotusNex supports selective federal and public sector programs requiring secure, auditable, production-grade AI systems engineering and platform delivery.',
  },
}

export default function PublicSectorPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">Federal &amp; public sector delivery</p>
          <h1>Engineering discipline for<br />program environments.</h1>
          <p className="lede">
            LotusNex supports selective federal and public sector programs that require secure, auditable AI systems built to operate under real program constraints — not adapted from commercial pilots after the fact.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="pov">
            <h3>Program environments are not commercial environments with extra steps.</h3>
            <p>
              They carry different operational burdens: audit requirements, access control obligations, approval structures, and delivery timelines that don&apos;t flex the same way. AI systems introduced into these environments must be engineered with those constraints as first-class inputs — not retrofitted to meet them after build.
            </p>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>Where we engage</h2>
          <p className="lede">
            We work on programs where engineering rigor is a requirement, not a preference — and where the team needs a delivery partner with production discipline, not a vendor managing scope.
          </p>
          <div className="grid-2">
            <div className="card">
              <h3>AI systems for program operations</h3>
              <p>Agentic workflows and retrieval systems designed for the access control, auditability, and human oversight requirements common to program environments.</p>
              <ul>
                <li>Permissioned knowledge retrieval with role-aligned access</li>
                <li>Agentic workflows with approval gates and human-in-the-loop controls</li>
                <li>Full tool-call audit logging and trace spans</li>
                <li>Evaluation harnesses and regression checks before deployment</li>
              </ul>
            </div>
            <div className="card">
              <h3>Platform modernization and reliability</h3>
              <p>Foundation engineering that prepares program platforms for AI workloads — or stabilizes existing systems that have accumulated operational debt.</p>
              <ul>
                <li>Cloud and hybrid architecture with Infrastructure as Code</li>
                <li>Application modernization across .NET, Python, and TypeScript stacks</li>
                <li>Observability, alerting, and incident response readiness</li>
                <li>DevSecOps pipelines with automated security gates</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>How we operate in program contexts</h2>
          <div className="stack">
            <div className="pov">
              <h3>Constraints are inputs, not obstacles.</h3>
              <p>
                Access restrictions, approval chains, data handling requirements, and environment limitations are defined upfront and built around — not discovered mid-engagement. Architecture reviews begin with program constraints, not commercial defaults.
              </p>
            </div>
            <div className="pov">
              <h3>Auditability is structural.</h3>
              <p>
                Every system we deliver in a program context is built with audit trails, access logging, and operational traceability as architectural requirements. These are not added at the end — they are part of the design from the first session.
              </p>
            </div>
            <div className="pov">
              <h3>Handoff is the delivery milestone.</h3>
              <p>
                Program teams must own and operate what we build. Runbooks, interface documentation, observability baselines, and clear ownership boundaries are part of every engagement — not optional deliverables that get cut when timelines compress.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>Production requirements we design for</h2>
          <div className="grid-2">
            <div className="list-block">
              <h3>Access and identity</h3>
              <ul>
                <li>Role-based access control aligned to program identity systems</li>
                <li>Least-privilege tool and data access</li>
                <li>SSO integration and session management</li>
              </ul>
            </div>
            <div className="list-block">
              <h3>Auditability and oversight</h3>
              <ul>
                <li>Full audit logging on system actions and data access</li>
                <li>Human approval gates for consequential operations</li>
                <li>Traceability from input to output across all AI interactions</li>
              </ul>
            </div>
            <div className="list-block">
              <h3>Operational reliability</h3>
              <ul>
                <li>Deterministic fallbacks — no silent degradation</li>
                <li>Incident response runbooks and escalation paths</li>
                <li>Monitoring, alerting, and error budgets</li>
              </ul>
            </div>
            <div className="list-block">
              <h3>Evaluation and quality</h3>
              <ul>
                <li>Offline test sets and regression checks before deployment</li>
                <li>Guardrail validation against defined boundary conditions</li>
                <li>Ongoing quality monitoring post-deployment</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="section cta-band">
        <div className="container">
          <h2>Discuss a program need</h2>
          <p className="lede">
            Share the program context, operational constraints, and where you are in the delivery lifecycle. We&apos;ll respond with a concrete assessment and next step.
          </p>
          <p className="sublede">No commitment required. You&apos;ll leave with a clear architectural assessment — whether we work together or not.</p>
          <div className="hero-actions">
            <Link className="button primary" href="/contact">Request a Review →</Link>
            <Link className="button" href="/solutions">See engineering disciplines</Link>
          </div>
        </div>
      </section>
    </>
  )
}
