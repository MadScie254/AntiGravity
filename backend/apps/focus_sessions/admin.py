"""
Admin configuration for sessions app.
"""
from django.contrib import admin
from .models import FocusSession


@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    """Focus session admin."""
    list_display = ('user', 'task', 'started_at', 'duration_minutes', 'interruptions', 'completed')
    list_filter = ('completed', 'started_at')
    search_fields = ('user__email', 'task__title')
    readonly_fields = ('started_at', 'ended_at', 'duration_seconds')
    
    def duration_minutes(self, obj):
        return f'{obj.duration_minutes} min'
    duration_minutes.short_description = 'Duration'
