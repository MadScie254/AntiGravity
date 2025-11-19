"""
Basic backend API tests.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_signup(self):
        """Test user registration."""
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'timezone': 'UTC',
        }
        response = client.post('/api/v1/auth/signup/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert User.objects.filter(email='test@example.com').exists()
    
    def test_login(self):
        """Test user login."""
        # Create user
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            name='Test User'
        )
        
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
        }
        response = client.post('/api/v1/auth/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'user' in response.data
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        client = APIClient()
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword',
        }
        response = client.post('/api/v1/auth/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTasks:
    """Test task endpoints."""
    
    def test_create_task(self):
        """Test task creation."""
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            name='Test User'
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        data = {
            'title': 'Test Task',
            'description': 'Test description',
            'priority': 'high',
            'estimated_minutes': 30,
        }
        response = client.post('/api/v1/tasks/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Task'
    
    def test_list_tasks(self):
        """Test listing user's tasks."""
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            name='Test User'
        )
        
        from apps.tasks.models import Task
        Task.objects.create(owner=user, title='Task 1', priority='medium')
        Task.objects.create(owner=user, title='Task 2', priority='high')
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get('/api/v1/tasks/')
        assert response.status_code == status.HTTP_200_OK
        # Handle both paginated and non-paginated responses
        tasks = response.data.get('results', response.data)
        assert len(tasks) == 2
    
    def test_mark_task_done(self):
        """Test marking task as done."""
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            name='Test User'
        )
        
        from apps.tasks.models import Task
        task = Task.objects.create(owner=user, title='Test Task', priority='medium')
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post(f'/api/v1/tasks/{task.id}/mark_done/')
        assert response.status_code == status.HTTP_200_OK
        
        task.refresh_from_db()
        assert task.status == Task.Status.DONE
        assert task.completed_at is not None
