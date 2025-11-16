# SAR Simulator

[![Tests](https://github.com/montge/sar-sim/actions/workflows/tests.yml/badge.svg)](https://github.com/montge/sar-sim/actions/workflows/tests.yml)
[![CodeQL](https://github.com/montge/sar-sim/actions/workflows/codeql.yml/badge.svg)](https://github.com/montge/sar-sim/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/montge/sar-sim/branch/main/graph/badge.svg)](https://codecov.io/gh/montge/sar-sim)
[![Python 3.10-3.13](https://img.shields.io/badge/python-3.10--3.13-blue.svg)](https://www.python.org/downloads/)

The SAR Simulator is a graphical tool for FMCW radar simulation and interactive exploration of parameters.
It can simulate FMCW radar signals based on an algorithmic scene description.
The resulting signal is then range-compressed and and image is reconstructed using backprojection (azimuth compression).
Various parameters can be changed using the GUI, allowing for interactive exploration.

Optionally existing signals (before or after range compression) can be loaded and processed with the simulator.
When available, GPU acceleration (using [Numba](https://numba.pydata.org/)/CUDA) is used.

This tool was created by the Architectures and Systems Group of the Institute of Microelectronic Systems ([IMS/AS](https://www.ims.uni-hannover.de/de/institut/architekturen-und-systeme/)) at the [Leibniz University](https://www.uni-hannover.de) in Germany.

![Screenshot](/doc/screenshot_1.png?raw=true)

## Documentation

- 📋 [CHANGELOG](CHANGELOG.md) - Release notes and version history
- 🛡️ [SECURITY](SECURITY.md) - Security policy and vulnerability reporting
- 🤝 [CONTRIBUTING](CONTRIBUTING.md) - Guidelines for contributors
- 📊 [ASSESSMENT](ASSESSMENT.md) - Security, testing, and documentation analysis
- 🐛 [Issue Tracker](https://github.com/montge/sar-sim/issues) - Bug reports and feature requests

## Getting Started

### Installation

**Requirements:** Python 3.8 or higher

Create virtual environment (venv) and install requirements:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

For development (includes testing, linting, and documentation tools):

```bash
pip install -r requirements-dev.txt
```

### Running the Simulator

Run as python module (Note: only usable with GUI currently):

```bash
python3 -m sarsim --gui
```

Select parameters on the left, hit RUN SIM on bottom left.
Simulation will be done in background, status at bottom.
Graphs will be updated automatically when done.
See also CLI console output for status and information.
If not using GPU acceleration (CUDA), azimuth compression will take a while.

The SAR Simulator was tested on Ubuntu 20.04 LTS but should work on most Linux distributions, and even on Windows.

## Features

- Exact FMCW Signal generation in phase-space
- Range and Azimuth compression
- Live-Update of preview graphs
- CUDA Acceleration of Azimuth Compression if possible
- Interactive parameter exploration through GUI
- SARDATA file format support for loading/saving radar data
- Autofocus functionality (PAFO algorithm)
- Multiple windowing functions (Rect, Hann, Hamming, Tukey, Blackman)

## Testing

Run the test suite to verify your installation:

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests (fast)
pytest tests/unit/ -v

# Run with coverage report
pytest --cov=sarsim --cov-report=html

# Skip slow integration tests
pytest tests/ -v -m "not slow"
```

See [tests/README.md](tests/README.md) for comprehensive testing documentation.

## Development

### Code Quality Tools

This project uses modern Python development tools:

- **Ruff** - Fast Python linter and formatter
- **MyPy** - Static type checking
- **pytest** - Testing framework with coverage reporting
- **pre-commit** - Git hooks for automated quality checks

Run code quality checks:

```bash
# Format code with Ruff
ruff format .

# Check for linting issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Type checking
mypy sarsim/
```

### Development Tools

- Run `python3 -m sarsim --write-stubs` to enable IDE support for better autocompletion

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for:

- Development setup instructions
- Code style requirements
- Testing guidelines
- Pull request process

For security vulnerabilities, please see our [Security Policy](SECURITY.md).

## Citation

If you use the SAR Simulator in scientific work, please cite our paper "[Interactive synthetic aperture radar simulator generating and visualizing realistic FMCW data](https://ieeexplore.ieee.org/document/10106365)".

```bibtex
@INPROCEEDINGS{fahnemann2022interactive,
  author={Fahnemann, C. and Rother, N. and Blume, H.},
  booktitle={International Conference on Radar Systems (RADAR 2022)}, 
  title={Interactive synthetic aperture radar simulator generating and visualizing realistic FMCW data}, 
  year={2022},
  volume={2022},
  number={},
  pages={725-730},
  doi={10.1049/ICP.2023.1281}}
```
