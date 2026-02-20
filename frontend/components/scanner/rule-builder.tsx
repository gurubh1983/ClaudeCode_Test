'use client'

import { useState } from 'react'

export type RuleNode = {
  operator: string
  left?: any
  right?: any
  params?: Record<string, any>
  children?: RuleNode[]
}

const indicators = ['SMA', 'EMA', 'WMA', 'RSI', 'MACD', 'VWAP', 'ADX', 'ATR', 'OBV', 'CMF', 'ROC', 'MOM']
const operators = ['>', '<', '>=', '<=', '==', '!=', 'cross_above', 'cross_below', 'between', 'rising_for_n_bars', 'falling_for_n_bars']

export default function RuleBuilder({ onChange }: { onChange: (rule: RuleNode) => void }) {
  const [leftName, setLeftName] = useState('RSI')
  const [rightValue, setRightValue] = useState('60')
  const [operator, setOperator] = useState('>')

  const emit = (nLeft = leftName, nOp = operator, nRight = rightValue) => {
    const rule: RuleNode = {
      operator: nOp,
      left: { type: 'indicator', name: nLeft, period: 14, source: 'close' },
      right: { type: 'value', value: Number(nRight) },
    }
    onChange(rule)
  }

  return (
    <div className="grid gap-3 md:grid-cols-3">
      <select className="input" value={leftName} onChange={(e) => { setLeftName(e.target.value); emit(e.target.value, operator, rightValue) }}>
        {indicators.map((i) => <option key={i}>{i}</option>)}
      </select>
      <select className="input" value={operator} onChange={(e) => { setOperator(e.target.value); emit(leftName, e.target.value, rightValue) }}>
        {operators.map((i) => <option key={i}>{i}</option>)}
      </select>
      <input className="input" value={rightValue} onChange={(e) => { setRightValue(e.target.value); emit(leftName, operator, e.target.value) }} />
    </div>
  )
}
