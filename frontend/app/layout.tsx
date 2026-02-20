import './globals.css'
import Navbar from '@/components/layout/navbar'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main className="mx-auto max-w-7xl p-6">{children}</main>
      </body>
    </html>
  )
}
