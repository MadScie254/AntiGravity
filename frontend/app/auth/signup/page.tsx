/**
 * Signup page with email/password registration.
 */

'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { authApi, setTokens } from '@/lib/api-client'
import { toast } from 'sonner'

export default function SignupPage() {
    const router = useRouter()
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        password_confirm: '',
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    })
    const [loading, setLoading] = useState(false)
    const [errors, setErrors] = useState<Record<string, string[]>>({})

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setErrors({})

        try {
            const { data } = await authApi.signup(formData)
            setTokens(data.access, data.refresh)
            toast.success('Account created successfully!')
            router.push('/dashboard')
        } catch (error: any) {
            if (error.response?.data) {
                const err = error.response.data
                if (typeof err === 'object') {
                    setErrors(err)
                } else {
                    toast.error('Failed to create account. Please try again.')
                }
            } else {
                toast.error('Failed to create account. Please try again.')
            }
        } finally {
            setLoading(false)
        }
    }

    const getPasswordStrength = (password: string): { strength: number; label: string; color: string } => {
        let strength = 0
        if (password.length >= 8) strength++
        if (password.length >= 12) strength++
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
        if (/\d/.test(password)) strength++
        if (/[^a-zA-Z0-9]/.test(password)) strength++

        if (strength <= 2) return { strength, label: 'Weak', color: 'bg-red-500' }
        if (strength <= 3) return { strength, label: 'Fair', color: 'bg-yellow-500' }
        if (strength <= 4) return { strength, label: 'Good', color: 'bg-blue-500' }
        return { strength, label: 'Strong', color: 'bg-green-500' }
    }

    const passwordStrength = formData.password ? getPasswordStrength(formData.password) : null

    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-primary-50 to-accent-50 dark:from-muted-950 dark:to-muted-900">
            <Card className="w-full max-w-md">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-3xl font-bold text-center">
                        Create an Account
                    </CardTitle>
                    <CardDescription className="text-center">
                        Start your productivity journey with Antigravity
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="name">Full Name</Label>
                            <Input
                                id="name"
                                name="name"
                                placeholder="John Doe"
                                value={formData.name}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                            {errors.name && (
                                <p className="text-sm text-red-500">{errors.name[0]}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                name="email"
                                type="email"
                                placeholder="you@example.com"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                            {errors.email && (
                                <p className="text-sm text-red-500">{errors.email[0]}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                name="password"
                                type="password"
                                placeholder="••••••••"
                                value={formData.password}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                            {passwordStrength && (
                                <div className="space-y-1">
                                    <div className="flex gap-1">
                                        {[...Array(5)].map((_, i) => (
                                            <div
                                                key={i}
                                                className={`h-1 flex-1 rounded ${i < passwordStrength.strength
                                                        ? passwordStrength.color
                                                        : 'bg-muted-200 dark:bg-muted-700'
                                                    }`}
                                            />
                                        ))}
                                    </div>
                                    <p className="text-xs text-muted-500">
                                        Password strength: {passwordStrength.label}
                                    </p>
                                </div>
                            )}
                            {errors.password && (
                                <p className="text-sm text-red-500">{errors.password[0]}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="password_confirm">Confirm Password</Label>
                            <Input
                                id="password_confirm"
                                name="password_confirm"
                                type="password"
                                placeholder="••••••••"
                                value={formData.password_confirm}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                            {errors.password_confirm && (
                                <p className="text-sm text-red-500">{errors.password_confirm[0]}</p>
                            )}
                        </div>

                        <Button type="submit" className="w-full" disabled={loading}>
                            {loading ? 'Creating account...' : 'Create Account'}
                        </Button>
                    </CardContent>
                </form>
                <CardFooter>
                    <div className="text-sm text-center text-muted-500 w-full">
                        Already have an account?{' '}
                        <Link href="/auth/login" className="text-primary hover:underline">
                            Sign in
                        </Link>
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}
