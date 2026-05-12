import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-slim">
        <div className="footer-brand">LotusNex</div>
        <div className="footer-links">
          <Link href="/solutions">Solutions</Link>
          <Link href="/work">Work</Link>
          <Link href="/company">Company</Link>
          <span>·</span>
          <a href="mailto:contact@lotusnex.com">contact@lotusnex.com</a>
          <span>·</span>
          <Link href="/discovery#start-audit">Start the Discovery →</Link>
          <span>·</span>
          <Link href="/contact">Request a Review →</Link>
        </div>
      </div>
      <div className="container footer-bottom">
        <small>© 2026 LotusNex. All rights reserved.</small>
      </div>
    </footer>
  )
}
