"""
Serializers for accounts app.
"""
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Workspace, WorkspaceMembership, Invite

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'timezone', 'avatar_url',
            'settings', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration/signup."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password_confirm', 'timezone']
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create new user."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


class TokenSerializer(serializers.Serializer):
    """Serializer for JWT tokens."""
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'New passwords do not match.'
            })
        return attrs


class WorkspaceSerializer(serializers.ModelSerializer):
    """Serializer for workspace."""
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    member_count = serializers.IntegerField(source='members.count', read_only=True)
    
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'owner', 'owner_email', 'member_count', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    """Serializer for workspace membership."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    workspace_name = serializers.CharField(source='workspace.name', read_only=True)
    
    class Meta:
        model = WorkspaceMembership
        fields = [
            'id', 'user', 'user_email', 'user_name',
            'workspace', 'workspace_name', 'role', 'joined_at'
        ]
        read_only_fields = ['id', 'joined_at']


class InviteSerializer(serializers.ModelSerializer):
    """Serializer for workspace invites."""
    workspace_name = serializers.CharField(source='workspace.name', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_pending = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Invite
        fields = [
            'id', 'workspace', 'workspace_name', 'invited_email',
            'token', 'created_by', 'created_by_email',
            'expires_at', 'accepted_at', 'is_expired', 'is_pending',
            'created_at'
        ]
        read_only_fields = ['id', 'token', 'created_by', 'created_at', 'accepted_at']


class InviteCreateSerializer(serializers.Serializer):
    """Serializer for creating invites."""
    email = serializers.EmailField(required=True)
    workspace_id = serializers.UUIDField(required=True)
