# Unsloth Optimiser

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=white)](https://reactjs.org/)
[![Celery](https://img.shields.io/badge/Celery-37814A.svg?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Web-based interface for configuring and monitoring model training optimization tasks using the Unsloth library.

## ✨ Features

### Modern UI
- 🎨 **Dark theme** with gradient accents
- 📊 **Dashboard** with real-time statistics
- 🔔 **Toast notifications** for user feedback
- 📱 **Responsive design** - works on mobile and desktop
- 🖼️ **Card-based layout** with hover effects
- ⚡ **Live updates** via WebSocket

### Optimization Methods
- **Quantization** (4-bit/8-bit) - Reduce model size with minimal quality loss
- **LoRA Fine-tuning** - Parameter-efficient model adaptation
- **AWQ** (Activation-aware Weight Quantization) - Memory-efficient quantization
- **GPTQ** - Post-training quantization for inference speedup

### Key Capabilities
- ✅ JWT-based authentication with password hashing
- ✅ Real-time task monitoring via WebSockets
- ✅ RESTful API with comprehensive endpoints
- ✅ Distributed task processing with Celery
- ✅ Prometheus metrics and health monitoring
- ✅ Docker & Kubernetes deployment configs
- ✅ CORS and security headers

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

One command to start everything:

```bash
# Clone the repository
git clone https://github.com/taxicabno1729/unsloth-optimiser.git
cd unsloth-optimiser

# Start all services (frontend + backend + database + worker)
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Access points:**
- 🌐 **Frontend**: http://localhost:3000
- 🔌 **API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

### Option 2: Local Development

```bash
# Install Python dependencies
pip install -e ".[dev]"

# Install frontend dependencies
cd frontend && npm install && cd ..

# Start Redis (required for Celery)
redis-server

# Terminal 1: Start backend API
uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Start Celery worker
celery -A src.api.tasks.celery worker --loglevel=info

# Terminal 3: Start frontend
cd frontend && npm start
```

## 📸 Screenshots

**Dashboard**
- Modern dark theme with gradient stat cards
- Real-time task statistics
- Quick action buttons

**Task Creation**
- Visual method selection cards
- Advanced parameters (bits, batch size, memory)
- Toast notifications on success/error

**Task Details**
- Live WebSocket updates panel
- Status badges with animations
- Copy task ID functionality

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   React SPA     │──────▶   FastAPI        │──────▶   PostgreSQL    │
│   Port 3000     │      │   Port 8000      │      │   Port 5432     │
│   (Frontend)    │      │   (Backend API)    │      │   (Database)    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                │
                                │ WebSocket
                                ▼
                       ┌──────────────────┐
                       │   Celery Workers │
                       │   Redis Queue    │
                       │   (Task Queue)   │
                       └──────────────────┘
```

### Backend Structure

```
src/api/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── database.py          # SQLAlchemy setup
├── models/              # Database models
│   ├── base.py
│   ├── user.py
│   └── task.py
├── schemas/             # Pydantic schemas
│   ├── auth.py
│   └── task.py
├── routers/             # API endpoints
│   ├── auth.py
│   └── tasks.py
├── tasks/               # Task orchestration
│   ├── celery.py
│   ├── orchestrator.py
│   └── manager.py
├── workers/             # Optimization workers
│   ├── base_worker.py
│   ├── quantization_worker.py
│   ├── lora_worker.py
│   ├── awq_worker.py
│   └── gptq_worker.py
├── monitoring/          # Metrics & health
│   ├── metrics.py
│   └── health.py
├── security/            # Security middleware
│   ├── cors.py
│   └── csrf.py
└── monitoring/          # Prometheus metrics
    └── metrics.py
```

### Frontend Structure

```
frontend/src/
├── App.js               # Main app with routing
├── index.js             # Entry point
├── styles.css           # Modern dark theme styles
├── api/
│   └── client.js        # Axios API client
├── components/
│   ├── Layout.js
│   ├── ConfigForm.js    # Task creation form (with cards)
│   ├── TaskList.js      # Task list with status badges
│   ├── Dashboard.js     # Stats dashboard
│   ├── Navigation.js
│   └── RealtimeMonitor.js
├── pages/
│   ├── CreateTask.js
│   └── TaskDetail.js    # Live updates panel
├── context/
│   └── ToastContext.js  # Toast notifications
├── hooks/
│   └── useWebSocket.js
└── styles.css           # Dark theme CSS variables
```

## 📡 API Endpoints

### Authentication
- `POST /api/v1/token` - Obtain JWT access token

### Tasks
- `POST /api/v1/tasks/` - Create optimization task
- `GET /api/v1/tasks/{task_id}` - Get task status

### Health & Monitoring
- `GET /api/v1/health` - Health check
- `GET /api/v1/ready` - Readiness probe
- `GET /metrics` - Prometheus metrics

### WebSocket
- `WS /ws/tasks/{task_id}` - Real-time task updates

## ⚙️ Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/db

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment Variables

```bash
# API URL
REACT_APP_API_URL=http://localhost:8000/api/v1

# WebSocket URL
REACT_APP_WS_URL=ws://localhost:8000
```

## 🐳 Docker

### Production Deployment

```bash
# Build all images
docker-compose build

# Start in production mode
docker-compose up -d

# Scale workers
docker-compose up -d --scale worker=3
```

### Individual Services

```bash
# Build backend only
docker build -t unsloth-optimiser-api .

# Build frontend only
cd frontend && docker build -t unsloth-optimiser-frontend .
```

## ☸️ Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods
kubectl get svc

# View logs
kubectl logs -f deployment/unsloth-optimiser-api
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run frontend tests
cd frontend && npm test

# Run specific test file
pytest tests/test_api_integration.py -v
```

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.13, FastAPI, SQLAlchemy |
| **Task Queue** | Celery, Redis |
| **Frontend** | React 18, React Router, Axios |
| **Styling** | CSS Variables, Flexbox, Grid |
| **Real-time** | WebSocket |
| **Database** | PostgreSQL (prod), SQLite (dev) |
| **Auth** | JWT, bcrypt |
| **Monitoring** | Prometheus |
| **Deployment** | Docker, Docker Compose, Kubernetes |

## 📦 Services (Docker Compose)

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| frontend | `unsloth-optimiser-frontend` | 3000 | React SPA with dark theme |
| api | `unsloth-optimiser-api` | 8000 | FastAPI backend |
| worker | `unsloth-optimiser-worker` | - | Celery task processor |
| postgres | `postgres:15-alpine` | 5432 | PostgreSQL database |
| redis | `redis:7-alpine` | 6379 | Redis message broker |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Unsloth](https://github.com/unsloth/unsloth) - The optimization library
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Celery](https://docs.celeryq.dev/) - Distributed task queue
- [React](https://reactjs.org/) - Frontend library

## 💬 Support

For issues and questions:
- GitHub Issues: https://github.com/taxicabno1729/unsloth-optimiser/issues

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐
