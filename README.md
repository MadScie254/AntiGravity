# Antigravity

**Antigravity** is a productivity and wellbeing orchestration web application designed to help individuals and small teams eliminate friction from daily work through unified task management, focus sessions, habit tracking, and intelligent daily planning.

## 🚀 Tech Stack

**Frontend:**
- Next.js 14 (App Router) + TypeScript
- Tailwind CSS + shadcn/ui components
- Framer Motion for animations
- React Query for state management

**Backend:**
- Django 4.x + Django REST Framework
- SQLite (local dev) / PostgreSQL (production)
- Redis + Celery for background tasks
- JWT authentication + Google OAuth

## 📋 Features

- ✅ **Smart Task Management** - Create tasks with subtasks, tags, priorities, and time estimates
- ⏱️ **Focus Sessions** - Pomodoro-style timer with session tracking
- 📊 **Analytics Dashboard** - Visualize productivity metrics and trends
- 🎯 **Habit Tracking** - Build streaks and maintain daily routines
- 🔐 **Secure Authentication** - Email/password + Google OAuth
- 🌙 **Dark Mode** - Full theme support with system preference detection
- ♿ **Accessible** - WCAG AA compliant, keyboard navigable

## 🏃 Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Redis (for background tasks)
- Git

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/antigravity.git
cd antigravity

# Copy environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Load seed data
python manage.py seed_data

# Start development server
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 4. Start Background Workers

```bash
cd backend

# Start Celery worker (in a new terminal)
celery -A config worker -l info

# Start Celery beat scheduler (in another terminal)
celery -A config beat -l info
```

## 🐳 Docker Setup (Alternative)

```bash
# Start all services
docker-compose up

# Run migrations
docker-compose exec backend python manage.py migrate

# Load seed data
docker-compose exec backend python manage.py seed_data

# Stop services
docker-compose down
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest --cov=apps --cov-report=html
# Coverage report available at: backend/htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend
npm run test
npm run test:coverage
```

### End-to-End Tests

```bash
cd frontend
npx playwright test
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/api/schema/swagger/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`

### Example API Usage

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@antigravity.app","password":"DemoPass123!"}'
```

**Create Task:**
```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Authorization: Bearer <your-access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project proposal",
    "description": "Write and submit Q1 proposal",
    "estimated_minutes": 90,
    "priority": "high",
    "due_date": "2024-12-31T17:00:00Z"
  }'
```

## 🗄️ Database

**Local Development:**
- SQLite database file: `backend/db.sqlite3`
- Use [DB Browser for SQLite](https://sqlitebrowser.org/) to inspect data

**Production:**
- Configure PostgreSQL via `DATABASE_URL` environment variable
- Run migrations: `python manage.py migrate`

## 🔐 OAuth Setup

### Google OAuth Configuration

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/` (dev)
   - `https://yourdomain.com/accounts/google/login/callback/` (prod)
6. Copy Client ID and Secret to `.env` file

## 🚀 Deployment

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Deploy to Vercel
vercel --prod
```

**Environment Variables to Set:**
- `NEXT_PUBLIC_API_URL` - Your production backend URL

### Backend (Docker)

```bash
cd backend
docker build -t antigravity-backend .
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  antigravity-backend
```

**Recommended Platforms:**
- [Render.com](https://render.com) - Easy Docker deployment
- [Railway.app](https://railway.app) - Simple setup
- AWS ECS/Fargate - Scalable container hosting

## 📁 Project Structure

```
antigravity/
├── backend/
│   ├── apps/
│   │   ├── accounts/    # User auth & workspaces
│   │   ├── tasks/       # Task management
│   │   ├── sessions/    # Focus sessions
│   │   └── analytics/   # Habits & analytics
│   ├── config/          # Django settings
│   ├── tests/           # Backend tests
│   └── manage.py
├── frontend/
│   ├── app/             # Next.js pages (app router)
│   ├── components/      # React components
│   ├── lib/             # Utilities & API client
│   └── tests/           # Frontend tests
├── .env.example
├── docker-compose.yml
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [Django REST Framework](https://www.django-rest-framework.org/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons by [Lucide](https://lucide.dev/)

---

**Demo Credentials:**
- Email: `demo@antigravity.app`
- Password: `DemoPass123!`

For issues and feature requests, please visit our [GitHub Issues](https://github.com/yourusername/antigravity/issues).
