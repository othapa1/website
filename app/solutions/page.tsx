import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Solutions',
  description: 'LotusNex builds workflow automation systems and production AI — agent orchestration, retrieval infrastructure, and platform & reliability engineering.',
  openGraph: {
    url: 'https://lotusnex.com/solutions',
    title: 'Solutions • LotusNex',
    description: 'LotusNex builds workflow automation systems and production AI — agent orchestration, retrieval infrastructure, and platform & reliability engineering.',
  },
  twitter: {
    title: 'Solutions • LotusNex',
    description: 'LotusNex builds workflow automation systems and production AI — agent orchestration, retrieval infrastructure, and platform & reliability engineering.',
  },
}

export default function SolutionsPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">What we build</p>
          <h1>What we build</h1>
          <p className="lede">
            We identify which workflows are worth automating, then build the AI systems to run them — with security, evaluation, observability, and ownership built in from the start.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="pov" style={{ marginBottom: 32 }}>
            <p style={{ margin: 0 }}>Not sure which of these fits your situation? <Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>Start the Workflow Discovery →</Link> — a 12-question diagnostic that identifies which workflows are ready to automate and where your architecture needs work before you commit to a build.</p>
          </div>
        </div>
        <div className="container">
          <p className="lede" style={{ maxWidth: '64ch', marginBottom: 32 }}>Six capabilities. Start with an audit if you&apos;re not sure what to build — or go straight to the service that matches where you are.</p>
          <div className="grid-2">
            <div className="card">
              <p className="card-hook">Your team runs the same workflow every day — manually. That&apos;s recoverable time, but only if the automation is built on a process that&apos;s actually ready to carry it.</p>
              <h3>Process Automation</h3>
              <ul>
                <li><strong>LLM extraction with confidence scoring</strong> — manual transcription eliminated, not just reduced</li>
                <li><strong>Human review routing for edge cases</strong> — people handle exceptions, the system handles the rest</li>
                <li><strong>End-to-end audit trail</strong> — the process is compliance-ready from day one</li>
              </ul>
              <div className="work-tease-outcome" style={{ marginTop: 14 }}>No silent extraction failures · Every edge case routed to human review · Audit trail from intake to write</div>
              <Link href="/solutions/process" style={{ marginTop: 14, display: 'inline-block' }}>Explore process automation →</Link>
            </div>

            <div className="card">
              <p className="card-hook">Whether you&apos;re building your first automated workflow or fixing one already failing in production — agent systems need defined boundaries, approval gates, and a plan for when they fail.</p>
              <h3>Agent Orchestration Systems</h3>
              <ul>
                <li><strong>Risk-tiered approval gates</strong> — agents handle routine decisions, humans approve what matters</li>
                <li><strong>Deterministic failure handling</strong> — no task degrades silently into a bad output</li>
                <li><strong>Per-workflow cost telemetry</strong> — token spend is predictable before you scale</li>
              </ul>
              <div className="work-tease-outcome" style={{ marginTop: 14 }}>No task degrades silently · Every decision is auditable · Your team owns it at handoff</div>
              <Link href="/solutions/agentic" style={{ marginTop: 14, display: 'inline-block' }}>Explore agent orchestration →</Link>
            </div>

            <div className="card">
              <p className="card-hook">If your team is searching for answers across documents and systems — whether you&apos;ve built something or are just starting — retrieval needs to be accurate, permission-aware, and measurable.</p>
              <h3>Knowledge Retrieval</h3>
              <ul>
                <li><strong>Permission-enforced retrieval at query time</strong> — the right content reaches the right person, enforced</li>
                <li><strong>Evaluation harnesses with recall baselines</strong> — retrieval quality is measurable, not guesswork</li>
                <li><strong>Structured ingestion and chunking</strong> — answers come from the right source, not just the most recent</li>
              </ul>
              <div className="work-tease-outcome" style={{ marginTop: 14 }}>Zero cross-tenant exposure by design · Quality measurable, not assumed · Degradation surfaces before users notice</div>
              <Link href="/solutions/rag" style={{ marginTop: 14, display: 'inline-block' }}>Explore knowledge retrieval →</Link>
            </div>

            <div className="card" id="security-hardening">
              <p className="card-hook">Your AWRA score flagged security gaps. Or you already know your AI handles sensitive data and no one has ever tested what happens when a user tries to break it.</p>
              <h3>AI Security &amp; Hardening</h3>
              <ul>
                <li><strong>Adversarial testing &amp; prompt injection red-teaming</strong> — we attempt to break your system before someone else does</li>
                <li><strong>Access control audit at the query layer</strong> — enforce who can reach what, at retrieval time, not via model instructions</li>
                <li><strong>Data sensitivity review</strong> — map PII, regulated, and customer data flows through your AI stack and close the gaps</li>
              </ul>
              <div className="work-tease-outcome" style={{ marginTop: 14 }}>Structured findings report · Prioritised remediation plan · Retesting included</div>
              <Link href="/contact" style={{ marginTop: 14, display: 'inline-block' }}>Request a security review →</Link>
            </div>

            <div className="card" id="platform">
              <p className="card-hook">The workflows you automate are only as reliable as the platform running them. Without the right foundation, the first production incident becomes the last time users trust it.</p>
              <h3>Platform &amp; Reliability Engineering</h3>
              <ul>
                <li><strong>Full-stack observability with alerting</strong> — incidents surface in dashboards, not customer complaints</li>
                <li><strong>CI/CD pipelines with rollback capability</strong> — deployments don&apos;t break what&apos;s already running</li>
                <li><strong>Cost telemetry and budget controls</strong> — infrastructure spend is trackable and predictable</li>
              </ul>
              <div className="work-tease-outcome" style={{ marginTop: 14 }}>Incidents in dashboards, not complaints · Spend predictable before you scale · No dependency on us to keep it running</div>
              <Link href="/solutions/platform" style={{ marginTop: 14, display: 'inline-block' }}>Explore platform &amp; reliability →</Link>
            </div>

            <div className="card" id="ai-audit">
              <p className="card-hook">Not sure which service you need — or whether you&apos;re ready to build at all? An audit gives you a structured answer, a prioritised set of findings, and a clear path forward before you commit to anything.</p>
              <h3>AI Readiness Audit</h3>
              <ul>
                <li><strong>AI Audit Lite</strong> — one workflow, one system. Covers process fit, architecture gaps, and data readiness. Delivered in two weeks. Includes a findings report and a prioritised action list.</li>
                <li><strong>AI Audit Full</strong> — your full workflow portfolio or a complex multi-system build. Covers all four readiness constructs: automation leverage, production risk, economic confidence, and evidence quality. Delivered in two weeks. Includes an architecture decision record, full findings report, and a phased build roadmap.</li>
              </ul>
              <div className="work-tease-outcome" style={{ marginTop: 14 }}>Named deliverable · Fixed scope · No open-ended retainer</div>
              <Link href="/contact" style={{ marginTop: 14, display: 'inline-block' }}>Book an audit →</Link>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
