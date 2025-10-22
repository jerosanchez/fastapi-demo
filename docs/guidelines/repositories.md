# Repositories Guidelines

## Purpose

`repositories.py` files encapsulate data access logic for resources in the project.

Repositories provide a clean interface for querying, creating, updating, and deleting data, abstracting away database details from business logic.

## Structure

- Each app or module may have its own `repositories.py` file.
- You may define more than one repository per app/module:
    - For example, separate repositories for posts and votes if the feature requires it.
- Repositories are typically implemented as classes or functions that interact with the database or ORM.
- Common patterns include:
  - CRUD operations (Create, Read, Update, Delete).
  - Querying with filters, sorting, and pagination.
  - Mapping database models to domain objects.

## Usage

- Repositories are used in service layers to perform data operations.
- Use repositories to centralize and reuse data access logic.
- Example usage in a service class:
  ```python
  # ...existing code...
  from .repositories import UserRepositoryABC

  class UserService:
      def __init__(self, repository: UserRepositoryABC):
          self.repository = repository

      def get_user_by_id(self, user_id: str, db: Session):
          return self.repository.get_user_by_id(db, user_id)
  ```
  The service is then used in use cases or other application layers.

## Best Practices

- Keep repository logic isolated from business and presentation logic.
- Name repository methods clearly to reflect their purpose (e.g., `get_by_id`, `list_active`, `create_user`).
- Reuse repository methods across services.
- Prefer asynchronous methods if using async database drivers.

## Examples

```python
# ...existing code...
class PostRepository:
    async def get_by_id(self, post_id: int):
        # ...fetch post from database...
        pass

    async def create(self, post_data):
        # ...create new post...
        pass

    async def delete(self, post_id: int):
        # ...delete post...
        pass
# ...existing code...
```

## Testing

- Usually there's no need to test repositories, since they contain pure DB access operations without logic.

## Updates

- Review and update repositories as data models or requirements change.
- Remove deprecated methods and document new ones.