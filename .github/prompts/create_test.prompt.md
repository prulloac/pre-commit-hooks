---
name: create-test
description: Generate a comprehensive unit test file for the currently selected Python file. The generated tests should cover all public functions and methods, include meaningful comments, use pytest, save the test file in the tests/ directory, and automatically run pytest after creation.
---

For the currently selected Python file:

1. Generate a new unit test file using pytest, covering all public functions and methods in the selected file.
2. Place the new test file in the tests/ directory at the repository root, using the naming convention test_<original_filename>.py.
3. Each test should include clear comments explaining its purpose and logic.
4. If the file already has a corresponding test file, add new tests for uncovered functions/methods without duplicating existing ones.
5. After creating or updating the test file, automatically run pytest and report the results.
6. Ensure the tests are self-contained and do not require external dependencies unless present in the project.
