'use client'

import { useState } from 'react'
import { api, authHeaders } from '@/lib/api'

export default function BacktestPage() {
  const [response, setResponse] = useState<any>(null)

  const run = async () => {
    const { data } = await api.post('/scanner/backtest', {
      timeframe: '15m',
      from_ts: '2024-01-01',
      to_ts: '2024-12-31',
      rule_ast: { operator: '>', left: { type: 'indicator', name: 'RSI', period: 14, source: 'close' }, right: { type: 'value', value: 60 } },
    }, { headers: authHeaders() })
    setResponse(data)
  }

  return <div className="space-y-4"><h1 className="text-3xl font-semibold">Backtesting</h1><button className="btn" onClick={run}>Run Backtest</button>{response && <pre className="card">{JSON.stringify(response, null, 2)}</pre>}</div>
}
