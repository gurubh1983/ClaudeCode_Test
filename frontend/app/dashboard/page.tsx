export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Trading Intelligence Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="card"><p className="text-slate-400">Active Scans</p><p className="text-2xl font-bold">0</p></div>
        <div className="card"><p className="text-slate-400">Signals Today</p><p className="text-2xl font-bold">0</p></div>
        <div className="card"><p className="text-slate-400">Current Plan</p><p className="text-2xl font-bold">Free</p></div>
      </div>
      <p className="card">Build complex nested conditions and scan all discovered F&O option strikes automatically from your broker data feed.</p>
    </div>
  )
}
