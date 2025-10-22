# ADR: Repository Testing Strategy

## Context
Our repositories are thin wrappers over SQLAlchemy, containing no custom logic.

## Decision
We will not write unit tests for repositories. Instead, we will rely on integration tests to verify database interactions.

## Rationale
- Unit tests for thin repositories add little value.
- Integration tests ensure correct behavior with the actual database.
- This aligns with community best practices.

## Consequences
- Faster test suite.
- Focus on meaningful tests.