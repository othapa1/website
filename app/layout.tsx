import type { Metadata } from 'next'
import '../styles/globals.css'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'

export const metadata: Metadata = {
  metadataBase: new URL('https://lotusnex.com'),
  title: {
    default: 'LotusNex',
    template: '%s • LotusNex',
  },
  description: 'LotusNex helps growing businesses automate the right workflows and build AI that runs reliably in production.',
  openGraph: {
    siteName: 'LotusNex',
    images: [{ url: '/og-image.png' }],
  },
  twitter: {
    card: 'summary_large_image',
  },
  icons: {
    icon: '/logo.png',
    apple: '/logo.png',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  )
}
