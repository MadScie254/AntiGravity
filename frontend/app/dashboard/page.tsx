/**
 * Dashboard page - main application interface.
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { authApi, tasksApi, sessionsApi, getAccessToken } from '@/lib/api-client'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'
import type { User, Task, FocusSession } from '@/lib/types'
import { CheckCircle2, Circle, Clock, Play, TrendingUp } from 'lucide-react'

export default function DashboardPage() {
    const router = useRouter()
    const [user, setUser] = useState<User | null>(null)
    const [tasks, setTasks] = useState<Task[]>([])
    const [activeSession, setActiveSession] = useState<FocusSession | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const token = getAccessToken()
        if (!token) {
            router.push('/auth/login')
            return
        }

        loadData()
    }, [])

    const loadData = async () => {
        try {
            // Load user profile
            const userRes = await authApi.getProfile()
            setUser(userRes.data)

            // Load active tasks
            const tasksRes = await tasksApi.list({ status: 'todo,in_progress', limit: 10 })
            setTasks(tasksRes.data.results || tasksRes.data)

            // Check for active session
            try {
                const sessionRes = await sessionsApi.getActive()
                setActiveSession(sessionRes.data)
            } catch (err) {
                // No active session
                setActiveSession(null)
            }
        } catch (error: any) {
            if (error.response?.status === 401) {
                router.push('/auth/login')
            } else {
                toast.error('Failed to load data')
            }
        } finally {
            setLoading(false)
        }
    }

    const handleMarkDone = async (taskId: string) => {
        try {
            await tasksApi.markDone(taskId)
            toast.success('Task completed!')
            loadData()
        } catch (error) {
            toast.error('Failed to mark task as done')
        }
    }

    const handleStartSession = async (taskId?: string) => {
        try {
            const { data } = await sessionsApi.start(taskId)
            setActiveSession(data)
            toast.success('Focus session started!')
        } catch (error: any) {
            if (error.response?.data?.error) {
                toast.error(error.response.data.error)
            } else {
                toast.error('Failed to start session')
            }
        }
    }

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'critical': return 'bg-red-500'
            case 'high': return 'bg-orange-500'
            case 'medium': return 'bg-yellow-500'
            case 'low': return 'bg-green-500'
            default: return 'bg-muted-500'
        }
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
                            <h1 className="text-2xl font-bold">Antigravity</h1>
                            <p className="text-sm text-muted-500">Welcome back, {user?.name || 'User'}!</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <Button variant="outline" onClick={() => router.push('/settings')}>
                                Settings
                            </Button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Active Session Banner */}
                {activeSession && (
                    <Card className="mb-6 bg-primary text-white border-primary">
                        <CardContent className="py-4">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <Play className="h-5 w-5" />
                                    <div>
                                        <p className="font-semibold">Focus session in progress</p>
                                        <p className="text-sm opacity-90">
                                            {activeSession.task_title || 'General focus'}
                                        </p>
                                    </div>
                                </div>
                                <Button variant="outline" size="sm" className="text-primary bg-white hover:bg-muted-100">
                                    Stop Session
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Tasks Column */}
                    <div className="lg:col-span-2">
                        <Card>
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <CardTitle>Today&apos;s Tasks</CardTitle>
                                    <Button size="sm" onClick={() => router.push('/tasks')}>
                                        View All
                                    </Button>
                                </div>
                            </CardHeader>
                            <CardContent>
                                {tasks.length === 0 ? (
                                    <div className="text-center py-12 text-muted-500">
                                        <CheckCircle2 className="h-12 w-12 mx-auto mb-2 opacity-50" />
                                        <p>No active tasks. Great job!</p>
                                    </div>
                                ) : (
                                    <div className="space-y-3">
                                        {tasks.map((task) => (
                                            <div
                                                key={task.id}
                                                className="flex items-start gap-3 p-3 rounded-lg border border-muted-200 dark:border-muted-800 hover:bg-muted-50 dark:hover:bg-muted-800/50 transition-colors"
                                            >
                                                <button
                                                    onClick={() => handleMarkDone(task.id)}
                                                    className="mt-0.5 text-muted-400 hover:text-primary transition-colors"
                                                >
                                                    {task.status === 'done' ? (
                                                        <CheckCircle2 className="h-5 w-5 text-green-500" />
                                                    ) : (
                                                        <Circle className="h-5 w-5" />
                                                    )}
                                                </button>
                                                <div className="flex-1 min-w-0">
                                                    <div className="flex items-center gap-2 mb-1">
                                                        <div className={`w-2 h-2 rounded-full ${getPriorityColor(task.priority)}`} />
                                                        <h3 className="font-medium truncate">{task.title}</h3>
                                                    </div>
                                                    {task.description && (
                                                        <p className="text-sm text-muted-500 line-clamp-2">
                                                            {task.description}
                                                        </p>
                                                    )}
                                                    <div className="flex items-center gap-2 mt-2">
                                                        {task.estimated_minutes && (
                                                            <Badge variant="secondary" className="text-xs">
                                                                <Clock className="h-3 w-3 mr-1" />
                                                                {task.estimated_minutes}m
                                                            </Badge>
                                                        )}
                                                        {task.tags.map((tag) => (
                                                            <Badge key={tag.id} variant="outline" className="text-xs">
                                                                {tag.name}
                                                            </Badge>
                                                        ))}
                                                    </div>
                                                </div>
                                                {!activeSession && task.status !== 'done' && (
                                                    <Button
                                                        size="sm"
                                                        variant="ghost"
                                                        onClick={() => handleStartSession(task.id)}
                                                    >
                                                        <Play className="h-4 w-4" />
                                                    </Button>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>

                    {/* Stats Column */}
                    <div className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <TrendingUp className="h-5 w-5" />
                                    Quick Stats
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <p className="text-sm text-muted-500">Active Tasks</p>
                                    <p className="text-2xl font-bold">{tasks.length}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-muted-500">Focus Sessions Today</p>
                                    <p className="text-2xl font-bold">0</p>
                                </div>
                                <div>
                                    <p className="text-sm text-muted-500">Current Streak</p>
                                    <p className="text-2xl font-bold">5 days 🔥</p>
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Quick Actions</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-2">
                                <Button className="w-full" onClick={() => router.push('/tasks')}>
                                    View All Tasks
                                </Button>
                                <Button variant="outline" className="w-full" onClick={() => router.push('/analytics')}>
                                    View Analytics
                                </Button>
                                {!activeSession && (
                                    <Button variant="secondary" className="w-full" onClick={() => handleStartSession()}>
                                        <Play className="h-4 w-4 mr-2" />
                                        Start Focus Session
                                    </Button>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </main>
        </div>
    )
}
