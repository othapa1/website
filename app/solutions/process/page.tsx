import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Process Automation',
  description: 'LotusNex builds document-level process automation pipelines — LLM extraction, human review routing, and end-to-end audit trails for high-volume, rule-bounded workflows.',
  openGraph: {
    url: 'https://lotusnex.com/solutions/process',
    title: 'Process Automation • LotusNex',
    description: 'LotusNex builds document-level process automation pipelines — LLM extraction, human review routing, and end-to-end audit trails for high-volume, rule-bounded workflows.',
  },
  twitter: {
    title: 'Process Automation • LotusNex',
    description: 'LotusNex builds document-level process automation pipelines — LLM extraction, human review routing, and end-to-end audit trails for high-volume, rule-bounded workflows.',
  },
}

export default function ProcessAutomationPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">Process automation</p>
          <h1>Eliminate the manual loop. Keep the human.</h1>
          <p className="lede">
            Document processing, data entry, report generation — workflows where the same structured work repeats at volume. Automation works here when the process is rule-bounded, errors are detectable, and humans stay in the loop for exceptions.
          </p>
          <p>The question isn&apos;t whether to automate. It&apos;s whether the workflow is consistent enough, the data accessible enough, and the architecture ready enough to carry it without creating a new class of silent errors.</p>
        </div>
      </section>

      <section className="section" id="process-automation">
        <div className="container">
          <div className="pov" style={{ marginBottom: 28 }}>
            <h3>Most automation projects fail on process fit, not technology.</h3>
            <p style={{ marginBottom: 0 }}>A workflow that looks rule-bounded often isn&apos;t — edge cases accumulate, confidence scores drift, and the human review queue fills up faster than anyone expected. We build the validation and review infrastructure first, so the automation runs on a foundation that can actually hold.</p>
          </div>

          <div className="grid-2" style={{ marginBottom: 20 }}>
            <div className="card">
              <h3>What we build</h3>
              <ul>
                <li>Document intake pipelines with format normalisation</li>
                <li>LLM extraction with per-field confidence scoring</li>
                <li>Human review routing for low-confidence outputs</li>
                <li>Write pipelines with dry-run mode and rollback on validation failure</li>
                <li>End-to-end audit trail from intake to system write</li>
              </ul>
            </div>
            <div className="card">
              <h3>Production properties</h3>
              <ul>
                <li>Validation layer catches format drift before extraction failures propagate</li>
                <li>Human review queue with SLA visibility and exception reporting</li>
                <li>Cost telemetry per document type with budget controls</li>
                <li>Evaluation harness against held-out document samples</li>
              </ul>
            </div>
          </div>

          <div className="pov" style={{ marginTop: 28 }}>
            <h3>What this architecture guarantees — by design.</h3>
            <p style={{ marginBottom: 12 }}>These aren&apos;t outcome projections. They&apos;re properties of how the system is built:</p>
            <ul style={{ marginBottom: 0 }}>
              <li><strong>No extraction failure goes undetected</strong> — the validation layer catches format drift and confidence drops before they reach downstream systems</li>
              <li><strong>Every low-confidence output routes to human review</strong> — exceptions don&apos;t fall through; they queue with SLA visibility</li>
              <li><strong>Full audit trail from intake to write</strong> — every decision is traceable, every output is attributable</li>
              <li><strong>Cost is predictable before you scale</strong> — per-document telemetry means you know the unit economics before volume grows</li>
            </ul>
          </div>

          <div className="pov" style={{ marginTop: 16 }}>
            <h3>Your ROI depends on your workflow, not ours.</h3>
            <p style={{ marginBottom: 0 }}>The return on process automation is a function of three variables: how many hours the workflow consumes today, how rule-bounded the process actually is, and what percentage of that time can shift from execution to review. The Workflow Discovery measures all three and produces your specific <strong>Efficiency Dividend</strong> — a conservative-to-optimistic range based on your team size, hours, and process characteristics. <Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>Calculate yours →</Link></p>
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="card">
            <h3>Without this architecture</h3>
            <ul>
              <li>Automation runs on workflows that aren&apos;t process-fit — cost shifts rather than gets removed</li>
              <li>Extraction failures propagate silently into downstream systems before anyone catches them</li>
              <li>Human review becomes a bottleneck with no SLA visibility or exception reporting</li>
              <li>No way to know whether the system is producing correct outputs at volume</li>
              <li>The first compliance audit surfaces gaps that were always there</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="section cta-band">
        <div className="container">
          <h2>Find out if your workflow is ready to automate.</h2>
          <p className="lede">The Workflow Discovery identifies which processes have the right characteristics for automation and where the architecture needs hardening first. 12 questions. Results immediately.</p>
          <p className="sublede">No commitment required. Findings are confidential.</p>
          <div className="hero-actions">
            <Link className="button primary" href="/discovery#start-audit">Start the Discovery →</Link>
            <Link className="button" href="/work#data-entry">See a process automation pattern →</Link>
          </div>
        </div>
      </section>
    </>
  )
}
