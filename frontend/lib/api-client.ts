/**
 * API client with Axios and JWT token management.
 */

import axios, { AxiosError, AxiosInstance } from 'axios'
import type { AuthResponse, APIError } from './types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

// Token storage keys
const ACCESS_TOKEN_KEY = 'antigravity_access_token'
const REFRESH_TOKEN_KEY = 'antigravity_refresh_token'

/**
 * Get stored access token from localStorage.
 */
export const getAccessToken = (): string | null => {
    if (typeof window === 'undefined') return null
    return localStorage.getItem(ACCESS_TOKEN_KEY)
}

/**
 * Get stored refresh token from localStorage.
 */
export const getRefreshToken = (): string | null => {
    if (typeof window === 'undefined') return null
    return localStorage.getItem(REFRESH_TOKEN_KEY)
}

/**
 * Store tokens in localStorage.
 */
export const setTokens = (access: string, refresh: string): void => {
    if (typeof window === 'undefined') return
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
}

/**
 * Clear stored tokens.
 */
export const clearTokens = (): void => {
    if (typeof window === 'undefined') return
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
}

/**
 * Create Axios instance with interceptors.
 */
const createApiClient = (): AxiosInstance => {
    const client = axios.create({
        baseURL: API_BASE_URL,
        headers: {
            'Content-Type': 'application/json',
        },
    })

    // Request interceptor - add auth token
    client.interceptors.request.use(
        (config) => {
            const token = getAccessToken()
            if (token) {
                config.headers.Authorization = `Bearer ${token}`
            }
            return config
        },
        (error) => Promise.reject(error)
    )

    // Response interceptor - handle token refresh
    client.interceptors.response.use(
        (response) => response,
        async (error: AxiosError<APIError>) => {
            const originalRequest = error.config

            // If 401 and we have a refresh token, try to refresh
            if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
                originalRequest._retry = true

                const refreshToken = getRefreshToken()
                if (refreshToken) {
                    try {
                        const { data } = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
                            refresh: refreshToken,
                        })

                        // Update tokens
                        setTokens(data.access, data.refresh || refreshToken)

                        // Retry original request
                        if (originalRequest.headers) {
                            originalRequest.headers.Authorization = `Bearer ${data.access}`
                        }
                        return client(originalRequest)
                    } catch (refreshError) {
                        // Refresh failed, clear tokens and redirect to login
                        clearTokens()
                        if (typeof window !== 'undefined') {
                            window.location.href = '/auth/login'
                        }
                        return Promise.reject(refreshError)
                    }
                } else {
                    // No refresh token, redirect to login
                    if (typeof window !== 'undefined') {
                        window.location.href = '/auth/login'
                    }
                }
            }

            return Promise.reject(error)
        }
    )

    return client
}

export const apiClient = createApiClient()

/**
 * API helper functions
 */

// Auth
export const authApi = {
    signup: (data: { email: string; name: string; password: string; password_confirm: string; timezone: string }) =>
        apiClient.post<AuthResponse>('/auth/signup/', data),

    login: (email: string, password: string) =>
        apiClient.post<AuthResponse>('/auth/login/', { email, password }),

    getProfile: () =>
        apiClient.get('/auth/me/'),

    updateProfile: (data: Partial<User>) =>
        apiClient.patch('/auth/me/', data),

    changePassword: (oldPassword: string, newPassword: string, newPasswordConfirm: string) =>
        apiClient.post('/auth/change-password/', {
            old_password: oldPassword,
            new_password: newPassword,
            new_password_confirm: newPasswordConfirm,
        }),
}

// Tasks
export const tasksApi = {
    list: (params?: Record<string, any>) =>
        apiClient.get('/tasks/', { params }),

    get: (id: string) =>
        apiClient.get(`/tasks/${id}/`),

    create: (data: any) =>
        apiClient.post('/tasks/', data),

    update: (id: string, data: any) =>
        apiClient.patch(`/tasks/${id}/`, data),

    delete: (id: string) =>
        apiClient.delete(`/tasks/${id}/`),

    markDone: (id: string) =>
        apiClient.post(`/tasks/${id}/mark_done/`),

    archive: (id: string) =>
        apiClient.post(`/tasks/${id}/archive/`),
}

// Tags
export const tagsApi = {
    list: () =>
        apiClient.get('/tasks/tags/'),

    create: (data: { name: string; color_hex: string }) =>
        apiClient.post('/tasks/tags/', data),

    update: (id: string, data: Partial<{ name: string; color_hex: string }>) =>
        apiClient.patch(`/tasks/tags/${id}/`, data),

    delete: (id: string) =>
        apiClient.delete(`/tasks/tags/${id}/`),
}

// Focus Sessions
export const sessionsApi = {
    list: (params?: Record<string, any>) =>
        apiClient.get('/sessions/', { params }),

    start: (taskId?: string) =>
        apiClient.post('/sessions/start/', taskId ? { task_id: taskId } : {}),

    stop: (id: string, interruptions?: number) =>
        apiClient.post(`/sessions/${id}/stop/`, interruptions ? { interruptions } : {}),

    getActive: () =>
        apiClient.get('/sessions/active/'),
}

// Habits
export const habitsApi = {
    list: () =>
        apiClient.get('/analytics/habits/'),

    get: (id: string) =>
        apiClient.get(`/analytics/habits/${id}/`),

    create: (data: { title: string; schedule: Record<string, any> }) =>
        apiClient.post('/analytics/habits/', data),

    update: (id: string, data: Partial<{ title: string; schedule: Record<string, any> }>) =>
        apiClient.patch(`/analytics/habits/${id}/`, data),

    delete: (id: string) =>
        apiClient.delete(`/analytics/habits/${id}/`),

    complete: (id: string) =>
        apiClient.post(`/analytics/habits/${id}/complete/`),
}

// Analytics
export const analyticsApi = {
    getSummary: (params?: { range?: string; from?: string; to?: string }) =>
        apiClient.get('/analytics/summary/', { params }),
}

export default apiClient
