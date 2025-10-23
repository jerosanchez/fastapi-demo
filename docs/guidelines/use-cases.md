# Use Cases Guidelines

## Purpose

`use_cases.py` files define the business logic entry points for each feature.  

Use cases orchestrate services, repositories, and policies to perform specific business operations, keeping HTTP and framework concerns out of this layer.

## Structure

- Each feature folder contains its own `use_cases.py` file.
- Define use case ABCs (abstract base classes) and implementation classes in the same file.
- Implementation classes must inherit from their ABC and be suffixed with `UseCase`.
- Each use case should have a single public method called `execute`.
- Inject dependencies (services, repositories, policies) via the constructor, using ABCs for testability.

## Usage

- Use cases are invoked by routers or other orchestration layers to perform business operations.
- Do not include HTTP or framework-specific logic in use cases.
- Raise domain exceptions for error scenarios; do not handle HTTP responses.
- Example usage in a router:
  ```python
  # ...existing code...
  class CreateUserRoutes:
      def __init__(self, create_user_use_case: CreateUserUseCaseABC):
          self.router = APIRouter()
          self._build_routes()

      def _build_routes(self):
          @self.router.post("/users")
          async def create_user(data: CreateUserData):
              return create_user_use_case.execute(data)
  # ...existing code...
  ```

## Best Practices

- Keep use case methods focused and single-responsibility.
- Use type hints for method arguments and return values.
- Add docstrings to each public method describing its purpose and expected inputs/outputs.
- Inject dependencies via constructor, using ABCs for easy mocking in tests.
- Document any non-obvious logic with inline comments.
- Do not handle HTTP responses or framework-specific logic.
- When in doubt, follow the structure of existing use cases for other features.

## Examples

```python
# ...existing code...
class CreateUserUseCaseABC:
    def execute(self, data: CreateUserData) -> User:
        raise NotImplementedError

class CreateUserUseCase(CreateUserUseCaseABC):
    def __init__(self, user_service: UserServiceABC):
        self._user_service = user_service

    def execute(self, data: CreateUserData) -> User:
        # ...existing code...
        return self._user_service.create_user(data)
# ...existing code...
```

## Testing

See [testing.md](testing.md) for comprehensive testing guidelines.

## Updates

- Review and update use cases as business requirements change.
- Remove unused methods and dependencies after refactoring.
- Ensure new logic is covered by tests and documented.
- Update ABCs and implementation classes together to maintain consistency.