# Domain Models Guidelines

## Purpose

`models.py` files define the domain and persistence models for each feature.  
Domain models represent core business entities and encapsulate persistence logic, typically using an ORM (e.g., SQLAlchemy).

`schemas.py` files define API contracts and validation logic using Pydantic schemas for request and response data.

`dtos.py` files define operation-specific DTOs used to transfer data between layers (e.g., from routers to use cases/services).

> **See [ADR 0005](../adr/0005-model-types-separation.md) for the architectural decision and rationale behind this separation.**

## Structure

- Each feature folder contains its own `models.py` file for ORM domain models.
- Define ORM models as classes inheriting from the shared `Base` (see `app/core/dependencies/database.py`).
- Use clear, descriptive names for models (e.g., `User`, `Post`, `Vote`).
- Each feature folder contains its own `schemas.py` file for Pydantic schemas used in API requests and responses.
- Each feature folder contains its own `dtos.py` file for operation-specific DTOs used to transfer data between layers.

## Usage

- Use domain models for persistence and business logic, not for API serialization.
- Do not expose ORM/domain models directly in API responses; use Pydantic schemas for DTOs.
- Reference domain models in repositories for database operations.
- Use Pydantic schemas for request validation and response serialization in the API layer.
- Use DTOs to encapsulate and transfer operation-specific data between routers, use cases, and services.

## Best Practices

- Keep models focused on persistence concerns; avoid business logic in ORM models.
- Use type hints for all fields and constructor arguments in all model types (domain, schema, DTO).
- Prefer explicit field definitions; avoid implicit defaults unless necessary.
- Add indexes and constraints at the model level for data integrity.
- Document non-obvious fields or relationships with inline comments.
- Avoid global state or mutable class-level attributes.
- Use abstract base classes for shared model logic if needed.
- Remove unused models, schemas, or DTOs after refactoring.
- Keep models, schemas, and DTOs framework-agnostic; do not depend on FastAPI-specific types except in `schemas.py`.
- **Keep DTOs and domain models in separate files to improve clarity, maintainability, and prevent accidental coupling.**
- **Keep Pydantic schemas in their own file to clearly separate API contracts from domain and operation-specific models.**

## Examples

**Domain Model (`models.py`):**
```python
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()")
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    __table_args__ = (Index("users_email_key", "email", unique=True),)
```

**Pydantic Schema (`schemas.py`):**
```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool
    created_at: str
```

**DTO (`dtos.py`):**
```python
class CreateUserData:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
```

## Updates

- Review and update models, schemas, and DTOs as business requirements or database schema change.
- Remove deprecated fields and document new ones.
- Ensure all changes are reflected in migration scripts, API docs, and tests.

- **Any changes to model separation should be discussed in the context of [ADR 0005](../adr/0005-model-types-separation.md).**