/**
 * TypeScript type definitions matching backend API models.
 */

export interface User {
    id: string
    email: string
    name: string
    timezone: string
    avatar_url?: string
    settings: UserSettings
    is_active: boolean
    created_at: string
    updated_at: string
}

export interface UserSettings {
    work_hours?: {
        start: string
        end: string
    }
    focus_length?: number
    default_priority?: 'low' | 'medium' | 'high' | 'critical'
}

export interface AuthResponse {
    user: User
    access: string
    refresh: string
}

export interface Task {
    id: string
    workspace?: string
    title: string
    description: string
    estimated_minutes?: number
    priority: 'low' | 'medium' | 'high' | 'critical'
    status: 'todo' | 'in_progress' | 'done' | 'archived'
    due_date?: string
    recurrence?: Record<string, any>
    parent_task?: string
    parent_task_title?: string
    tags: Tag[]
    tag_ids?: string[]
    subtasks?: Task[]
    subtask_count?: number
    completed_subtask_count?: number
    is_overdue: boolean
    created_at: string
    updated_at: string
    completed_at?: string
}

export interface Tag {
    id: string
    name: string
    color_hex: string
    created_at: string
}

export interface FocusSession {
    id: string
    user: string
    task?: string
    task_title?: string
    started_at: string
    ended_at?: string
    duration_seconds: number
    duration_minutes: number
    interruptions: number
    completed: boolean
    is_active: boolean
}

export interface Habit {
    id: string
    title: string
    schedule: Record<string, any>
    streak_count: number
    last_completed_at?: string
    created_at: string
    updated_at: string
}

export interface AnalyticsAggregate {
    id: string
    date: string
    focus_seconds: number
    focus_minutes: number
    tasks_completed: number
    habits_completed: number
}

export interface AnalyticsSummary {
    total_focus_seconds: number
    total_focus_minutes: number
    total_tasks_completed: number
    total_habits_completed: number
    avg_focus_minutes_per_day: number
    avg_tasks_per_day: number
    daily_data: AnalyticsAggregate[]
}

export interface Workspace {
    id: string
    name: string
    owner: string
    owner_email: string
    member_count: number
    created_at: string
}

export interface PaginatedResponse<T> {
    count: number
    next?: string
    previous?: string
    results: T[]
}

export interface APIError {
    error?: string
    detail?: string
    [key: string]: any
}
