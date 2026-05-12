'use client'

import { useState, useCallback } from 'react'

const AWRA_API = process.env.NEXT_PUBLIC_AWRA_API_URL || 'https://awra-api.onrender.com'

// ── QUESTIONS ─────────────────────────────────────────────────────────────

type Stage = 'pre_ai' | 'pilot' | 'production'
type QType = 'radio' | 'checkbox'

interface Option {
  id: string
  label: string
  unsure?: boolean
  nyi?: boolean
}

interface Question {
  id: string
  pillar: string
  pillarLabel: string
  wording: Record<Stage, string>
  type: QType
  options: Option[]
}

const QUESTIONS: Question[] = [
  {
    id: 'q1', pillar: 'process',
    pillarLabel: 'Process Fit & Automation Leverage',
    wording: {
      pre_ai: 'How consistent are the workflows you are considering automating?',
      pilot: 'How consistent are the workflows you want to automate?',
      production: 'How consistent are the workflows your AI currently handles?',
    },
    type: 'radio',
    options: [
      { id: 'very_consistent', label: 'Very consistent — nearly identical each time, minimal judgment required' },
      { id: 'mostly_consistent', label: 'Mostly consistent with occasional exceptions that need human review' },
      { id: 'frequently_varies', label: 'Frequently varies — the right output depends on context and judgment' },
      { id: 'highly_variable', label: 'Highly variable — most instances require significant human judgment' },
      { id: 'not_sure', label: 'Not sure', unsure: true },
    ],
  },
  {
    id: 'q2', pillar: 'process',
    pillarLabel: 'Process Fit & Automation Leverage',
    wording: {
      pre_ai: 'When a manual process produces a wrong output, how quickly does your team catch it?',
      pilot: 'When a manual process produces a wrong output, how quickly does someone on your team catch it?',
      production: 'When the AI produces a wrong output, how quickly does your team catch it?',
    },
    type: 'radio',
    options: [
      { id: 'same_day', label: "Same day — there's a clear check before the output leaves the team" },
      { id: 'within_week', label: 'Within a week — someone downstream usually notices' },
      { id: 'days_later', label: 'We often find out through downstream effects, days later' },
      { id: 'rarely', label: 'Rarely — unless a customer or external party reports it' },
      { id: 'not_sure', label: 'Not sure', unsure: true },
    ],
  },
  {
    id: 'q3', pillar: 'process',
    pillarLabel: 'Process Fit & Automation Leverage',
    wording: {
      pre_ai: 'How much of the manual work involves re-entering the same data across multiple systems?',
      pilot: 'How much of the manual work you want to automate involves re-entering the same data across multiple systems?',
      production: 'How much of the remaining manual work involves re-entering data across multiple systems?',
    },
    type: 'radio',
    options: [
      { id: 'more_than_half', label: 'More than half — the same information gets entered in 2+ systems routinely' },
      { id: 'significant', label: 'A significant portion — this happens daily for our team' },
      { id: 'occasionally', label: 'Occasionally — maybe a few times per week' },
      { id: 'rarely', label: 'Rarely — most workflows are contained in a single system' },
      { id: 'not_sure', label: 'Not sure', unsure: true },
    ],
  },
  {
    id: 'q4', pillar: 'process',
    pillarLabel: 'Process Fit & Automation Leverage',
    wording: {
      pre_ai: 'Which types of workflows are you hoping to automate?',
      pilot: 'Which workflows is your AI pilot targeting?',
      production: 'Which workflow types does your AI system currently handle?',
    },
    type: 'checkbox',
    options: [
      { id: 'document_processing', label: 'Document processing — invoices, contracts, reports' },
      { id: 'support_ticket_triage', label: 'Customer support and ticket triage' },
      { id: 'internal_knowledge_retrieval', label: 'Internal knowledge retrieval and Q&A' },
      { id: 'data_entry_duplicate_entry', label: 'Data entry and cross-system re-entry' },
      { id: 'report_generation', label: 'Report generation and analytics prep' },
      { id: 'compliance_evidence', label: 'Compliance evidence and audit trail generation' },
      { id: 'sales_cs_handoffs', label: 'Sales and CS handoffs or summaries' },
      { id: 'qa_test_generation', label: 'QA and test case generation' },
      { id: 'incident_summarization', label: 'Incident summarization and post-mortems' },
      { id: 'invoice_ap_ar', label: 'Invoice processing / AP-AR workflows' },
      { id: 'onboarding_offboarding', label: 'Employee onboarding or offboarding tasks' },
      { id: 'meeting_notes', label: 'Meeting notes and action item extraction' },
      { id: 'other', label: 'Something else — still figuring it out' },
    ],
  },
  {
    id: 'q5', pillar: 'security',
    pillarLabel: 'Security & Tenant Isolation',
    wording: {
      pre_ai: 'If you built AI for these workflows, how would you enforce which records each user is allowed to see?',
      pilot: "When your AI returns information to a user, does it enforce which records that user is allowed to see?",
      production: "When your AI returns information to a user, does it enforce which records that user is allowed to see?",
    },
    type: 'radio',
    options: [
      { id: 'enforced_tested', label: "Yes — enforced at query time with controls we've tested" },
      { id: 'mostly_filtered', label: "Mostly — we filter results, but haven't tested edge cases formally" },
      { id: 'system_prompt', label: 'We rely on the model to respect the context set in the system prompt' },
      { id: 'no_controls', label: 'No controls in place — all users can reach all content' },
      { id: 'not_applicable', label: 'Not applicable — single-tenant or no AI in production yet', unsure: true },
    ],
  },
  {
    id: 'q6', pillar: 'security',
    pillarLabel: 'Security & Tenant Isolation',
    wording: {
      pre_ai: 'If you built AI for these workflows, would it need to act in external systems? How would you secure that?',
      pilot: 'Has your AI been tested against prompt injection — attempts by users to override its instructions?',
      production: 'Has your AI been tested against prompt injection — attempts by users to override its instructions?',
    },
    type: 'radio',
    options: [
      { id: 'adversarially_tested', label: "Yes — we've run adversarial testing or red-teamed it" },
      { id: 'informal_mitigations', label: "We've thought about it and have some informal mitigations" },
      { id: 'on_the_list', label: "No — it's on our list but we haven't gotten to it" },
      { id: 'no_external_inputs', label: "No — and the system accepts external inputs we don't fully control" },
      { id: 'not_applicable', label: 'Not applicable — no external users interact with the system', unsure: true },
    ],
  },
  {
    id: 'q7', pillar: 'security',
    pillarLabel: 'Security & Tenant Isolation',
    wording: {
      pre_ai: 'What types of data would the AI system access or process?',
      pilot: 'What types of data does your AI system access or process?',
      production: 'What types of data does your AI system access or process?',
    },
    type: 'checkbox',
    options: [
      { id: 'public_or_low_risk', label: 'Public or low-risk data only' },
      { id: 'internal_business', label: 'Internal business documents — contracts, policies, knowledge base' },
      { id: 'customer_data', label: 'Customer account or usage data' },
      { id: 'pii', label: 'Personal PII — names, emails, IDs, contact details' },
      { id: 'financial', label: 'Financial records — invoices, transactions, revenue data' },
      { id: 'hr', label: 'HR or employee records' },
      { id: 'regulated', label: 'Regulated data — HIPAA, SOC 2, PCI, or similar' },
      { id: 'none', label: 'None of the above — or no AI in production yet' },
    ],
  },
  {
    id: 'q8', pillar: 'tokenomics',
    pillarLabel: 'Tokenomics & Cost Scalability',
    wording: {
      pre_ai: 'How would you track what each automated task costs in tokens or compute?',
      pilot: 'Do you know what each automated task or workflow costs in tokens or compute today?',
      production: 'Do you track what each workflow costs in tokens or compute?',
    },
    type: 'radio',
    options: [
      { id: 'per_workflow_attribution', label: 'Yes — we track cost per workflow or task with clear attribution' },
      { id: 'overall_spend', label: 'We have overall AI spend but not per-task breakdowns' },
      { id: 'monthly_bill', label: "We know the monthly bill, but not what's driving it" },
      { id: 'no_tracking', label: 'No cost tracking at all yet' },
      { id: 'not_sure', label: 'Not sure', unsure: true },
    ],
  },
  {
    id: 'q9', pillar: 'tokenomics',
    pillarLabel: 'Tokenomics & Cost Scalability',
    wording: {
      pre_ai: 'If usage 10× after launch, would the AI cost structure stay within acceptable unit economics?',
      pilot: "If your usage 10×'d tomorrow, would your current AI cost structure stay within acceptable unit economics?",
      production: "If your AI usage 10×'d, would costs stay within acceptable unit economics?",
    },
    type: 'radio',
    options: [
      { id: 'modeled_holds', label: "Yes — we've modeled cost at scale and it holds" },
      { id: 'probably', label: "Probably — we've thought about it but haven't formally modeled it" },
      { id: 'uncertain', label: "Uncertain — we haven't stress-tested the economics" },
      { id: 'would_spiral', label: 'No — costs would almost certainly spiral without architectural changes' },
      { id: 'not_sure', label: 'Not sure', unsure: true },
    ],
  },
  {
    id: 'q10', pillar: 'tokenomics',
    pillarLabel: 'Tokenomics & Cost Scalability',
    wording: {
      pre_ai: 'Which cost controls would you plan to put in place?',
      pilot: 'Which cost controls do you have in place?',
      production: 'Which cost controls are active in your production system?',
    },
    type: 'checkbox',
    options: [
      { id: 'token_budgets', label: 'Token / cost budgets per workflow or user' },
      { id: 'rate_limits', label: 'Rate limits on AI calls' },
      { id: 'model_routing', label: 'Model routing — smaller models for simpler tasks' },
      { id: 'none', label: 'None in place yet' },
    ],
  },
  {
    id: 'q11', pillar: 'reliability',
    pillarLabel: 'Reliability & Production Architecture',
    wording: {
      pre_ai: 'If the AI returns a wrong or low-confidence answer, what would the handling mechanism be?',
      pilot: 'What happens when your AI system returns a wrong or low-confidence answer?',
      production: 'What happens when your AI system returns a wrong or low-confidence answer?',
    },
    type: 'radio',
    options: [
      { id: 'human_review_queue', label: 'A guardrail catches it and routes to a human review queue' },
      { id: 'log_and_handle', label: 'We log it and handle it manually after the fact' },
      { id: 'passes_through', label: 'The output goes through — we usually find out later when something breaks' },
      { id: 'no_mechanism', label: "We don't have a mechanism for this yet", nyi: true },
      { id: 'not_sure', label: 'Not sure / No AI in production yet', unsure: true },
    ],
  },
  {
    id: 'q12', pillar: 'reliability',
    pillarLabel: 'Reliability & Production Architecture',
    wording: {
      pre_ai: 'How would you monitor the AI system for degraded outputs or reliability issues?',
      pilot: 'Do you have observability in place — dashboards or alerts for when the AI is degrading or producing bad outputs?',
      production: 'Do you have active observability — dashboards or alerts that surface AI degradation before users do?',
    },
    type: 'radio',
    options: [
      { id: 'active_alerting', label: 'Yes — active alerting with defined response runbooks' },
      { id: 'logging_no_alerting', label: 'Logging in place, but no active monitoring or alerting' },
      { id: 'basic_logging', label: 'Basic infrastructure error logging only' },
      { id: 'no_observability', label: 'No observability yet', nyi: true },
      { id: 'not_sure', label: 'Not sure / No AI in production yet', unsure: true },
    ],
  },
]

