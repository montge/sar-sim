# GitHub Issues to Create

This file contains all the GitHub issues that should be created to track the work identified in the repository assessment. Copy each issue and create it on GitHub.

---

## Issue #1: [SECURITY] Update PyQt5 to fix critical CVEs

**Labels**: `security`, `critical`, `dependencies`
**Priority**: CRITICAL 🔴
**Effort**: 2-4 hours

### Description
PyQt5 5.15.7 has multiple critical security vulnerabilities that need immediate attention.

### Security Issues

**CVE-2024-30161 (CVSS 9.8 - Critical)**
- **Component**: QAbstractOAuth in Qt Network Authorization
- **Issue**: Uses only time to seed PRNG, resulting in guessable values
- **Impact**: High - Potential security bypass if OAuth features are used
- **Affected Versions**: < 5.15.17

**CVE-2024-38394 (CVSS 8.6 - High)**
- **Component**: HTTP2 implementation
- **Issue**: Security-relevant code may execute too early on established connections
- **Impact**: Medium-High - Depends on HTTP2 usage
- **Affected Versions**: < 5.15.18

### Current State
- Current version: `PyQt5==5.15.7`
- Required version: `PyQt5>=5.15.18`

### Solution
The `pyproject.toml` file has already been updated with the correct version requirement. Need to:

1. Update `requirements.txt`:
   ```
   PyQt5==5.15.18
   PyQt5-Qt5==5.15.2
   PyQt5-sip==12.11.0
   ```

2. Test the application with updated dependencies:
   ```bash
   pip install --upgrade PyQt5
   python3 -m sarsim --gui
   ```

3. Verify all GUI functionality works correctly

4. Run any existing tests (once implemented)

### Acceptance Criteria
- [ ] `requirements.txt` updated to PyQt5>=5.15.18
- [ ] Application tested with new PyQt5 version
- [ ] GUI launches without errors
- [ ] All GUI functionality verified working
- [ ] No regression in existing features
- [ ] Documentation updated if needed

### Related
- See `ASSESSMENT.md` Section 1.1 for full security analysis
- Related to dependency scanning issue

---

## Issue #2: [SECURITY] Set up automated dependency vulnerability scanning

**Labels**: `security`, `high`, `ci/cd`, `automation`
**Priority**: HIGH 🟡
**Effort**: 4-6 hours

### Description
Implement automated scanning for known vulnerabilities in project dependencies to catch security issues early.

### Problem
Currently, there is no automated process to detect when dependencies have known security vulnerabilities. This led to PyQt5 CVEs going unnoticed.

### Solution
Implement multiple layers of dependency scanning:

1. **pip-audit** (already configured in CI):
   ```bash
   pip install pip-audit
   pip-audit --requirement requirements.txt
   ```

2. **GitHub Dependabot**:
   - Enable in repository settings
   - Configure `.github/dependabot.yml`
   - Auto-creates PRs for dependency updates

3. **Safety** (alternative/additional):
   ```bash
   pip install safety
   safety check --file requirements.txt
   ```

### Implementation Steps

1. Create `.github/dependabot.yml`:
   ```yaml
   version: 2
   updates:
     - package-ecosystem: "pip"
       directory: "/"
       schedule:
         interval: "weekly"
       open-pull-requests-limit: 10
   ```

2. Verify pip-audit in CI (already in `.github/workflows/tests.yml`)

3. Add security check to pre-commit hooks (optional):
   ```yaml
   - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
     rev: v1.3.1
     hooks:
       - id: python-safety-dependencies-check
   ```

4. Document process in `SECURITY.md`

### Acceptance Criteria
- [ ] Dependabot enabled and configured
- [ ] pip-audit running in CI
- [ ] First dependency scan completed
- [ ] Process documented
- [ ] Team notified of how to respond to alerts

### Related
- Directly addresses PyQt5 vulnerability issue
- See `ASSESSMENT.md` Section 1.4

---

## Issue #3: [TESTING] Create core unit test suite (Phase 1: 40% coverage)

**Labels**: `testing`, `high`, `quality`
**Priority**: HIGH 🟡
**Effort**: 16-24 hours

