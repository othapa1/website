import type { Metadata } from 'next'
import DiscoveryTool from '@/components/discovery/DiscoveryTool'

export const metadata: Metadata = {
  title: 'Workflow Discovery',
  description: 'A 12-question diagnostic for operations and engineering leaders. Find out which workflows are worth automating and where your AI system is fragile — before you ship.',
  openGraph: {
    url: 'https://lotusnex.com/discovery',
    title: 'Workflow Discovery · LotusNex',
    description: 'A 12-question diagnostic for operations and engineering leaders. Find out which workflows are worth automating and where your AI system is fragile — before you ship.',
  },
  twitter: {
    title: 'Workflow Discovery · LotusNex',
    description: 'A 12-question diagnostic for operations and engineering leaders. Find out which workflows are worth automating and where your AI system is fragile — before you ship.',
  },
}

export default function DiscoveryPage() {
  return <DiscoveryTool />
}