// ── TYPES ─────────────────────────────────────────────────────────────────

interface IntakeData {
  name: string
  email: string
  company: string
  role: string
  primary_interest: string
  stage: Stage
}

interface RadioAnswer {
  id: string
  unsure: boolean
  nyi: boolean
}

interface CheckboxAnswer {
  selected: string[]
}

type Answer = RadioAnswer | CheckboxAnswer

interface CalculatorState {
  employees: string
  hoursPerWeek: string
  hourlyCost: string
  automationPct: number
}

type Phase = 'intake' | 'questions' | 'calculator' | 'loading' | 'results'

// ── API RESULT TYPES ──────────────────────────────────────────────────────

interface EfficiencyDividend {
  conservative?: number
  expected?: number
  optimistic?: number
  hours_per_week_recovered?: number
  caveat?: string
}

interface Finding {
  severity_label?: string
  severity_score?: number
  title?: string
  evidence?: string
  consequence?: string
  validation_step?: string
}

interface Quadrant {
  id?: string
  label?: string
  body?: string
}

interface Strength {
  label?: string
  score?: number
  description?: string
}

interface Contradiction {
  title?: string
  body?: string
}

interface CtaBlock {
  heading?: string
  body?: string
  url?: string
  button_label?: string
}

interface RoadmapPhase {
  phase?: string
  title?: string
  description?: string
  actions?: string[]
}