### Description
Create initial unit test suite covering core functionality with target of 40% code coverage.

### Current State
- Test coverage: 0%
- No test infrastructure existed (now added)
- 2 sample test files created (siunits, operations)

### Goal
Achieve 40% code coverage by testing core modules and critical functions.

### Priority Test Modules

1. **sarsim/siunits.py** ✅ (sample tests exist)
   - SI unit parsing
   - SI unit formatting
   - Range validation

2. **sarsim/operations.py** ✅ (sample tests exist)
   - Window functions (Rect, Hann, Hamming, Tukey, Blackman)
   - Window parameter validation

3. **sarsim/simstate.py** (NEW)
   - Parameter creation and validation
   - Type conversions
   - Serialization/deserialization
   - `read_from_file()` and `write_to_file()`

4. **sarsim/simscene.py** (NEW)
   - Reflector creation
   - Scene creation
   - Default scene validation

5. **sarsim/profiling.py** (NEW)
   - TimeStamper functionality
   - tic/toc operations

### Implementation Plan

1. Expand existing tests in `test_siunits.py` and `test_operations.py`

2. Create `test_simstate.py`:
   ```python
   - test_parameter_creation()
   - test_parameter_validation()
   - test_type_conversions()
   - test_serialize_deserialize()
   - test_invalid_values()
   ```

3. Create `test_simscene.py`:
   ```python
   - test_reflector_creation()
   - test_default_scene()
   - test_scene_validation()
   ```

4. Create `test_profiling.py`:
   ```python
   - test_timestamper_basic()
   - test_tic_toc()
   - test_multiple_timings()
   ```

5. Add fixtures to `conftest.py` as needed

### Running Tests
```bash
pytest --cov=sarsim --cov-report=html --cov-report=term
```

### Acceptance Criteria
- [ ] All priority modules have tests
- [ ] Code coverage >= 40%
- [ ] All tests pass
- [ ] Tests run in CI
- [ ] Coverage report generated
- [ ] No critical code paths untested

### Related
- See `ASSESSMENT.md` Section 2.4 for detailed test priorities
- Related to CI/CD setup issue

---

## Issue #4: [TESTING] Add integration tests for simulation pipeline

**Labels**: `testing`, `high`, `integration`
**Priority**: HIGH 🟡
**Effort**: 12-16 hours

### Description
Create integration tests that validate the complete simulation pipeline end-to-end.

### Current State
- No integration tests exist
- Need to test interaction between modules
- Need to validate full workflows

### Test Scenarios

1. **Complete FMCW Simulation Pipeline**
   ```python
   def test_full_fmcw_simulation():
       # Create state and scene
       # Run FMCW simulation
       # Verify range compression
       # Verify azimuth compression
       # Check output shapes and values
   ```

2. **File I/O Pipeline**
   ```python
   def test_load_process_sardata():
       # Load sample .sardata file
       # Process through pipeline
       # Verify results
   ```

3. **Parameter Change Workflow**
   ```python
   def test_parameter_modification():
       # Load default state
       # Modify parameters
       # Run simulation
       # Verify changes reflected in output
   ```

4. **GPU vs CPU Comparison** (if GPU available)
   ```python
   def test_gpu_cpu_equivalence():
       # Run same simulation on GPU and CPU
       # Compare results (should be nearly identical)
   ```

5. **Scripting Command Pipeline**
   ```python
   def test_scripting_workflow():
       # Execute series of scripting commands
       # Verify state changes
       # Verify outputs
   ```

### Test Data Requirements

1. Create `tests/fixtures/test_data/`:
   - Sample `.sardata` directory with minimal data
   - Sample script files (`.do`)
   - Expected output files for comparison

2. Create test data generators:
   ```python
   def create_simple_test_scene()
   def create_minimal_sardata()
   ```

### Implementation Steps

1. Create `tests/integration/` directory

2. Create `test_simulation_pipeline.py`

3. Create `test_file_io_pipeline.py`

4. Create test fixtures and sample data

5. Add integration test marker:
   ```python
   @pytest.mark.integration
   ```

6. Update CI to run integration tests

