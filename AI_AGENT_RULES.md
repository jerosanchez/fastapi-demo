# AI Agent Rules

## Router and Use Case Design Rules

- Use dependency injection for use cases in routers, passing them as constructor arguments.
- Each use case should be implemented as a class and inherit from its own ABC (using `ABC` suffix).
- Use cases should not depend on HTTP or FastAPI details (e.g., should not raise `HTTPException` or use schemas).
- Use cases should accept and return plain Python types (e.g., dicts, models), not Pydantic schemas.
- Use cases should raise custom domain exceptions for error scenarios (e.g., `EmailAlreadyExistsException`).
- Define custom exceptions in a dedicated `exceptions.py` file.
- Routers should catch domain exceptions and convert them to HTTP responses using static helper methods (e.g., `_report_user_exists`).
- Register route handlers using a private helper method (e.g., `_build_routes`) for clarity.
- Organize router methods so the public API (route handlers) is shown first, followed by private helpers.
- Use comment headers (e.g., `# === Public Route Handlers ===`, `# === Private Helpers ===`) to separate sections for clarity.
- Always convert Pydantic models to dicts before passing to use cases (e.g., `user_data.model_dump()`).
- Keep business logic and HTTP logic separated for testability and clarity.

## Unit Test Writing Rules

- Always wrap related test functions in a class, even if no setup is needed.
- Use `setup_method(self)` for per-test setup and to initialize shared mocks or objects.
- Create test-specific mocks or data inside the test method if only needed there.
- Use descriptive docstrings for test methods, stating the expected result or behavior.
- Separate test logic with blank lines, not comments like Arrange/Act/Assert.
- Test one behavior per test as a general rule.
- Prefer consistent structure and naming across all test files.
- Cover both success and error scenarios for each SUT.
- Place success (happy path) test cases before error cases in the test class.
- Suffix success (happy path) test method names with `_happy_path`.
- Use `pytest` conventions for setup and assertions.
- Always mock external dependencies so we can verify their usage with assertions and test the expected behavior of the SUT.
- Keep tests isolated and independent from each other.
- Run `make lint && make test` to validate all tests, and make the required fixes if required.
- Do not modify production code to fix the tests; if you detect a bug in production code as a consequence of running a test, ask before changing code.
- Create tests under `tests/<package_name>` folder