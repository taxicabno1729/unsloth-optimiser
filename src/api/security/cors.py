"""CORS configuration for the API."""

from fastapi.middleware.cors import CORSMiddleware

# CORS origins configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",     # React dev server
    "http://localhost:8080",     # Alternative frontend port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

def setup_cors(app):
    """Configure CORS middleware for the FastAPI app"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
        max_age=600,  # 10 minutes cache for preflight
    )
