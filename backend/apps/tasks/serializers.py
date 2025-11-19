"""
Serializers for tasks app.
"""
from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color_hex', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        """Create tag with current user."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for task lists."""
    tags = TagSerializer(many=True, read_only=True)
    subtask_count = serializers.IntegerField(read_only=True)
    completed_subtask_count = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'priority', 'status', 'due_date',
            'estimated_minutes', 'tags', 'subtask_count',
            'completed_subtask_count', 'is_overdue',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single task."""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        required=False,
        source='tags'
    )
    subtasks = serializers.SerializerMethodField(read_only=True)
    parent_task_title = serializers.CharField(
        source='parent_task.title',
        read_only=True,
        allow_null=True
    )
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'workspace', 'title', 'description',
            'estimated_minutes', 'priority', 'status', 'due_date',
            'recurrence', 'parent_task', 'parent_task_title',
            'tags', 'tag_ids', 'subtasks', 'is_overdue',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    
    def get_subtasks(self, obj):
        """Get subtasks recursively."""
        subtasks = obj.subtasks.all()
        return TaskListSerializer(subtasks, many=True).data
    
    def create(self, validated_data):
        """Create task with current user as owner."""
        validated_data['owner'] = self.context['request'].user
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        if tags:
            task.tags.set(tags)
        return task
    
    def update(self, instance, validated_data):
        """Update task, handling tags separately."""
        tags = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags is not None:
            instance.tags.set(tags)
        
        return instance


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks."""
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
        source='tags'
    )
    
    class Meta:
        model = Task
        fields = [
            'workspace', 'title', 'description', 'estimated_minutes',
            'priority', 'status', 'due_date', 'recurrence',
            'parent_task', 'tag_ids'
        ]
    
    def create(self, validated_data):
        """Create task with owner."""
        validated_data['owner'] = self.context['request'].user
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        if tags:
            task.tags.set(tags)
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tasks."""
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
        source='tags'
    )
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'estimated_minutes',
            'priority', 'status', 'due_date', 'recurrence',
            'parent_task', 'tag_ids'
        ]
    
    def update(self, instance, validated_data):
        """Update task."""
        tags = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags is not None:
            instance.tags.set(tags)
        
        return instance
