from .routes import UserRoutes
from .services import UserService
from .use_cases import CreateUserUseCase, GetUserByIdUseCase


def build_user_router():
    service = UserService()
    create_user_use_case = CreateUserUseCase(service)
    get_user_by_id_use_case = GetUserByIdUseCase(service)
    user_routes = UserRoutes(
        create_user_use_case=create_user_use_case,
        get_user_by_id_use_case=get_user_by_id_use_case,
    )
    return user_routes.router
