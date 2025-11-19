"""
Models for tasks and tags.
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    """
    Tag model for categorizing tasks.
    
    Fields:
        - id: Auto primary key
        - name: Tag name (unique)
        - color_hex: Color for UI display
        - user: Owner of the tag
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=50)
    color_hex = models.CharField(
        _('color'),
        max_length=7,
        default='#3B82F6',
        help_text='Hex color code (e.g., #3B82F6)'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name=_('user')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tags'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        unique_together = [['user', 'name']]
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Task model with support for subtasks, tags, priority, and recurrence.
    
    Fields:
        - id: UUID primary key
        - workspace: Optional workspace (null for personal tasks)
        - owner: User who created the task
        - title: Task title
        - description: Detailed description (supports markdown)
        - estimated_minutes: Time estimate in minutes
        - priority: Priority level (low, medium, high, critical)
        - status: Current status (todo, in_progress, done, archived)
        - due_date: Optional due date
        - recurrence: JSON field for recurrence rules
        - parent_task: For subtasks (null for top-level tasks)
        - tags: Many-to-many with Tag
        - completed_at: When task was completed
        - created_at, updated_at: Timestamps
    """
    
    class Priority(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')
        CRITICAL = 'critical', _('Critical')
    
    class Status(models.TextChoices):
        TODO = 'todo', _('To Do')
        IN_PROGRESS = 'in_progress', _('In Progress')
        DONE = 'done', _('Done')
        ARCHIVED = 'archived', _('Archived')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        'accounts.Workspace',
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True,
        verbose_name=_('workspace')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('owner')
    )
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    estimated_minutes = models.IntegerField(
        _('estimated minutes'),
        null=True,
        blank=True,
        help_text='Estimated time to complete in minutes'
    )
    priority = models.CharField(
        _('priority'),
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status = models.CharField(
        _('status'),
        max_length=15,
        choices=Status.choices,
        default=Status.TODO
    )
    due_date = models.DateTimeField(_('due date'), null=True, blank=True)
    
    # Recurrence stored as JSON (e.g., {"freq": "daily", "interval": 1, "until": "2024-12-31"})
    recurrence = models.JSONField(
        _('recurrence'),
        null=True,
        blank=True,
        help_text='Recurrence rule in JSON format'
    )
    
    # For subtasks
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subtasks',
        null=True,
        blank=True,
        verbose_name=_('parent task')
    )
    
    # Tags
    tags = models.ManyToManyField(
        Tag,
        related_name='tasks',
        blank=True,
        verbose_name=_('tags')
    )
    
    # Timestamps
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tasks'
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['owner', 'due_date']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def mark_done(self):
        """Mark task as done and set completed_at."""
        from django.utils import timezone
        self.status = self.Status.DONE
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])
    
    def archive(self):
        """Archive the task."""
        self.status = self.Status.ARCHIVED
        self.save(update_fields=['status'])
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        from django.utils import timezone
        if self.due_date and self.status not in [self.Status.DONE, self.Status.ARCHIVED]:
            return timezone.now() > self.due_date
        return False
    
    @property
    def subtask_count(self):
        """Get count of subtasks."""
        return self.subtasks.count()
    
    @property
    def completed_subtask_count(self):
        """Get count of completed subtasks."""
        return self.subtasks.filter(status=self.Status.DONE).count()
