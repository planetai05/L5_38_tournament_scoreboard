
Name: Anish A Kunder
SRN: PES1UG24AM343

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Shell command through `os.system` | Security (Bandit) | 67 | The server value was joined into a shell command. | Use `subprocess.run` with an argument list, `shell=False`, a timeout, a validated server value, and an absolute source path. The narrowly scoped Bandit suppression documents that this direct invocation is intentional. |
| Unsafe temporary filename | Security (Bandit) | 62 | `tempfile.mktemp()` reserves no file and can create a race condition. | Use `NamedTemporaryFile` with `delete=False` and return the created file's path. |
| Hardcoded password-like constant | Security (Bandit) | 6 | A password-like value was stored in the source even though the demo never used it. | Remove the unused constant instead of retaining an unnecessary credential. |
| Mutable default argument | Code quality / bug (Pylint) | 11 | `players=[]` could share one list between separate calls. | Default to `None` and create a new list for each team. |
| Non-standard function and parameter names | Code quality (Pylint) | 11, 16, 24, 40, 45, 49, 53, 57, 60, 65 | CamelCase names made the code inconsistent with normal Python naming conventions. | Rename the functions and parameters to `snake_case` and update their call sites. |
| Missing docstrings and module description | Code quality (Pylint) | Throughout | The module and functions did not explain their purpose. | Add a module docstring and concise function docstrings. |
| Fragile top-two check | Reliability | 55 | Indexing the first two table entries can fail when fewer than two teams are registered. | Check membership in `league_table()[:2]`. |
| Insufficient input checks | Reliability | 23–37 | A match could reference an unregistered team, a team could play itself, or a negative score could be recorded. | Validate the teams and score before updating statistics. |
| Spacing and formatting issues | Style (Flake8) | 4 and throughout | Whitespace and spacing were inconsistent. | Apply consistent PEP 8 formatting and verify with Flake8. |
