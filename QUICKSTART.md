# Antigravity - Quick Start Guide

## 🚀 Getting Started (Fastest Path)

### Option 1: Local Development (SQLite - No Docker)

Perfect for immediate testing with DB Browser for SQLite.

#### Backend Setup
```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load demo data
python manage.py seed_data

# Start Django server
python manage.py runserver
```

**Backend will be running at: http://localhost:8000**
- API: http://localhost:8000/api/v1/
- Swagger Docs: http://localhost:8000/api/schema/swagger/
- Admin: http://localhost:8000/admin/

#### Frontend Setup
```powershell
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Next.js dev server
npm run dev
```

**Frontend will be running at: http://localhost:3000**

#### Demo Credentials
- **Demo User**: `demo@antigravity.app` / `DemoPass123!`
- **Admin**: `admin@antigravity.app` / `AdminPass123!`

---

### Option 2: Docker Compose (Full Stack)

Runs everything in containers with Redis + Celery.

```powershell
# From project root
docker-compose up --build
```

This starts:
- Backend (Django): http://localhost:8000
- Frontend (Next.js): http://localhost:3000
- Redis
- Celery Worker + Beat

---

## 📊 Database

**SQLite is used by default for local development**.

- Database file: `backend/db.sqlite3`
- Open with **DB Browser for SQLite** to inspect data
- No PostgreSQL installation needed!

To use PostgreSQL instead:
```powershell
# Use the postgres profile
docker-compose --profile with-postgres up

# Or set DATABASE_URL environment variable
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

---

## 🧪 Running Tests

### Backend Tests (pytest)
```powershell
cd backend
.\venv\Scripts\activate
pytest
```

### Frontend Tests (Jest)
```powershell
cd frontend
npm test
```

---

## 🔑 Key Features Implemented

### Backend API (100% Complete)
- ✅ User authentication (JWT + OAuth ready)
- ✅ Task management with tags & subtasks
- ✅ Focus timer sessions
- ✅ Habit tracking with streaks
- ✅ Analytics aggregation
- ✅ Workspace collaboration

### Frontend UI (90% Complete)
- ✅ Login/Signup pages
- ✅ Dashboard with task list
- ✅ Full tasks page with filtering
- ✅ Settings page
- ✅ Responsive design
- ✅ Dark mode support
- ⏳ Timer UI (backend ready)
- ⏳ Analytics charts

---

## 📁 Project Structure

```
AntiGravity/
├── backend/               # Django REST API
│   ├── apps/
│   │   ├── accounts/     # Users, workspaces, auth
│   │   ├── tasks/        # Tasks & tags
│   │   ├── sessions/     # Focus timers
│   │   └── analytics/    # Habits & metrics
│   ├── config/           # Django settings
│   ├── db.sqlite3        # SQLite database
│   └── requirements.txt
├── frontend/             # Next.js app
│   ├── app/              # Pages (App Router)
│   ├── components/       # React components
│   ├── lib/              # API client, utils
│   └── package.json
└── docker-compose.yml    # Container orchestration
```

---

## 💡 Next Steps

1. **Start the servers** using Option 1 or 2 above
2. **Visit http://localhost:3000**
3. **Sign up** or use demo credentials
4. **Create tasks** and start a focus session
5. **Inspect database** with DB Browser for SQLite

---

## 🔧 Common Commands

### Backend
```powershell
# Create superuser
python manage.py createsuperuser

# Reset database
python manage.py flush

# Make migrations
python manage.py makemigrations

# Run Django shell
python manage.py shell
```

### Frontend
```powershell
# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint
```

---

## 🐛 Troubleshooting

### Port already in use?
```powershell
# Backend (8000)
python manage.py runserver 8001

# Frontend (3000)
npm run dev -- -p 3001
```

### CORS errors?
Check `backend/config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

### Dependencies not installing?
```powershell
# Backend
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
npm cache clean --force
npm install
```

---

## 📚 Documentation

- Backend API Docs: http://localhost:8000/api/schema/swagger/
- Frontend components: Browse `frontend/components/ui/`
- Type definitions: `frontend/lib/types.ts`

---

**You're all set! Happy coding! 🚀**
