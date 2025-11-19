"""
Views for analytics app.
"""
from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Habit, AnalyticsAggregate
from .serializers import (
    HabitSerializer,
    AnalyticsAggregateSerializer,
    AnalyticsSummarySerializer,
)


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for habit management.
    
    Provides CRUD operations and completion tracking.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return habits for current user."""
        return Habit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create habit with current user."""
        serializer.save(user=self.request.user)
    
    @extend_schema(responses={200: HabitSerializer})
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark habit as completed for today."""
        habit = self.get_object()
        habit.mark_completed()
        serializer = HabitSerializer(habit)
        return Response(serializer.data)


@extend_schema(tags=['Analytics'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_summary(request):
    """
    Get analytics summary for a date range.
    
    Query Parameters:
        - range: Predefined range (7d, 30d, 90d) or custom
        - from: Start date (ISO format, when range=custom)
        - to: End date (ISO format, when range=custom)
        - group_by: Grouping (day, week, month) - default: day
    """
    # Parse date range
    range_param = request.query_params.get('range', '7d')
    to_date = timezone.now().date()
    
    if range_param == '7d':
        from_date = to_date - timedelta(days=7)
    elif range_param == '30d':
        from_date = to_date - timedelta(days=30)
    elif range_param == '90d':
        from_date = to_date - timedelta(days=90)
    elif range_param == 'custom':
        from_str = request.query_params.get('from')
        to_str = request.query_params.get('to')
        
        if not from_str or not to_str:
            return Response({
                'error': 'For custom range, both "from" and "to" parameters are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from_date = datetime.fromisoformat(from_str).date()
            to_date = datetime.fromisoformat(to_str).date()
        except ValueError:
            return Response({
                'error': 'Invalid date format. Use ISO format (YYYY-MM-DD).'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'error': 'Invalid range parameter. Use: 7d, 30d, 90d, or custom.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get aggregates for date range
    aggregates = AnalyticsAggregate.objects.filter(
        user=request.user,
        date__gte=from_date,
        date__lte=to_date
    ).order_by('date')
    
    # Calculate summary statistics
    totals = aggregates.aggregate(
        total_focus_seconds=Sum('focus_seconds'),
        total_tasks_completed=Sum('tasks_completed'),
        total_habits_completed=Sum('habits_completed'),
        avg_focus_seconds=Avg('focus_seconds'),
        avg_tasks=Avg('tasks_completed'),
    )
    
    # Calculate number of days
    num_days = (to_date - from_date).days + 1
    
    summary_data = {
        'total_focus_seconds': totals['total_focus_seconds'] or 0,
        'total_focus_minutes': round((totals['total_focus_seconds'] or 0) / 60, 1),
        'total_tasks_completed': totals['total_tasks_completed'] or 0,
        'total_habits_completed': totals['total_habits_completed'] or 0,
        'avg_focus_minutes_per_day': round((totals['avg_focus_seconds'] or 0) / 60, 1),
        'avg_tasks_per_day': round(totals['avg_tasks'] or 0, 1),
        'daily_data': AnalyticsAggregateSerializer(aggregates, many=True).data,
    }
    
    serializer = AnalyticsSummarySerializer(summary_data)
    return Response(serializer.data)
