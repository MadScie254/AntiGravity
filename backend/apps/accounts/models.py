"""
Models for user accounts, workspaces, and invitations.
"""
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model with email as username and additional fields.
    
    Fields:
        - id: UUID primary key
        - email: Unique email address (used for authentication)
        - name: Full name
        - timezone: IANA timezone string
        - avatar_url: URL to user avatar image
        - settings: JSON field for user preferences
        - created_at, updated_at: Timestamps
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=255, blank=True)
    timezone = models.CharField(
        _('timezone'),
        max_length=63,
        default='UTC',
        help_text='IANA timezone identifier (e.g., America/New_York)'
    )
    avatar_url = models.URLField(_('avatar URL'), blank=True, null=True)
    
    # JSON field for user settings (work hours, focus length, etc.)
    settings = models.JSONField(
        _('user settings'),
        default=dict,
        blank=True,
        help_text='User preferences: work_hours, focus_length, default_priority, etc.'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name or email if name is not set."""
        return self.name or self.email
    
    def get_short_name(self):
        """Return the short name (first name) or email."""
        if self.name:
            return self.name.split()[0]
        return self.email


class Workspace(models.Model):
    """
    Team workspace model for collaborative features.
    
    Fields:
        - id: UUID primary key
        - name: Workspace name
        - owner: User who created the workspace
        - members: Many-to-many relationship with users through WorkspaceMembership
        - created_at: Timestamp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('workspace name'), max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_workspaces',
        verbose_name=_('owner')
    )
    members = models.ManyToManyField(
        User,
        through='WorkspaceMembership',
        related_name='workspaces',
        verbose_name=_('members')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'workspaces'
        verbose_name = _('workspace')
        verbose_name_plural = _('workspaces')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class WorkspaceMembership(models.Model):
    """
    Through model for workspace membership with roles.
    
    Roles:
        - owner: Full control over workspace
        - admin: Can manage members and settings
        - member: Can access workspace resources
    """
    class Role(models.TextChoices):
        OWNER = 'owner', _('Owner')
        ADMIN = 'admin', _('Admin')
        MEMBER = 'member', _('Member')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(
        _('role'),
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'workspace_memberships'
        verbose_name = _('workspace membership')
        verbose_name_plural = _('workspace memberships')
        unique_together = [['user', 'workspace']]
        ordering = ['-joined_at']
    
    def __str__(self):
        return f'{self.user.email} - {self.workspace.name} ({self.role})'


class Invite(models.Model):
    """
    Invitation model for inviting users to workspaces.
    
    Fields:
        - id: UUID primary key
        - workspace: Workspace being invited to
        - invited_email: Email address of invitee
        - token: Unique invitation token
        - created_by: User who sent the invitation
        - expires_at: Invitation expiration datetime
        - accepted_at: When invitation was accepted (null if pending)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='invites',
        verbose_name=_('workspace')
    )
    invited_email = models.EmailField(_('invited email'))
    token = models.UUIDField(_('token'), default=uuid.uuid4, unique=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_invites',
        verbose_name=_('created by')
    )
    expires_at = models.DateTimeField(_('expires at'))
    accepted_at = models.DateTimeField(_('accepted at'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invites'
        verbose_name = _('invite')
        verbose_name_plural = _('invites')
        ordering = ['-created_at']
        unique_together = [['workspace', 'invited_email']]
    
    def __str__(self):
        return f'Invite to {self.workspace.name} for {self.invited_email}'
    
    @property
    def is_expired(self):
        """Check if invitation has expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    @property
    def is_pending(self):
        """Check if invitation is still pending."""
        return self.accepted_at is None and not self.is_expired
