from .providers import JwtOAuth2TokenProvider
from .repositories import AuthRepository
from .routes import AuthRouter
from .services import AuthService
from .use_cases import AuthenticateUserUseCase


def build_auth_router():
    repository = AuthRepository()
    service = AuthService(repository)
    token_provider = JwtOAuth2TokenProvider()
    authenticate_user_use_case = AuthenticateUserUseCase(service, token_provider)

    return AuthRouter(authenticate_user_use_case).router
