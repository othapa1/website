'use client'

import Link from 'next/link'
import Image from 'next/image'
import { usePathname } from 'next/navigation'

export default function Header() {
  const pathname = usePathname()

  const isActive = (href: string) => {
    if (href === '/solutions') return pathname.startsWith('/solutions')
    if (href === '/work') return pathname === '/work'
    if (href === '/company') return pathname === '/company'
    return false
  }

  const isDiscovery = pathname === '/discovery'

  return (
    <header className="site-header">
      <div className="container header-inner">
        <Link className="brand brand-logo" href="/">
          <Image src="/logo.png" alt="LotusNex logo" width={32} height={32} />
          <span>LotusNex</span>
        </Link>
        <nav className="site-nav" aria-label="Primary">
          <Link className={isActive('/solutions') ? 'active' : ''} href="/solutions">Solutions</Link>
          <Link className={isActive('/work') ? 'active' : ''} href="/work">Work</Link>
          <Link className={isActive('/company') ? 'active' : ''} href="/company">Company</Link>
          <Link className={`cta${isDiscovery ? ' active' : ''}`} href="/discovery#start-audit">Start the Discovery →</Link>
        </nav>
      </div>
    </header>
  )
}
