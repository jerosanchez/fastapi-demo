# Documentation Guidelines

These guidelines ensure all documentation in the FastAPI Demo project is clear, consistent, and useful for contributors and users.

## 1. Structure & Location

- **Project-wide docs** live in the `/docs` folder.
- **Guidelines** go in `/docs/guidelines/`.
- **Architecture Decision Records (ADRs)** are stored in `/docs/adr/`.
- **Getting Started** and onboarding instructions are in `/docs/getting-started.md`.
- **To-Do and improvement ideas** are tracked in `/docs/TODO.md`.
- **Specifications** (functional requirements, system design, ER diagrams, etc.) are kept in `/docs/specs/`.

## 2. Content Standards

- **Audience:** Write for developers new to the project. Assume basic Python/FastAPI knowledge.
- **Clarity:** Use simple, direct language. Avoid jargon unless defined.
- **Consistency:** Follow the formatting and terminology used in existing docs.
- **Completeness:** Document rationale, usage, and examples where relevant.

## 3. Organization

- Use headings (`#`, `##`, `###`) to structure content.
- Insert a blank line after each heading to improve readability for humans.
- Start each document with a brief summary of its purpose.
- Use lists, tables, and code blocks for clarity.
- Link to related documents (e.g., ADRs, guidelines, README) where helpful.
- Place specifications, requirements, and diagrams in `/docs/specs/` for discoverability.

## 4. Diagrams & Visuals

- Favor the use of **Mermaid** for diagrams (ER diagrams, flowcharts, system design, etc.).
- Embed Mermaid diagrams directly in Markdown files for version control and easy editing.
- Ensure diagrams are clear, labeled, and referenced in related documentation.

## 5. Maintenance

- **Update docs** with every significant code or architectural change.
- **Review docs** during code reviews for accuracy and completeness.
- **Deprecate outdated docs** by marking them clearly and linking to replacements.

## 6. Best Practices

- Prefer Markdown for all documentation.
- Use relative links for cross-referencing files within the repo.
- Include code snippets and examples where possible.
- Document decisions and rationales, not just instructions.

## 7. AI Agent Contributions

- AI-generated documentation must follow these guidelines.
- Review and edit AI suggestions for clarity and accuracy before merging.

## 8. Contribution Workflow

- Propose documentation changes via pull requests.
- Tag documentation updates in commit messages (e.g., `docs: update guidelines`).
- Assign reviewers for major documentation changes.

---

For more on project conventions, see [README.md](../../README.md) and other guidelines in this folder.