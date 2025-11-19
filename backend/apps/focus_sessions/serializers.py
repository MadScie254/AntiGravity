"""
Serializers for sessions app.
"""
from rest_framework import serializers
from .models import FocusSession


class FocusSessionSerializer(serializers.ModelSerializer):
    """Serializer for focus sessions."""
    task_title = serializers.CharField(source='task.title', read_only=True, allow_null=True)
    duration_minutes = serializers.FloatField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = FocusSession
        fields = [
            'id', 'user', 'task', 'task_title',
            'started_at', 'ended_at', 'duration_seconds',
            'duration_minutes', 'interruptions', 'completed',
            'is_active'
        ]
        read_only_fields = ['id', 'user', 'started_at', 'ended_at', 'duration_seconds']


class FocusSessionStartSerializer(serializers.Serializer):
    """Serializer for starting a focus session."""
    task_id = serializers.UUIDField(required=False, allow_null=True)


class FocusSessionStopSerializer(serializers.Serializer):
    """Serializer for stopping a focus session."""
    interruptions = serializers.IntegerField(required=False, default=0, min_value=0)
