# Contributing to SAR Simulator

Thank you for your interest in contributing to the SAR Simulator! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Getting Started

The SAR Simulator is a Python-based tool for FMCW radar simulation with GPU acceleration. We welcome contributions in the form of:

- Bug fixes
- New features
- Documentation improvements
- Test coverage improvements
- Performance optimizations

## Development Setup

### 1. Fork and Clone

Fork the repository on GitHub and clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/sar-sim.git
cd sar-sim
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with all development dependencies including:
- pytest (testing framework)
- pytest-cov (coverage measurement)
- ruff (linter and formatter)
- mypy (type checker)
- pre-commit (git hooks)

### 4. Install Pre-commit Hooks (Optional but Recommended)

```bash
pre-commit install
```

This will automatically run code quality checks before each commit.

### 5. Verify Installation

```bash
python3 -m sarsim --help
pytest tests/  # Run tests (once tests are created)
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=sarsim --cov-report=html
```

View coverage report by opening `htmlcov/index.html` in a browser.

### Run Specific Tests

```bash
pytest tests/unit/test_simstate.py           # Specific file
pytest tests/unit/test_simstate.py::test_foo # Specific test
pytest -k "compression"                       # Tests matching pattern
```

### Run Tests in Parallel

```bash
pytest -n auto  # Uses all CPU cores
```

## Code Style

We use automated tools to maintain consistent code style:

### Linting and Formatting

```bash
# Format code with Ruff
ruff format .

# Check for linting issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

### Type Checking

```bash
mypy sarsim/
```

### Code Style Guidelines

- Follow PEP 8 conventions (enforced by Ruff)
- Maximum line length: 120 characters
- Use type hints for function signatures
- Write docstrings for public functions/classes (Google or NumPy style)
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

### Example Docstring

```python
def calculate_range(frequency: float, duration: float) -> float:
    """Calculate the range resolution for FMCW radar.

    Args:
        frequency: The frequency bandwidth in Hz.
        duration: The ramp duration in seconds.

    Returns:
        The range resolution in meters.

    Raises:
        ValueError: If frequency or duration is negative.
    """
    if frequency < 0 or duration < 0:
        raise ValueError("Frequency and duration must be positive")
    return (3e8 / (2 * frequency))
```

## Submitting Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test additions/improvements
- `refactor/` - Code refactoring

### 2. Make Your Changes

- Write clear, concise commit messages
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Maintain or improve code coverage

### 3. Commit Your Changes

```bash
git add .
git commit -m "Add feature X that does Y"
```

Good commit messages:
- Use present tense ("Add feature" not "Added feature")
- Be specific and descriptive
- Reference issue numbers when applicable

Example:
```
Fix range compression window parameter validation

- Add bounds checking for window parameters
- Add unit tests for edge cases
- Update documentation with valid ranges

Fixes #123
```

### 4. Push and Create Pull Request

```bash
git push origin feature/my-new-feature
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots/examples if applicable
- Confirmation that tests pass

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] No linting errors
- [ ] Type hints added where appropriate
- [ ] Commit messages are clear and descriptive

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Minimal code example or steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - Python version
   - Operating system
   - Relevant package versions
   - GPU/CUDA information (if applicable)

### Feature Requests

For feature requests, please include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Any alternative approaches considered?
4. **Additional Context**: Any other relevant information

## Development Guidelines

### Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Test both success and failure cases
- Use fixtures for common test setup
- Mock external dependencies when appropriate

### Performance

- Profile code before optimizing
- Document performance-critical sections
- Consider GPU vs CPU trade-offs
- Test with realistic data sizes

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public APIs
- Include examples in docstrings
- Update CHANGELOG.md with notable changes

### Security

- Never commit credentials or sensitive data
- Validate all external inputs
- Report security issues privately (see SECURITY.md)
- Keep dependencies up to date

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: See SECURITY.md for reporting process
- **Email**: Contact the maintainers at ims-as@uni-hannover.de

## Code of Conduct

Please note that this project follows a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## License

By contributing to SAR Simulator, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to SAR Simulator! 🎉
