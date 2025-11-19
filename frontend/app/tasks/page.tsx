/**
 * Tasks page - comprehensive task management.
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { tasksApi, tagsApi, getAccessToken } from '@/lib/api-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'
import type { Task, Tag } from '@/lib/types'
import { CheckCircle2, Circle, Clock, Plus, Search, Filter } from 'lucide-react'

export default function TasksPage() {
    const router = useRouter()
    const [tasks, setTasks] = useState<Task[]>([])
    const [tags, setTags] = useState<Tag[]>([])
    const [loading, setLoading] = useState(true)
    const [searchQuery, setSearchQuery] = useState('')
    const [filterStatus, setFilterStatus] = useState('all')
    const [showNewTask, setShowNewTask] = useState(false)
    const [newTask, setNewTask] = useState({
        title: '',
        description: '',
        estimated_minutes: '',
        priority: 'medium' as const,
    })

    useEffect(() => {
        const token = getAccessToken()
        if (!token) {
            router.push('/auth/login')
            return
        }
        loadData()
    }, [filterStatus])

    const loadData = async () => {
        try {
            const params: any = {}
            if (filterStatus !== 'all') {
                params.status = filterStatus
            }
            if (searchQuery) {
                params.q = searchQuery
            }

            const [tasksRes, tagsRes] = await Promise.all([
                tasksApi.list(params),
                tagsApi.list(),
            ])

            setTasks(tasksRes.data.results || tasksRes.data)
            setTags(tagsRes.data.results || tagsRes.data)
        } catch (error: any) {
            if (error.response?.status === 401) {
                router.push('/auth/login')
            } else {
                toast.error('Failed to load tasks')
            }
        } finally {
            setLoading(false)
        }
    }

    const handleCreateTask = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            await tasksApi.create({
                ...newTask,
                estimated_minutes: newTask.estimated_minutes ? parseInt(newTask.estimated_minutes) : null,
            })
            toast.success('Task created!')
            setNewTask({ title: '', description: '', estimated_minutes: '', priority: 'medium' })
            setShowNewTask(false)
            loadData()
        } catch (error) {
            toast.error('Failed to create task')
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

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'critical': return 'bg-red-500'
            case 'high': return 'bg-orange-500'
            case 'medium': return 'bg-yellow-500'
            case 'low': return 'bg-green-500'
            default: return 'bg-muted-500'
        }
    }

    const getStatusBadge = (status: string) => {
        switch (status) {
            case 'todo': return <Badge variant="secondary">To Do</Badge>
            case 'in_progress': return <Badge className="bg-blue-500">In Progress</Badge>
            case 'done': return <Badge className="bg-green-500">Done</Badge>
            case 'archived': return <Badge variant="outline">Archived</Badge>
            default: return <Badge>{status}</Badge>
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
                            <h1 className="text-2xl font-bold">Tasks</h1>
                            <p className="text-sm text-muted-500">Manage your tasks and to-dos</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <Button variant="outline" onClick={() => router.push('/dashboard')}>
                                Dashboard
                            </Button>
                            <Button onClick={() => setShowNewTask(true)}>
                                <Plus className="h-4 w-4 mr-2" />
                                New Task
                            </Button>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Filters */}
                <div className="mb-6 flex flex-col sm:flex-row gap-4">
                    <div className="flex-1">
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-400" />
                            <Input
                                placeholder="Search tasks..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && loadData()}
                                className="pl-10"
                            />
                        </div>
                    </div>
                    <div className="flex gap-2">
                        {['all', 'todo', 'in_progress', 'done'].map((status) => (
                            <Button
                                key={status}
                                variant={filterStatus === status ? 'default' : 'outline'}
                                size="sm"
                                onClick={() => setFilterStatus(status)}
                            >
                                {status === 'all' ? 'All' : status.replace('_', ' ')}
                            </Button>
                        ))}
                    </div>
                </div>

                {/* New Task Form */}
                {showNewTask && (
                    <Card className="mb-6">
                        <CardHeader>
                            <CardTitle>Create New Task</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleCreateTask} className="space-y-4">
                                <div>
                                    <Label htmlFor="title">Title</Label>
                                    <Input
                                        id="title"
                                        value={newTask.title}
                                        onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                                        required
                                        placeholder="What needs to be done?"
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="description">Description</Label>
                                    <Input
                                        id="description"
                                        value={newTask.description}
                                        onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                                        placeholder="Add more details..."
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="estimated_minutes">Estimated Time (minutes)</Label>
                                        <Input
                                            id="estimated_minutes"
                                            type="number"
                                            value={newTask.estimated_minutes}
                                            onChange={(e) => setNewTask({ ...newTask, estimated_minutes: e.target.value })}
                                            placeholder="30"
                                        />
                                    </div>
                                    <div>
                                        <Label htmlFor="priority">Priority</Label>
                                        <select
                                            id="priority"
                                            value={newTask.priority}
                                            onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as any })}
                                            className="flex h-10 w-full rounded-md border border-muted-300 bg-white px-3 py-2 text-sm dark:border-muted-700 dark:bg-muted-900"
                                        >
                                            <option value="low">Low</option>
                                            <option value="medium">Medium</option>
                                            <option value="high">High</option>
                                            <option value="critical">Critical</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="flex gap-2">
                                    <Button type="submit">Create Task</Button>
                                    <Button type="button" variant="outline" onClick={() => setShowNewTask(false)}>
                                        Cancel
                                    </Button>
                                </div>
                            </form>
                        </CardContent>
                    </Card>
                )}

                {/* Tasks List */}
                <div className="space-y-3">
                    {tasks.length === 0 ? (
                        <Card>
                            <CardContent className="text-center py-12 text-muted-500">
                                <p>No tasks found. Create one to get started!</p>
                            </CardContent>
                        </Card>
                    ) : (
                        tasks.map((task) => (
                            <Card key={task.id} className="hover:shadow-md transition-shadow">
                                <CardContent className="p-4">
                                    <div className="flex items-start gap-3">
                                        <button
                                            onClick={() => handleMarkDone(task.id)}
                                            className="mt-1 text-muted-400 hover:text-primary transition-colors"
                                            disabled={task.status === 'done'}
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
                                                <h3 className={`font-medium ${task.status === 'done' ? 'line-through text-muted-500' : ''}`}>
                                                    {task.title}
                                                </h3>
                                                {getStatusBadge(task.status)}
                                            </div>
                                            {task.description && (
                                                <p className="text-sm text-muted-500 mb-2">
                                                    {task.description}
                                                </p>
                                            )}
                                            <div className="flex items-center gap-2 flex-wrap">
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
                                                {task.subtask_count > 0 && (
                                                    <Badge variant="secondary" className="text-xs">
                                                        {task.completed_subtask_count}/{task.subtask_count} subtasks
                                                    </Badge>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </div>
            </main>
        </div>
    )
}
