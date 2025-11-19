"""
Celery tasks for analytics app.
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import AnalyticsAggregate
from apps.sessions.models import FocusSession
from apps.tasks. models import Task

User = get_user_model()


@shared_task
def aggregate_daily_analytics():
    """
    Aggregate analytics data for all users for yesterday.
    
    This task should run daily (via Celery Beat).
    """
    yesterday = (timezone.now() - timedelta(days=1)).date()
    
    users = User.objects.filter(is_active=True)
    
    for user in users:
        # Calculate focus time
        sessions = FocusSession.objects.filter(
            user=user,
            started_at__date=yesterday
        )
        focus_seconds = sum(s.duration_seconds for s in sessions)
        
        # Count completed tasks
        tasks_completed = Task.objects.filter(
            owner=user,
            status=Task.Status.DONE,
            completed_at__date=yesterday
        ).count()
        
        # Count completed habits
        from .models import Habit
        habits = Habit.objects.filter(
            user=user,
            last_completed_at__date=yesterday
        )
        habits_completed = habits.count()
        
        # Create or update aggregate
        AnalyticsAggregate.objects.update_or_create(
            user=user,
            date=yesterday,
            defaults={
                'focus_seconds': focus_seconds,
                'tasks_completed': tasks_completed,
                'habits_completed': habits_completed,
            }
        )
    
    return f'Aggregated analytics for {users.count()} users on {yesterday}'


@shared_task
def send_welcome_email(user_id):
    """
    Send welcome email to new on user.
    
    TODO: Implement actual email sending with template.
    """
    try:
        user = User.objects.get(id=user_id)
        # Placeholder for email sending
        print(f'Sending welcome email to {user.email}')
        # In production, use Django's send_mail or email service provider
        return f'Welcome email sent to {user.email}'
    except User.DoesNotExist:
        return f'User {user_id} not found'
