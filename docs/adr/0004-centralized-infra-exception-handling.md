# ADR 0004: Centralized Infrastructure Exception Handling

## Status

Accepted

## Context

Infrastructure errors (such as database connection issues, cache failures, external API timeouts, or unexpected service outages) can occur during API requests.

By default, these errors may propagate uncaught, exposing internal details to clients or requiring repetitive error handling throughout route and service code.

As our system grows, we may integrate additional infrastructure frameworks (e.g., Redis, message brokers, third-party APIs) that can also raise exceptions outside our domain logic.

## Decision

We will capture uncaught infrastructure exceptions (e.g., `SQLAlchemyError`, `RedisError`, HTTP client errors) at the FastAPI application level using global exception handlers.

These handlers will return generic error responses to clients, avoiding exposure of internal details and keeping feature code clean from infrastructure error handling.

## Rationale

- **Security:** Prevents leaking internal infrastructure error details to API consumers.
- **Clean Code:** Avoids repetitive try/except blocks for infrastructure errors in route handlers and services.
- **Consistency:** Ensures all uncaught infrastructure errors are handled uniformly across the application.
- **Best Practice:** Centralized error handling for infrastructure exceptions is recommended in FastAPI and other web frameworks.
- **Maintainability:** Makes it easier to update error handling logic in one place if requirements change.
- **Extensibility:** Supports future integrations with other infrastructure frameworks by following the same pattern.

## Consequences

- Clients receive a generic error message for uncaught infrastructure errors, which may obscure specific failure reasons.
- Custom domain exceptions and business logic errors should still be handled explicitly in feature code.
- Infrastructure errors are less likely to pollute business logic, improving code clarity and separation of concerns.
- New infrastructure frameworks can be integrated with minimal changes to error handling strategy.