import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from '@/components/ui/toaster'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
    title: 'Antigravity - Productivity & Wellbeing',
    description: 'Lift friction from daily work with unified task management, focus sessions, and habit tracking',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en" className={inter.variable}>
            <body className="min-h-screen bg-muted-50 dark:bg-muted-950">
                {children}
                <Toaster />
            </body>
        </html>
    )
}
