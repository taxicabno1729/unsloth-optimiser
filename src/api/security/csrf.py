"""CSRF protection middleware."""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets

# Simple CSRF token handling
CSRF_TOKEN_HEADER = "X-CSRF-Token"

class CSRFProtection:
    """CSRF protection middleware"""
    
    def __init__(self, exempt_paths=None):
        self.exempt_paths = exempt_paths or []
        self.security = HTTPBearer(auto_error=False)
    
    async def __call__(self, request: Request):
        # Skip CSRF for GET, HEAD, OPTIONS (read-only)
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return
        
        # Skip exempt paths
        for path in self.exempt_paths:
            if request.url.path.startswith(path):
                return
        
        # In production, validate CSRF token here
        # For now, just pass through
        pass

def generate_csrf_token() -> str:
    """Generate a new CSRF token"""
    return secrets.token_urlsafe(32)
