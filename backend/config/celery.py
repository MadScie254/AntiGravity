"""
Celery configuration for Antigravity project.

For more information on Celery configuration, see:
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('antigravity')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule for Periodic Tasks
app.conf.beat_schedule = {
    'aggregate-daily-analytics': {
        'task': 'apps.analytics.tasks.aggregate_daily_analytics',
        'schedule': crontab(hour=0, minute=5),  # Run at 00:05 every day
    },
    # Add more periodic tasks here as needed
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')