interface EvidenceItem {
  question_id?: string
  question_wording?: string
  answer_label?: string
  score?: number
  evidence?: string
  consequence?: string
  validation_step?: string
}

interface AwraResult {
  composite_score?: number
  composite_tier?: string
  stage?: string
  scoring_model_version?: string
  segment?: string
  construct_scores?: Record<string, number>
  construct_tiers?: Record<string, string>
  pillar_scores?: Record<string, number>
  pillar_gaps?: Record<string, number>
  efficiency_dividend?: EfficiencyDividend
  quadrant?: Quadrant
  findings?: Finding[]
  top_strength?: Strength
  contradictions?: Contradiction[]
  contradiction_count?: number
  cta?: CtaBlock
  q4_leverage_multiplier?: number
  q7_impact_multiplier?: number
  roadmap?: RoadmapPhase[]
  evidence_chain?: EvidenceItem[]
}

// ── HELPERS ───────────────────────────────────────────────────────────────

function fmtCurrency(n: number): string {
  if (n >= 1000000) return '$' + (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return '$' + Math.round(n / 1000) + 'K'
  return '$' + n
}

function severityClass(label: string): string {
  if (!label) return 'note'
  return label.toLowerCase()
}

function barColor(v: number): string {
  if (v < 40) return '#EF4444'
  if (v < 60) return '#F59E0B'
  return '#1E4E7A'
}

// ── MAIN COMPONENT ────────────────────────────────────────────────────────

export default function DiscoveryTool() {
  const [phase, setPhase] = useState<Phase>('intake')
  const [intake, setIntake] = useState<IntakeData>({
    name: '', email: '', company: '', role: '', primary_interest: '', stage: 'pilot',
  })
  const [stage, setStage] = useState<Stage>('pilot')
  const [currentQ, setCurrentQ] = useState(0)
  const [answers, setAnswers] = useState<Record<string, Answer>>({})
  const [calculator, setCalculator] = useState<CalculatorState>({
    employees: '3', hoursPerWeek: '8', hourlyCost: '75', automationPct: 70,
  })
  const [result, setResult] = useState<AwraResult | null>(null)
  const [errorMsg, setErrorMsg] = useState('')
  const [formError, setFormError] = useState('')
  const [saveState, setSaveState] = useState<'idle' | 'loading' | 'error'>('idle')

  // ── INTAKE ────────────────────────────────────────────────────────────

  const handleIntakeSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!intake.name || !intake.email || !intake.company || !intake.role || !intake.primary_interest || !intake.stage) {
      setFormError('Please fill in all required fields.')
      return
    }
    setFormError('')
    setStage(intake.stage)
    setCurrentQ(0)
    setAnswers({})
    setResult(null)
    setPhase('questions')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // ── QUESTIONS ─────────────────────────────────────────────────────────

  const getQuestionText = (q: Question) => {
    return q.wording[stage] || q.wording.pilot
  }

  const handleOptionClick = useCallback((q: Question, opt: Option) => {
    if (q.type === 'radio') {
      setAnswers(prev => ({ ...prev, [q.id]: { id: opt.id, unsure: !!opt.unsure, nyi: !!opt.nyi } }))
    } else {
      setAnswers(prev => {
        const prev_ans = prev[q.id] as CheckboxAnswer | undefined
        const selected = prev_ans?.selected || []
        const updated = selected.includes(opt.id)
          ? selected.filter(v => v !== opt.id)
          : [...selected, opt.id]
        return { ...prev, [q.id]: { selected: updated } }
      })
    }
  }, [])

  const isSelected = (q: Question, opt: Option): boolean => {
    const ans = answers[q.id]
    if (!ans) return false
    if (q.type === 'radio') return (ans as RadioAnswer).id === opt.id
    return ((ans as CheckboxAnswer).selected || []).includes(opt.id)
  }

  const [shakeQ, setShakeQ] = useState(false)

  const handleNext = () => {
    const q = QUESTIONS[currentQ]
    if (q.type === 'radio' && !answers[q.id]) {
      setShakeQ(true)
      setTimeout(() => setShakeQ(false), 300)
      return
    }
    if (currentQ < QUESTIONS.length - 1) {
      setCurrentQ(prev => prev + 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } else {
      setPhase('calculator')
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const handlePrev = () => {
    if (currentQ > 0) {
      setCurrentQ(prev => prev - 1)
    }
  }

  // ── CALCULATOR ────────────────────────────────────────────────────────

  const handleCalcSubmit = () => {
    submitToBackend()
  }

  const handleCalcBack = () => {
    setCurrentQ(QUESTIONS.length - 1)
    setPhase('questions')
  }

  // ── BACKEND ───────────────────────────────────────────────────────────

  const formatAnswersForBackend = () => {
    return QUESTIONS.map(q => {
      const a = answers[q.id]
      if (!a) return null
      const item: Record<string, unknown> = { id: q.id }
      if (q.type === 'radio') {
        const ra = a as RadioAnswer
        if (ra.unsure) item.is_not_sure = true
        else if (ra.nyi) item.is_not_yet_implemented = true
        else item.answer_id = ra.id
      } else {
        item.selected_option_ids = (a as CheckboxAnswer).selected || []
      }
      return item
    }).filter(Boolean)
  }

  const submitToBackend = async () => {
    setPhase('loading')
    setErrorMsg('')

    const payload = {
      stage,
      intake,
      answers: formatAnswersForBackend(),
      calculatorInputs: {
        people: parseFloat(calculator.employees) || 0,
        hoursPerWeek: parseFloat(calculator.hoursPerWeek) || 0,
        automationPct: calculator.automationPct,
        hourlyCost: parseFloat(calculator.hourlyCost) || 0,
      },
    }

    try {
      const r = await fetch(AWRA_API + '/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!r.ok) throw new Error('Score API returned ' + r.status)
      const data = await r.json()
      setResult(data)
      setPhase('results')
      sendToCRM(data)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (err) {
      console.error('AWRA score error:', err)
      setErrorMsg('Could not reach the scoring service. Please check your connection and try again.')
      setPhase('loading')
    }
  }

  const sendToCRM = (r: AwraResult) => {
    const cs = r.construct_scores || {}
    const ct = r.construct_tiers || {}
    const ps = r.pillar_scores || {}
    const div = r.efficiency_dividend || {}
    const top = r.findings || []
    const str = r.top_strength || {}
    const contra = r.contradictions || []
    const score = r.composite_score || 0

    const findingFields: Record<string, string> = {}
    top.forEach((f, i) => {
      findingFields[`finding_${i + 1}`] =
        `[${f.severity_label}·${f.severity_score}] ${f.title} | Evidence: ${f.evidence} | Impact: ${f.consequence} | Validate: ${f.validation_step}`
    })

    const contraFields: Record<string, string> = {}
    contra.forEach((c, i) => {
      contraFields[`contradiction_${i + 1}`] = `${c.title} — ${c.body}`
    })

    const roadmapFields: Record<string, string> = {}
    ;(r.roadmap || []).forEach((p, i) => {
      const actions = p.actions?.length ? ` | Actions: ${p.actions.join('; ')}` : ''
      roadmapFields[`roadmap_phase_${i + 1}`] = `${p.phase} — ${p.title}: ${p.description}${actions}`
    })

    const evidenceFields: Record<string, string> = {}
    ;(r.evidence_chain || []).forEach((e, i) => {
      evidenceFields[`evidence_${e.question_id || i + 1}`] =
        `[${e.answer_label}] score: ${e.score} | ${e.evidence} | Impact: ${e.consequence} | Validate: ${e.validation_step}`
    })

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        access_key: '958ccf05-92c0-4596-bf7d-7a1be7b37533',
        subject: `AWRA: ${intake.name || 'Unknown'} · ${intake.company || 'Unknown'} — Score ${score} (${r.composite_tier || ''})`,
        from_name: intake.name || 'LotusNex AWRA',
        name: intake.name, email: intake.email, replyto: intake.email,
        company: intake.company, role: intake.role, interest: intake.primary_interest,
        completed_at: new Date().toISOString(),
        awra_stage: r.stage, composite_score: `${score}/100`, composite_tier: r.composite_tier,
        automation_leverage: cs.automation_leverage, production_risk: cs.production_risk,
        economic_confidence: cs.economic_confidence, evidence_confidence: cs.evidence_confidence,
        automation_leverage_tier: ct.automation_leverage, production_risk_tier: ct.production_risk,
        economic_confidence_tier: ct.economic_confidence, evidence_confidence_tier: ct.evidence_confidence,
        quadrant: r.quadrant?.id, quadrant_label: r.quadrant?.label, quadrant_body: r.quadrant?.body,
        segment: r.segment,
        pillar_process: ps.process, pillar_security: ps.security,
        pillar_tokenomics: ps.tokenomics, pillar_reliability: ps.reliability,
        dividend_conservative: fmtCurrency(div.conservative || 0),
        dividend_expected: fmtCurrency(div.expected || 0),
        dividend_optimistic: fmtCurrency(div.optimistic || 0),
        dividend_hrs_per_week: div.hours_per_week_recovered,
        dividend_caveat: div.caveat,
        top_strength: str.label ? `${str.label} (${str.score}) — ${str.description}` : 'None',
        ...findingFields,
        contradiction_count: r.contradiction_count,
        ...contraFields,
        ...roadmapFields,
        ...evidenceFields,
        q4_leverage_multiplier: r.q4_leverage_multiplier, q7_impact_multiplier: r.q7_impact_multiplier,
        scoring_model_version: r.scoring_model_version, botcheck: false,
      }),
    }).catch(() => {})
  }

  const handleSavePDF = async () => {
    if (!result) return
    setSaveState('loading')
    try {
      const r = await fetch(AWRA_API + '/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result),
      })
      if (!r.ok) throw new Error('Report API returned ' + r.status)
      const blob = await r.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `awra-report-${(intake.company || 'report').replace(/\s+/g, '-').toLowerCase()}.pdf`
      a.click()
      URL.revokeObjectURL(url)
      setSaveState('idle')
    } catch {
      setSaveState('error')
    }
  }

  // ── RENDER ────────────────────────────────────────────────────────────

  const q4Wf: Record<string, string> = {
    document_processing: 'document processing', data_entry_duplicate_entry: 'data entry',
    support_ticket_triage: 'support triage', report_generation: 'report generation',
    internal_knowledge_retrieval: 'knowledge retrieval', compliance_evidence: 'compliance evidence',
    sales_cs_handoffs: 'sales & CS handoffs', qa_test_generation: 'QA & test generation',
    incident_summarization: 'incident summarization', invoice_ap_ar: 'invoice / AP-AR',
    onboarding_offboarding: 'onboarding & offboarding', meeting_notes: 'meeting notes',
  }
  const q4Ans = (answers['q4'] as CheckboxAnswer | undefined)?.selected || []
  const wfList = q4Ans.filter(v => v !== 'other' && q4Wf[v]).map(v => q4Wf[v])
  const wfStr = wfList.length ? wfList.join(', ') : 'your target workflows'

  const pillarNames: Record<string, string> = {
    process: 'Process Fit', security: 'Security', tokenomics: 'Tokenomics', reliability: 'Reliability',
  }

  return (
    <>
      {/* ── INTAKE FORM ─────────────────────────────────────────────────── */}
      {phase === 'intake' && (
        <div id="wd-marketing">
          <section className="section" id="start-audit" style={{ background: 'var(--blue-soft)', borderTop: '1px solid var(--border-light)' }}>
            <div className="container">
              <div className="mid-funnel" style={{ textAlign: 'left', maxWidth: 640 }}>
                <p className="eyebrow" style={{ marginBottom: 8 }}>Workflow Discovery</p>
                <h3 style={{ marginBottom: 6, fontSize: 22 }}>Find out which workflows are worth automating — and what it takes to run them reliably.</h3>
                <p style={{ color: 'var(--text-muted)', marginBottom: 24 }}>12 questions + a brief efficiency calculator. Results immediately.</p>

                <form id="awra-form" onSubmit={handleIntakeSubmit} noValidate>
                  <div className="form-grid">
                    <div className="form-group">
                      <label className="form-label" htmlFor="awra-name">Name</label>
                      <input className="form-input" type="text" id="awra-name" name="name" placeholder="Your name" required
                        value={intake.name} onChange={e => setIntake(p => ({ ...p, name: e.target.value }))} />
                    </div>
                    <div className="form-group">
                      <label className="form-label" htmlFor="awra-email">Work Email</label>
                      <input className="form-input" type="email" id="awra-email" name="email" placeholder="you@company.com" required
                        value={intake.email} onChange={e => setIntake(p => ({ ...p, email: e.target.value }))} />
                    </div>
                  </div>
                  <div className="form-grid">
                    <div className="form-group">
                      <label className="form-label" htmlFor="awra-company">Company</label>
                      <input className="form-input" type="text" id="awra-company" name="company" placeholder="Company name" required
                        value={intake.company} onChange={e => setIntake(p => ({ ...p, company: e.target.value }))} />
                    </div>
                    <div className="form-group">
                      <label className="form-label" htmlFor="awra-role">Your Role</label>
                      <select className="form-select" id="awra-role" name="role" required
                        value={intake.role} onChange={e => setIntake(p => ({ ...p, role: e.target.value }))}>
                        <option value="" disabled>Select your role</option>
                        <option value="coo">COO</option>
                        <option value="cto">CTO</option>
                        <option value="vp-ops">VP Operations</option>
                        <option value="vp-eng">VP Engineering</option>
                        <option value="founder">Founder / CEO</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="form-label" htmlFor="awra-interest">What are you trying to solve?</label>
                    <select className="form-select" id="awra-interest" name="primary_interest" required
                      value={intake.primary_interest} onChange={e => setIntake(p => ({ ...p, primary_interest: e.target.value }))}>
                      <option value="" disabled>Select your primary challenge</option>
                      <option value="manual-workflows">My team spends too many hours on manual, repetitive work</option>
                      <option value="ai-reliability">Our AI system isn&apos;t reliable in production</option>
                      <option value="both">Both — workflow inefficiency and architecture problems</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label" htmlFor="awra-stage">Where are you today?</label>
                    <select className="form-select" id="awra-stage" name="stage"
                      value={intake.stage} onChange={e => setIntake(p => ({ ...p, stage: e.target.value as Stage }))}>
                      <option value="" disabled>Select your current stage</option>
                      <option value="pre_ai">No AI yet — evaluating which workflows to automate</option>
                      <option value="pilot">Pilot — AI built but not fully in production</option>
                      <option value="production">Production — AI running, optimizing or recovering</option>
                    </select>
                  </div>
                  <input type="checkbox" name="botcheck" style={{ display: 'none' }} tabIndex={-1} autoComplete="off" />
                  {formError && <p style={{ color: '#c0392b', fontSize: 13, marginTop: 10 }}>{formError}</p>}
                  <button type="submit" className="button primary" style={{ width: '100%', marginTop: 8 }}>Start the Diagnostic →</button>
                </form>

                <p style={{ fontSize: 13, color: 'var(--text-faint)', marginTop: 16, textAlign: 'center' }}>12 questions + a brief workflow calculator. Takes about 5 minutes.</p>
                <p style={{ fontSize: 13, color: 'var(--text-faint)', marginTop: 6, textAlign: 'center' }}>We don&apos;t share your information. Results remain confidential.</p>
                <p style={{ fontSize: 13, color: 'var(--text-faint)', marginTop: 6, textAlign: 'center' }}>Already know what you need? <a href="/contact" style={{ color: 'var(--navy-700)' }}>Request a Review →</a></p>
              </div>
            </div>
          </section>
        </div>
      )}

      {/* ── DIAGNOSTIC APP ───────────────────────────────────────────────── */}
      {phase !== 'intake' && (
        <div id="wd-app">
          <div className="container">
            <div className="wd-card">

              {/* Meta row */}
              <div className="wd-meta-row">
                <span className="wd-step-label">
                  {phase === 'questions' ? pillarNames[QUESTIONS[currentQ].pillar] :
                   phase === 'calculator' ? 'Efficiency Calculator' :
                   phase === 'loading' ? 'Analyzing' : 'Your Results'}
                </span>
                <span className="wd-counter">
                  {phase === 'questions' ? `Question ${currentQ + 1} of ${QUESTIONS.length}` :
                   phase === 'calculator' ? 'Almost done' :
                   phase === 'loading' ? 'Scoring your responses…' : 'Workflow Readiness Score'}
                </span>
              </div>

              {/* Progress bar */}
              <div className="wd-progress-wrap">
                <div className="wd-progress-bar" style={{
                  width: phase === 'questions' ? `${(currentQ / QUESTIONS.length) * 100}%` :
                         phase === 'calculator' ? '92%' :
                         phase === 'loading' ? '98%' : '100%'
                }} />
              </div>

              {/* Questions panel */}
              {phase === 'questions' && (
                <div id="wd-questions">
                  {(() => {
                    const q = QUESTIONS[currentQ]
                    return (
                      <>
                        <p className="wd-pillar-badge">{q.pillarLabel}</p>
                        <p className="wd-question-text">{getQuestionText(q)}</p>
                        {q.type === 'checkbox' && <p className="wd-multiselect-note">Select all that apply.</p>}
                        <div
                          className="wd-options"
                          style={{ transform: shakeQ ? 'translateX(0)' : undefined,
                            animation: shakeQ ? 'none' : undefined }}
                        >
                          {q.options.map(opt => (
                            <div
                              key={opt.id}
                              className={`wd-option${isSelected(q, opt) ? ' selected' : ''}`}
                              onClick={() => handleOptionClick(q, opt)}
                            >
                              <input
                                type={q.type}
                                name={q.id}
                                value={opt.id}
                                checked={isSelected(q, opt)}
                                onChange={() => {}}
                              />
                              <span className="wd-option-label">{opt.label}</span>
                            </div>
                          ))}
                        </div>
                        <div className="wd-nav">
                          {currentQ > 0 ? (
                            <button className="button" onClick={handlePrev}>← Previous</button>
                          ) : <span />}
                          <button className="button primary" onClick={handleNext}>
                            {currentQ === QUESTIONS.length - 1 ? 'Continue →' : 'Next →'}
                          </button>
                        </div>
                      </>
                    )
                  })()}
                </div>
              )}

              {/* Calculator panel */}
              {phase === 'calculator' && (
                <div id="wd-calculator">
                  <div className="wd-calc-wrap">
                    <p className="eyebrow" style={{ marginBottom: 8 }}>Efficiency Calculator</p>
                    <h3 style={{ marginBottom: 6 }}>Quantify the recoverable cost.</h3>
                    <p style={{ color: 'var(--text-muted)', marginBottom: 24, fontSize: 14 }}>
                      We&apos;ll use this to calculate the Efficiency Dividend for {wfStr}. Takes 30 seconds.
                    </p>
                    <div className="form-group">
                      <label className="form-label" htmlFor="calc-employees">How many people do this manual work regularly?</label>
                      <input className="form-input" type="number" id="calc-employees" min={1} max={9999}
                        value={calculator.employees}
                        onChange={e => setCalculator(p => ({ ...p, employees: e.target.value }))}
                        placeholder="e.g. 3" />
                    </div>
                    <div className="form-group">
                      <label className="form-label" htmlFor="calc-hours">Roughly how many hours per person per week does this work take?</label>
                      <input className="form-input" type="number" id="calc-hours" min={0.5} max={80} step={0.5}
                        value={calculator.hoursPerWeek}
                        onChange={e => setCalculator(p => ({ ...p, hoursPerWeek: e.target.value }))}
                        placeholder="e.g. 8" />
                    </div>
                    <div className="form-group">
                      <label className="form-label" htmlFor="calc-cost">Approximate fully-loaded hourly cost per person ($)?</label>
                      <input className="form-input" type="number" id="calc-cost" min={10} max={500}
                        value={calculator.hourlyCost}
                        onChange={e => setCalculator(p => ({ ...p, hourlyCost: e.target.value }))}
                        placeholder="e.g. 75" />
                      <p style={{ fontSize: 12, color: 'var(--text-faint)', marginTop: 4 }}>Typical range: $40–$100/hr ops staff, $80–$160/hr engineers. A rough estimate is fine.</p>
                    </div>
                    <div className="form-group">
                      <label className="form-label">
                        What % of this work could realistically be automated? &nbsp;
                        <span style={{ color: 'var(--navy-700)', fontWeight: 600 }}>{calculator.automationPct}%</span>
                      </label>
                      <div className="wd-range-wrap">
                        <span className="wd-range-end">0%</span>
                        <input type="range" id="calc-pct" min={0} max={100} step={5}
                          value={calculator.automationPct}
                          onChange={e => setCalculator(p => ({ ...p, automationPct: parseInt(e.target.value) }))} />
                        <span className="wd-range-end">100%</span>
                      </div>
                      <p style={{ fontSize: 12, color: 'var(--text-faint)', marginTop: 6 }}>We apply a 70% realisation factor — practical automation rarely captures 100% of theoretical potential.</p>
                    </div>
                    <div className="wd-nav" style={{ marginTop: 24 }}>
                      <button className="button" onClick={handleCalcBack}>← Back</button>
                      <button className="button primary" onClick={handleCalcSubmit}>Calculate My Score →</button>
                    </div>
                  </div>
                </div>
              )}

              {/* Loading panel */}
              {phase === 'loading' && (
                <div id="wd-results">
                  {errorMsg ? (
                    <div style={{ textAlign: 'center', padding: '40px 20px' }}>
                      <p style={{ color: '#c62828', marginBottom: 12 }}>{errorMsg}</p>
                      <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Please check your connection and try again, or <a href="/contact">contact us directly</a>.</p>
                      <button className="button" style={{ marginTop: 20 }} onClick={() => window.location.reload()}>Try Again</button>
                    </div>
                  ) : (
                    <div className="wd-loading" style={{ textAlign: 'center', padding: '60px 0' }}>
                      <div className="wd-spinner" />
                      <p style={{ color: 'var(--text-muted)', marginTop: 16 }}>Calculating your Workflow Readiness Score…</p>
                    </div>
                  )}
                </div>
              )}

              {/* Results panel */}
              {phase === 'results' && result && <ResultsPanel result={result} intake={intake} onSavePDF={handleSavePDF} saveState={saveState} />}

            </div>
          </div>
        </div>
      )}
    </>
  )
}

