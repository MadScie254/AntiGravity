"""
URL routing for sessions app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.FocusSessionViewSet, basename='session')

urlpatterns = router.urls
