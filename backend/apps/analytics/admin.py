"""
Admin configuration for analytics app.
"""
from django.contrib import admin
from .models import Habit, AnalyticsAggregate


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Habit admin."""
    list_display = ('title', 'user', 'streak_count', 'last_completed_at', 'created_at')
    list_filter = ('created_at', 'last_completed_at')
    search_fields = ('title', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AnalyticsAggregate)
class AnalyticsAggregateAdmin(admin.ModelAdmin):
    """Analytics aggregate admin."""
    list_display = ('user', 'date', 'focus_minutes', 'tasks_completed', 'habits_completed')
    list_filter = ('date',)
    search_fields = ('user__email',)
    readonly_fields = ('id',)
    
    def focus_minutes(self, obj):
        return f'{obj.focus_minutes} min'
    focus_minutes.short_description = 'Focus Time'
