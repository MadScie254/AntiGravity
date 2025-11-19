/**
 * Settings page - user account and preferences.
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { authApi, clearTokens, getAccessToken } from '@/lib/api-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { toast } from 'sonner'
import type { User } from '@/lib/types'

export default function SettingsPage() {
    const router = useRouter()
    const [user, setUser] = useState<User | null>(null)
    const [loading, setLoading] = useState(true)
    const [updating, setUpdating] = useState(false)
    const [profileData, setProfileData] = useState({
        name: '',
        email: '',
        timezone: '',
    })
    const [passwordData, setPasswordData] = useState({
        old_password: '',
        new_password: '',
        new_password_confirm: '',
    })

    useEffect(() => {
        const token = getAccessToken()
        if (!token) {
            router.push('/auth/login')
            return
        }
        loadProfile()
    }, [])

    const loadProfile = async () => {
        try {
            const { data } = await authApi.getProfile()
            setUser(data)
            setProfileData({
                name: data.name,
                email: data.email,
                timezone: data.timezone,
            })
        } catch (error: any) {
            if (error.response?.status === 401) {
                router.push('/auth/login')
            } else {
                toast.error('Failed to load profile')
            }
        } finally {
            setLoading(false)
        }
    }

    const handleUpdateProfile = async (e: React.FormEvent) => {
        e.preventDefault()
        setUpdating(true)
        try {
            await authApi.updateProfile(profileData)
            toast.success('Profile updated successfully!')
            loadProfile()
        } catch (error) {
            toast.error('Failed to update profile')
        } finally {
            setUpdating(false)
        }
    }

    const handleChangePassword = async (e: React.FormEvent) => {
        e.preventDefault()
        if (passwordData.new_password !== passwordData.new_password_confirm) {
            toast.error('New passwords do not match')
            return
        }
        setUpdating(true)
        try {
            await authApi.changePassword(
                passwordData.old_password,
                passwordData.new_password,
                passwordData.new_password_confirm
            )
            toast.success('Password changed successfully!')
            setPasswordData({ old_password: '', new_password: '', new_password_confirm: '' })
        } catch (error: any) {
            if (error.response?.data?.old_password) {
                toast.error(error.response.data.old_password[0])
            } else {
                toast.error('Failed to change password')
            }
        } finally {
            setUpdating(false)
        }
    }

    const handleLogout = () => {
        clearTokens()
        toast.success('Logged out successfully')
        router.push('/auth/login')
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-muted-50 dark:bg-muted-950">
            {/* Header */}
            <header className="bg-white dark:bg-muted-900 border-b border-muted-200 dark:border-muted-800">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold">Settings</h1>
                            <p className="text-sm text-muted-500">Manage your account and preferences</p>
                        </div>
                        <Button variant="outline" onClick={() => router.push('/dashboard')}>
                            Back to Dashboard
                        </Button>
                    </div>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="space-y-6">
                    {/* Profile Settings */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Profile Information</CardTitle>
                            <CardDescription>
                                Update your personal details and email address
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleUpdateProfile} className="space-y-4">
                                <div>
                                    <Label htmlFor="name">Full Name</Label>
                                    <Input
                                        id="name"
                                        value={profileData.name}
                                        onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                                        disabled={updating}
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="email">Email</Label>
                                    <Input
                                        id="email"
                                        type="email"
                                        value={profileData.email}
                                        onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                                        disabled={updating}
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="timezone">Timezone</Label>
                                    <Input
                                        id="timezone"
                                        value={profileData.timezone}
                                        onChange={(e) => setProfileData({ ...profileData, timezone: e.target.value })}
                                        disabled={updating}
                                        placeholder="America/New_York"
                                    />
                                </div>
                                <Button type="submit" disabled={updating}>
                                    {updating ? 'Saving...' : 'Save Changes'}
                                </Button>
                            </form>
                        </CardContent>
                    </Card>

                    {/* Password Change */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Change Password</CardTitle>
                            <CardDescription>
                                Update your password to keep your account secure
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleChangePassword} className="space-y-4">
                                <div>
                                    <Label htmlFor="old_password">Current Password</Label>
                                    <Input
                                        id="old_password"
                                        type="password"
                                        value={passwordData.old_password}
                                        onChange={(e) => setPasswordData({ ...passwordData, old_password: e.target.value })}
                                        disabled={updating}
                                        placeholder="••••••••"
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="new_password">New Password</Label>
                                    <Input
                                        id="new_password"
                                        type="password"
                                        value={passwordData.new_password}
                                        onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                                        disabled={updating}
                                        placeholder="••••••••"
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="new_password_confirm">Confirm New Password</Label>
                                    <Input
                                        id="new_password_confirm"
                                        type="password"
                                        value={passwordData.new_password_confirm}
                                        onChange={(e) => setPasswordData({ ...passwordData, new_password_confirm: e.target.value })}
                                        disabled={updating}
                                        placeholder="••••••••"
                                    />
                                </div>
                                <Button type="submit" disabled={updating}>
                                    {updating ? 'Changing...' : 'Change Password'}
                                </Button>
                            </form>
                        </CardContent>
                    </Card>

                    {/* Account Actions */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Account Actions</CardTitle>
                            <CardDescription>
                                Manage your account and session
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                <div>
                                    <p className="text-sm text-muted-500 mb-2">
                                        Sign out of your account on this device
                                    </p>
                                    <Button variant="destructive" onClick={handleLogout}>
                                        Sign Out
                                    </Button>
                                </div>
                                <div className="pt-4 border-t border-muted-200 dark:border-muted-800">
                                    <p className="text-sm text-muted-500">
                                        Account ID: <code className="text-xs bg-muted-100 dark:bg-muted-800 px-2 py-1 rounded">{user?.id}</code>
                                    </p>
                                    <p className="text-sm text-muted-500 mt-1">
                                        Member since: {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                                    </p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </main>
        </div>
    )
}
