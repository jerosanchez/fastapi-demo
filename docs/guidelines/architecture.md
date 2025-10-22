# Project Architecture Guidelines

This project follows a **layered architecture** to promote separation of concerns, maintainability, and scalability.

Each feature (e.g., `votes`) is organized into its own folder, containing all related components. This structure enables teams and AI agents to work consistently across the codebase.

> **Note:** The rationale behind this architecture, as well as specific design decisions and trade-offs, are documented in our [Architecture Decision Records (ADRs)](../adr/). Please consult the ADRs to understand why certain patterns, conventions, or exceptions exist in the codebase.

## Layered System

The main layers are:

- **API Layer**: Handles HTTP requests and responses, typically via FastAPI routes.
- **Use Case Layer**: Encapsulates business logic and orchestrates interactions between services, repositories, and policies.
- **Service Layer**: Contains reusable logic that may be shared across use cases.
- **Repository Layer**: Manages data persistence and retrieval, abstracting the underlying database or storage.
- **Model Layer**: Defines ORM/database models representing persistent entities.
- **Schema Layer**: Defines Pydantic models for request/response validation and serialization.
- **Policy Layer**: Encapsulates authorization and business rules.
- **Exception Layer**: Centralizes custom exceptions for error handling.

## Dependency Injection (DI)

All dependencies (repositories, services, policies, etc.) are injected using FastAPI's dependency system or custom composition modules.

This promotes testability and loose coupling between layers.

## Feature Organization

Each feature contains:

- `routes.py`: API endpoints.
- `use_cases.py`: Business logic entry points.
- `services.py`: Shared logic.
- `repositories.py`: Data access.
- `models.py`: ORM/database models.
- `schemas.py`: Pydantic models for validation.
- `policies.py`: Authorization/business rules.
- `exceptions.py`: Feature-specific exceptions.
- `composition.py`: Dependency wiring for the feature.

## Consistency Guidelines

- **Naming**: Use clear, descriptive names for files and classes matching their roles.
- **Isolation**: Keep feature logic self-contained; avoid cross-feature imports except via well-defined interfaces.
- **Extensibility**: Add new features by replicating the established folder and file structure.
- **Testing**: Organize tests to mirror the feature structure for clarity.

## Purpose

This architecture ensures:

- **Separation of concerns**: Each layer has a distinct responsibility.
- **Scalability**: New features can be added with minimal impact on existing code.
- **Testability**: Layers and dependencies are easily mockable.
- **Consistency**: Developers and AI agents can navigate and extend the codebase efficiently.

Refer to the specific guidelines for each component type for further details.