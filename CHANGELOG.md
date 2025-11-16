# Changelog

All notable changes to the SAR Simulator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive testing infrastructure with pytest
  - 74+ unit tests covering core modules (~78% coverage for simstate, simscene, profiling)
  - 6 integration tests for end-to-end simulation workflows
  - Security-focused tests for file I/O operations
  - Test fixtures and shared test configuration
- GitHub Actions CI/CD workflows
  - Automated testing across Python 3.8-3.11
  - CodeQL security scanning
  - Coverage reporting with Codecov integration
- Dependabot configuration for automated dependency updates
  - Weekly Python dependency checks
  - Monthly GitHub Actions updates
  - Grouped minor/patch updates
- Code quality tooling
  - Ruff linter and formatter configuration
  - MyPy type checking setup
  - Pre-commit hooks for automated quality checks
- Comprehensive project documentation
  - ASSESSMENT.md: Security, testing, and documentation analysis
  - CONTRIBUTING.md: Developer contribution guidelines
  - SECURITY.md: Security policy and vulnerability reporting
  - tests/README.md: Comprehensive testing guide
  - GITHUB_ISSUES.md: Detailed issue tracking (12 issues)
  - ISSUES_SUMMARY.md: Quick reference and workflow guide
- Modern Python packaging
  - pyproject.toml for project configuration
  - Separate requirements-dev.txt for development dependencies
- Issue creation automation
  - create_issues.py script for bulk issue creation
  - Pre-written detailed issues ready to publish

### Changed
- **[SECURITY]** Updated PyQt5 from 5.15.7 to 5.15.11
  - Addresses Qt framework vulnerabilities (CVE-2024-30161, CVE-2024-38394)
  - PyQt5-Qt5 5.15.18 includes framework-level security fixes
  - Note: PyQt5 5.15.18 not available on PyPI, using latest compatible version
- Updated core dependencies for security and compatibility
  - NumPy: 1.22.0 → 1.26.4
  - SciPy: 1.8.1 → 1.14.1
  - Numba: 0.55.2 → 0.60.0
  - llvmlite: 0.38.1 → 0.43.0
  - pyqtgraph: 0.12.4 → 0.13.7
- Reformatted codebase with Ruff formatter
  - Consistent code style across all modules
  - Auto-fixed 55+ linting issues
  - Improved import organization

### Fixed
- **[SECURITY]** Path traversal vulnerability in sardata.py
  - Added path normalization with os.path.abspath()
  - Validate directory existence before processing
  - Better exception types (ValueError, FileNotFoundError vs generic Exception)
- **[SECURITY]** File size validation in binary file loading
  - Added 10 GB maximum file size limit (DoS prevention)
  - Validate expected vs actual file sizes
  - Check for empty files before processing
  - Proper EOFError handling for truncated files
- **[SECURITY]** Data dimension validation
  - Verify range-compressed data dimensions match expected values
  - Flight path array dimension validation
- Error handling improvements in sardata.py
  - Clear, specific error messages for debugging
  - Proper exception propagation

### Security
- Addressed 2 Critical CVEs in PyQt5/Qt framework
- Implemented automated dependency vulnerability scanning (Dependabot)
- Added security-focused test suite for file I/O operations
- Documented security policy and vulnerability reporting process

## [0.1.0] - 2022 (Estimated)

### Added
- Initial release of SAR Simulator
- FMCW radar signal simulation based on algorithmic scene descriptions
- Range compression using matched filtering
- Azimuth compression using backprojection
- GPU acceleration support via Numba/CUDA
- Interactive PyQt5-based GUI
  - Real-time parameter adjustment
  - Live preview graphs
  - Background simulation execution
- Command-line scripting support
  - --do and --do-file for batch processing
  - Parameter modification via script commands
  - Export capabilities (NumPy arrays)
- SARDATA file format support
  - Custom binary format for radar data
  - Configuration file (INI format)
  - Flight path data storage
- Scene generation
  - Simple reflector models
  - Default test scenes
  - Reflector array generation
- Autofocus functionality (PAFO algorithm)
- Flight path distortion simulation
- Multiple windowing functions (Rect, Hann, Hamming, Tukey, Blackman)
- Comprehensive parameter management system
- Performance profiling utilities

### Documentation
- README with installation and usage instructions
- SARDATA file format specification
- Citation information for academic use
- Screenshot examples

---

## Migration Notes

### Upgrading to Unreleased Version

**Python Environment:**
```bash
# Recommended: Use virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install updated dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

**Testing:**
```bash
# Run test suite to verify installation
pytest tests/unit/ -v

# Check test coverage
pytest --cov=sarsim --cov-report=html
```

**Security Notes:**
- PyQt5 updated to latest available version (5.15.11)
- Qt framework updated to 5.15.18 (via PyQt5-Qt5)
- Review SECURITY.md for vulnerability reporting process
- File size limits now enforced (10 GB maximum)

**Breaking Changes:**
- None - this release maintains backward compatibility
- All existing .sardata files and scripts should work unchanged

---

## Links

- [Repository](https://github.com/montge/sar-sim)
- [Issue Tracker](https://github.com/montge/sar-sim/issues)
- [Assessment Report](ASSESSMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

---

## Versioning Strategy

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible new features
- **PATCH**: Backwards-compatible bug fixes

Security updates are released as PATCH versions and clearly marked with `[SECURITY]` in the changelog.
