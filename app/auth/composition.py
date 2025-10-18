"""
Composition root for the auth package.
Encapsulates construction of routers and other auth-related components.
"""

from .routes import AuthRouter
from .service import AuthService


def build_auth_router():
    service = AuthService()
    return AuthRouter(service).router
