# CUDA GPU Testing Guide

This document explains how to test CUDA GPU code paths in the SAR Simulator.

## Overview

The SAR Simulator includes optional CUDA GPU acceleration for azimuth compression. The test suite includes comprehensive tests for both:
- **CUDA execution paths** (require NVIDIA GPU)
- **CPU fallback paths** (work on any machine)

## Test Organization

### CUDA-Specific Tests (`TestCUDAExecution`)
These tests **only run on machines with CUDA-capable NVIDIA GPUs**. They are automatically skipped on CPU-only machines.

**Location:** `tests/unit/test_simjob.py::TestCUDAExecution`

**Tests included:**
- `test_cuda_device_selection` - Test GPU device selection
- `test_azimuth_compression_cuda_enabled` - Test CUDA azimuth compression
- `test_cuda_vs_cpu_consistency` - Verify CUDA and CPU produce same results
- `test_cuda_single_pulse_mode` - Test single pulse GPU processing
- `test_cuda_with_large_image` - Test large image memory handling
- `test_cuda_full_simulation` - Test full simulation pipeline with GPU
- `test_cuda_with_autofocus` - Test autofocus with GPU acceleration
- `test_cuda_beam_limit_enforcement` - Test beam angle limits on GPU

### CPU Fallback Tests (`TestCUDAFallback`)
These tests **only run when CUDA is NOT available**. They verify CPU fallback works correctly.

**Location:** `tests/unit/test_simjob.py::TestCUDAFallback`

**Tests included:**
- `test_simulation_works_without_cuda` - Verify CPU-only simulation works
- `test_cpu_azimuth_compression_fallback` - Test CPU azimuth compression

## Running Tests

### On CPU-Only Machines (Current System)
```bash
# Run all tests (CUDA tests will be skipped)
pytest tests/unit/test_simjob.py -v

# Run only CPU fallback tests
pytest tests/unit/test_simjob.py::TestCUDAFallback -v

# Expected output:
# - TestCUDAExecution: 8 skipped
# - TestCUDAFallback: 2 passed
```

### On CUDA-Enabled Machines (GPU Required)
```bash
# Run only CUDA tests
pytest tests/unit/test_simjob.py::TestCUDAExecution -v

# Run with verbose CUDA output
CUDA_VISIBLE_DEVICES=0 pytest tests/unit/test_simjob.py::TestCUDAExecution -v -s

# Expected output:
# - TestCUDAExecution: 8 passed
# - TestCUDAFallback: 2 skipped
```

## Requirements for CUDA Testing

### Hardware Requirements
- NVIDIA GPU with CUDA Compute Capability 3.5 or higher
- Minimum 2GB GPU memory (4GB+ recommended)

### Software Requirements
- NVIDIA CUDA Toolkit 11.0 or higher
- Numba with CUDA support: `pip install numba[cuda]`
- CUDA drivers properly installed

### Verifying CUDA Installation
```bash
# Check CUDA availability
python -c "from numba import cuda; print(f'CUDA available: {cuda.is_available()}')"

# Check GPU info
python -c "from numba import cuda; cuda.detect()"
```

## CUDA Test Coverage

The CUDA tests cover the following code paths in `sarsim/simjob.py`:

- **Lines 19-26:** CUDA initialization and error handling
- **Line 54:** `cuda.select_device(gpu_id)` - GPU selection
- **Lines 206-236:** `_ac_kernel` - CUDA kernel definition
- **Lines 289-324:** CUDA GPU memory management and kernel invocation

These lines are **NOT covered on CPU-only machines** and will show as "missing" in coverage reports.

## Expected Coverage

### On CPU-Only Machines
- simjob.py coverage: ~72-73%
- Missing: CUDA-specific code (~90 lines)

### On CUDA-Enabled Machines
- simjob.py coverage: ~85%+ (when CUDA tests pass)
- All code paths covered

## Debugging CUDA Tests

If CUDA tests fail on a GPU machine:

1. **Check CUDA is detected:**
   ```bash
   python -c "from sarsim import simjob; print(f'CUDA: {simjob.CUDA_NUMBA_AVAILABLE}')"
   ```

2. **Run with verbose output:**
   ```bash
   pytest tests/unit/test_simjob.py::TestCUDAExecution::test_cuda_device_selection -v -s
   ```

3. **Check GPU memory:**
   ```bash
   nvidia-smi
   ```

4. **Run single test with full traceback:**
   ```bash
   pytest tests/unit/test_simjob.py::TestCUDAExecution::test_cuda_vs_cpu_consistency -vvs --tb=long
   ```

## Common Issues

### "CUDA not available" on GPU Machine
- Install CUDA toolkit: `conda install cudatoolkit` or download from NVIDIA
- Reinstall numba with CUDA: `pip install --upgrade numba[cuda]`
- Check drivers: `nvidia-smi`

### CUDA Tests Failing with Memory Error
- Reduce image size in tests
- Close other GPU applications
- Check available GPU memory with `nvidia-smi`

### CPU vs CUDA Results Don't Match
- This is expected due to floating-point precision differences
- Tests use `rtol=1e-5, atol=1e-8` tolerance
- GPU and CPU use different precision in some operations

## Adding New CUDA Tests

When adding new CUDA tests:

1. Add to `TestCUDAExecution` class
2. Use `@pytest.mark.skipif(not simjob.CUDA_NUMBA_AVAILABLE, ...)` decorator (inherited from class)
3. Test both CUDA code path and results validation
4. Consider adding CPU comparison test
5. Update this README with new test description

Example:
```python
def test_new_cuda_feature(self, default_state):
    """Test description here."""
    # Setup
    # ...

    # Run with CUDA
    result = simjob.run_sim(default_state, scene, gpu_id=0)

    # Validate
    assert result is not None
```

## CI/CD Integration

The CI/CD pipeline runs on CPU-only GitHub Actions runners, so:
- ✅ CUDA tests are automatically skipped in CI
- ✅ CPU fallback tests always run in CI
- ✅ Coverage reports show CUDA code as "missing" (expected)

When you have access to a GPU machine:
- Run CUDA tests locally to verify GPU code paths
- Coverage will increase to ~85% with CUDA tests passing

## Reference

- [Numba CUDA Documentation](https://numba.readthedocs.io/en/stable/cuda/index.html)
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
- [pytest Skip Documentation](https://docs.pytest.org/en/stable/how-to/skipping.html)
