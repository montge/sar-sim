# Programming Languages and Technologies

This document outlines the programming languages and technologies used in the SAR Simulator project.

## Primary Language

### Python (3.8-3.13)
- **Primary language** for all simulation logic, GUI, and data processing
- **Version support**: Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **Files**: All `.py` files in `sarsim/` and `tests/` directories (25 Python files)
- **Total coverage**: 40.54% (161 passing tests)

#### Python Modules
- **Core simulation**: `simjob.py`, `simstate.py`, `simscene.py`
- **Signal processing**: `operations.py`, `sardata.py`
- **GUI**: `gui.py` (PyQt5-based)
- **Utilities**: `siunits.py`, `profiling.py`, `commands.py`
- **Tests**: 8 test modules with 161+ tests

## Configuration Languages

### YAML (4 files)
- **GitHub Actions workflows**: `.github/workflows/tests.yml`, `.github/workflows/codeql.yml`
- **Configuration**: `.github/dependabot.yml`, `.pre-commit-config.yaml`
- **Purpose**: CI/CD pipeline configuration and automation

### TOML (1 file)
- **Project configuration**: `pyproject.toml`
- **Purpose**: Modern Python packaging, pytest, ruff, mypy, and coverage configuration

### Markdown (10 files)
- **Documentation**: README.md, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, etc.
- **Purpose**: Project documentation and guides

## Data Formats

### JSON
- **Usage**: Configuration data, metadata
- **Libraries**: Python `json` module

### SARDATA Format
- **Custom binary format** for radar data
- **Specification**: `doc/sardata-spec.md`
- **Implementation**: `sarsim/sardata.py`

## GPU/Accelerated Computing

### CUDA (Conditional)
- **Language**: CUDA C (via Numba JIT compilation)
- **Implementation**: `@cuda.jit()` decorators in `simjob.py`
- **Purpose**: GPU-accelerated azimuth compression
- **Fallback**: CPU implementation available when CUDA unavailable
- **Detection**: Automatic via Numba's `cuda.is_available()`

## Build and Development Tools

### Shell Scripts
- **Usage**: CI/CD, automation
- **Platform**: Bash (Linux/Unix)

### Git
- **Version control**: All source files tracked
- **Workflows**: GitHub Actions for CI/CD

## Key Dependencies by Language

### Python Dependencies
- **Numerical computing**: NumPy (1.26.4), SciPy (1.14.1)
- **GPU acceleration**: Numba (0.60.0), llvmlite (0.43.0)
- **GUI framework**: PyQt5 (5.15.11)
- **Visualization**: pyqtgraph (0.13.7)
- **Testing**: pytest (7.0+), pytest-cov (4.0+)
- **Code quality**: Ruff (0.1+), MyPy (1.0+)

## Language Statistics

| Language | Files | Percentage | Primary Use |
|----------|-------|------------|-------------|
| Python | 25 | ~60% | Core application, tests, utilities |
| Markdown | 10 | ~24% | Documentation |
| YAML | 4 | ~10% | CI/CD configuration |
| TOML | 1 | ~2% | Project configuration |
| Other | 2 | ~4% | Git ignore, misc config |

## Code Quality Tools

All tools are Python-based:
- **Linting**: Ruff (replaces flake8, isort, pyupgrade)
- **Type checking**: MyPy
- **Testing**: pytest with coverage reporting
- **Security**: Bandit, pip-audit, CodeQL
- **Formatting**: Ruff format (replaces Black)

## Development Environment

### Recommended Setup
```bash
# Python 3.8+ required
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run linting
ruff check .

# Run type checking
mypy sarsim/
```

### Optional: CUDA Support
- **NVIDIA GPU** with CUDA support
- **CUDA Toolkit** 11.0+
- **Numba** with CUDA support
- Automatically detected and enabled if available

## Platform Support

- **Linux**: Primary platform (tested on Ubuntu 20.04+)
- **Windows**: Supported
- **macOS**: Should work (not officially tested)

## Summary

The SAR Simulator is primarily a **Python-based** application with:
- Modern Python packaging (pyproject.toml)
- Extensive test coverage (161+ tests)
- Optional GPU acceleration (CUDA/Numba)
- Configuration in YAML/TOML
- Comprehensive documentation in Markdown
- CI/CD automation via GitHub Actions

For more information:
- [Contributing Guide](CONTRIBUTING.md)
- [README](README.md)
- [Testing Documentation](tests/README.md)
