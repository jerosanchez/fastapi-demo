# Contributing to FastAPI Demo

Welcome! This guide will help you get started as a contributor to the FastAPI Demo project.

Please read it carefully before submitting changes.

---

## 1. Project Overview

- **Layered architecture** with vertical slicing by feature (see [ADR 0000](docs/adr/0000-project-architecture.md)).
- Each feature contains its own models, repositories, services, use cases, routes, schemas, and composition.
- All documentation, specs, and ADRs are kept in the [`docs/`](docs/) folder.

---

## 2. Getting Started

- Read [docs/getting-started.md](docs/getting-started.md) for setup instructions.
- Review the [README.md](README.md) for project features and conventions.
- Familiarize yourself with the [Architecture Decision Records](docs/adr/) and [Guidelines](docs/guidelines/).

---

## 3. Code Style & Best Practices

- Follow the [Formatting Guidelines](docs/guidelines/formatting.md):
  - Line length: **≤ 90 characters**
  - 4 spaces per indentation level, no tabs
  - Group imports: standard library, third-party, local modules
  - Use `snake_case` for variables/functions, `PascalCase` for classes
  - Prefer explicit type hints for public APIs
  - Avoid mixing unrelated logic in the same file
  - Remove unused imports and dependencies

- **Testing:**  
  - Write unit tests for all new logic.
  - Organize tests to mirror the feature structure.
  - Run `make test` before submitting changes.

- **Documentation:**  
  - Update relevant docs with every significant code or architectural change.
  - Use Markdown, headings, lists, and code blocks for clarity.
  - Reference ADRs and guidelines where relevant.
  - Prefer Mermaid diagrams for visuals.

- **Error Handling:**  
  - Use explicit exception handling (`try`/`except`).
  - Catch only specific exceptions.
  - Log errors with context.

---

## 4. Contribution Workflow

- Fork the repository and create a feature branch (`feature/<name>`, `fix/<name>`, or `docs/<name>`).
- Make atomic, well-documented commits.  
  - Tag documentation updates in commit messages (e.g., `docs: update guidelines`).
- Run `make lint` and `make format` before pushing.
- Submit a pull request (PR) with a clear description of changes and rationale.
- Assign reviewers for major changes.
- Address review feedback promptly.

---

## 5. Community Standards

- Be respectful and collaborative.
- Ask for clarification if requirements are ambiguous.
- Propose architectural changes via ADRs.
- Deprecate outdated docs by marking them and linking to replacements.
- Remove deprecated code, models, or methods after refactoring.

---

## 6. References

- [AI Agent Guidelines](docs/guidelines/ai-agent.md)
- [Feature Design Guidelines](docs/guidelines/design.md)
- [Services Guidelines](docs/guidelines/services.md)
- [Repositories Guidelines](docs/guidelines/repositories.md)
- [Models Guidelines](docs/guidelines/models.md)
- [Documentation Guidelines](docs/guidelines/documentation.md)
- [TODOs & Ideas](docs/TODO.md)

---

Thank you for contributing!  
For questions, open an issue or ask in the project discussion board.