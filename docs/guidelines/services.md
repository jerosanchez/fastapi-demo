# Services Guidelines

## Purpose

`services.py` files encapsulate reusable domain logic that may be shared across use cases within a feature.

Services help keep business logic organized, testable, and separate from data access and HTTP concerns.

They are responsible for orchestrating repository calls, applying business rules, and performing operations that do not belong in use cases or repositories.

## Structure

- Each feature folder contains its own `services.py` file.
- Define service ABCs (abstract base classes) and implementation classes in the same file for easy mocking and testing.
- Implementation classes must inherit from their ABC and follow the naming convention (e.g., `PostService`).
- Group public methods first, followed by private helper methods, separated by comment headers.
- Inject repositories, policies, or other dependencies via the constructor, using ABCs for testability.

## Usage

- Services are injected into use cases via constructor injection.
- Do not include HTTP or framework-specific logic in services.
- Services may call multiple repositories, apply business rules, or coordinate complex operations.
- Example usage in a use case:
  ```python
  # ...existing code...
  class CreatePostUseCase(CreatePostUseCaseABC):
      def __init__(self, post_service: PostServiceABC):
          self._post_service = post_service
      # ...existing code...
  ```
- Services should not be directly exposed to routers or API layers.

## Best Practices

- Keep service methods focused and single-responsibility.
- Extract blocks of logic from public methods to private helper functions for readability.
- Use type hints for method arguments and return values.
- Use dependency injection for all collaborators to enable easy mocking in tests.
- Document any non-obvious logic with inline comments.
- Keep services framework-agnostic; do not depend on FastAPI-specific types or objects.
- Organize services to maximize code reuse and minimize duplication across use cases.
- Document service responsibilities and interactions in feature-level documentation or ADRs if non-standard.

## Examples

```python
# ...existing code...
class PostServiceABC:
    def create_post(self, data: CreatePostData) -> Post:
        raise NotImplementedError

class PostService(PostServiceABC):
    def __init__(self, post_repository: PostRepositoryABC, post_policy: PostPolicyABC):
        self._post_repository = post_repository
        self._post_policy = post_policy

    # === Public API ===
    def create_post(self, data: CreatePostData) -> Post:
        # ...existing code...
        return self._post_repository.save(data)
    # === Helper methods ===
    def _validate_post_data(self, data: CreatePostData) -> None:
        # ...existing code...
# ...existing code...
```

## Testing

See [testing.md](testing.md) for comprehensive testing guidelines.

## Updates

- Review and update services as business requirements change.
- Remove unused methods and dependencies after refactoring.
- Ensure new logic is covered by tests and documented.
- Update ABCs and implementation classes together to maintain consistency.
