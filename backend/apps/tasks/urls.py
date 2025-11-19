"""
URL routing for tasks app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.TaskViewSet, basename='task')
router.register(r'tags', views.TagViewSet, basename='tag')

urlpatterns = router.urls
