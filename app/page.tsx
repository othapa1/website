import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Home',
  description: 'LotusNex helps growing businesses automate the right workflows and build AI that runs reliably in production. Process-first. Architecture-first.',
  openGraph: {
    url: 'https://lotusnex.com/',
    title: 'Home • LotusNex',
    description: 'LotusNex helps growing businesses automate the right workflows and build AI that runs reliably in production. Process-first. Architecture-first.',
  },
  twitter: {
    title: 'Home • LotusNex',
    description: 'LotusNex helps growing businesses automate the right workflows and build AI that runs reliably in production. Process-first. Architecture-first.',
  },
}

export default function HomePage() {
  return (
    <>
      <section className="hero">
        <div className="container">
          <p className="eyebrow">AI Engineering Studio</p>
          <h1>We help growing businesses automate the right workflows — and build the AI to run them in production.</h1>
          <p className="lede">
            LotusNex helps operations and engineering leaders identify which repetitive processes are worth automating — and builds the production AI systems to run them safely. Process-first. Architecture-first. Built to operate — by your team or ours.
          </p>
          <p className="audience-signal">Workflow automation · AI security · Production reliability</p>
          <div className="hero-actions">
            <Link className="button primary" href="/discovery#start-audit">Start the Discovery →</Link>
            <a className="button" href="#how-we-work">See how we work →</a>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>Sound familiar?</h2>
          <div className="grid-3">
            <div className="card">
              <h3>You know which workflows should be automated. You&apos;re not confident they&apos;re actually ready.</h3>
              <p>
                The candidates are obvious — document review, data re-entry, report generation. What&apos;s less obvious is whether your processes are consistent enough, your data accessible enough, and your systems connected enough to make automation work without creating new problems.
              </p>
            </div>
            <div className="card">
              <h3>It works in your demo. Real users are a different story.</h3>
              <p>
                Your AI feature impresses in controlled conditions. With real users, real data, and real edge cases, it hallucinates, breaks, or fails silently — and you don&apos;t have the visibility to know until something downstream goes wrong.
              </p>
            </div>
            <div className="card">
              <h3>You&apos;re live. But costs are climbing, errors are quiet, and you&apos;re not sure why.</h3>
              <p>
                The system is running. Token spend keeps drifting upward. Edge cases surface as customer complaints rather than alerts. You don&apos;t have a clear line from a bad output back to the decision that caused it — and that gap is getting harder to ignore.
              </p>
            </div>
          </div>
          <p className="section-transition">This is the moment we&apos;re built for.</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="pov">
            <p style={{ marginBottom: 8 }}>We&apos;ve built document extraction pipelines for professional services firms, permissioned retrieval systems for regulated SaaS platforms, agent orchestration with human approval gates for operations teams, and security hardening for AI systems already in production.</p>
            <a href="/work" style={{ fontWeight: 600, color: 'var(--navy-700)' }}>See our work →</a>
          </div>
        </div>
      </section>

      <section className="section" id="how-we-work">
        <div className="container">
          <h2>How we work</h2>
          <p className="lede">
            Every engagement starts with process and architecture — defining what to automate, how it will fail, and what it takes to operate it before a line of production code is written.
          </p>

          <div className="how-we-work-prestep">
            <p className="eyebrow" style={{ marginBottom: 6 }}>Before you engage</p>
            <p style={{ margin: 0 }}><strong><Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)' }}>Workflow Discovery</Link></strong> — free, 12 questions, 1 business day. You get a Workflow Readiness Score and an Efficiency Dividend: the dollar case for which workflows to automate first.</p>
          </div>

          <div className="steps">
            <div className="step">
              <p className="step-timeline">1–2 weeks</p>
              <h3>1) Audit</h3>
              <ul>
                <li>Target workflows mapped against production constraints</li>
                <li>Evaluation criteria and success metrics agreed upfront</li>
                <li>Failure modes defined before any code is written</li>
              </ul>
              <p className="step-outcome">You get: a scoped build plan — or an honest &quot;not yet.&quot;</p>
            </div>
            <div className="step">
              <p className="step-timeline">4–8 weeks</p>
              <h3>2) Build</h3>
              <ul>
                <li>Agents, pipelines, and integrations built to spec</li>
                <li>Evaluated against real data throughout — not just at the end</li>
                <li>Milestone checkpoints with your team — no black-box delivery</li>
              </ul>
              <p className="step-outcome">You get: a running system that holds up under real inputs.</p>
            </div>
            <div className="step">
              <p className="step-timeline">2 weeks + optional ongoing</p>
              <h3>3) Harden &amp; Own</h3>
              <ul>
                <li>Observability and alerting live before go-live</li>
                <li>Guardrails and approval flows validated</li>
                <li>Runbooks written for the people who operate it</li>
              </ul>
              <p className="step-outcome">You get: a system your team owns and can operate — or we stay involved on your terms.</p>
            </div>
          </div>

          <div className="cta-band" style={{ marginTop: 32, padding: '28px 32px', borderRadius: 'var(--radius)', border: '1px solid var(--border-light)' }}>
            <p style={{ margin: '0 0 16px', fontSize: 16, fontWeight: 600, color: 'var(--navy-900)' }}>The first step is the Workflow Discovery.</p>
            <p style={{ margin: '0 0 20px', color: 'var(--text-muted)', fontSize: 14 }}>12 questions. Results immediately. Free — whether we work together or not.</p>
            <div className="hero-actions" style={{ marginTop: 0 }}>
              <Link className="button primary" href="/discovery#start-audit">Start the Discovery →</Link>
              <Link className="button" href="/contact">Request a Review →</Link>
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-faint)', marginTop: 16, marginBottom: 0 }}>We work with 2–3 companies at a time. Current intake: open.</p>
          </div>
        </div>
      </section>
    </>
  )
}
