Name: Anish A Kunder
SRN: PES1UG24AM343

Note: The supplied three-page lab handout refers to four reflection questions but does not show their exact wording. These draft answers align with the stated learning outcomes. Replace the prompts if a separate question sheet was supplied by the instructor.

1. What is static code analysis, and why is it useful?

Static code analysis checks source code without running the program. It helps identify possible bugs, unsafe coding patterns, and style issues early. Finding these problems before deployment can make code easier to maintain and reduce avoidable risks.

2. How are Pylint, Bandit, and Flake8 different?

Pylint focuses on code quality, naming, and common programming mistakes. Bandit looks for common security risks in Python code. Flake8 checks Python style and formatting. Using all three gives a broader review than relying on one tool.

3. What issues were fixed in this program?

The fixes include replacing a mutable default list with a safe default, removing an unused hardcoded password-like constant, using a safer temporary-file API, replacing shell-based command execution with an argument list and input validation, improving names and docstrings, and adding checks for invalid match data. Formatting was also made consistent.

4. Can static analysis guarantee that a program is secure and correct?

No. Static analysis can find many known patterns, but it may miss issues that depend on runtime behaviour or system configuration. It can also report patterns that need human review. The program should still be tested, reviewed, and monitored in its intended environment.
