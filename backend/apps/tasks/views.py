"""
Views for tasks app.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Task, Tag
from .serializers import (
    TaskListSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TagSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for task management.
    
    Provides CRUD operations, searching, filtering, and custom actions.
    
    Query Parameters:
        - q: Search in title and description
        - tags: Filter by tag IDs (comma-separated)
        - status: Filter by status
        - priority: Filter by priority
        - due_before: Filter tasks due before date (ISO format)
        - due_after: Filter tasks due after date (ISO format)
        - expand: Include subtasks in response (value: 'subtasks')
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return tasks for current user.
        Apply filters from query parameters.
        """
        queryset = Task.objects.filter(owner=self.request.user)
        
        # Only show top-level tasks by default (not subtasks)
        # unless specifically requesting a task with parent
        if self.action == 'list':
            queryset = queryset.filter(parent_task__isnull=True)
        
        # Filter by tags
        tags = self.request.query_params.get('tags')
        if tags:
            tag_ids = tags.split(',')
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        
        # Filter by status
        task_status = self.request.query_params.get('status')
        if task_status:
            queryset = queryset.filter(status=task_status)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by due date range
        due_before = self.request.query_params.get('due_before')
        if due_before:
            queryset = queryset.filter(due_date__lte=due_before)
        
        due_after = self.request.query_params.get('due_after')
        if due_after:
            queryset = queryset.filter(due_date__gte=due_after)
        
        # Annotate with subtask counts
        queryset = queryset.annotate(
            subtask_count=Count('subtasks', distinct=True),
            completed_subtask_count=Count(
                'subtasks',
                filter=Q(subtasks__status=Task.Status.DONE),
                distinct=True
            )
        )
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return TaskListSerializer
        elif self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskDetailSerializer
    
    @extend_schema(responses={200: TaskDetailSerializer})
    @action(detail=True, methods=['post'])
    def mark_done(self, request, pk=None):
        """Mark task as done."""
        task = self.get_object()
        task.mark_done()
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)
    
    @extend_schema(responses={200: TaskDetailSerializer})
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive task."""
        task = self.get_object()
        task.archive()
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)
    
    @extend_schema(
        responses={200: TaskListSerializer(many=True)},
        description="Get all subtasks of this task"
    )
    @action(detail=True, methods=['get'])
    def subtasks(self, request, pk=None):
        """Get all subtasks."""
        task = self.get_object()
        subtasks = task.subtasks.all()
        serializer = TaskListSerializer(subtasks, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for tag management.
    
    Provides CRUD operations for tags.
    """
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return tags for current user."""
        return Tag.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create tag with current user."""
        serializer.save(user=self.request.user)
