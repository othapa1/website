import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Platform & Reliability Engineering',
  description: 'Platform foundations for AI workflow systems: observability, CI/CD, security controls, cost telemetry, and reliability engineering for production deployments.',
  openGraph: {
    url: 'https://lotusnex.com/solutions/platform',
    title: 'Platform & Reliability Engineering • LotusNex',
    description: 'Platform foundations for AI workflow systems: observability, CI/CD, security controls, cost telemetry, and reliability engineering for production deployments.',
  },
  twitter: {
    title: 'Platform & Reliability Engineering • LotusNex',
    description: 'Platform foundations for AI workflow systems: observability, CI/CD, security controls, cost telemetry, and reliability engineering for production deployments.',
  },
}

export default function PlatformPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">Platform &amp; infrastructure</p>
          <h1>Platform &amp; Reliability Engineering</h1>
          <p className="lede">
            The workflows you automate are only as durable as the platform running them. AI systems fail in production not at the model layer — but because the surrounding infrastructure was never built to carry them: no observability, no rollback, no cost controls.
          </p>
          <p>We build the platform layer that makes AI workflow systems observable, operable, and maintainable — before the first production incident, not after.</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="pov">
            <h3>AI systems are software systems. They require the same CI/CD, observability, security, and reliability patterns as any production service — and most are deployed without them.</h3>
            <p style={{ marginBottom: 0 }}>The first production incident is rarely a model failure. It&apos;s a deployment with no rollback capability, an alert that should have fired at hour two but fires at day four, or a cost spike that was always predictable with the right telemetry in place.</p>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="grid-2" style={{ marginBottom: 20 }}>
            <div className="card">
              <h3>What we build</h3>
              <ul>
                <li>Full-stack observability with tracing, logging, and configured alerting</li>
                <li>CI/CD pipelines with rollback capability and deployment safeguards</li>
                <li>Cost telemetry with per-workflow attribution and budget controls</li>
                <li>Security controls — access management, audit logging, least-privilege policies</li>
                <li>Incident response runbooks and escalation paths delivered at go-live</li>
              </ul>
            </div>
            <div className="card">
              <h3>Production properties</h3>
              <ul>
                <li>Incidents surface in dashboards and alerts — not in customer complaints</li>
                <li>Deployments don&apos;t break what&apos;s already running</li>
                <li>Infrastructure spend is trackable and predictable before you scale</li>
                <li>Access controls are auditable and aligned to compliance requirements</li>
                <li>Systems designed for long-term maintainability by your team</li>
              </ul>
            </div>
          </div>

          <div className="pov" style={{ marginTop: 28 }}>
            <h3>What this architecture guarantees — by design.</h3>
            <p style={{ marginBottom: 12 }}>These aren&apos;t outcome projections. They&apos;re properties of how the system is built:</p>
            <ul style={{ marginBottom: 0 }}>
              <li><strong>Incidents surface before users notice them</strong> — full-stack observability with configured alerting means the dashboard fires first, not a customer complaint</li>
              <li><strong>Deployments don&apos;t break what&apos;s running</strong> — CI/CD pipelines with rollback capability and deployment safeguards are part of every build, not retrofitted after an incident</li>
              <li><strong>Spend is predictable before you scale</strong> — per-workflow cost telemetry and budget controls mean no surprise infrastructure bills as volume grows</li>
              <li><strong>Your team owns it at handoff</strong> — runbooks, escalation paths, and ownership documentation are delivered at go-live, not left as institutional knowledge</li>
            </ul>
          </div>

          <div className="pov" style={{ marginTop: 16 }}>
            <h3>Your ROI depends on your platform gaps, not ours.</h3>
            <p style={{ marginBottom: 0 }}>The cost of missing platform infrastructure is measured in incident response time, cost overruns, and the engineering hours spent on manual operational work. The Workflow Discovery surfaces your reliability and observability gaps and scores them against your deployment context. <Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>See where you stand →</Link></p>
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="card">
            <h3>Without this architecture</h3>
            <ul>
              <li>Systems fail without visibility or clear root cause — you find out when users do</li>
              <li>Deployments introduce instability with no rollback path</li>
              <li>AI spend grows without cost attribution to tell you why</li>
              <li>Teams rely on manual intervention and tribal knowledge to keep systems running</li>
              <li>Compliance exposure when access decisions can&apos;t be audited</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="section cta-band">
        <div className="container">
          <h2>If your AI system is difficult to operate, the issue is not the model — it&apos;s the platform.</h2>
          <p className="lede">Start with the Workflow Discovery to surface reliability and observability gaps before your automated workflows depend on a system that wasn&apos;t built to carry them.</p>
          <p className="sublede">No commitment required. Findings are confidential.</p>
          <div className="hero-actions">
            <Link className="button primary" href="/discovery#start-audit">Start the Discovery →</Link>
            <Link className="button" href="/contact">Request a Review →</Link>
          </div>
        </div>
      </section>
    </>
  )
}
