# Routers Guidelines

## Purpose

`routes.py` files define the HTTP API endpoints for each feature in the project.

Routers handle request/response validation, exception mapping, and delegate business logic to use cases.

They serve as the entry point for client interactions with the backend.

## Structure

- Each feature has its own `routes.py` file containing a single router class.
- The router class encapsulates all route handlers for the feature.
- Route registration is performed in a private `_build_routes` method.
- Route handler methods are grouped by HTTP verb and resource for clarity.
- Use FastAPI's `APIRouter` for endpoint registration.
- Route handlers should only handle HTTP logic, request/response validation, and exception mapping.
- Prefer explicit HTTP status codes and response models for each endpoint.
- Use dependency injection (`Depends`) for authentication, authorization, and shared resources.

## Usage

- Routers are mounted in the application via the feature's `composition.py` and `__init__.py`.
- Inject use cases via the router class constructor or FastAPI dependencies; never instantiate use cases directly in handlers.
- Example usage:
  ```python
  # ...existing code...
  class UserRoutes:
      def __init__(self, create_user_use_case: CreateUserUseCaseABC):
          self.router = APIRouter(prefix="/users", tags=["Users"])
          self._build_routes()
      # ...existing code...
  ```
- Use FastAPI's dependency system to inject authentication, authorization, and database session objects.
- Document endpoints with summary and description arguments for better API docs.

## Best Practices

- Keep route handlers thin; delegate business logic to use cases.
- Map domain exceptions to appropriate HTTP responses using FastAPI exception handlers.
- Use Pydantic schemas for request bodies and responses; never expose domain models directly.
- Do not add docstrings to route handlers unless purpose is not self evident.
- Avoid business logic or data access in route handlers.
- Group public route handler methods first, followed by helper methods, separated by comment headers.
- Follow naming and structure conventions from existing routers.
- Use path and query parameters for resource identification and filtering.
- Prefer async route handlers if underlying operations are asynchronous.
- Use FastAPI's built-in response classes (e.g., `JSONResponse`) for custom responses when needed.
- Use routers to document API endpoints via tags and descriptions for automatic OpenAPI generation.

## Examples

```python
# ...existing code...
class PostsRoutes:
    def __init__(self, get_posts_use_case: GetPostsUseCaseABC):
        self.router = APIRouter(prefix="/posts", tags=["Posts"])
        self._build_routes()

    def get_posts(self, ...):
        """Fetch paginated list of posts."""
        # ...existing code...

    def _build_routes(self):
        self.router.get("/", response_model=...)(self.get_posts)
# ...existing code...
```

## Testing

See [testing.md](testing.md) for comprehensive testing guidelines.

## Updates

- Review and update routers as API requirements change.
- Ensure deprecated endpoints are removed and new ones are documented.
- Update OpenAPI documentation and tags as endpoints evolve.