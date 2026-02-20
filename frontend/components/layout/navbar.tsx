import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="border-b border-slate-800 bg-slate-950/80 px-6 py-4 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <Link href="/dashboard" className="text-xl font-semibold text-indigo-300">StrikeGenius.ai</Link>
        <div className="flex gap-4 text-sm">
          <Link href="/scanner">Scanner</Link>
          <Link href="/backtest">Backtesting</Link>
          <Link href="/billing">Billing</Link>
          <Link href="/legal">Legal</Link>
        </div>
      </div>
    </nav>
  )
}
