# Testing Guidelines

## Purpose

Tests ensure the correctness, reliability, and maintainability of the codebase.

They help prevent regressions, document expected behavior, and enable safe refactoring.

## Structure

- Place tests for each feature in a corresponding subfolder under `tests/<feature_name>/`.
- Name test files according to the layer being tested (e.g., `test_<feature>_routes.py`, `test_<feature>_services.py`, `test_<feature>_use_cases.py`).
- Organize tests to mirror the feature and layer structure for clarity.

## Types of Tests

- **Unit tests**: Test individual units of logic (functions, methods, classes) in isolation.
- **Integration tests**: Test interactions between multiple components or layers.
- **API tests**: Use FastAPI's `TestClient` to test endpoint behavior and HTTP orchestration.

## Usage

- Use `pytest` as the test runner.
- Mock dependencies (repositories, services, use cases) using their ABCs and the `Mock` class.
- Do not create custom mock classes; use standard mocking tools.
- Set return values and side effects in each test function for clarity.
- Use fixtures for reusable setup logic.
- Test only one unit of logic per test function; keep tests focused and single-responsibility.
- Cover both success and error scenarios, including domain exceptions.
- For routers, test only HTTP orchestration, not business logic.
- Validate request and response schemas in API tests to ensure correct serialization.

## Best Practices

- Use descriptive test function names following the patterns `test_<action>_should_<expected_result>`.
- Avoid testing implementation details; focus on public API and expected outcomes.
- Keep tests isolated and independent.
- Prefer explicit assertions and avoid broad exception catching.
- Use fixtures for setup and teardown when needed.
- For layers that act only as thin forwarders, writing dedicated tests is optional.

## Examples

```python
# ...existing code...
def test_create_post_should_return_post_when_valid_data():
    # ...setup mocks and dependencies...
    # ...call method and assert result...

def test_update_post_should_raise_exception_when_not_found():
    # ...setup mocks and dependencies...
    # ...call method and assert exception...
# ...existing code...
```

## Updates

- Review and update tests as business logic or requirements change.
- Remove or update tests for deprecated features.
- Ensure new logic is covered by tests and documented.

## References

- See [pytest documentation](https://docs.pytest.org/en/stable/) for advanced usage.
- See [formatting.md](formatting.md) for code formatting standards.
