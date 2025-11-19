"""
Management command to seed database with demo data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from apps.tasks.models import Task, Tag
from apps.sessions.models import FocusSession
from apps.analytics.models import Habit, AnalyticsAggregate

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with demo data for testing'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create demo users
        admin_user = self.create_admin_user()
        demo_user = self.create_demo_user()
        
        # Create tags for demo user
        tags = self.create_tags(demo_user)
        
        # Create tasks for demo user
        tasks = self.create_tasks(demo_user, tags)
        
        # Create habits for demo user
        habits = self.create_habits(demo_user)
        
        # Create focus sessions for demo user
        self.create_focus_sessions(demo_user, tasks)
        
        # Create analytics aggregates
        self.create_analytics(demo_user)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
        self.stdout.write(f'Admin user: admin@antigravity.app / AdminPass123!')
        self.stdout.write(f'Demo user: demo@antigravity.app / DemoPass123!')
    
    def create_admin_user(self):
        """Create admin user."""
        user, created = User.objects.get_or_create(
            email='admin@antigravity.app',
            defaults={
                'name': 'Admin User',
                'timezone': 'UTC',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password('AdminPass123!')
            user.save()
            self.stdout.write(f'Created admin user: {user.email}')
        return user
    
    def create_demo_user(self):
        """Create demo user."""
        user, created = User.objects.get_or_create(
            email='demo@antigravity.app',
            defaults={
                'name': 'Demo User',
                'timezone': 'America/New_York',
                'settings': {
                    'work_hours': {'start': '09:00', 'end': '17:00'},
                    'focus_length': 25,
                    'default_priority': 'medium',
                }
            }
        )
        if created:
            user.set_password('DemoPass123!')
            user.save()
            self.stdout.write(f'Created demo user: {user.email}')
        return user
    
    def create_tags(self, user):
        """Create sample tags."""
        tag_data = [
            {'name': 'work', 'color_hex': '#3B82F6'},
            {'name': 'personal', 'color_hex': '#10B981'},
            {'name': 'urgent', 'color_hex': '#EF4444'},
            {'name': 'learning', 'color_hex': '#8B5CF6'},
        ]
        
        tags = []
        for data in tag_data:
            tag, created = Tag.objects.get_or_create(
                user=user,
                name=data['name'],
                defaults={'color_hex': data['color_hex']}
            )
            tags.append(tag)
        
        self.stdout.write(f'Created {len(tags)} tags')
        return tags
    
    def create_tasks(self, user, tags):
        """Create sample tasks."""
        task_data = [
            {
                'title': 'High-priority bug fix',
                'description': 'Fix the critical authentication bug reported by users',
                'estimated_minutes': 60,
                'priority': 'high',
                'status': 'in_progress',
                'tags': [tags[0], tags[2]],  # work, urgent
            },
            {
                'title': 'Deep work: write proposal',
                'description': '## Q1 Proposal\n\nWrite comprehensive proposal for Q1 initiatives',
                'estimated_minutes': 90,
                'priority': 'high',
                'status': 'todo',
                'due_date': timezone.now() + timedelta(days=3),
                'tags': [tags[0]],  # work
            },
            {
                'title': 'Learn new framework',
                'description': 'Complete tutorial on the new framework',
                'estimated_minutes': 120,
                'priority': 'medium',
                'status': 'todo',
                'tags': [tags[3]],  # learning
            },
            {
                'title': 'Plan weekend trip',
                'description': 'Research and book weekend getaway',
                'estimated_minutes': 30,
                'priority': 'low',
                'status': 'todo',
                'tags': [tags[1]],  # personal
            },
            {
                'title': 'Review team PRs',
                'description': 'Review and provide feedback on team pull requests',
                'estimated_minutes': 45,
                'priority': 'medium',
                'status': 'done',
                'completed_at': timezone.now() - timedelta(days=1),
                'tags': [tags[0]],  # work
            },
        ]
        
        tasks = []
        for data in task_data:
            tag_list = data.pop('tags', [])
            task, created = Task.objects.get_or_create(
                owner=user,
                title=data['title'],
                defaults=data
            )
            if created:
                task.tags.set(tag_list)
            tasks.append(task)
        
        # Create subtasks for first task
        if tasks:
            subtask_data = [
                {'title': 'Identify root cause', 'status': 'done'},
                {'title': 'Write fix', 'status': 'in_progress'},
                {'title': 'Write tests', 'status': 'todo'},
            ]
            for sub_data in subtask_data:
                Task.objects.get_or_create(
                    owner=user,
                    parent_task=tasks[0],
                    title=sub_data['title'],
                    defaults={
                        'priority': 'medium',
                        'status': sub_data['status'],
                    }
                )
        
        self.stdout.write(f'Created {len(tasks)} tasks')
        return tasks
    
    def create_habits(self, user):
        """Create sample habits."""
        habit_data = [
            {
                'title': 'Morning meditation',
                'schedule': {'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'], 'time': '08:00'},
                'streak_count': 5,
            },
            {
                'title': 'Daily exercise',
                'schedule': {'days': ['everyday'], 'time': '18:00'},
                'streak_count': 3,
            },
            {
                'title': 'Read for 30 minutes',
                'schedule': {'days': ['everyday'], 'time': '21:00'},
                'streak_count': 7,
            },
        ]
        
        habits = []
        for data in habit_data:
            habit, created = Habit.objects.get_or_create(
                user=user,
                title=data['title'],
                defaults={
                    'schedule': data['schedule'],
                    'streak_count': data['streak_count'],
                    'last_completed_at': timezone.now() - timedelta(hours=2),
                }
            )
            habits.append(habit)
        
        self.stdout.write(f'Created {len(habits)} habits')
        return habits
    
    def create_focus_sessions(self, user, tasks):
        """Create sample focus sessions."""
        # Create some completed sessions over the past week
        for i in range(7):
            date = timezone.now() - timedelta(days=i)
            
            # 1-3 sessions per day
            num_sessions = random.randint(1, 3)
            for _ in range(num_sessions):
                duration = random.randint(15, 60) * 60  # 15-60 minutes
                started = date.replace(hour=random.randint(9, 16), minute=0)
                
                FocusSession.objects.get_or_create(
                    user=user,
                    task=random.choice(tasks) if tasks else None,
                    started_at=started,
                    defaults={
                        'ended_at': started + timedelta(seconds=duration),
                        'duration_seconds': duration,
                        'interruptions': random.randint(0, 2),
                        'completed': True,
                    }
                )
        
        self.stdout.write('Created focus sessions for past 7 days')
    
    def create_analytics(self, user):
        """Create analytics aggregates for past week."""
        for i in range(7):
            date = (timezone.now() - timedelta(days=i)).date()
            
            AnalyticsAggregate.objects.get_or_create(
                user=user,
                date=date,
                defaults={
                    'focus_seconds': random.randint(1800, 7200),  # 30min - 2h
                    'tasks_completed': random.randint(2, 8),
                    'habits_completed': random.randint(1, 3),
                }
            )
        
        self.stdout.write('Created analytics for past 7 days')
