# Security Policy

## Supported Versions

The SAR Simulator project currently supports the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Known Security Considerations

The SAR Simulator is a scientific computing tool intended for research use. Please be aware of the following security considerations:

### File Loading
- The simulator loads and processes `.sardata` files which may contain binary data
- Only load `.sardata` files from trusted sources
- The file parser does not currently implement strict size limits or sandboxing
- Maliciously crafted files could potentially cause resource exhaustion

### Script Execution
- The `--do` and `--do-file` flags allow executing scripting commands
- Only run scripts from trusted sources
- Commands have limited scope (no direct shell access) but can manipulate file system

### Dependencies
- Several dependencies have known security considerations:
  - PyQt5 < 5.15.18: CVE-2024-30161, CVE-2024-38394
  - Keep all dependencies updated to latest secure versions

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### 1. Do Not Open a Public Issue

Please **do not** report security vulnerabilities through public GitHub issues.

### 2. Contact the Security Team

Send a detailed report to: **ims-as@uni-hannover.de**

Include the following information:
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue and potential attack scenarios

### 3. What to Expect

- **Initial Response**: Within 5 business days, we will acknowledge receipt of your report
- **Assessment**: We will investigate and assess the vulnerability
- **Updates**: We will provide regular updates on our progress
- **Resolution**: Once resolved, we will:
  - Release a security patch
  - Credit you for the discovery (unless you prefer to remain anonymous)
  - Publish a security advisory if appropriate

### 4. Disclosure Policy

- Please give us reasonable time to address the vulnerability before public disclosure
- We aim to resolve critical issues within 90 days
- We will coordinate with you on disclosure timing
- We appreciate coordinated disclosure to protect users

## Security Best Practices for Users

### Installation
```bash
# Always verify package integrity
pip install --upgrade pip
pip install -r requirements.txt

# Use virtual environments
python3 -m venv venv
source venv/bin/activate
```

### Running the Simulator
```bash
# Only load data from trusted sources
python3 -m sarsim --gui  # Interactive mode

# Verify script contents before execution
cat script.do  # Review before running
python3 -m sarsim --do-file script.do
```

### Dependency Security
```bash
# Regularly check for vulnerabilities
pip install pip-audit
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt
```

### GPU Usage
```bash
# If using CUDA, ensure proper permissions
# Run with minimal privileges when possible
python3 -m sarsim --gpu 0
```

## Security Checklist for Contributors

When contributing code, please ensure:

- [ ] Input validation for all external data (files, user input)
- [ ] No hardcoded credentials or sensitive information
- [ ] Proper error handling (avoid exposing sensitive details)
- [ ] Dependencies are up to date
- [ ] Code has been reviewed for common vulnerabilities:
  - [ ] Path traversal
  - [ ] Code injection
  - [ ] Resource exhaustion
  - [ ] Buffer overflows (in CUDA code)
  - [ ] Integer overflows

## Automated Security Scanning

We employ the following security measures:

- **Dependency Scanning**: Automated checks for known vulnerabilities in dependencies
- **Static Analysis**: Code analysis for common security issues
- **Regular Updates**: Dependencies are regularly updated to address security issues

## Security Updates

Security updates will be announced through:
- GitHub Security Advisories
- Release notes
- CHANGELOG.md with `[SECURITY]` prefix

## Known Limitations

The following are known security limitations:

1. **File Parsing**: Limited validation of input file formats
2. **Resource Limits**: No strict memory or CPU usage limits
3. **Script Sandboxing**: Script commands are not sandboxed
4. **GPU Code**: CUDA kernels have minimal input validation

We are working to address these limitations in future releases.

## Security-Related Configuration

### Recommended Security Settings

```python
# In production/untrusted environments, consider:
# 1. File size limits for loaded data
# 2. Timeout limits for long-running operations
# 3. Restricted script command set
# 4. Input sanitization for all file paths
```

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [NumPy Security](https://numpy.org/doc/stable/reference/security.html)

## Contact

For security concerns, contact:
- **Email**: ims-as@uni-hannover.de
- **Institution**: Institute of Microelectronic Systems, Leibniz University Hannover

---

Last Updated: 2025-11-16
