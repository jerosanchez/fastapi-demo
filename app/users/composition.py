from .routes import UserRoutes
from .use_cases import CreateUser, GetUserById


def build_user_router():
    create_user_use_case = CreateUser()
    get_user_by_id_use_case = GetUserById()
    user_routes = UserRoutes(
        create_user_use_case=create_user_use_case,
        get_user_by_id_use_case=get_user_by_id_use_case,
    )
    return user_routes.router
