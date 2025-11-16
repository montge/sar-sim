#!/usr/bin/env python3
"""
Script to create GitHub issues for SAR Simulator project.

Usage:
    python create_issues.py <github_token>

Get a token from: https://github.com/settings/tokens
Requires: repo scope for creating issues
"""

import sys
import requests
import json
from typing import Dict, List

# GitHub repository
REPO_OWNER = "montge"
REPO_NAME = "sar-sim"
API_BASE = "https://api.github.com"


def create_issue(token: str, title: str, body: str, labels: List[str]) -> Dict:
    """Create a GitHub issue via the API."""
    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/issues"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    data = {
        "title": title,
        "body": body,
        "labels": labels,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        issue = response.json()
        print(f"✓ Created issue #{issue['number']}: {title}")
        return issue
    else:
        print(f"✗ Failed to create issue: {title}")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")
        return {}


def main():
    if len(sys.argv) < 2:
        print("Usage: python create_issues.py <github_token>")
        print("\nGet a token from: https://github.com/settings/tokens")
        print("Required scope: repo (or public_repo for public repos)")
        sys.exit(1)

    token = sys.argv[1]

    # Define all issues to create
    issues = [
        {
            "title": "[SECURITY] Update PyQt5 to fix critical CVEs",
            "labels": ["security", "critical", "dependencies"],
            "body": """## Priority: CRITICAL 🔴

## Description
PyQt5 5.15.7 has multiple critical security vulnerabilities that need immediate attention.

## Security Issues

### CVE-2024-30161 (CVSS 9.8 - Critical)
- **Component**: QAbstractOAuth in Qt Network Authorization
- **Issue**: Uses only time to seed PRNG, resulting in guessable values
- **Impact**: High - Potential security bypass if OAuth features are used
- **Affected Versions**: < 5.15.17

### CVE-2024-38394 (CVSS 8.6 - High)
- **Component**: HTTP2 implementation
- **Issue**: Security-relevant code may execute too early on established connections
- **Impact**: Medium-High - Depends on HTTP2 usage
- **Affected Versions**: < 5.15.18

## Current State
- Current version: `PyQt5==5.15.7`
- Required version: `PyQt5>=5.15.18`

## Solution
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

## Acceptance Criteria
- [ ] `requirements.txt` updated to PyQt5>=5.15.18
- [ ] Application tested with new PyQt5 version
- [ ] GUI launches without errors
- [ ] All GUI functionality verified working
- [ ] No regression in existing features
- [ ] Documentation updated if needed

## Related
- See `ASSESSMENT.md` Section 1.1 for full security analysis

## Estimated Effort
2-4 hours (testing + verification)
"""
        },
        {
            "title": "[SECURITY] Set up automated dependency vulnerability scanning",
            "labels": ["security", "high", "ci/cd", "automation"],
            "body": """## Priority: HIGH 🟡

## Description
Implement automated scanning for known vulnerabilities in project dependencies to catch security issues early.

## Problem
Currently, there is no automated process to detect when dependencies have known security vulnerabilities. This led to PyQt5 CVEs going unnoticed.

## Solution
Implement multiple layers of dependency scanning:

1. **pip-audit** (already configured in CI)
2. **GitHub Dependabot** (auto-creates PRs for updates)
3. **Safety** (alternative/additional)

## Implementation Steps

1. Create `.github/dependabot.yml`
2. Verify pip-audit in CI (already in `.github/workflows/tests.yml`)
3. Add security check to pre-commit hooks (optional)
4. Document process in `SECURITY.md`

## Acceptance Criteria
- [ ] Dependabot enabled and configured
- [ ] pip-audit running in CI
- [ ] First dependency scan completed
- [ ] Process documented
- [ ] Team notified of how to respond to alerts

## Related
- See `ASSESSMENT.md` Section 1.4

## Estimated Effort
4-6 hours
"""
        },
        {
            "title": "[TESTING] Create core unit test suite (Phase 1: 40% coverage)",
            "labels": ["testing", "high", "quality"],
            "body": """## Priority: HIGH 🟡

## Description
Create initial unit test suite covering core functionality with target of 40% code coverage.

## Current State
- Test coverage: 0%
- Test infrastructure now added
- 2 sample test files created (siunits, operations)

## Goal
Achieve 40% code coverage by testing core modules and critical functions.

## Priority Test Modules

1. **sarsim/siunits.py** ✅ (sample tests exist)
2. **sarsim/operations.py** ✅ (sample tests exist)
3. **sarsim/simstate.py** (NEW - parameter management)
4. **sarsim/simscene.py** (NEW - scene creation)
5. **sarsim/profiling.py** (NEW - timing utilities)

## Running Tests
```bash
pytest --cov=sarsim --cov-report=html --cov-report=term
```

## Acceptance Criteria
- [ ] All priority modules have tests
- [ ] Code coverage >= 40%
- [ ] All tests pass
- [ ] Tests run in CI
- [ ] Coverage report generated
- [ ] No critical code paths untested

## Related
- See `ASSESSMENT.md` Section 2.4 for detailed test priorities

## Estimated Effort
16-24 hours
"""
        },
        {
            "title": "[TESTING] Add integration tests for simulation pipeline",
            "labels": ["testing", "high", "integration"],
            "body": """## Priority: HIGH 🟡

## Description
Create integration tests that validate the complete simulation pipeline end-to-end.

## Test Scenarios

1. Complete FMCW Simulation Pipeline
2. File I/O Pipeline
3. Parameter Change Workflow
4. GPU vs CPU Comparison (if GPU available)
5. Scripting Command Pipeline

## Implementation Steps

1. Create `tests/integration/` directory
2. Create test data fixtures
3. Implement 5+ integration test scenarios
4. Add integration test marker
5. Update CI to run integration tests

## Acceptance Criteria
- [ ] 5+ integration test scenarios implemented
- [ ] Test data fixtures created
- [ ] All integration tests pass
- [ ] Integration tests run in CI
- [ ] GPU tests skip gracefully if no GPU available
- [ ] Clear documentation of test scenarios

## Related
- Builds on unit test foundation
- See `ASSESSMENT.md` Section 2.3

## Estimated Effort
12-16 hours
"""
        },
        {
            "title": "[CI/CD] Enable and configure GitHub Actions workflows",
            "labels": ["ci/cd", "high", "automation"],
            "body": """## Priority: HIGH 🟡

## Description
Enable the GitHub Actions workflows that have been created for automated testing and security scanning.

## Current State
- Workflows created in `.github/workflows/`:
  - `tests.yml` - Run tests on push/PR
  - `codeql.yml` - Security scanning
- Not yet enabled/verified

## Tasks

1. Verify Test Workflow runs successfully
2. Verify Security Workflow runs successfully
3. Set up Codecov for coverage reporting
4. Add status badges to README.md
5. Configure branch protection (optional)

## Acceptance Criteria
- [ ] Tests workflow runs successfully
- [ ] CodeQL workflow runs successfully
- [ ] Codecov configured and receiving data
- [ ] Status badges added to README
- [ ] Documentation updated with CI information
- [ ] Team notified of CI setup

## Related
- Requires tests to be written
- See `ASSESSMENT.md` Section 5.2

## Estimated Effort
2-4 hours
"""
        },
        {
            "title": "[CODE QUALITY] Set up Ruff linter and formatter",
            "labels": ["code-quality", "medium", "tooling"],
            "body": """## Priority: MEDIUM 🟢

## Description
Configure and run Ruff linter/formatter to establish consistent code style and catch common issues.

## Current State
- Ruff configured in `pyproject.toml`
- Pre-commit hooks configured
- Not yet run on codebase

## Tasks

1. Run Ruff check and document issues
2. Auto-fix safe issues: `ruff check --fix .`
3. Format code: `ruff format .`
4. Review and fix manual issues
5. Enable pre-commit hooks
6. Ensure CI enforces checks

## Expected Issues
- Import sorting issues
- Line length violations (>120 chars)
- Unused imports
- Missing type hints warnings

## Acceptance Criteria
- [ ] Ruff check passes with no errors
- [ ] Code formatted with Ruff
- [ ] Pre-commit hooks working
- [ ] CI enforces Ruff checks
- [ ] Documentation updated
- [ ] Team trained on Ruff usage

## Related
- See `ASSESSMENT.md` Section 4.1

## Estimated Effort
4-6 hours
"""
        },
        {
            "title": "[CODE QUALITY] Implement MyPy type checking",
            "labels": ["code-quality", "medium", "tooling", "type-hints"],
            "body": """## Priority: MEDIUM 🟢

## Description
Add type hints throughout the codebase and configure MyPy for static type checking.

## Current State
- MyPy configured in `pyproject.toml`
- Some type hints exist (in simjob.py)
- Most code lacks type annotations
- ~52 functions to annotate

## Implementation Strategy

**Phase 1**: Simple utility functions (siunits, profiling, operations)
**Phase 2**: Core modules (simstate, simscene, sardata)
**Phase 3**: Complex modules (simjob, commands)
**Phase 4**: GUI (optional, lower priority)

## Benefits
- Catch type errors before runtime
- Improve IDE autocomplete
- Better documentation
- Easier refactoring

## Acceptance Criteria
- [ ] All public functions have type hints
- [ ] MyPy passes with minimal errors
- [ ] Type stubs for external deps configured
- [ ] CI runs MyPy checks
- [ ] Documentation includes type hints
- [ ] CONTRIBUTING.md updated with guidelines

## Related
- See `ASSESSMENT.md` Section 3.3

## Estimated Effort
16-24 hours
"""
        },
        {
            "title": "[DOCUMENTATION] Set up API documentation with MkDocs",
            "labels": ["documentation", "medium", "api-docs"],
            "body": """## Priority: MEDIUM 🟢

## Description
Set up automated API documentation using MkDocs to generate comprehensive developer documentation.

## Current State
- No auto-generated API docs
- README has basic usage info
- Some docstrings exist but inconsistent

## Implementation Steps

1. Create `mkdocs.yml` configuration
2. Create docs/ directory structure
3. Write initial content (convert README sections)
4. Improve docstrings (Google or NumPy style)
5. Set up GitHub Pages hosting
6. Add docs build to CI

## Benefits
- Professional documentation site
- Auto-generated API reference
- Easy to maintain and update
- Free hosting on GitHub Pages

## Acceptance Criteria
- [ ] MkDocs configured and builds successfully
- [ ] API documentation auto-generated for all modules
- [ ] Docstrings improved for public APIs
- [ ] Documentation hosted on GitHub Pages
- [ ] CI builds and validates docs
- [ ] README links to full documentation

## Related
- See `ASSESSMENT.md` Section 3

## Estimated Effort
12-16 hours
"""
        },
        {
            "title": "[DOCUMENTATION] Create comprehensive CHANGELOG",
            "labels": ["documentation", "low", "maintenance"],
            "body": """## Priority: LOW 🔵

## Description
Create and maintain a CHANGELOG.md following the Keep a Changelog format.

## Current State
- No CHANGELOG exists
- Version history not documented
- Changes not tracked

## Tasks

1. Create `CHANGELOG.md`
2. Document current version (0.1.0)
3. Add unreleased section for current work
4. Document recent commits as changelog entries
5. Add to version release process

## Format
Follow [Keep a Changelog](https://keepachangelog.com/)

## Acceptance Criteria
- [ ] CHANGELOG.md created
- [ ] Follows Keep a Changelog format
- [ ] Current version documented
- [ ] Unreleased changes tracked
- [ ] Linked from README

## Estimated Effort
2-4 hours
"""
        },
        {
            "title": "[TESTING] Add test coverage for file I/O and security",
            "labels": ["testing", "security", "high"],
            "body": """## Priority: HIGH 🟡

## Description
Create comprehensive tests for file I/O operations, particularly focusing on security-sensitive code paths.

## Security Concerns
- Potential path traversal in `import_from_directory()`
- No validation of directory paths
- No file size limits
- Limited error handling in binary file reads

## Test Scenarios

1. **Valid Input Tests**: Load well-formed files
2. **Invalid Input Tests**: Missing files, malformed configs
3. **Security Tests**: Path traversal, large files, symlinks
4. **Edge Cases**: Empty files, unicode, special characters

## Security Improvements
While testing, also implement:
- Path validation/sanitization
- File size checks
- Better error handling
- Input validation

## Acceptance Criteria
- [ ] 20+ test cases for file I/O
- [ ] All security scenarios tested
- [ ] Test fixtures created
- [ ] Path validation implemented
- [ ] File size limits added
- [ ] Error handling improved
- [ ] All tests passing
- [ ] Security improvements documented

## Related
- See `ASSESSMENT.md` Section 1.2

## Estimated Effort
8-12 hours
"""
        },
        {
            "title": "[TESTING] Add GPU/CUDA test coverage",
            "labels": ["testing", "medium", "gpu", "cuda"],
            "body": """## Priority: MEDIUM 🟢

## Description
Create tests for GPU/CUDA code paths, ensuring CUDA kernels work correctly and match CPU results.

## Current State
- CUDA code in simjob.py (azimuth compression, autofocus)
- No tests for GPU code paths
- No CPU vs GPU equivalence testing

## Test Cases

1. **Azimuth Compression**: CPU, GPU, equivalence, performance
2. **Autofocus PAFO**: CPU, GPU, equivalence
3. **GPU Utilities**: Memory management, device selection, fallback
4. **Edge Cases**: Large datasets, concurrent ops, error handling

## CI Configuration
Tests should skip gracefully if no GPU available.

## Acceptance Criteria
- [ ] GPU tests created for all CUDA kernels
- [ ] CPU/GPU equivalence tests passing
- [ ] Tests skip gracefully without GPU
- [ ] Performance benchmarks added
- [ ] CI configured to handle GPU tests
- [ ] Documentation for GPU testing complete

## Related
- See `ASSESSMENT.md` Section 2.4

## Estimated Effort
8-12 hours
"""
        },
        {
            "title": "[INFRASTRUCTURE] Update requirements.txt and add requirements-dev.txt",
            "labels": ["dependencies", "medium", "infrastructure"],
            "body": """## Priority: MEDIUM 🟢

## Description
Update `requirements.txt` with security fixes and create separate `requirements-dev.txt` for development dependencies.

## Current State
- `requirements.txt` has pinned versions from 2-3 years ago
- No separation of prod vs dev dependencies
- `pyproject.toml` has updated versions but `requirements.txt` doesn't match

## Tasks

1. Update `requirements.txt` with newer, tested versions
2. Create `requirements-dev.txt` with dev/test dependencies
3. Test updated dependencies thoroughly
4. Update documentation
5. Consider adding `requirements-lock.txt`

## Key Updates
- PyQt5: 5.15.7 → 5.15.18 (SECURITY)
- NumPy: 1.22.0 → 1.26.4
- SciPy: 1.8.1 → 1.14.1
- Numba: 0.55.2 → 0.60.0

## Acceptance Criteria
- [ ] `requirements.txt` updated with tested versions
- [ ] `requirements-dev.txt` created
- [ ] All dependencies tested and working
- [ ] No regression in functionality
- [ ] Documentation updated
- [ ] PyQt5 security issues resolved
- [ ] CI uses updated dependencies

## Related
- CRITICAL: PyQt5 security update
- See `ASSESSMENT.md` Section 1.1

## Estimated Effort
2-3 hours
"""
        },
    ]

    print(f"\nCreating {len(issues)} GitHub issues for {REPO_OWNER}/{REPO_NAME}...\n")

    created_issues = []
    for issue in issues:
        result = create_issue(token, issue["title"], issue["body"], issue["labels"])
        if result:
            created_issues.append(result)

    print(f"\n{'='*60}")
    print(f"Successfully created {len(created_issues)}/{len(issues)} issues")
    print(f"{'='*60}\n")

    if created_issues:
        print("Created issues:")
        for issue in created_issues:
            print(f"  #{issue['number']}: {issue['title']}")
            print(f"    {issue['html_url']}")

    print("\nView all issues at:")
    print(f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues")


if __name__ == "__main__":
    main()
