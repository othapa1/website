import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Contact',
  description: 'Request a Review with LotusNex. In 30 minutes, we\'ll map your AI system, identify production risks, and give you a concrete path forward.',
  openGraph: {
    url: 'https://lotusnex.com/contact',
    title: 'Contact • LotusNex',
    description: 'Request a Review with LotusNex. In 30 minutes, we\'ll map your AI system, identify production risks, and give you a concrete path forward.',
  },
  twitter: {
    title: 'Contact • LotusNex',
    description: 'Request a Review with LotusNex. In 30 minutes, we\'ll map your AI system, identify production risks, and give you a concrete path forward.',
  },
}

export default function ContactPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">For teams who know what they need</p>
          <h1>Request a Review</h1>
          <p className="lede">
            In a 30-minute review, we&apos;ll map your current AI system, identify the top production risks, and give you a concrete path forward — whether you work with us or not. No pitch. No generic acknowledgment. A direct technical reaction to your architecture.
          </p>
          <p style={{ marginTop: 14, fontSize: 14, color: 'var(--text-muted)' }}>Not sure what you need yet? <Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>Start the Workflow Discovery first →</Link> It takes 12 questions and gives you a clear picture of which workflows to automate and where your system is fragile — before committing to a build.</p>
        </div>
      </section>

      <section className="section">
        <div className="container grid-2">
          <div className="card">
            <h2>Email</h2>
            <p>The most direct path. Send a short note with the context below and we&apos;ll respond within one business day with a concrete reaction or follow-up question.</p>
            <ul>
              <li><a href="mailto:contact@lotusnex.com">contact@lotusnex.com</a></li>
              <li>Fairfax Station, VA, USA</li>
              <li>Standard U.S. business hours<br /><span style={{ fontSize: 13, color: 'var(--text-faint)' }}>Flexible for critical release windows</span></li>
            </ul>
          </div>
          <div className="card">
            <h2>Schedule a call</h2>
            <p>Prefer to talk through the architecture directly? Book your review. We&apos;ll review your system constraints, identify the key risks, and discuss a concrete build approach.</p>
            <ul>
              <li>30-minute focused session</li>
              <li>Bring a description of your system and where it&apos;s breaking</li>
              <li>You&apos;ll leave with identified risks and a concrete next step — or an honest &quot;not the right fit&quot;</li>
            </ul>
            <a className="button primary" href="https://calendar.app.google/YbWaPGo2vLwS1K396" target="_blank" rel="noopener noreferrer" style={{ marginTop: 16, display: 'inline-flex' }}>
              Book a 30-min call →
            </a>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>What to include</h2>
          <p className="lede" style={{ marginBottom: 28 }}>
            The more context you provide upfront, the more useful the first response. We don&apos;t need a polished brief — rough notes work.
          </p>
          <div className="grid-2">
            <div className="list-block">
              <h3>The workflow</h3>
              <ul>
                <li>What process or workflow you&apos;re trying to automate, harden, or recover</li>
                <li>Who runs it today and at what volume or frequency</li>
                <li>What data flows through it and how sensitive it is</li>
                <li>What you&apos;ve built already, if anything</li>
              </ul>
            </div>
            <div className="list-block">
              <h3>The constraints</h3>
              <ul>
                <li>Security, compliance, and audit requirements</li>
                <li>Timeline and delivery expectations</li>
                <li>How you define a successful outcome</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="pov">
            <h3>What to expect after you reach out.</h3>
            <p>
              We review every inbound request ourselves. If there&apos;s a fit, we&apos;ll respond with a direct reaction to the workflow and constraints you&apos;ve described — not a generic acknowledgment. We respond within one business day. If it&apos;s not the right engagement for us, we&apos;ll say so clearly and, where possible, point you in a useful direction.
            </p>
            <p style={{ marginBottom: 0, fontSize: 15 }}>Ready to book directly? <a href="https://calendar.app.google/YbWaPGo2vLwS1K396" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>Book a 30-min call →</a></p>
          </div>
        </div>
      </section>
    </>
  )
}
