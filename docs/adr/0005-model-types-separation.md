# ADR 0005: Separation of Model Types (Domain Models, DTOs, Schemas)

## Status

Accepted

## Context

As the project grows, we use three distinct types of models:
- **Domain models** (ORM/persistence models) for representing business entities and database structure.
- **DTOs** (operation-specific models) for transferring data between layers (e.g., routers, use cases, services).
- **Schemas** (Pydantic models) for API contracts, request validation, and response serialization.

Previously, DTOs and domain models were sometimes defined in the same file, leading to confusion and accidental coupling.

API schemas were also occasionally mixed with domain logic.

## Decision

We will maintain a clear separation between:
- **Domain models** in `models.py`
- **DTOs** in `dtos.py`
- **Schemas** in `schemas.py`

Each feature folder will contain these files as needed.

This separation will be enforced in guidelines and code reviews.

## Consequences

- **Improved clarity:** Developers can easily locate and understand the purpose of each model type.
- **Reduced coupling:** Changes in one layer (e.g., persistence) do not unintentionally affect others (e.g., API).
- **Better maintainability:** Refactoring and onboarding are easier due to clear boundaries.
- **Alignment with best practices:** Follows community recommendations for layered architecture and clean code.

## Alternatives Considered

- Keeping all models in a single file per feature: rejected due to maintainability and clarity concerns.
- Using only Pydantic models for all layers: rejected to avoid mixing persistence and API concerns.
