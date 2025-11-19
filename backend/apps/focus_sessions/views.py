"""
Views for sessions app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from .models import FocusSession
from .serializers import (
    FocusSessionSerializer,
    FocusSessionStartSerializer,
    FocusSessionStopSerializer,
)
from apps.tasks.models import Task


class FocusSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for focus session management.
    
    Provides CRUD operations and custom actions for starting/stopping sessions.
    
    Query Parameters:
        - from: Filter sessions starting from date (ISO format)
        - to: Filter sessions ending before date (ISO format)
        - task: Filter by task ID
    """
    serializer_class = FocusSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return focus sessions for current user with optional filters."""
        queryset = FocusSession.objects.filter(user=self.request.user)
        
        # Filter by date range
        from_date = self.request.query_params.get('from')
        if from_date:
            queryset = queryset.filter(started_at__gte=from_date)
        
        to_date = self.request.query_params.get('to')
        if to_date:
            queryset = queryset.filter(started_at__lte=to_date)
        
        # Filter by task
        task_id = self.request.query_params.get('task')
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        
        return queryset.order_by('-started_at')
    
    @extend_schema(
        request=FocusSessionStartSerializer,
        responses={201: FocusSessionSerializer}
    )
    @action(detail=False, methods=['post'])
    def start(self, request):
        """
        Start a new focus session.
        
        Optionally link to a task.
        """
        serializer = FocusSessionStartSerializer(data=request.data)
        if serializer.is_valid():
            task_id = serializer.validated_data.get('task_id')
            
            # Validate task exists and belongs to user
            task = None
            if task_id:
                try:
                    task = Task.objects.get(id=task_id, owner=request.user)
                except Task.DoesNotExist:
                    return Response({
                        'task_id': ['Task not found or does not belong to you.']
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user has an active session
            active_session = FocusSession.objects.filter(
                user=request.user,
                ended_at__isnull=True
            ).first()
            
            if active_session:
                return Response({
                    'error': 'You already have an active session. Please stop it first.',
                    'active_session': FocusSessionSerializer(active_session).data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new session
            session = FocusSession.objects.create(
                user=request.user,
                task=task
            )
            
            return Response(
                FocusSessionSerializer(session).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=FocusSessionStopSerializer,
        responses={200: FocusSessionSerializer}
    )
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """
        Stop an active focus session.
        
        Calculates duration and marks as completed.
        """
        session = self.get_object()
        
        if session.ended_at:
            return Response({
                'error': 'This session has already been stopped.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FocusSessionStopSerializer(data=request.data)
        if serializer.is_valid():
            interruptions = serializer.validated_data.get('interruptions', 0)
            session.stop(interruptions=interruptions)
            
            return Response(FocusSessionSerializer(session).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses={200: FocusSessionSerializer})
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the current active session if any."""
        session = FocusSession.objects.filter(
            user=request.user,
            ended_at__isnull=True
        ).first()
        
        if session:
            return Response(FocusSessionSerializer(session).data)
        else:
            return Response({
                'message': 'No active session.'
            }, status=status.HTTP_404_NOT_FOUND)
