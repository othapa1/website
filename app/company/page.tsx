import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Company',
  description: 'LotusNex is an AI engineering studio that helps growing businesses automate the right workflows and build production AI systems — process-first, architecture-first, built to operate.',
  openGraph: {
    url: 'https://lotusnex.com/company',
    title: 'Company • LotusNex',
    description: 'LotusNex is an AI engineering studio that helps growing businesses automate the right workflows and build production AI systems — process-first, architecture-first, built to operate.',
  },
  twitter: {
    title: 'Company • LotusNex',
    description: 'LotusNex is an AI engineering studio that helps growing businesses automate the right workflows and build production AI systems — process-first, architecture-first, built to operate.',
  },
}

export default function CompanyPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">Who we are</p>
          <h1>Built from platform engineering.<br />Applied to AI systems.</h1>
          <p className="lede">
            LotusNex comes out of more than a decade in production software engineering — enterprise platforms, education systems, process control environments — where reliability, observability, and failure handling were not optional.
          </p>
          <p>When AI systems began entering production, what failed was rarely the model. It was the surrounding architecture: evaluation, boundaries, monitoring, ownership. And before any of that, the wrong question was being asked — <em>which workflow should we automate first?</em></p>
          <p><strong>LotusNex was built to close both gaps.</strong> The <Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>Workflow Discovery</Link> identifies which workflows are ready to automate and where the architecture needs hardening first. The engineering practice builds the systems around the model — evaluated, observable, and owned in production.</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>Who you&apos;ll work with</h2>
          <div className="card" style={{ maxWidth: 640 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20 }}>
              <Image
                src="/images/om-headshot.png"
                alt="Om Thapa"
                width={72}
                height={72}
                style={{ borderRadius: '50%', objectFit: 'cover', border: '2px solid #0B2E4F', flexShrink: 0 }}
              />
              <div>
                <h3 style={{ margin: '0 0 4px' }}>Om Thapa</h3>
                <p className="eyebrow" style={{ margin: 0 }}>Founder &amp; Lead Engineer</p>
              </div>
            </div>
            <p>Om has been building production software since 2011 across enterprise platforms, education systems, and process control environments — where reliability, system boundaries, and operational clarity are critical.</p>
            <p>His background spans cloud architecture, reliability engineering, and large-scale systems integration, with a focus on systems that must perform under real-world constraints.</p>
            <p>He founded LotusNex after consistently seeing AI systems break in production — not at the model layer, but in the surrounding architecture required to make them usable and reliable.</p>
            <p>He works with teams that treat AI as production infrastructure — not experimentation.</p>
            <p>Every LotusNex engagement is led directly by Om, from initial architecture review through final handoff.</p>
            <a href="https://www.linkedin.com/in/othapa" target="_blank" rel="noopener noreferrer">LinkedIn →</a>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>How we are structured</h2>
          <p className="lede">
            LotusNex operates as a focused engineering studio. Every engagement is led directly by the founder — architecture through handoff. Engagements are kept small by design: tight scope, clear interfaces, measurable outcomes.
          </p>
          <div className="grid-2">
            <div className="card">
              <h3>What we bring</h3>
              <ul>
                <li>Years of enterprise platform and cloud architecture delivery</li>
                <li>Deep DevSecOps and reliability engineering practice</li>
                <li>Production AI systems across agentic and retrieval domains</li>
                <li>AI security hardening — adversarial testing, access control audits, and data sensitivity review</li>
              </ul>
            </div>
            <div className="card">
              <h3>How we engage</h3>
              <ul>
                <li>Architecture review before any build commitment</li>
                <li>Explicit evaluation criteria defined upfront</li>
                <li>Hardening, observability, and guardrails before handoff</li>
                <li>Clean documentation and operational ownership on exit</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>Operating principles</h2>
          <div className="stack">
            <div className="pov">
              <h3>We build systems, not experiments.</h3>
              <p>
                Every engagement is scoped around production constraints: real users, real data, real operational burden. If a system cannot be evaluated, monitored, and owned, it is not ready to ship.
              </p>
            </div>
            <div className="pov">
              <h3>We take on fewer, more serious engagements.</h3>
              <p>
                LotusNex is selective by design. We engage where there is a real architectural problem and clear intent to ship production systems. We do not optimize for volume.
              </p>
            </div>
            <div className="pov">
              <h3>We build for whoever operates the system — your team or ours.</h3>
              <p>
                Clean handoff is part of every engagement. Runbooks, interface documentation, observability baselines, and ownership clarity are not optional. Some clients take full ownership at handoff. Others retain us for ongoing operations. Either way, the system is built to be operated clearly.
              </p>
            </div>
            <div className="pov">
              <h3>We treat security as architecture, not a feature.</h3>
              <p>
                Access control, adversarial posture, and data sensitivity are design inputs — not a checklist applied at the end. In AI systems, security gaps that aren&apos;t caught in architecture surface as incidents in production. We build the controls in from the start.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="section cta-band">
        <div className="container">
          <h2>If this matches how you think about building.</h2>
          <p className="lede">Start with the Workflow Discovery — 12 questions, results immediately — or reach out directly if you already know what you need.</p>
          <div className="hero-actions">
            <Link className="button primary" href="/discovery#start-audit">Start the Discovery →</Link>
            <Link className="button" href="/contact">Request a Review →</Link>
          </div>
        </div>
      </section>
    </>
  )
}
