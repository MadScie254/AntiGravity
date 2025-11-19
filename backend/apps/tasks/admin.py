"""
Admin configuration for tasks app.
"""
from django.contrib import admin
from .models import Task, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Task admin."""
    list_display = ('title', 'owner', 'priority', 'status', 'due_date', 'created_at')
    list_filter = ('priority', 'status', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'owner__email')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    filter_horizontal = ('tags',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'owner', 'workspace')
        }),
        ('Details', {
            'fields': ('estimated_minutes', 'priority', 'status', 'due_date', 'recurrence')
        }),
        ('Hierarchy', {
            'fields': ('parent_task',)
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""
    list_display = ('name', 'color_hex', 'user', 'task_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__email')
    readonly_fields = ('created_at',)
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks'
