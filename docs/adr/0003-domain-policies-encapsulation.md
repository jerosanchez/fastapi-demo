# ADR: Domain Policies Encapsulation

## Context
Our system enforces various business rules and permissions (e.g., who can vote, view, update, or delete resources).

As the project grows, we anticipate more complex and varied authorization and business rules across features.

## Decision
We will encapsulate domain policies in separate policy classes, outside of services and use cases. Each feature will define its own policy class to centralize permission and business rule logic.

## Rationale
- **Separation of Concerns:** Keeps business rules and permission logic distinct from service orchestration and data access.
- **Reusability:** Policies can be reused across services, use cases, and route handlers without duplication.
- **Testability:** Policies are simple, stateless, and easy to test in isolation.
- **Clarity:** Centralizes rules, making it easier to audit and update permissions and business logic.
- **Extensibility:** Facilitates future changes, such as adding new rules or supporting more complex authorization scenarios.

## Consequences
- Requires discipline to consistently use policies across the codebase.
- Policy classes become the single source of truth for business rules and permissions.
- Simplifies services and use cases by delegating rule checks to policies.