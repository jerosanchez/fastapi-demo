# ADR 0006: Documentation within Repository

## Status

Accepted

## Context

As the project grows, maintaining clear and accessible documentation for specifications, guidelines, and future tasks is essential for collaboration, onboarding, and long-term maintainability.

There are several approaches to documentation management, including external wikis, separate documentation repositories, or keeping documentation files directly within the codebase.

## Decision

We will keep all documentation for specifications, guidelines, and TODOs directly alongside the repository, under the `/docs` folder. This includes:

- **Specs** (functional requirements, system design, ER diagrams, etc.) in `/docs/specs/`
- **Guidelines** (coding, architecture, documentation, AI agent, etc.) in `/docs/guidelines/`
- **TODOs and improvement ideas** in `/docs/TODO.md`
- **Architecture Decision Records (ADRs)** in `/docs/adr/`

Diagrams will favor the use of Mermaid, embedded in Markdown files for version control and easy editing.

## Rationale

- **Discoverability:** Contributors can easily find and update documentation without leaving the codebase.
- **Versioning:** Documentation changes are tracked alongside code changes, ensuring consistency.
- **Onboarding:** New developers have immediate access to all relevant information.
- **Collaboration:** Pull requests and code reviews can include documentation updates, improving quality.
- **Maintainability:** Specs, guidelines, and TODOs evolve with the code, reducing the risk of outdated docs.
- **Tooling:** Markdown and Mermaid are supported by most modern editors and platforms.

## Consequences

- Documentation must be maintained as part of the development workflow.
- Contributors are expected to update relevant docs with code changes.
- The `/docs` folder will be the single source of truth for project documentation.
- External documentation platforms (e.g., wikis) are discouraged unless strictly necessary.

## Alternatives Considered

- **External Wiki:** Rejected due to lack of versioning and integration with code reviews.
- **Separate Docs Repo:** Rejected due to increased maintenance overhead and risk of divergence.

## References

- [Documentation Guidelines](../guidelines/documentation.md)
- [README.md](../../README.md)