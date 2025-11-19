"""
Models for focus sessions.
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class FocusSession(models.Model):
    """
    Focus session model for tracking focused work time.
    
    Fields:
        - id: UUID primary key
        - user: User who started the session
        - task: Optional related task
        - started_at: When session began
        - ended_at: When session ended (null if active)
        - duration_seconds: Calculated duration
        - interruptions: Count of interruptions
        - completed: Whether session was completed successfully
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='focus_sessions',
        verbose_name=_('user')
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        related_name='focus_sessions',
        null=True,
        blank=True,
        verbose_name=_('task')
    )
    started_at = models.DateTimeField(_('started at'), auto_now_add=True)
    ended_at = models.DateTimeField(_('ended at'), null=True, blank=True)
    duration_seconds = models.IntegerField(
        _('duration (seconds)'),
        default=0,
        help_text='Calculated duration of the session in seconds'
    )
    interruptions = models.IntegerField(_('interruptions'), default=0)
    completed = models.BooleanField(
        _('completed'),
        default=False,
        help_text='Whether the session was completed successfully'
    )
    
    class Meta:
        db_table = 'focus_sessions'
        verbose_name = _('focus session')
        verbose_name_plural = _('focus sessions')
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'started_at']),
            models.Index(fields=['-started_at']),
        ]
    
    def __str__(self):
        task_info = f' - {self.task.title}' if self.task else ''
        return f'Session by {self.user.email}{task_info} ({self.started_at.strftime("%Y-%m-%d %H:%M")})'
    
    def calculate_duration(self):
        """Calculate and update duration based on start and end times."""
        if self.started_at and self.ended_at:
            delta = self.ended_at - self.started_at
            self.duration_seconds = int(delta.total_seconds())
            return self.duration_seconds
        return 0
    
    def stop(self, interruptions=None):
        """Stop the session and calculate duration."""
        from django.utils import timezone
        if not self.ended_at:
            self.ended_at = timezone.now()
            if interruptions is not None:
                self.interruptions = interruptions
            self.duration_seconds = self.calculate_duration()
            # Consider completed if duration > 1 minute
            self.completed = self.duration_seconds > 60
            self.save()
    
    @property
    def is_active(self):
        """Check if session is currently active."""
        return self.ended_at is None
    
    @property
    def duration_minutes(self):
        """Get duration in minutes."""
        return round(self.duration_seconds / 60, 1)
