# Formatting Guidelines

These rules ensure code consistency and readability for all contributors, including AI agents.

---

## Line Length

- Keep all lines under **90 characters**.
  - This matches the `.flake8` and Makefile settings.
  - Improves readability and avoids horizontal scrolling.
- Break long expressions across multiple lines using parentheses, not backslashes.

## Indentation

- Use **4 spaces** per indentation level.
- Do **not** use tabs.
- Indent continued lines by an extra level for clarity.

## Imports

- Place all imports at the top of the file, after any module comments and docstrings.
- Group imports by standard library, third-party, and local modules.
- Remove unused imports after code changes.
- Use dot notation (e.g. `import .<module>`) for modules within the same feature folder
- Use absolute imports for cross-feature references.
- Avoid wildcard imports (`from module import *`).

## Blank Lines

- Separate top-level functions and classes with **two blank lines**.
- Use **one blank line** between methods in a class.
- Use blank lines to separate logical sections within functions for readability.

## Whitespace

- Avoid trailing whitespace.
- No extra blank lines at the end of files.
- Use a single space after commas, colons, and semicolons.
- Do not use spaces immediately inside parentheses, brackets, or braces.

## Naming Conventions

- Use descriptive names; avoid single-letter names except for counters or iterators.
- Prefix unused variables with an underscore (e.g., `_unused`).
- Use `snake_case` for variables, functions, and methods.
- Use `PascalCase` for class names.
- Use `UPPER_CASE` for constants.

## Docstrings & Comments

- As a general rule, do not add docstrings to classes and methods, their names should be shelf-explanatory.
- Use inline comments to explain non-obvious logic.
- Avoid redundant comments.
- Use `# TODO:` and `# FIXME:` tags for tasks and known issues.
- Write comments in English.

## File Structure

- Place each class or function in the appropriate layer and feature folder.
- Do not mix unrelated logic in the same file.
- Extract private helper methods outside the class, unless they need `self`. 
- Limit file length to a reasonable size; split large files into smaller modules.

## Code Blocks

- For AI agents:  
  - Use Markdown code blocks with language identifiers.
  - Add file path comments for context.
- For humans:  
  - Use triple backticks for code blocks in Markdown documentation.

## Linting & Formatting Tools

- Run `make lint` and `make format` before committing.
- Fix all lint errors unless explicitly instructed otherwise.
- Use editorconfig or IDE settings to enforce formatting rules.

## Error Handling

- Prefer explicit exception handling using `try`/`except`.
- Catch only specific exceptions, not broad `except:` clauses.
- Log errors with context when possible.

## Type Annotations

- Use type hints for function arguments and return values where practical.
- Prefer explicit types for public APIs.

## Testing

- Write unit tests for all public functions and classes.
- Use descriptive test names.
- Keep tests isolated and independent.
- Add a comment to each test starting with `Should...` explaining the expected behaviour or result.

---

## References
- **PEP 8 – Style Guide for Python Code:**  
  [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
  *If a formatting rule is not mentioned here or you are in doubt, follow PEP 8 as the default standard.*


