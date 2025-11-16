# SAR Simulator Test Suite

This directory contains the test suite for the SAR Simulator project.

## Test Structure

```
tests/
├── conftest.py                   # Shared fixtures and configuration
├── unit/                         # Unit tests for individual modules
│   ├── test_siunits.py          # SI unit conversion tests (12 tests)
│   ├── test_operations.py       # Signal processing operations tests (11 tests)
│   ├── test_simstate.py         # Parameter state management tests (54 tests)
│   ├── test_simscene.py         # Scene creation tests (11 tests)
│   ├── test_profiling.py        # Profiling and timing tests (18 tests)
│   └── test_sardata_security.py # File I/O security tests (15 tests)
├── integration/                 # Integration tests
│   └── test_simulation_pipeline.py  # End-to-end workflow tests (6 tests)
└── README.md                    # This file
```

**Test Statistics:**
- Total Tests: 108 (107 passing, 1 skipped)
- Code Coverage: 34.76%
- Unit Tests: 101
- Integration Tests: 6

## Running Tests

### Prerequisites

Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
pytest tests/unit/test_siunits.py
pytest tests/unit/test_operations.py
```

### Run Specific Test Classes or Functions

```bash
pytest tests/unit/test_siunits.py::TestSIUnitConversions
pytest tests/unit/test_siunits.py::TestSIUnitConversions::test_si_scale_parse_basic
```

### Run Tests by Pattern

```bash
pytest -k "window"          # Run tests matching "window"
pytest -k "not slow"        # Exclude slow tests
```

### Run with Coverage

```bash
pytest --cov=sarsim --cov-report=html
```

View the coverage report by opening `htmlcov/index.html` in your browser.

### Run in Parallel

```bash
pytest -n auto              # Use all CPU cores
pytest -n 4                 # Use 4 workers
```

### Verbose Output

```bash
pytest -v                   # Verbose
pytest -vv                  # Very verbose
pytest -s                   # Show print statements
```

## Writing Tests

### Test File Naming

- Test files should be named `test_*.py`
- Test files should mirror the structure of the source code
- Example: `sarsim/siunits.py` → `tests/unit/test_siunits.py`

### Test Function Naming

- Test functions should be named `test_*`
- Use descriptive names that explain what is being tested
- Example: `test_si_scale_parse_with_kilo_prefix()`

### Test Class Naming

- Test classes should be named `Test*`
- Group related tests in classes
- Example: `class TestSIUnitConversions:`

### Using Fixtures

Fixtures are defined in `conftest.py` and can be used in any test:

```python
def test_something(default_state, simple_scene):
    # default_state and simple_scene are automatically provided
    assert default_state is not None
    assert simple_scene is not None
```

### Example Test

```python
import pytest
import numpy as np
from sarsim import operations


class TestMyFeature:
    """Test suite for my feature."""

    def test_basic_functionality(self):
        """Test basic functionality works as expected."""
        result = my_function(input_data)
        assert result == expected_value

    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            my_function(invalid_input)

    def test_with_fixture(self, default_state):
        """Test using a fixture."""
        result = my_function(default_state)
        assert result is not None

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_parameterized(self, input, expected):
        """Test with multiple parameter sets."""
        assert my_function(input) == expected
```

## Test Categories

### Unit Tests (`tests/unit/`)

Test individual functions and classes in isolation.

**Characteristics:**
- Fast execution
- No external dependencies
- Mock external resources
- High coverage of edge cases

**Example modules to test:**
- `test_siunits.py` - SI unit conversions
- `test_operations.py` - Windowing functions
- `test_simstate.py` - Parameter management
- `test_simscene.py` - Scene creation

### Integration Tests (`tests/integration/`)

Test interaction between multiple components.

**Characteristics:**
- Slower execution
- Test realistic workflows
- May use actual data files
- Validate end-to-end functionality

**Example tests to write:**
- FMCW signal generation pipeline
- Full simulation workflow
- File loading and processing

### Performance Tests (`tests/performance/`)

Benchmark and validate performance characteristics.

**Characteristics:**
- May be slow
- Useful for regression detection
- Compare CPU vs GPU performance
- Memory usage validation

## Test Markers

Pytest markers are registered in `pyproject.toml` and help categorize tests:

### Registered Markers

- `slow` - Marks tests as slow (deselect with `-m "not slow"`)
- `integration` - Marks tests as integration tests
- `unit` - Marks tests as unit tests

### Using Markers

```python
import pytest

@pytest.mark.slow
def test_long_running_operation():
    """This test takes a long time."""
    pass

@pytest.mark.integration
def test_full_pipeline():
    """This is an integration test."""
    pass

@pytest.mark.unit
def test_single_function():
    """This is a unit test."""
    pass
```

### Running Tests by Marker

```bash
pytest -m "not slow"        # Skip slow tests (recommended for development)
pytest -m "slow"            # Run only slow tests
pytest -m "unit"            # Run only unit tests
pytest -m "integration"     # Run only integration tests
pytest -m "unit or integration"  # Run unit or integration tests
```

## Fixtures

Shared fixtures are defined in `conftest.py`:

### Available Fixtures

- `default_state` - A default simulation state
- `simple_scene` - A simple test scene with reflectors
- `sample_fmcw_params` - Typical FMCW parameters
- `sample_flight_path` - A simple flight path
- `mock_rc_lines` - Mock range-compressed data

### Creating New Fixtures

Add new fixtures to `conftest.py`:

```python
@pytest.fixture
def my_fixture():
    """Description of what this fixture provides."""
    # Setup
    resource = create_resource()

    yield resource  # Provide to test

    # Teardown (optional)
    resource.cleanup()
```

## Test Coverage Goals

| Component | Current | Target | Priority | Notes |
|-----------|---------|--------|----------|-------|
| simstate.py | 78.6% | 85% | High | Parameter management |
| simscene.py | 71.9% | 80% | High | Scene creation |
| sardata.py | 92.0% | 95% | High | File I/O with security |
| profiling.py | 83.3% | 90% | Medium | Timing utilities |
| operations.py | 83.3% | 85% | Medium | Window functions |
| siunits.py | 69.4% | 80% | Medium | SI unit parsing |
| simjob.py | 52.1% | 70% | High | Simulation execution |
| gui.py | 0% | 30% | Low | GUI components |
| commands.py | 0% | 60% | Medium | CLI commands |
| Overall | **34.76%** | **70%** | High | Project-wide coverage |

## Continuous Integration

Tests run automatically on:
- Every push to main/develop branches
- Every pull request
- Weekly schedule (security scans)

See `.github/workflows/tests.yml` for CI configuration.

## Common Issues

### PyQt5 Display Issues

If tests fail with display errors:
```bash
xvfb-run pytest  # Run with virtual display
```

### CUDA Not Available

Tests requiring GPU should skip gracefully:
```python
@pytest.mark.skipif(not CUDA_AVAILABLE, reason="CUDA not available")
def test_gpu_feature():
    pass
```

### Slow Tests

Mark slow tests appropriately:
```python
@pytest.mark.slow
def test_expensive_operation():
    pass
```

Run without slow tests:
```bash
pytest -m "not slow"
```

## Contributing

When adding new features:

1. Write tests first (TDD recommended)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov=sarsim`
4. Aim for >80% coverage for new code
5. Update this README if adding new test categories

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/latest/explanation/fixtures.html)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## Questions?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more information on contributing to the project.
