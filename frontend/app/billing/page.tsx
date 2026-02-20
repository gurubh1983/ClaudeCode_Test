'use client'

import { useEffect, useState } from 'react'
import { api, authHeaders } from '@/lib/api'

export default function BillingPage() {
  const [plan, setPlan] = useState<any>(null)
  useEffect(() => { api.get('/billing/plan', { headers: authHeaders() }).then((r) => setPlan(r.data)).catch(() => null) }, [])

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-semibold">Plans & Billing</h1>
      <div className="card">Current: {plan?.plan || 'Unknown'} | Daily Scan Limit: {plan?.daily_scan_limit || '-'}</div>
      <div className="grid gap-4 md:grid-cols-3">
        {['free', 'pro', 'elite'].map((p) => <div key={p} className="card"><h2 className="text-xl capitalize">{p}</h2><button className="btn mt-3">Choose {p}</button></div>)}
      </div>
    </div>
  )
}
