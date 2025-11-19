"""
URL routing for accounts app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r'workspaces', views.WorkspaceViewSet, basename='workspace')

urlpatterns = [
    # Authentication endpoints
    path('signup/', views.signup, name='auth-signup'),
    path('login/', views.login, name='auth-login'),
    path('me/', views.user_profile, name='auth-profile'),
    path('change-password/', views.change_password, name='auth-change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Workspace invites
    path('invites/<uuid:token>/accept/', views.accept_invite, name='accept-invite'),
    
    # Router URLs (includes workspaces)
    path('', include(router.urls)),
]
