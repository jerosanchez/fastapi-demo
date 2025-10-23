# Composition Guidelines

## Purpose

`composition.py` files act as the composition root for each feature, wiring together all dependencies (repositories, services, policies, use cases, routers) in a single place.

Composition ensures that each layer receives its dependencies via constructor injection, promoting testability and loose coupling.

## Structure

- Each feature folder contains its own `composition.py` file.
- The composition file instantiates and connects all required components for the feature:
  - Repositories
  - Services
  - Policies
  - Use cases
  - Routers
- Typically, a single function (e.g., `build_<feature>_router`) returns the fully composed FastAPI `APIRouter` for the feature.
- Prefer explicit imports and instantiation over dynamic or reflective wiring for clarity.

## Usage

- The composition root is called from the main application to include the feature's router.
- All dependencies are instantiated and injected in the correct order.
- Example usage in the main app:
  ```python
  # ...existing code...
  from app.posts.composition import build_posts_router

  app.include_router(build_posts_router())
  # ...existing code...
  ```
- If using FastAPI's dependency injection system, register dependencies in the composition root for feature-level scoping.

## Best Practices

- Instantiate dependencies in the order required by constructors.
- Inject ABCs (abstract base classes) for testability and mocking.
- Avoid business logic, global state or adding config logic in composition files; only wire dependencies.
- Name composition functions clearly (e.g., `build_<feature>_router`).
- Keep composition logic isolated per feature; do not cross-wire dependencies between features.
- Document the dependency graph if it becomes complex.
- Use composition roots to enable feature modularity and facilitate future refactoring.
- Avoid global singletons; prefer explicit wiring for each feature.

## Examples

```python
# ...existing code...
def build_posts_router() -> APIRouter:
    post_repository = PostRepository()
    post_policy = PostPolicy()
    post_service = PostService(post_repository, post_policy)
    get_posts_use_case = GetPostsUseCase(post_service)
    create_post_use_case = CreatePostUseCase(post_service)
    get_post_by_id_use_case = GetPostByIdUseCase(post_service)
    update_post_use_case = UpdatePostUseCase(post_service)
    delete_post_use_case = DeletePostUseCase(post_service)

    return PostsRoutes(
        get_posts_use_case,
        create_post_use_case,
        get_post_by_id_use_case,
        update_post_use_case,
        delete_post_use_case,
    ).router
# ...existing code...
```

## Testing

See [testing.md](testing.md) for comprehensive testing guidelines.

## Updates

- Update composition roots when adding, removing, or changing dependencies.
- Keep the wiring up to date with feature requirements.
- Remove unused dependencies after refactoring.
- Review composition roots when upgrading FastAPI or changing dependency injection patterns.