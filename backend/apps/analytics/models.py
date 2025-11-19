"""
Models for habits and analytics aggregates.
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Habit(models.Model):
    """
    Habit model for tracking daily routines and building streaks.
    
    Fields:
        - id: UUID primary key
        - user: User who owns the habit
        - title: Habit name/description
        - schedule: JSON field for scheduling (days of week, time)
        - streak_count: Current streak (consecutive days)
        - last_completed_at: Last completion timestamp
        - created_at: When habit was created
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name=_('user')
    )
    title = models.CharField(_('title'), max_length=255)
    
    # Schedule as JSON (e.g., {"days": ["monday", "wednesday", "friday"], "time": "09:00"})
    schedule = models.JSONField(
        _('schedule'),
        default=dict,
        blank=True,
        help_text='Schedule configuration (days, time, frequency, etc.)'
    )
    
    streak_count = models.IntegerField(_('streak count'), default=0)
    last_completed_at = models.DateTimeField(_('last completed at'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'habits'
        verbose_name = _('habit')
        verbose_name_plural = _('habits')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'last_completed_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def mark_completed(self):
        """Mark habit as completed and update streak."""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        
        # Check if already completed today
        if self.last_completed_at:
            same_day = (
                self.last_completed_at.date() == now.date()
            )
            if same_day:
                return  # Already completed today
            
            # Check if streak should continue (within 48 hours)
            time_diff = now - self.last_completed_at
            if time_diff <= timedelta(hours=48):
                self.streak_count += 1
            else:
                # Streak broken, reset to 1
                self.streak_count = 1
        else:
            # First completion
            self.streak_count = 1
        
        self.last_completed_at = now
        self.save(update_fields=['streak_count', 'last_completed_at'])


class AnalyticsAggregate(models.Model):
    """
    Precomputed analytics data for performance.
    
    Fields:
        - id: Auto primary key
        - user: User this aggregate belongs to
        - date: Date of the aggregate
        - focus_seconds: Total focus time for the day
        - tasks_completed: Number of tasks completed
        - habits_completed: Number of habits completed
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analytics_aggregates',
        verbose_name=_('user')
    )
    date = models.DateField(_('date'))
    focus_seconds = models.IntegerField(_('focus seconds'), default=0)
    tasks_completed = models.IntegerField(_('tasks completed'), default=0)
    habits_completed = models.IntegerField(_('habits completed'), default=0)
    
    class Meta:
        db_table = 'analytics_aggregates'
        verbose_name = _('analytics aggregate')
        verbose_name_plural = _('analytics aggregates')
        unique_together = [['user', 'date']]
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f'{self.user.email} - {self.date}'
    
    @property
    def focus_minutes(self):
        """Get focus time in minutes."""
        return round(self.focus_seconds / 60, 1)
