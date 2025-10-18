"""
Composition root for the auth package.
Encapsulates construction of routers and other auth-related components.
"""

from .routes import AuthRouter


def build_auth_router():
    return AuthRouter().router
