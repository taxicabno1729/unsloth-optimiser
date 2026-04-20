"""Prometheus metrics for the Unsloth Optimiser API."""
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Define metrics
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "API request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

TASK_COUNT = Counter(
    "tasks_created_total",
    "Total tasks created",
    ["optimization_method"]
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect request metrics."""

    async def dispatch(self, request: Request, call_next):
        """Process request and record metrics."""
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Record metrics
        duration = time.time() - start_time
        method = request.method
        endpoint = request.url.path
        status_code = str(response.status_code)

        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

        return response


def get_metrics():
    """Generate Prometheus metrics output."""
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST
    )