### Acceptance Criteria
- [ ] 5+ integration test scenarios implemented
- [ ] Test data fixtures created
- [ ] All integration tests pass
- [ ] Integration tests run in CI (may be slower)
- [ ] GPU tests skip gracefully if no GPU available
- [ ] Clear documentation of test scenarios

### Related
- Builds on unit test foundation (Issue #3)
- See `ASSESSMENT.md` Section 2.3

---

## Issue #5: [CI/CD] Enable and configure GitHub Actions workflows

**Labels**: `ci/cd`, `high`, `automation`
**Priority**: HIGH 🟡
**Effort**: 2-4 hours

### Description
Enable the GitHub Actions workflows that have been created for automated testing and security scanning.

### Current State
- Workflows created in `.github/workflows/`:
  - `tests.yml` - Run tests on push/PR
  - `codeql.yml` - Security scanning
- Not yet enabled/verified

### Tasks

1. **Verify Test Workflow** (`.github/workflows/tests.yml`):
   - Runs on push to main/develop
   - Runs on PRs
   - Tests Python 3.8, 3.9, 3.10, 3.11
   - Runs linting (Ruff)
   - Runs type checking (MyPy)
   - Runs tests with coverage
   - Uploads to Codecov

2. **Verify Security Workflow** (`.github/workflows/codeql.yml`):
   - Runs on push to main/develop
   - Runs on PRs
   - Runs weekly on schedule
   - Performs CodeQL analysis

3. **Set up Codecov**:
   - Sign up at https://codecov.io
   - Add repository
   - Get Codecov token
   - Add as GitHub secret: `CODECOV_TOKEN`
   - Update README with coverage badge

4. **Configure Branch Protection** (optional):
   - Require CI to pass before merge
   - Require code reviews
   - Prevent force pushes

### Implementation Steps

1. Push workflows to main branch (merge current PR)

2. Verify first workflow run:
   ```bash
   # Push a commit and watch actions
   git push origin main
   # Go to: https://github.com/montge/sar-sim/actions
   ```

3. Set up Codecov:
   - Visit https://codecov.io/gh/montge/sar-sim
   - Add `CODECOV_TOKEN` to repository secrets
   - Verify coverage uploads

4. Add status badges to README.md:
   ```markdown
   ![Tests](https://github.com/montge/sar-sim/workflows/Tests/badge.svg)
   ![Coverage](https://codecov.io/gh/montge/sar-sim/branch/main/graph/badge.svg)
   ![CodeQL](https://github.com/montge/sar-sim/workflows/CodeQL/badge.svg)
   ```

### Acceptance Criteria
- [ ] Tests workflow runs successfully
- [ ] CodeQL workflow runs successfully
- [ ] Codecov configured and receiving data
- [ ] Status badges added to README
- [ ] Documentation updated with CI information
- [ ] Team notified of CI setup

### Related
- Requires tests to be written (Issue #3, #4)
- See `ASSESSMENT.md` Section 5.2

---

## Issue #6: [CODE QUALITY] Set up Ruff linter and formatter

**Labels**: `code-quality`, `medium`, `tooling`
**Priority**: MEDIUM 🟢
**Effort**: 4-6 hours

### Description
Configure and run Ruff linter/formatter to establish consistent code style and catch common issues.

### Current State
- Ruff configured in `pyproject.toml`
- Pre-commit hooks configured
- Not yet run on codebase

### Why Ruff?
- Fast (written in Rust, 10-100x faster than alternatives)
- Replaces multiple tools (flake8, black, isort, pyupgrade)
- Compatible with existing Python tooling
- Used by major projects (FastAPI, Pandas, etc.)

### Configuration
Already in `pyproject.toml`:
```toml
[tool.ruff]
target-version = "py38"
line-length = 120
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
```

### Tasks

1. **Run Ruff Check**:
   ```bash
   ruff check .
   ```
   - Document all issues found
   - Create prioritized fix list

2. **Auto-fix Safe Issues**:
   ```bash
   ruff check --fix .
   ```

3. **Format Code**:
   ```bash
   ruff format .
   ```

4. **Review Manual Fixes**:
   - Address complex linting issues
   - Refactor problematic patterns
   - Document any suppressions needed

5. **Update Pre-commit**:
   ```bash
   pre-commit install
   pre-commit run --all-files
   ```

### Expected Issues

Based on codebase review, expect:
- Import sorting issues
- Line length violations (>120 chars)
- Unused imports
- Undefined names in some areas
- Missing type hints warnings

### Implementation Plan

1. Run initial check and generate report
2. Auto-fix 80%+ of issues
3. Manually fix remaining issues
4. Commit formatted code
5. Enable in CI (already configured)
6. Document process in CONTRIBUTING.md

### Acceptance Criteria
- [ ] Ruff check passes with no errors
- [ ] Code formatted with Ruff
- [ ] Pre-commit hooks working
- [ ] CI enforces Ruff checks
- [ ] Documentation updated
- [ ] Team trained on Ruff usage

### Related
- See `ASSESSMENT.md` Section 4.1
- Complements MyPy setup (Issue #7)

---

## Issue #7: [CODE QUALITY] Implement MyPy type checking

**Labels**: `code-quality`, `medium`, `tooling`, `type-hints`
**Priority**: MEDIUM 🟢
**Effort**: 16-24 hours

### Description
Add type hints throughout the codebase and configure MyPy for static type checking.

### Current State
- MyPy configured in `pyproject.toml`
- Some type hints exist (in simjob.py)
- Most code lacks type annotations
- ~52 functions to annotate

### Benefits
- Catch type errors before runtime
- Improve IDE autocomplete
- Better documentation
- Easier refactoring

### Configuration
Already in `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.8"
disallow_untyped_defs = false  # Start lenient
check_untyped_defs = true
warn_redundant_casts = true
warn_unused_ignores = true
```

### Implementation Strategy

**Phase 1: Low-hanging fruit (Week 1)**
1. Add type hints to simple utility functions:
   - `sarsim/siunits.py`
   - `sarsim/profiling.py`
   - `sarsim/operations.py`

**Phase 2: Core modules (Week 2-3)**
2. Add type hints to core modules:
   - `sarsim/simstate.py`
   - `sarsim/simscene.py`
   - `sarsim/sardata.py`

**Phase 3: Complex modules (Week 3-4)**
3. Add type hints to complex modules:
   - `sarsim/simjob.py` (already has some)
   - `sarsim/commands.py`

**Phase 4: GUI (Optional)**
4. GUI module (lower priority):
   - `sarsim/gui.py` (898 lines, complex PyQt5 code)

### Example Type Hints

Before:
```python
def si_scale_parse(value):
    # Parse value
    return float_value
```

After:
```python
def si_scale_parse(value: str) -> float:
    """Parse SI-scaled string to float value."""
    # Parse value
    return float_value
```

### Tasks

1. **Install MyPy** (already in dev deps):
   ```bash
   pip install mypy
   ```

2. **Run MyPy baseline**:
   ```bash
   mypy sarsim/ --ignore-missing-imports > mypy_baseline.txt
   ```

3. **Add type hints incrementally**:
   - Start with one module at a time
   - Run MyPy after each module
   - Fix errors before moving on

4. **Add stub files for external deps**:
   ```bash
   mypy --install-types
   ```

5. **Increase strictness over time**:
   ```toml
   disallow_untyped_defs = true  # Eventually
   ```

### Acceptance Criteria
- [ ] All public functions have type hints
- [ ] MyPy passes with minimal errors
- [ ] Type stubs for external deps configured
- [ ] CI runs MyPy checks
- [ ] Documentation includes type hints
- [ ] CONTRIBUTING.md updated with type hint guidelines

### Related
- See `ASSESSMENT.md` Section 3.3
- Complements Ruff setup (Issue #6)

---

## Issue #8: [DOCUMENTATION] Set up API documentation with MkDocs

**Labels**: `documentation`, `medium`, `api-docs`
**Priority**: MEDIUM 🟢
**Effort**: 12-16 hours

### Description
Set up automated API documentation using MkDocs to generate comprehensive developer documentation.

### Current State
- No auto-generated API docs
- README has basic usage info
- Some docstrings exist but inconsistent

### Why MkDocs?
- Easy to use and maintain
- Material theme is beautiful and professional
- `mkdocstrings` auto-generates API docs from docstrings
- Can host on GitHub Pages for free
- Used by major projects (FastAPI, etc.)

### Installation
Already in `pyproject.toml`:
```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
    "mkdocstrings[python]>=0.24",
]
```

### Site Structure
```
docs/
├── index.md              # Home page
├── getting-started.md    # Installation and quickstart
├── user-guide/
│   ├── basic-usage.md
│   ├── gui.md
│   ├── scripting.md
│   └── parameters.md
├── api/
│   ├── simjob.md         # Auto-generated
│   ├── simstate.md       # Auto-generated
│   ├── sardata.md        # Auto-generated
│   └── ...
├── development/
│   ├── contributing.md   # Link to CONTRIBUTING.md
│   ├── testing.md
│   └── architecture.md
└── security.md           # Link to SECURITY.md
```

### Implementation Steps

1. **Create mkdocs.yml**:
   ```yaml
   site_name: SAR Simulator
   theme:
     name: material
     palette:
       primary: indigo
   plugins:
     - search
     - mkdocstrings:
         handlers:
           python:
             paths: [sarsim]
   nav:
     - Home: index.md
     - Getting Started: getting-started.md
     - API Reference: api/
   ```

2. **Create docs/ directory structure**

3. **Write initial content**:
   - Convert README sections to docs/
   - Add API reference pages
   - Link existing docs

4. **Improve docstrings**:
   - Use Google or NumPy style
   - Add examples to key functions
   - Document parameters and returns

5. **Set up GitHub Pages**:
   ```bash
   mkdocs gh-deploy
   ```

6. **Add build to CI**:
   ```yaml
   - name: Build docs
     run: mkdocs build --strict
   ```

### Example Docstring
```python
def calculate_range_resolution(bandwidth: float, speed_of_light: float = 3e8) -> float:
    """Calculate the range resolution for FMCW radar.

    The range resolution is determined by the bandwidth of the FMCW sweep.
    A larger bandwidth results in better (smaller) range resolution.

    Args:
        bandwidth: The frequency bandwidth in Hz.
        speed_of_light: Speed of light in m/s. Defaults to 3e8.

    Returns:
        The range resolution in meters.

    Raises:
        ValueError: If bandwidth is not positive.

    Example:
        >>> calculate_range_resolution(5e9)  # 5 GHz bandwidth
        0.03

    References:
        - Richards, M. A. (2014). Fundamentals of Radar Signal Processing.
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be positive")
    return speed_of_light / (2 * bandwidth)
```

### Acceptance Criteria
- [ ] MkDocs configured and builds successfully
- [ ] API documentation auto-generated for all modules
- [ ] Docstrings improved for public APIs
- [ ] Documentation hosted on GitHub Pages
- [ ] CI builds and validates docs
- [ ] README links to full documentation

### Related
- See `ASSESSMENT.md` Section 3
- Requires improved docstrings (Issue #7 helps)

---

## Issue #9: [DOCUMENTATION] Create comprehensive CHANGELOG

**Labels**: `documentation`, `low`, `maintenance`
**Priority**: LOW 🔵
**Effort**: 2-4 hours

### Description
Create and maintain a CHANGELOG.md following the Keep a Changelog format.

### Current State
- No CHANGELOG exists
- Version history not documented
- Changes not tracked

### Format
Follow [Keep a Changelog](https://keepachangelog.com/):
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive testing infrastructure
- GitHub Actions CI/CD workflows
- Security scanning with CodeQL

### Changed
- Updated PyQt5 to 5.15.18 (security fix)

### Fixed
- Fixed potential path traversal in file loading

## [0.1.0] - 2025-11-16

### Added
- Initial release
- FMCW radar simulation
- GPU acceleration support
- GUI interface
- Scripting support
```

### Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

### Tasks

1. Create `CHANGELOG.md`
2. Document current version (0.1.0)
3. Add unreleased section for current work
4. Document recent commits as changelog entries
5. Add to version release process

### Acceptance Criteria
- [ ] CHANGELOG.md created
- [ ] Follows Keep a Changelog format
- [ ] Current version documented
- [ ] Unreleased changes tracked
- [ ] Linked from README

### Related
- See `ASSESSMENT.md` Section 3.3

---

## Issue #10: [TESTING] Add test coverage for file I/O and security

**Labels**: `testing`, `security`, `high`
**Priority**: HIGH 🟡
**Effort**: 8-12 hours

### Description
Create comprehensive tests for file I/O operations, particularly focusing on security-sensitive code paths.

### Current State
- `sardata.py` handles file loading (potential security issues)
- No tests for file parsing
- No tests for malformed input handling
- Path traversal vulnerability identified

### Security Concerns

From `ASSESSMENT.md` Section 1.2:
- Potential path traversal in `import_from_directory()`
- No validation of directory paths
- No file size limits
- Limited error handling in binary file reads

### Test Scenarios

1. **Valid Input Tests**:
   ```python
   def test_load_valid_sardata():
       # Load well-formed .sardata directory
       # Verify all fields parsed correctly

   def test_load_fmcw_binary():
       # Load binary FMCW data
       # Verify correct shape and values

   def test_load_range_compressed():
       # Load range-compressed data
       # Verify complex values
   ```

2. **Invalid Input Tests**:
   ```python
   def test_invalid_directory_path():
       # Test with non-existent path
       # Should raise appropriate exception

   def test_missing_config_file():
       # Test directory without params.cfg
       # Should handle gracefully

   def test_malformed_config():
       # Test with invalid INI format
       # Should not crash

   def test_corrupted_binary_file():
       # Test with truncated/corrupted .bin
       # Should handle gracefully
   ```

3. **Security Tests**:
   ```python
   def test_path_traversal_prevention():
       # Test with paths like "../../../etc/passwd"
       # Should be rejected or sanitized

   def test_large_file_handling():
       # Test with very large files
       # Should have size limits or stream

   def test_symlink_handling():
       # Test with symlinks in .sardata
       # Should handle safely
   ```

4. **Edge Cases**:
   ```python
   def test_empty_files():
   def test_zero_length_arrays():
   def test_special_characters_in_paths():
   def test_unicode_in_config():
   ```

### Test Fixtures

Create in `tests/fixtures/`:
```
test_data/
├── valid_simple.sardata/
│   ├── params.cfg
│   └── fmcw.bin
├── valid_range_compressed.sardata/
│   ├── params.cfg
│   └── range_comp.bin
├── invalid_missing_cfg.sardata/
│   └── fmcw.bin
├── invalid_corrupted.sardata/
│   ├── params.cfg
│   └── corrupted.bin
└── malicious_paths.sardata/
    └── ...
```

### Security Improvements

While testing, also implement:
1. Path validation/sanitization
2. File size checks
3. Better error handling
4. Input validation

Example fix:
```python
@staticmethod
def import_from_directory(directory: str) -> 'SarData':
    # Validate and sanitize path
    directory = os.path.abspath(directory)
    if not directory.endswith('.sardata'):
        raise ValueError("Directory must end with .sardata")
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Continue with loading...
```

### Acceptance Criteria
- [ ] 20+ test cases for file I/O
- [ ] All security scenarios tested
- [ ] Test fixtures created
- [ ] Path validation implemented
- [ ] File size limits added
- [ ] Error handling improved
- [ ] All tests passing
- [ ] Security improvements documented

### Related
- See `ASSESSMENT.md` Section 1.2 (Security)
- Related to Issue #1 (security)
- Part of Issue #3 (core testing)

---

## Issue #11: [TESTING] Add GPU/CUDA test coverage

**Labels**: `testing`, `medium`, `gpu`, `cuda`
**Priority**: MEDIUM 🟢
**Effort**: 8-12 hours

### Description
Create tests for GPU/CUDA code paths, ensuring CUDA kernels work correctly and match CPU results.

### Current State
- CUDA code in `simjob.py` (azimuth compression, autofocus)
- No tests for GPU code paths
- No CPU vs GPU equivalence testing

### Challenges
- CI environments typically don't have GPUs
- Need to test both GPU and non-GPU code paths
- Need to verify GPU results match CPU results

### Test Strategy

1. **Conditional GPU Tests**:
   ```python
   import pytest
   from sarsim.simjob import CUDA_NUMBA_AVAILABLE

   @pytest.mark.skipif(not CUDA_NUMBA_AVAILABLE, reason="CUDA not available")
   def test_gpu_azimuth_compression():
       # Test GPU kernel
       pass

   @pytest.mark.gpu
   def test_gpu_kernel_accuracy():
       # Compare GPU vs CPU results
       pass
   ```

2. **CPU/GPU Equivalence Tests**:
   ```python
   @pytest.mark.skipif(not CUDA_NUMBA_AVAILABLE, reason="CUDA not available")
   def test_cpu_gpu_equivalence():
       # Run same operation on CPU and GPU
       cpu_result = run_on_cpu(data)
       gpu_result = run_on_gpu(data)

       # Should be nearly identical (allow for float precision)
       np.testing.assert_allclose(cpu_result, gpu_result, rtol=1e-5)
   ```

### Test Cases

1. **Azimuth Compression**:
   - `test_azimuth_compression_cpu()`
   - `test_azimuth_compression_gpu()` (skip if no GPU)
   - `test_azimuth_compression_equivalence()` (CPU vs GPU)
   - `test_azimuth_compression_performance()` (GPU should be faster)

2. **Autofocus PAFO**:
   - `test_autofocus_cpu()`
   - `test_autofocus_gpu()` (skip if no GPU)
   - `test_autofocus_equivalence()`
   - `test_pafo_cost_function()`

3. **GPU Utilities**:
   - `test_cuda_memory_management()`
   - `test_gpu_device_selection()`
   - `test_gpu_fallback_to_cpu()`

4. **Edge Cases**:
   - `test_large_dataset_gpu()` (memory limits)
   - `test_concurrent_gpu_operations()`
   - `test_gpu_error_handling()`

### Test Fixtures

```python
@pytest.fixture
def gpu_test_data():
    """Generate test data suitable for GPU testing."""
    return {
        'rc_lines': np.random.randn(100, 512) + 1j * np.random.randn(100, 512),
        'flight_path': create_simple_flight_path(),
        'state': create_test_state(),
    }

@pytest.fixture(scope="session")
def gpu_available():
    """Check if GPU is available for testing."""
    return CUDA_NUMBA_AVAILABLE
```

### Performance Benchmarks

```python
@pytest.mark.benchmark
@pytest.mark.skipif(not CUDA_NUMBA_AVAILABLE, reason="CUDA not available")
def test_gpu_speedup(benchmark):
    """Benchmark GPU vs CPU performance."""

    # GPU should be significantly faster
    gpu_time = benchmark(run_on_gpu, large_dataset)
    cpu_time = time_function(run_on_cpu, large_dataset)

    speedup = cpu_time / gpu_time
    assert speedup > 5.0, f"GPU speedup only {speedup}x, expected >5x"
```

### CI Configuration

Update `.github/workflows/tests.yml`:
```yaml
- name: Run GPU tests
  run: pytest -m gpu
  continue-on-error: true  # Don't fail if no GPU
```

### Local Testing

For developers with CUDA:
```bash
# Run all tests including GPU
pytest

# Run only GPU tests
pytest -m gpu

# Run with GPU benchmarks
pytest -m benchmark
```

### Documentation

Create `docs/testing-gpu.md`:
- How to set up CUDA for testing
- How to run GPU tests
- How to interpret GPU test results
- Troubleshooting GPU test failures

### Acceptance Criteria
- [ ] GPU tests created for all CUDA kernels
- [ ] CPU/GPU equivalence tests passing
- [ ] Tests skip gracefully without GPU
- [ ] Performance benchmarks added
- [ ] CI configured to handle GPU tests
- [ ] Documentation for GPU testing complete

### Related
- See `ASSESSMENT.md` Section 2.4
- Related to core testing (Issue #3, #4)

---

## Issue #12: [INFRASTRUCTURE] Update requirements.txt and add requirements-dev.txt

**Labels**: `dependencies`, `medium`, `infrastructure`
**Priority**: MEDIUM 🟢
**Effort**: 2-3 hours

### Description
Update `requirements.txt` with security fixes and create separate `requirements-dev.txt` for development dependencies.

### Current State
- `requirements.txt` has pinned versions from 2-3 years ago
- No separation of prod vs dev dependencies
- `pyproject.toml` has updated versions but `requirements.txt` doesn't match

### Tasks

1. **Update requirements.txt**:
   ```
   llvmlite==0.43.0      # Updated from 0.38.1
   numba==0.60.0         # Updated from 0.55.2
   numpy==1.26.4         # Updated from 1.22.0
   PyGraph==0.2.1        # No update needed
   PyQt5==5.15.18        # SECURITY UPDATE from 5.15.7
   PyQt5-Qt5==5.15.2     # Keep
   PyQt5-sip==12.11.0    # Keep
   pyqtgraph==0.13.7     # Updated from 0.12.4
   scipy==1.14.1         # Updated from 1.8.1
   ```

2. **Create requirements-dev.txt**:
   ```
   -r requirements.txt   # Include base requirements

   # Testing
   pytest>=7.0
   pytest-cov>=4.0
   pytest-xdist>=3.0
   pytest-benchmark>=4.0

   # Code Quality
   ruff>=0.1.0
   mypy>=1.0
   pre-commit>=3.0

   # Security
   pip-audit>=2.0
   safety>=3.0

   # Documentation
   mkdocs>=1.5
   mkdocs-material>=9.0
   mkdocstrings[python]>=0.24
   ```

3. **Test Updated Dependencies**:
   ```bash
   # Fresh environment
   python3 -m venv test-env
   source test-env/bin/activate

   # Install and test
   pip install -r requirements.txt
   python3 -m sarsim --gui

   # Test all features
   # - GUI launches
   # - Simulation runs
   # - File loading works
   # - No import errors
   ```

4. **Update Documentation**:
   - Update README.md installation instructions
   - Update CONTRIBUTING.md
   - Note any breaking changes

5. **Consider Dependency Locking**:
   ```bash
   # Generate lockfile
   pip freeze > requirements-lock.txt
   ```

### Breaking Changes?

Test for potential breaking changes:
- NumPy 1.22→1.26: Check array operations
- SciPy 1.8→1.14: Check signal processing functions
- Numba 0.55→0.60: Check CUDA kernels
- PyQt5 5.15.7→5.15.18: Check GUI components

### Acceptance Criteria
- [ ] `requirements.txt` updated with tested versions
- [ ] `requirements-dev.txt` created
- [ ] All dependencies tested and working
- [ ] No regression in functionality
- [ ] Documentation updated
- [ ] PyQt5 security issues resolved
- [ ] CI uses updated dependencies

### Related
- CRITICAL: Issue #1 (PyQt5 security)
- See `ASSESSMENT.md` Section 1.1

---

## Summary

Total issues created: 12

### Priority Breakdown
- **CRITICAL (1)**: Issue #1 - PyQt5 security update
- **HIGH (5)**: Issues #2, #3, #4, #5, #10 - Security scanning, testing, CI/CD
- **MEDIUM (5)**: Issues #6, #7, #8, #11, #12 - Code quality, docs, GPU tests
- **LOW (1)**: Issue #9 - CHANGELOG

### Effort Estimate
- Total: 90-136 hours
- Critical path: ~30-40 hours (security + basic testing + CI)

### Recommended Order
1. Issue #1 - PyQt5 update (CRITICAL)
2. Issue #12 - Update requirements.txt
3. Issue #3 - Core unit tests
4. Issue #10 - File I/O security tests
5. Issue #5 - Enable CI/CD
6. Issue #2 - Dependency scanning
7. Issue #6 - Ruff linting
8. Issue #4 - Integration tests
9. Issue #7 - MyPy type checking
10. Issue #11 - GPU tests
11. Issue #8 - API documentation
12. Issue #9 - CHANGELOG
