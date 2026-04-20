# Unsloth Optimiser

Web-based interface for configuring and monitoring model training optimization tasks using the Unsloth library.

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=white)](https://reactjs.org/)
[![Celery](https://img.shields.io/badge/Celery-37814A.svg?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

Unsloth Optimiser provides a complete solution for managing AI model optimization workflows:

- **Backend**: FastAPI with SQLAlchemy, JWT authentication, and Celery task queue
- **Frontend**: React SPA with real-time WebSocket updates
- **Workers**: Distributed Celery workers for optimization tasks
- **Deployment**: Docker and Kubernetes ready

## Features

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

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- Redis 7+ (for Celery)
- PostgreSQL 15+ (optional, SQLite for dev)

### Installation

```bash
# Clone the repository
git clone https://github.com/taxicabno1729/unsloth-optimiser.git
cd unsloth-optimiser

# Install Python dependencies
pip install -e ".[dev]"

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running Locally

```bash
# Start Redis (required for Celery)
redis-server

# Start the backend API
uvicorn src.api.main:app --reload --port 8000

# Start Celery worker (in another terminal)
celery -A src.api.tasks.celery worker --loglevel=info

# Start the frontend (in another terminal)
cd frontend
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   React SPA     │──────▶   FastAPI        │──────▶   PostgreSQL    │
│   (Frontend)    │      │   (Backend API)  │      │   (Database)    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Celery Workers │
                       │   (Redis)        │
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
└── security/            # Security middleware
    ├── cors.py
    └── csrf.py
```

### Frontend Structure

```
frontend/src/
├── App.js               # Main app with routing
├── index.js             # Entry point
├── api/
│   └── client.js        # Axios API client
├── components/
│   ├── Layout.js
│   ├── ConfigForm.js    # Task creation form
│   ├── TaskList.js
│   ├── Navigation.js
│   └── RealtimeMonitor.js
├── pages/
│   ├── CreateTask.js
│   └── TaskDetail.js
└── hooks/
    └── useWebSocket.js
```

## API Endpoints

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

## Configuration

Environment variables:

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

## Deployment

### Docker

```bash
# Build image
docker build -t unsloth-optimiser .

# Run container
docker run -p 8000:8000 \
  -e REDIS_URL=redis://host.docker.internal:6379/0 \
  unsloth-optimiser
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods
kubectl get svc
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run frontend tests
cd frontend && npm test
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.13, FastAPI, SQLAlchemy |
| Task Queue | Celery, Redis |
| Frontend | React 18, React Router, Axios |
| Real-time | WebSocket |
| Database | PostgreSQL (prod), SQLite (dev) |
| Auth | JWT, bcrypt |
| Monitoring | Prometheus |
| Deployment | Docker, Kubernetes |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Unsloth](https://github.com/unsloth/unsloth) - The optimization library
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Celery](https://docs.celeryq.dev/) - Distributed task queue

## Support

For issues and questions:
- GitHub Issues: https://github.com/taxicabno1729/unsloth-optimiser/issues
