"""
Focus sessions app configuration.
"""
from django.apps import AppConfig


class FocusSessionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.focus_sessions'
    verbose_name = 'Focus Sessions'
