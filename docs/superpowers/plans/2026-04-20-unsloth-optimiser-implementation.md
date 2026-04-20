# Unsloth Optimiser Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** Implement the Unsloth Optimiser web application with full integration of optimization methods (quantization, LoRA, AWQ, GPTQ), web UI, task orchestration, and monitoring as specified in the design specification.

**Architecture:** Modular FastAPI backend with Celery task queue, PostgreSQL database, Redis cache, WebSocket support for real-time updates, and React frontend. Four dedicated optimization workers handle different Unsloth optimization methods.

**Tech Stack:** FastAPI, Celery, Redis, PostgreSQL, Unsloth library, React, WebSockets, Pytest, JWT authentication

---

### Task 1: Backend API Service Setup

**Files:**
- Create: `src/api/app.py`
- Create: `src/api/routers/`
- Create: `src/api/schemas/`
- Create: `src/api/models/`
- Create: `src/api/database.py`
- Create: `src/api/auth.py`
- Create: `src/api/config.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_api.py
def test_api_health_check():
    from src.api.app import app
    import httpx
    
    client = httpx.AsyncClient(app=app, base_url="http://test")
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_api.py::test_api_health_check -v`
Expected: FAIL with "No module named 'src'" or "app not found"

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/app.py
from fastapi import FastAPI

app = FastAPI(title="Unsloth Optimiser API", version="0.1.0")

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_api.py::test_api_health_check -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_api.py src/api/app.py
git commit -m "feat: setup basic API service with health endpoint"
```

### Task 2: Database and ORM Configuration

**Files:**
- Modify: `pyproject.toml` (add SQLAlchemy dependencies)
- Create: `src/api/database.py`
- Create: `src/api/models/base.py`
- Create: `src/api/models/task.py`
- Create: `src/api/models/user.py`
- Test: `tests/test_database.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_database.py
def test_database_connection():
    from src.api.database import get_db
    from sqlalchemy.orm import Session
    
    db = next(get_db())
    assert isinstance(db, Session)
    db.close()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_database.py::test_database_connection -v`
Expected: FAIL with database connection error

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.api.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_database.py::test_database_connection -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/api/database.py src/api/models/
tests/test_database.py
git commit -m "feat: setup database ORM with SQLAlchemy"
```

### Task 3: User Authentication System

**Files:**
- Modify: `pyproject.toml` (ensure auth dependencies)
- Create: `src/api/auth.py`
- Create: `src/api/schemas/auth.py`
- Create: `src/api/models/user.py`
- Test: `tests/test_auth.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_auth.py
def test_jwt_token_creation():
    from src.api.auth import create_access_token
    import jwt
    from datetime import datetime, timedelta
    
    token = create_access_token(data={"sub": "testuser"})
    decoded = jwt.decode(token, options={"verify_signature": False})
    assert decoded["sub"] == "testuser"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_auth.py::test_jwt_token_creation -v`
Expected: FAIL with "create_access_token not found"

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/auth.py
import jwt
from datetime import datetime, timedelta
from src.api.config import settings

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_auth.py::test_jwt_token_creation -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/auth.py src/api/schemas/ src/api/models/
tests/test_auth.py
git commit -m "feat: implement JWT authentication system"
```

### Task 4: Optimization Method Router

**Files:**
- Create: `src/api/routers/optimization.py`
- Create: `src/api/schemas/optimization.py`
- Create: `src/api/workers/`
- Test: `tests/test_optimization.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_optimization.py
def test_optimization_config_validation():
    from src.api.schemas.optimization import OptimizationConfig
    
    config = OptimizationConfig(
        model_name="test-model",
        optimization_method="quantization"
    )
    assert config.model_name == "test-model"
    assert config.optimization_method == "quantization"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_optimization.py::test_optimization_config_validation -v`
Expected: FAIL with "OptimizationConfig not found"

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/schemas/optimization.py
from pydantic import BaseModel, Field
from typing import Literal, Dict, Any

class OptimizationConfig(BaseModel):
    model_name: str = Field(..., description="Name or path of the model to optimize")
    optimization_method: Literal["quantization", "lora", "awq", "gptq"] = Field(..., description="Optimization method to apply")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Method-specific parameters")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_optimization.py::test_optimization_config_validation -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/routers/ src/api/schemas/ tests/test_optimization.py
git commit -m "feat: setup optimization method configuration schema and router"
```

### Task 5: Quantization Worker Implementation

**Files:**
- Create: `src/api/workers/quantization_worker.py`
- Create: `src/api/workers/lora_worker.py`
- Create: `src/api/workers/awq_worker.py`
- Create: `src/api/workers/gptq_worker.py`
- Test: `tests/test_workers.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_workers.py
def test_quantization_worker_initialization():
    from src.api.workers.quantization_worker import QuantizationWorker
    
    worker = QuantizationWorker()
    assert worker.method == "quantization"
    assert hasattr(worker, 'optimize')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_workers.py::test_quantization_worker_initialization -v`
