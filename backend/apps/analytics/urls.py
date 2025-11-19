"""
URL routing for analytics app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'habits', views.HabitViewSet, basename='habit')

urlpatterns = [
    path('summary/', views.analytics_summary, name='analytics-summary'),
    path('', include(router.urls)),
]
