# ADR: Thin Use Cases for Consistency

## Context
Our use cases layer orchestrates business logic and dependencies, but often the orchestration logic is minimal.

## Decision
We will keep use case classes thin, even when they only delegate calls to services or repositories. All business operations will be routed through use cases for consistency.

## Rationale
- Ensures a consistent entry point for business logic across features.
- Simplifies dependency injection and testing.
- Makes it easier to evolve business logic in the future without refactoring API boundaries.
- Aligns with domain-driven design and layered architecture principles.

## Consequences
- Some use cases may appear as simple pass-throughs.
- Maintains clear separation of concerns and testability.
- Facilitates future changes and feature growth.