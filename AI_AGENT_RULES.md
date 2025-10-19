# AI Agent Rules

## Unit Test Writing Rules

- Always wrap related test functions in a class, even if no setup is needed.
- Use `setup_method(self)` for per-test setup and to initialize shared mocks or objects.
- Create test-specific mocks or data inside the test method if only needed there.
- Use descriptive docstrings for test methods, stating the expected result or behavior.
- Separate test logic with blank lines, not comments like Arrange/Act/Assert.
- Prefer consistent structure and naming across all test files.
- Cover both success and error scenarios for each use case.
- Place success (happy path) test cases before error cases in the test class.
- Suffix success (happy path) test method names with `_happy_path`.
- Use pytest conventions for setup and assertions.
- Mock external dependencies and verify their usage with assertions.
- Keep tests isolated and independent from each other.
