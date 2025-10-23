# Core Guidelines: Cross-Cutting Concerns

## Purpose

The `app/core` folder contains cross-cutting concerns—shared utilities, configuration, and dependencies used across multiple features and layers.

This promotes DRY principles, consistency, and maintainability.

## Structure

- Place all cross-cutting modules in `app/core/`.
- Organize by concern:
  - `config.py`: Application-wide configuration and settings.
  - `dependencies/`: FastAPI dependency functions (e.g., database/session, current user).
  - Utilities (e.g., logging, error handling) may be added as needed.
- Avoid mixing feature-specific logic in core modules.

## Usage

- Import core utilities and dependencies in feature composition roots or routers as needed.
- Use FastAPI's dependency injection for shared dependencies (e.g., database session, authentication).
- Reference core configuration via `core.config` for environment variables and settings.
- Keep core modules framework-agnostic where possible; only use FastAPI-specific patterns in `dependencies/`.

## Best Practices

- Keep core modules focused and single-responsibility.
- Document public APIs and usage patterns in code and guidelines.
- Avoid circular dependencies between core and feature modules.
- Update core modules when cross-cutting requirements change (e.g., new logging, error handling).
- Remove unused core utilities after refactoring.
- Prefer explicit imports over dynamic loading for clarity and testability.

## Examples

```python
# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    # ...other settings...

settings = Settings()
```

```python
# app/core/dependencies/database.py
from sqlalchemy.orm import Session
from app.core.config import settings

def get_db() -> Session:
    # ...return database session...
    pass
```

## Updates

- Review and refactor core modules as new cross-cutting concerns arise.
- Document rationale for major changes in ADRs.
- Ensure all features use core utilities consistently.

## References

- See [architecture.md](architecture.md) for project structure.
- See [composition.md](composition.md) for dependency wiring.
- See [formatting.md](formatting.md) for code style.