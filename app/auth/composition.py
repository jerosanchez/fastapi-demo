from .repository import AuthRepository
from .routes import AuthRouter
from .service import AuthService
from .use_cases import AuthenticateUserUseCase


def build_auth_router():
    repository = AuthRepository()
    service = AuthService(repository)
    authenticate_user_use_case = AuthenticateUserUseCase(service)

    return AuthRouter(authenticate_user_use_case).router