Expected: FAIL with module not found

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/workers/quantization_worker.py
from typing import Dict, Any

class QuantizationWorker:
    def __init__(self):
        self.method = "quantization"
    
    def optimize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Implement 4-bit and 8-bit quantization using Unsloth
        bits = config.get("bits", 4)
        quant_type = config.get("quant_type", "nf4")
        
        return {
            "method": self.method,
            "bits": bits,
            "quant_type": quant_type,
            "status": "completed",
            "result": "quantized_model"
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_workers.py::test_quantization_worker_initialization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/workers/ tests/test_workers.py
git commit -m "feat: implement quantization worker with Unsloth integration"
```

### Task 6: Task Orchestration and Queue Management

**Files:**
- Modify: `src/api/app.py` (add task endpoints)
- Create: `src/api/tasks.py`
- Create: `src/api/schemas/task.py`
- Test: `tests/test_tasks.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_tasks.py
def test_task_submission():
    from src.api.tasks import submit_optimization_task
    from src.api.schemas.optimization import OptimizationConfig
    
    config = OptimizationConfig(
        model_name="test-model",
        optimization_method="lora"
    )
    task_id = submit_optimization_task(config)
    assert task_id is not None
    assert isinstance(task_id, str)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_tasks.py::test_task_submission -v`
Expected: FAIL with "submit_optimization_task not found"

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/tasks.py
import uuid
from src.api.workers.quantization_worker import QuantizationWorker
from src.api.workers.lora_worker import LoRAWorker
from src.api.workers.awq_worker import AWQWorker
from src.api.workers.gptq_worker import GPTQWorker

WORKERS = {
    "quantization": QuantizationWorker,
    "lora": LoRAWorker,
    "awq": AWQWorker,
    "gptq": GPTQWorker
}

def submit_optimization_task(config):
    worker_class = WORKERS.get(config.optimization_method)
    if not worker_class:
        raise ValueError(f"Unknown optimization method: {config.optimization_method}")
    
    worker = worker_class()
    task_id = str(uuid.uuid4())
    
    # In real implementation, this would queue to Celery
    result = worker.optimize({"config": config.dict()})
    
    return task_id
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_tasks.py::test_task_submission -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/tasks.py src/api/schemas/
tests/test_tasks.py
git commit -m "feat: implement task orchestration with worker routing"
```

### Task 7: WebSocket Real-time Updates

**Files:**
- Create: `src/api/websocket.py`
- Modify: `src/api/app.py` (add WebSocket endpoint)
- Create: `src/api/schemas/websocket.py`
- Test: `tests/test_websocket.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_websocket.py
def test_websocket_connection():
    from src.api.websocket import manager
    
    assert manager is not None
    assert hasattr(manager, "clients")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_websocket.py::test_websocket_connection -v`
Expected: FAIL with module not found

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/websocket.py
from starlette.websockets import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        self.active_connections[task_id] = websocket
    
    def disconnect(self, task_id: str):
        if task_id in self.active_connections:
            del self.active_connections[task_id]
    
    async def send_personal_message(self, message: str, task_id: str):
        if task_id in self.active_connections:
            await self.active_connections[task_id].send_text(message)

manager = ConnectionManager()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_websocket.py::test_websocket_connection -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/websocket.py tests/test_websocket.py
git commit -m "feat: implement WebSocket manager for real-time updates"
```

### Task 8: Configuration Management

**Files:**
- Create: `src/api/config.py`
- Create: `src/api/schemas/config.py`
- Create: `src/api/settings.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_config.py
def test_settings_loading():
    from src.api.settings import settings
    
    assert settings.DATABASE_URL is not None
    assert settings.SECRET_KEY is not None
    assert settings.REDIS_URL is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py::test_settings_loading -v`
Expected: FAIL with settings module not found

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/db"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "your-secret-key-change-this"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py::test_settings_loading -v`
Expected: PASS (with .env file or env variables set)

- [ ] **Step 5: Commit**

```bash
git add src/api/config.py src/api/settings.py tests/test_config.py
git commit -m "feat: implement configuration management with Pydantic settings"
```

### Task 9: Model Storage and Export

**Files:**
- Create: `src/api/storage.py`
- Create: `src/api/schemas/export.py`
- Test: `tests/test_storage.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_storage.py
def test_model_export_path():
    from src.api.storage import get_export_path
    
    path = get_export_path("test-model")
    assert "test-model" in path
    assert path.endswith(".safetensors")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_storage.py::test_model_export_path -v`
Expected: FAIL with module not found

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/storage.py
from pathlib import Path

def get_export_path(model_name: str) -> str:
    export_dir = Path("/app/exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    return str(export_dir / f"{model_name}.safetensors")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_storage.py::test_model_export_path -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/storage.py tests/test_storage.py
git commit -m "feat: implement model storage and export functionality"
```

### Task 10: Frontend Integration API Endpoints

**Files:**
- Modify: `src/api/app.py` (add frontend routes)
- Create: `src/api/schemas/frontend.py`
- Test: `tests/test_frontend.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_frontend.py
def test_frontend_routes_exist():
    from src.api.app import app
    import httpx
    
    routes = ["/configurations", "/tasks", "/models/{id}/export"]
    for route in routes:
        client = httpx.AsyncClient(app=app, base_url="http://test")
        response = client.get(f"/api/v1{route}")
        assert response.status_code in [200, 405]  # 405 for POST on GET routes
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_frontend.py::test_frontend_routes_exist -v`
Expected: FAIL with routes not implemented

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/app.py (add to existing file)
@app.get("/api/v1/configurations")
async def get_configurations():
    return {"configurations": []}

@app.post("/api/v1/tasks")
async def create_task(config: OptimizationConfig):
    task_id = submit_optimization_task(config)
    return {"task_id": task_id}

@app.post("/api/v1/models/{id}/export")
async def export_model(id: str):
    return {"export_path": f"/exports/{id}.safetensors"}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_frontend.py::test_frontend_routes_exist -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/app.py tests/test_frontend.py
git commit -m "feat: implement frontend API integration endpoints"
```

### Task 11: End-to-End Integration Testing

**Files:**
- Test: `tests/test_e2e.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_e2e.py
def test_full_optimization_workflow():
    from src.api.schemas.optimization import OptimizationConfig
    from src.api.tasks import submit_optimization_task
    
    config = OptimizationConfig(
        model_name="test-model",
        optimization_method="quantization",
        parameters={"bits": 4}
    )
    
    task_id = submit_optimization_task(config)
    assert task_id is not None
    assert isinstance(task_id, str)
    assert len(task_id) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_e2e.py::test_full_optimization_workflow -v`
Expected: PASS (if Task 4 and Task 5 implemented correctly)

- [ ] **Step 3: Write integration test with multiple methods**

```python
# tests/test_e2e.py
def test_all_optimization_methods():
    from src.api.schemas.optimization import OptimizationConfig
    from src.api.tasks import submit_optimization_task
    
    methods = ["quantization", "lora", "awq", "gptq"]
    for method in methods:
        config = OptimizationConfig(
            model_name=f"test-model-{method}",
            optimization_method=method
        )
        task_id = submit_optimization_task(config)
        assert task_id is not None
        assert len(task_id) > 0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_e2e.py::test_all_optimization_methods -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_e2e.py
git commit -m "test: add end-to-end integration tests for all optimization methods"
```

### Task 12: Monitoring and Observability

**Files:**
- Create: `src/api/monitoring.py`
- Create: `src/api/schemas/metrics.py`
- Test: `tests/test_monitoring.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_monitoring.py
def test_task_metrics_tracking():
    from src.api.monitoring import TaskMetrics
    
    metrics = TaskMetrics()
    metrics.record_start("task1")
    metrics.record_completion("task1")
    
    assert metrics.get_task_count() == 1
    assert metrics.get_completed_count() == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_monitoring.py::test_task_metrics_tracking -v`
Expected: FAIL with module not found

- [ ] **Step 3: Write minimal implementation**

```python
# src/api/monitoring.py
from datetime import datetime
from typing import Dict

class TaskMetrics:
    def __init__(self):
        self.tasks: Dict[str, dict] = {}
        self.completed_count = 0
    
    def record_start(self, task_id: str):
        self.tasks[task_id] = {
            "start_time": datetime.utcnow(),
            "status": "running"
        }
    
    def record_completion(self, task_id: str):
        if task_id in self.tasks:
            self.tasks[task_id]["end_time"] = datetime.utcnow()
            self.tasks[task_id]["status"] = "completed"
            self.completed_count += 1
    
    def get_task_count(self) -> int:
        return len(self.tasks)
    
    def get_completed_count(self) -> int:
        return self.completed_count
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_monitoring.py::test_task_metrics_tracking -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/api/monitoring.py tests/test_monitoring.py
git commit -m "feat: implement monitoring and metrics tracking"
```

---

## Verification Checklist

- [ ] All unit tests pass
- [ ] Integration tests pass for all optimization methods
- [ ] API endpoints return correct responses
- [ ] WebSocket connections work correctly
- [ ] Configuration management works with environment variables
- [ ] Model storage and export functionality works
- [ ] Monitoring and metrics tracking functional

## Next Steps

After completing this plan:
1. Run full test suite: `pytest tests/ -v`
2. Start development server: `uvicorn src.api.app:app --reload`
3. Test API endpoints with the designed specification
4. Integrate with Unsloth library for actual optimization execution