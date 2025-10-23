# AI Agent Guidelines

## Purpose
Instructions for AI agents (e.g., GitHub Copilot) to ensure generated code and suggestions follow project conventions.

## General Rules
- Always follow the layered architecture and vertical slicing by feature.
- Use ABCs for dependency injection and mocking.
- Reference existing code for naming and structure.
- Extract blocks of logic from class methods to private helper functions with meaningful names in the same file to improve readability.
- In classes, group public methods first, followed by helper methods, separated by comment headers (e.g., `# === Public API ===`, `# === Helper methods ===`).

## Interaction
- Respond in Markdown with code blocks and file path comments.
- Ask for clarification if requirements are ambiguous.
- Do not stop due to lint errors; remove unused dependencies after code changes.

## Code Generation
- Place new files in the appropriate feature folder.
- Use the same structure as existing features.
- Add/Do not add docstrings and comments as per guidelines.
- After each code generation or changes, remove any unused dependencies signaled by the linter.

## Limitations
- Do not expose domain models in API responses.
- Avoid business logic in routers; delegate to use cases.
- Do not couple layers below routers to DTOs (aka schemas).

## Documentation
- When adding comments or docstrings, follow the style and patterns used in existing guidelines and project files.
- Reference ADRs and guidelines for rationale when making architectural or design suggestions; if no ADR exists yet, draft a proposal for review.

## References
- See [ADRs](../adr/) for architectural decisions.

- See [architecture.md](architecture.md) for architecture guidelines.
- See [design.md](design.md) for general design rules.
- See [formatting.md](formatting.md) for code formatting standards.
- See [testing.md](testing.md) for testing guidelines.

- See [composition.md](composition.md) for root composition guidelines. 

- See [routers.md](routers.md) for router layer guidelines.
- See [use-cases.md](use-cases.md) for use cases layer guidelines.
- See [services.md](services.md) for service layer guidelines.
- See [repositories.md](repositories.md) for repository layer guidelines.
- See [policies.md](policies.md) for policies guidelines.

- See [models.md](models.md) for domain models guidelines.
- See [schemas.md](schemas.md) for DTOs/schemas guidelines.

- See [core.md](core.md) for cross-cutting concerns guidelines.