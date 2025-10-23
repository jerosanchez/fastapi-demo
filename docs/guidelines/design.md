# Feature Design Guidelines

This document provides guidance on designing features in this project, using the `posts` feature as an example.

Follow these principles and conventions to ensure consistency, maintainability, and scalability.

---

## General Design Principles

- **SOLID**: Design components to be single-purpose, open for extension, and easy to substitute.
- **DRY**: Avoid code duplication by extracting reusable logic into services or utilities.
- **KISS**: Keep implementations simple and straightforward.
- **YAGNI**: Only implement what is needed for current requirements.

---

## Feature Structure

For the recommended feature folder and file structure, see the [Architecture Guidelines](architecture.md#feature-organization).  

Each file serves a distinct purpose as described there. Replicate this structure for new features.

---

## Domain Modeling

- Model domain concepts (e.g., `Post`, `Author`) in `models.py`.
- Use clear, descriptive names and keep models focused on persistence concerns.
- Represent API contracts and validation logic in `schemas.py`.
- Define operation-specific DTOs (e.g., `CreatePostData`, `UpdatePostData`) in a separate file (e.g., `dtos.py`) within each feature folder.
- Maintain a clear separation between API schemas (`schemas.py`), operation-specific DTOs (`dtos.py`), and domain models (`models.py`) to improve clarity, maintainability, and prevent accidental coupling between layers.

---

## Error Handling

- Define feature-specific exceptions in `exceptions.py`.
- Handle errors gracefully in use cases or services and propagate meaningful messages to the API layer.
- Use FastAPI's exception handling mechanisms for consistent error responses.
- Centralize handling of infrastructure-related errors to keep business logic clean and focused.

---

## API Design Conventions

- Use RESTful naming and HTTP methods in `routes.py`.
- Structure endpoints for clarity (e.g., `/posts/{id}` for retrieval).
- Version APIs if breaking changes are introduced.
- Ensure request and response schemas are well-documented and validated.

---

## Extensibility & Maintainability

- Isolate feature logic; avoid cross-feature dependencies except via explicit interfaces.
- Use composition roots to inject dependencies (see `composition.py`) for loose coupling.
- Extract shared logic to `services.py` or common modules.
- Write modular, testable code in each layer.
- For layers that act only as thin forwarders (e.g., simple use cases that delegate directly to another layer), writing dedicated tests is optional.

---

## Cross-Cutting Concerns

- Implement logging, validation, and security checks in appropriate layers.
- Use policies for authorization logic.

---

## Documentation of Design Decisions

- Record significant design choices and trade-offs in [Architecture Decision Records (ADRs)](../adr/).
- In particular, document any non-standard patterns or exceptions in ADRs.
- Reference ADRs in code comments or documentation where relevant.
- Follow the [Documentation Guidelines](documentation.md) for standards on structure, clarity, and maintenance of all design-related documentation.

---

## Composition, Inheritance, and Interfaces

- Prefer composition over inheritance for flexibility.
- Use abstract base classes or protocols for shared interfaces (e.g., repository patterns).
- Only use inheritance when it simplifies code without introducing tight coupling.

---

## Code Readability & Consistency

- Follow naming conventions and file structure as shown in the architecture guidelines.
- Write clear docstrings and comments where necessary.
- In particular, avoid obvious comments, explain convoluted parts in detail.
- Look to improve readability by extracting blocks of code into private helper methods or functions.
- Organize tests to mirror the feature structure.

---

## Testing

See [testing.md](testing.md) for comprehensive testing guidelines.

---

## Summary

Design features to be modular, testable, and consistent with the layered architecture. Consult this document and ADRs before making significant design changes.