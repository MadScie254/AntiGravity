import { redirect } from 'next/navigation'

export default function Home() {
    // Redirect to dashboard for now
    // In production, this could be a landing page for non-authenticated users
    redirect('/dashboard')
}
