'use client'

import { useMemo, useState } from 'react'
import RuleBuilder, { RuleNode } from '@/components/scanner/rule-builder'
import { api, authHeaders } from '@/lib/api'

export default function ScannerPage() {
  const [rule, setRule] = useState<RuleNode>({ operator: '>', left: { type: 'indicator', name: 'RSI', period: 14, source: 'close' }, right: { type: 'value', value: 60 } })
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any[]>([])
  const [error, setError] = useState('')

  const preview = useMemo(() => `${rule.left?.name || 'LHS'} ${rule.operator} ${rule.right?.value ?? 'RHS'}`, [rule])

  const runScan = async () => {
    setLoading(true); setError('')
    try {
      const { data } = await api.post('/scanner/run', {
        timeframe: '5m',
        rule_ast: rule,
        strike_filter: { moneyness: 'ATM' },
        option_type: 'both',
      }, { headers: authHeaders() })
      setResults(data.results || [])
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Unable to run scan. Check broker credentials and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Universal F&O Option Scanner</h1>
      <div className="card space-y-3">
        <RuleBuilder onChange={setRule} />
        <p className="text-sm text-slate-400">Rule preview: {preview}</p>
        <button className="btn" onClick={runScan} disabled={loading}>{loading ? 'Scanning...' : 'Run Scan'}</button>
        {error && <p className="text-sm text-rose-400">{error}</p>}
      </div>
      <div className="card overflow-auto">
        <table className="w-full text-sm">
          <thead><tr className="text-left text-slate-400"><th>Symbol</th><th>Expiry</th><th>Strike</th><th>Type</th><th>LTP</th><th>Timestamp</th></tr></thead>
          <tbody>{results.length === 0 ? <tr><td colSpan={6} className="py-8 text-center text-slate-500">No matches yet</td></tr> : results.map((r, i) => (
            <tr key={i} className="border-t border-slate-800"><td>{r.symbol}</td><td>{r.expiry}</td><td>{r.strike}</td><td>{r.option_type}</td><td>{r.ltp}</td><td>{r.timestamp}</td></tr>
          ))}</tbody>
        </table>
      </div>
    </div>
  )
}
