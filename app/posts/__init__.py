from app.posts.composition import build_posts_router


def init_service(app):
    app.include_router(build_posts_router())
