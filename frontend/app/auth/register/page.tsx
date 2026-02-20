'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'

export default function RegisterPage() {
  const router = useRouter(); const setToken = useAuthStore((s) => s.setToken)
  const [email, setEmail] = useState(''); const [password, setPassword] = useState('')
  const submit = async () => { const { data } = await api.post('/auth/register', { email, password }); setToken(data.access_token); router.push('/dashboard') }
  return <div className="mx-auto max-w-md card space-y-3"><h1 className="text-2xl">Create account</h1><input className="input" placeholder="Email" value={email} onChange={(e)=>setEmail(e.target.value)} /><input className="input" type="password" placeholder="Password" value={password} onChange={(e)=>setPassword(e.target.value)} /><button className="btn" onClick={submit}>Register</button></div>
}
