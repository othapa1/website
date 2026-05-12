/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      { source: '/index.html', destination: '/', permanent: true },
      { source: '/solutions.html', destination: '/solutions', permanent: true },
      { source: '/solutions-process.html', destination: '/solutions/process', permanent: true },
      { source: '/solutions-agentic.html', destination: '/solutions/agentic', permanent: true },
      { source: '/solutions-rag.html', destination: '/solutions/rag', permanent: true },
      { source: '/solutions-platform.html', destination: '/solutions/platform', permanent: true },
      { source: '/work.html', destination: '/work', permanent: true },
      { source: '/company.html', destination: '/company', permanent: true },
      { source: '/contact.html', destination: '/contact', permanent: true },
      { source: '/awra.html', destination: '/discovery', permanent: true },
      { source: '/thank-you.html', destination: '/thank-you', permanent: true },
      { source: '/public-sector.html', destination: '/public-sector', permanent: true },
      { source: '/meet.html', destination: '/company', permanent: true },
      { source: '/meet_mobile.html', destination: '/company', permanent: true },
    ]
  },
}

export default nextConfig