// ── RESULTS PANEL ──────────────────────────────────────────────────────────

function ResultsPanel({
  result, intake, onSavePDF, saveState,
}: {
  result: AwraResult
  intake: IntakeData
  onSavePDF: () => void
  saveState: 'idle' | 'loading' | 'error'
}) {
  const cs = result.construct_scores || {}
  const ct = result.construct_tiers || {}
  const ps = result.pillar_scores || {}
  const gaps = result.pillar_gaps || {}
  const div = result.efficiency_dividend || {}
  const q = result.quadrant || {}
  const top = result.findings || []
  const str = result.top_strength || {}
  const contra = result.contradictions || []
  const cta = result.cta || {}
  const score = result.composite_score || 0
  const tier = result.composite_tier || ''

  const constructNames: Record<string, string> = {
    automation_leverage: 'Automation Leverage',
    production_risk: 'Production Risk',
    economic_confidence: 'Economic Confidence',
    evidence_confidence: 'Evidence Confidence',
  }

  const pillarLabels: Record<string, string> = {
    process: 'Process Fit & Automation Leverage',
    security: 'Security & Tenant Isolation',
    tokenomics: 'Tokenomics & Cost Scalability',
    reliability: 'Reliability & Architecture',
  }

  return (
    <div id="wd-results">
      {/* Score hero */}
      <div className="wd-score-hero">
        <div className="wd-score-number">{score}</div>
        <div className="wd-score-label">Workflow Readiness Score</div>
        <div className={`wd-tier-badge wd-tier-${tier.toLowerCase().replace(/[^a-z]/g, '-')}`}>{tier}</div>
        <p style={{ fontSize: 13, color: 'var(--text-faint)', marginTop: 8 }}>
          Stage: {(result.stage || '').replace('_', ' ')} · Model {result.scoring_model_version}
        </p>
      </div>

      {/* Four constructs */}
      <h4 style={{ margin: '24px 0 12px' }}>Four Decision Constructs</h4>
      <div className="wd-construct-grid">
        {Object.keys(constructNames).map(k => (
          <div key={k} className="wd-construct-card">
            <div className="wd-construct-label">{constructNames[k]}</div>
            <div className="wd-construct-score">{cs[k] || 0}</div>
            <div className="wd-construct-tier">{ct[k] || ''}</div>
          </div>
        ))}
      </div>

      {/* Quadrant */}
      <h4 style={{ margin: '24px 0 10px' }}>Quadrant Assessment</h4>
      <div className="wd-quadrant-card">
        <div className="wd-quadrant-label">{q.label || ''}</div>
        <p className="wd-quadrant-body">{q.body || ''}</p>
      </div>

      {/* Dividend */}
      <h4 style={{ margin: '24px 0 12px' }}>Efficiency Dividend</h4>
      <div className="wd-dividend-range">
        <div className="wd-dividend-col">
          <div className="wd-d-label">Conservative</div>
          <div className="wd-d-value">{fmtCurrency(div.conservative || 0)}/yr</div>
        </div>
        <div className="wd-dividend-col expected">
          <div className="wd-d-label">Expected</div>
          <div className="wd-d-value">{fmtCurrency(div.expected || 0)}/yr</div>
          <div className="wd-d-sub">{div.hours_per_week_recovered || 0} hrs/week recovered</div>
        </div>
        <div className="wd-dividend-col">
          <div className="wd-d-label">Optimistic</div>
          <div className="wd-d-value">{fmtCurrency(div.optimistic || 0)}/yr</div>
        </div>
      </div>
      <p className="wd-dividend-caveat">{div.caveat || ''}</p>

      {/* Pillar breakdown */}
      <h4 style={{ margin: '24px 0 12px' }}>Pillar Breakdown</h4>
      {Object.keys(pillarLabels).map(k => {
        const v = ps[k] || 0
        const gap = gaps[k] || 0
        return (
          <div key={k} className="wd-pillar-row">
            <div className="wd-pillar-row-top">
              <span className="wd-pillar-name">{pillarLabels[k]}</span>
              <div className="wd-pillar-track">
                <div className="wd-pillar-fill" style={{ width: `${v}%`, background: barColor(v) }} />
              </div>
              <div className="wd-pillar-score-group">
                <span className="wd-pillar-score">{v}</span>
                <span className={`wd-pillar-gap ${gap >= 0 ? 'positive' : 'negative'}`}>
                  {gap >= 0 ? '+' : ''}{gap} vs baseline
                </span>
              </div>
            </div>
          </div>
        )
      })}

      {/* Findings */}
      <h4 style={{ margin: '24px 0 12px' }}>Top Findings</h4>
      {top.length ? top.map((f, i) => (
        <div key={i} className="wd-finding-card">
          <div className="wd-finding-header">
            <span className={`wd-severity-badge ${severityClass(f.severity_label || '')}`}>
              {f.severity_label || 'Note'} · {f.severity_score}
            </span>
            <span className="wd-finding-title">{f.title}</span>
          </div>
          <p className="wd-finding-evidence">{f.evidence}</p>
          <p className="wd-finding-meta"><strong>Impact:</strong> {f.consequence}</p>
          <p className="wd-finding-meta"><strong>Validate:</strong> {f.validation_step}</p>
        </div>
      )) : <p style={{ color: 'var(--text-faint)', fontSize: 14 }}>No critical findings detected.</p>}

      {/* Strength */}
      {str.label && (
        <>
          <h4 style={{ margin: '24px 0 12px' }}>Top Strength</h4>
          <div className="wd-strength-card">
            <div className="wd-strength-label">Top Strength</div>
            <div className="wd-strength-title">{str.label} — {str.score}</div>
            <p className="wd-strength-desc">{str.description}</p>
          </div>
        </>
      )}

      {/* Reflections */}
      <h4 style={{ margin: '24px 0 12px' }}>Reflection Prompts</h4>
      {contra.length ? contra.map((c, i) => (
        <div key={i} className="wd-reflection-prompt">
          <div className="wd-reflection-title">{c.title}</div>
          <p className="wd-reflection-body">{c.body}</p>
        </div>
      )) : <p style={{ color: 'var(--text-faint)', fontSize: 14 }}>No contradictions detected — your answers are internally consistent.</p>}

      {/* CTA */}
      <div style={{ marginTop: 32, paddingTop: 24, borderTop: '1px solid var(--border-light)', textAlign: 'center' }}>
        <h3 style={{ marginBottom: 8 }}>{cta.heading || 'Get a walkthrough of your results.'}</h3>
        <p style={{ color: 'var(--text-muted)', fontSize: 14, maxWidth: '44ch', margin: '0 auto 20px' }}>{cta.body || ''}</p>
        <div className="hero-actions" style={{ justifyContent: 'center' }}>
          <a className="button primary" href={cta.url || 'https://lotusnex.com/contact'} target="_blank" rel="noopener noreferrer">
            {cta.button_label || 'Book the Review →'}
          </a>
          <button
            className="button"
            onClick={onSavePDF}
            disabled={saveState === 'loading'}
          >
            {saveState === 'loading' ? 'Generating…' : saveState === 'error' ? 'PDF unavailable' : 'Save Report (PDF)'}
          </button>
        </div>
        <p style={{ fontSize: 13, color: 'var(--text-faint)', marginTop: 16 }}>
          Results are confidential. <a href="mailto:contact@lotusnex.com" style={{ color: 'var(--navy-700)' }}>contact@lotusnex.com</a>
        </p>
      </div>
    </div>
  )
}
