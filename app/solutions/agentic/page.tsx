import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Agent Orchestration',
  description: 'LotusNex builds agent orchestration systems for production — defined tool boundaries, risk-tiered approval gates, deterministic failure handling, and full auditability.',
  openGraph: {
    url: 'https://lotusnex.com/solutions/agentic',
    title: 'Agent Orchestration • LotusNex',
    description: 'LotusNex builds agent orchestration systems for production — defined tool boundaries, risk-tiered approval gates, deterministic failure handling, and full auditability.',
  },
  twitter: {
    title: 'Agent Orchestration • LotusNex',
    description: 'LotusNex builds agent orchestration systems for production — defined tool boundaries, risk-tiered approval gates, deterministic failure handling, and full auditability.',
  },
}

export default function AgentOrchestrationPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container">
          <p className="eyebrow">Agent orchestration systems</p>
          <h1>Agents are bounded systems. Not autonomous loops.</h1>
          <p className="lede">
            Support triage, operations handoffs, approval routing, research pipelines — workflows where agents handle routine decisions and humans approve what matters. They fail in production when tool access is unbounded and failure modes are undefined.
          </p>
          <p>The difference between an agent that works in a demo and one that holds up in production is architecture — explicit tool boundaries, deterministic fallbacks, and a human escalation path that actually fires when it needs to.</p>
        </div>
      </section>

      <section className="section" id="agent-orchestration">
        <div className="container">
          <div className="pov" style={{ marginBottom: 28 }}>
            <h3>Most agent failures are architecture failures, not model failures.</h3>
            <p style={{ marginBottom: 0 }}>When an agent goes off-script, it&apos;s usually because tool permissions were too broad, failure modes weren&apos;t defined, or there was no human override path. We define those boundaries before anything goes to production — so incidents surface as alerts, not customer complaints.</p>
          </div>

          <div className="grid-2" style={{ marginBottom: 20 }}>
            <div className="card">
              <h3>What we build</h3>
              <ul>
                <li>Orchestration loops with explicit tool boundary definitions</li>
                <li>Least-privilege tool access and permission scoping</li>
                <li>Risk-tiered approval flow: auto-execute, human-in-loop, hard-stop</li>
                <li>Deterministic fallbacks — no task degrades silently</li>
                <li>Tool-call logging and execution trace spans</li>
              </ul>
            </div>
            <div className="card">
              <h3>Production properties</h3>
              <ul>
                <li>Full auditability through tool-call logs and execution traces</li>
                <li>Evaluation test set covering edge cases and adversarial inputs</li>
                <li>Per-workflow cost telemetry with token budgets</li>
                <li>Escalation path with notification and override mechanics</li>
                <li>Regression checks integrated into CI pipeline</li>
              </ul>
            </div>
          </div>

          <div className="pov" style={{ marginTop: 28 }}>
            <h3>What this architecture guarantees — by design.</h3>
            <p style={{ marginBottom: 12 }}>These aren&apos;t outcome projections. They&apos;re properties of how the system is built:</p>
            <ul style={{ marginBottom: 0 }}>
              <li><strong>No task degrades silently</strong> — deterministic fallbacks mean every failure either stops cleanly or escalates to a human, never drifts into a bad output</li>
              <li><strong>Every agent action is auditable</strong> — tool-call logs and execution traces give you a full decision record, not just a final answer</li>
              <li><strong>Cost is bounded before you scale</strong> — per-workflow token budgets and telemetry mean spending is predictable at volume, not just at demo scale</li>
              <li><strong>Your team owns it at handoff</strong> — regression checks in CI and documented escalation paths mean no dependency on us to keep it running</li>
            </ul>
          </div>

          <div className="pov" style={{ marginTop: 16 }}>
            <h3>Your ROI depends on your workflow, not ours.</h3>
            <p style={{ marginBottom: 0 }}>The return on agent orchestration is driven by how many hours your team spends on decisions that could be routed or automated — and how much risk those decisions carry if they go wrong. The Workflow Discovery maps both, and produces your specific <strong>Efficiency Dividend</strong> alongside a production risk score. <Link href="/discovery#start-audit" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>Calculate yours →</Link></p>
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="card">
            <h3>Without this architecture</h3>
            <ul>
              <li>Agents operate beyond intended boundaries when tool access isn&apos;t explicitly scoped</li>
              <li>Failures degrade silently rather than stopping deterministically</li>
              <li>No human override path means edge cases become incidents before anyone can intervene</li>
              <li>Costs become unpredictable under real usage volume without per-workflow telemetry</li>
              <li>No audit trail means you can&apos;t trace a bad output back to the decision that caused it</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="section cta-band">
        <div className="container">
          <h2>Find out if your workflow is ready for agent orchestration.</h2>
          <p className="lede">The Workflow Discovery identifies which multi-step processes have the right characteristics for agent automation and where the architecture needs hardening first. 12 questions. Results immediately.</p>
          <p className="sublede">No commitment required. Findings are confidential.</p>
          <div className="hero-actions">
            <Link className="button primary" href="/discovery#start-audit">Start the Discovery →</Link>
            <Link className="button" href="/contact">Request an architecture review →</Link>
          </div>
        </div>
      </section>
    </>
  )
}
