"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Workspace, WorkspaceMembership, Invite


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'timezone', 'avatar_url', 'settings')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('email', 'name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    """Workspace admin."""
    list_display = ('name', 'owner', 'member_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__email')
    readonly_fields = ('created_at',)
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(WorkspaceMembership)
class WorkspaceMembershipAdmin(admin.ModelAdmin):
    """Workspace membership admin."""
    list_display = ('user', 'workspace', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__email', 'workspace__name')
    readonly_fields = ('joined_at',)


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    """Invite admin."""
    list_display = ('invited_email', 'workspace', 'created_by', 'is_pending', 'expires_at')
    list_filter = ('created_at', 'expires_at', 'accepted_at')
    search_fields = ('invited_email', 'workspace__name', 'created_by__email')
    readonly_fields = ('token', 'created_at')
