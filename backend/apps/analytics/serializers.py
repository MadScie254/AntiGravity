"""
Serializers for analytics app.
"""
from rest_framework import serializers
from .models import Habit, AnalyticsAggregate


class HabitSerializer(serializers.ModelSerializer):
    """Serializer for habits."""
    
    class Meta:
        model = Habit
        fields = [
            'id', 'title', 'schedule', 'streak_count',
            'last_completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'streak_count', 'last_completed_at', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create habit with current user."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AnalyticsAggregateSerializer(serializers.ModelSerializer):
    """Serializer for analytics aggregates."""
    focus_minutes = serializers.FloatField(read_only=True)
    
    class Meta:
        model = AnalyticsAggregate
        fields = [
            'id', 'date', 'focus_seconds', 'focus_minutes',
            'tasks_completed', 'habits_completed'
        ]
        read_only_fields = ['id']


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary response."""
    total_focus_seconds = serializers.IntegerField()
    total_focus_minutes = serializers.FloatField()
    total_tasks_completed = serializers.IntegerField()
    total_habits_completed = serializers.IntegerField()
    avg_focus_minutes_per_day = serializers.FloatField()
    avg_tasks_per_day = serializers.FloatField()
    daily_data = AnalyticsAggregateSerializer(many=True)
