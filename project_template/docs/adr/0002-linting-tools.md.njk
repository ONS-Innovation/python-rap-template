# ADR 0002: Linting and Code Quality Tools

## Status

Accepted

## Context

Maintaining code quality and consistency is essential for a sustainable Python project. We needed to select appropriate linting and code quality tools that would:

1. Enforce consistent code style
2. Catch common errors and anti-patterns
3. Ensure type safety
4. Identify security vulnerabilities
5. Work efficiently in our development workflow
6. Integrate well with our CI/CD pipeline

## Decision

We have selected the following tools for our project:

1. **Ruff** - For linting and code formatting
2. **MyPy** - For static type checking
3. **Bandit** - For security vulnerability scanning
4. **Pre-commit** - For running checks before commits
5. **detect-secrets** - For preventing secrets from being committed
6. **nbstripout** - For cleaning Jupyter notebook outputs

## Rationale

### Ruff

Ruff was chosen as our primary linting and formatting tool because:

1. **Speed**: It's significantly faster than alternatives like flake8, pylint, or black
2. **Consolidation**: Replaces multiple tools (flake8, isort, pyupgrade, etc.) with a single tool
3. **Configurability**: Highly configurable through pyproject.toml
4. **Auto-fixing**: Can automatically fix many issues
5. **Modern**: Built with Rust, actively maintained, and rapidly improving

### MyPy

MyPy was selected for static type checking because:

1. **Standard**: It's the reference implementation for Python type checking
2. **Maturity**: Well-established with extensive documentation
3. **Gradual Typing**: Allows incremental adoption of type annotations
4. **Integration**: Works well with modern IDEs and editors

### Bandit

Bandit was chosen for security scanning because:

1. **Focus**: Specifically designed for Python security issues
2. **Simplicity**: Easy to integrate into CI/CD pipelines
3. **Customization**: Configurable to suit project-specific needs

### Pre-commit

Pre-commit was selected as our git hook manager because:

1. **Automation**: Ensures checks run before code is committed
2. **Consistency**: Enforces the same checks for all developers
3. **Flexibility**: Supports a wide range of hooks and tools

### detect-secrets

detect-secrets was chosen to prevent accidental secret exposure because:

1. **Prevention**: Stops secrets from being committed to the repository
2. **Baseline**: Supports a baseline file to avoid false positives
3. **Integration**: Works well with pre-commit

### nbstripout

nbstripout was selected for Jupyter notebook management because:

1. **Clean History**: Prevents notebook outputs from cluttering git history
2. **Reproducibility**: Encourages re-running notebooks for validation
3. **Security**: Prevents accidental exposure of sensitive data in outputs

## Consequences

- All developers will need to install and configure these tools
- CI/CD pipelines will enforce these checks
- Code that doesn't meet these standards will be rejected
- Initial setup time may be higher, but long-term maintenance will be easier
- Documentation will include guidance on working with these tools

## Alternatives Considered

### Flake8 + Black + isort

- **Pros**: Well-established, widely understood
- **Cons**: Slower, requires multiple tools, configuration spread across files

### Pylint

- **Pros**: Very thorough analysis
- **Cons**: Slower, more verbose, higher false positive rate

### Pyright

- **Pros**: Faster than MyPy in some cases
- **Cons**: Less mature in the Python ecosystem, different behaviour from MyPy
