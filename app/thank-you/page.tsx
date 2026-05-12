import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Request received',
  description: 'LotusNex — AI Engineering Studio for B2B SaaS',
  robots: { index: false },
  openGraph: {
    url: 'https://lotusnex.com/thank-you',
    title: 'Request received · LotusNex',
    description: 'LotusNex — AI Engineering Studio for B2B SaaS',
  },
  twitter: {
    title: 'Request received · LotusNex',
    description: 'LotusNex — AI Engineering Studio for B2B SaaS',
  },
}

export default function ThankYouPage() {
  return (
    <>
      <section className="hero hero-compact">
        <div className="container" style={{ textAlign: 'center', maxWidth: 560, margin: '0 auto' }}>
          <p style={{ fontSize: 36, marginBottom: 12 }}>✓</p>
          <p className="eyebrow">Request received</p>
          <h1>You&apos;re on the list.</h1>
          <p className="lede">
            We&apos;ll review your intake and send you the diagnostic link within 1 business day.
          </p>
          <p style={{ fontSize: 14, color: 'var(--text-muted)', marginTop: 8 }}>
            Questions in the meantime? <a href="mailto:contact@lotusnex.com" style={{ color: 'var(--navy-700)', fontWeight: 500 }}>contact@lotusnex.com</a>
          </p>
          <div className="hero-actions" style={{ marginTop: 32, justifyContent: 'center' }}>
            <Link className="button" href="/">← Back to home</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container" style={{ maxWidth: 640, margin: '0 auto' }}>
          <h2>What happens next</h2>
          <div className="steps">
            <div className="step">
              <h3>1) We review your intake</h3>
              <p style={{ fontSize: 14, color: 'var(--text-muted)' }}>We read every submission. If your intake is unclear or we need more context, we&apos;ll email you before sending the diagnostic.</p>
            </div>
            <div className="step">
              <h3>2) You receive the diagnostic link</h3>
              <p style={{ fontSize: 14, color: 'var(--text-muted)' }}>Within 1 business day. 12 questions across Process Fit, Security, Tokenomics, and Reliability.</p>
            </div>
            <div className="step">
              <h3>3) 30-minute peer review</h3>
              <p style={{ fontSize: 14, color: 'var(--text-muted)' }}>We walk through your Workflow Readiness Score and Efficiency Dividend together — process fit and production architecture in one call.</p>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
