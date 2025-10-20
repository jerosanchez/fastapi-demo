# AI Agent Rules

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
- Do not modify production code to fix the tests; if you detect a bug in propduction code as a consequence of running a test, ask before changing code.