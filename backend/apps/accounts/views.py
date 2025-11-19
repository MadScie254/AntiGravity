"""
Views for accounts app - authentication and workspace management.
"""
from datetime import timedelta
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Workspace, WorkspaceMembership, Invite
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
    TokenSerializer,
    ChangePasswordSerializer,
    WorkspaceSerializer,
    WorkspaceMembershipSerializer,
    InviteSerializer,
    InviteCreateSerializer,
)

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT tokens for user."""
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


@extend_schema(tags=['Authentication'])
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    User registration endpoint.
    
    Creates a new user account and returns JWT tokens.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint.
    
    Authenticates user with email and password, returns JWT tokens.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                tokens = get_tokens_for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'access': tokens['access'],
                    'refresh': tokens['refresh'],
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'User account is disabled.'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'error': 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get or update authenticated user's profile.
    
    GET: Returns current user data
    PUT/PATCH: Updates user profile
    """
    user = request.user
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UserSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password."""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'old_password': ['Incorrect password.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully.'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workspace management.
    
    Provides CRUD operations for workspaces.
    """
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return workspaces user has access to."""
        return Workspace.objects.filter(
            members=self.request.user
        ).distinct()
    
    def perform_create(self, serializer):
        """Create workspace and add creator as owner."""
        workspace = serializer.save(owner=self.request.user)
        # Add creator as owner member
        WorkspaceMembership.objects.create(
            user=self.request.user,
            workspace=workspace,
            role=WorkspaceMembership.Role.OWNER
        )
    
    @extend_schema(
        request=InviteCreateSerializer,
        responses={201: InviteSerializer}
    )
    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        """
        Invite a user to the workspace.
        
        Requires workspace admin or owner role.
        """
        workspace = self.get_object()
        
        # Check if user has permission to invite
        membership = WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=request.user,
            role__in=[WorkspaceMembership.Role.OWNER, WorkspaceMembership.Role.ADMIN]
        ).first()
        
        if not membership:
            return Response({
                'error': 'You do not have permission to invite users to this workspace.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = InviteCreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if user already invited
            existing_invite = Invite.objects.filter(
                workspace=workspace,
                invited_email=email,
                accepted_at__isnull=True
            ).first()
            
            if existing_invite:
                return Response({
                    'error': 'User already invited.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create invite
            invite = Invite.objects.create(
                workspace=workspace,
                invited_email=email,
                created_by=request.user,
                expires_at=timezone.now() + timedelta(days=7)
            )
            
            # TODO: Send email notification
            
            return Response(
                InviteSerializer(invite).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses={200: WorkspaceMembershipSerializer(many=True)})
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of the workspace."""
        workspace = self.get_object()
        memberships = WorkspaceMembership.objects.filter(workspace=workspace)
        serializer = WorkspaceMembershipSerializer(memberships, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Invites'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invite(request, token):
    """Accept a workspace invitation."""
    try:
        invite = Invite.objects.get(token=token)
    except Invite.DoesNotExist:
        return Response({
            'error': 'Invalid invitation token.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if invite.is_expired:
        return Response({
            'error': 'Invitation has expired.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if invite.accepted_at:
        return Response({
            'error': 'Invitation already accepted.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email matches
    if invite.invited_email != request.user.email:
        return Response({
            'error': 'This invitation is for a different email address.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Add user to workspace
    membership, created = WorkspaceMembership.objects.get_or_create(
        user=request.user,
        workspace=invite.workspace,
        defaults={'role': WorkspaceMembership.Role.MEMBER}
    )
    
    # Mark invite as accepted
    invite.accepted_at = timezone.now()
    invite.save()
    
    return Response({
        'message': 'Invitation accepted successfully.',
        'workspace': WorkspaceSerializer(invite.workspace).data,
    }, status=status.HTTP_200_OK)
