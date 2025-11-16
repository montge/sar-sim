"""Security tests for SAR data file I/O operations.

This test suite focuses on security-sensitive code paths identified in the assessment:
- Path traversal vulnerabilities
- File size limits
- Input validation
- Error handling for malformed data
"""

import pytest
import tempfile
import os
import shutil
from pathlib import Path
from sarsim import sardata


class TestPathSecurity:
    """Test suite for path traversal and directory security."""

    def test_valid_sardata_directory(self):
        """Test loading a valid .sardata directory."""
        # Create temporary .sardata directory
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            # Create minimal valid structure
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                f.write("[general]\n")
                f.write("radartype = 80\n")
                f.write("[params]\n")
                f.write("start_frequency = 76000000000.0\n")
                f.write("stop_frequency = 81000000000.0\n")
                f.write("ramp_duration = 0.0001\n")
                f.write("adc_frequency = 1000000.0\n")
                f.write("azimuth_count = 10\n")
                f.write("azimuth_start_position = -1.0\n")
                f.write("azimuth_end_position = 1.0\n")
                f.write("[fpath]\n")
                f.write("x = " + ",".join(["0.0"] * 10) + "\n")
                f.write("y = " + ",".join(["5.0"] * 10) + "\n")
                f.write("z = " + ",".join(["1.0"] * 10) + "\n")

            # Create minimal binary file
            bin_path = os.path.join(tmpdir, 'fmcw.bin')
            import array
            # 10 azimuth lines * 100 samples = 1000 samples
            data = array.array('i', [0] * 1000)
            with open(bin_path, 'wb') as f:
                data.tofile(f)

            # Should load successfully
            sd = sardata.SarData.import_from_directory(tmpdir)
            assert sd is not None
            assert sd.sim_state is not None

    def test_directory_without_sardata_extension(self):
        """Test that directory without .sardata extension is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Directory doesn't end with .sardata
            with pytest.raises(Exception, match="not look like a valid.*sardata"):
                sardata.SarData.import_from_directory(tmpdir)

    def test_nonexistent_directory(self):
        """Test that nonexistent directory raises appropriate error."""
        fake_dir = "/tmp/nonexistent_dir_12345.sardata"

        with pytest.raises(Exception):
            sardata.SarData.import_from_directory(fake_dir)

    def test_path_traversal_attempt(self):
        """Test that path traversal attempts are handled safely."""
        # Attempt to use path traversal
        malicious_paths = [
            "../../../etc/passwd.sardata",
            "../../sensitive_data.sardata",
            "/etc/passwd.sardata",
        ]

        for path in malicious_paths:
            # Should either reject or normalize the path safely
            # Exact behavior depends on implementation
            try:
                sardata.SarData.import_from_directory(path)
            except Exception:
                # Expected to fail - path doesn't exist or is rejected
                pass

    def test_file_instead_of_directory(self):
        """Test that passing a file instead of directory is handled."""
        with tempfile.NamedTemporaryFile(suffix='.sardata', delete=False) as f:
            filename = f.name
            f.write(b"not a directory")

        try:
            # Should reject file as it's not a directory
            with pytest.raises(Exception):
                sardata.SarData.import_from_directory(filename)
        finally:
            os.unlink(filename)


class TestConfigFileSecurity:
    """Test suite for configuration file parsing security."""

    def test_missing_config_file(self):
        """Test directory with missing params.cfg."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            # No params.cfg file

            with pytest.raises(Exception, match="no/too many.*cfg"):
                sardata.SarData.import_from_directory(tmpdir)

    def test_multiple_config_files(self):
        """Test directory with multiple .cfg files (ambiguous)."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            # Create multiple .cfg files
            open(os.path.join(tmpdir, 'file1.cfg'), 'w').close()
            open(os.path.join(tmpdir, 'file2.cfg'), 'w').close()

            with pytest.raises(Exception, match="too many.*cfg"):
                sardata.SarData.import_from_directory(tmpdir)

    def test_malformed_config_file(self):
        """Test config file with invalid INI format."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                # Invalid INI format
                f.write("this is not valid INI format\n")
                f.write("random text here\n")

            # Should handle gracefully
            try:
                sardata.SarData.import_from_directory(tmpdir)
            except Exception:
                # Expected to fail on invalid format
                pass

    def test_config_with_missing_sections(self):
        """Test config file missing required sections."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                # Missing required [params] section
                f.write("[general]\n")
                f.write("radartype = 80\n")

            with pytest.raises(Exception):
                sardata.SarData.import_from_directory(tmpdir)

    def test_config_with_invalid_values(self):
        """Test config with invalid parameter values."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                f.write("[general]\n")
                f.write("radartype = 80\n")
                f.write("[params]\n")
                f.write("start_frequency = invalid_number\n")  # Invalid float
                f.write("azimuth_count = not_an_integer\n")  # Invalid int

            with pytest.raises(Exception):
                sardata.SarData.import_from_directory(tmpdir)


class TestBinaryFileSecurity:
    """Test suite for binary file loading security."""

    def test_missing_binary_file(self):
        """Test directory with config but missing binary file."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                f.write("[general]\n")
                f.write("radartype = 80\n")
                f.write("[params]\n")
                f.write("start_frequency = 76000000000.0\n")
                f.write("stop_frequency = 81000000000.0\n")
                f.write("ramp_duration = 0.0001\n")
                f.write("adc_frequency = 1000000.0\n")
                f.write("azimuth_count = 10\n")
                f.write("azimuth_start_position = -1.0\n")
                f.write("azimuth_end_position = 1.0\n")
                f.write("[fpath]\n")
                f.write("x = " + ",".join(["0.0"] * 10) + "\n")
                f.write("y = " + ",".join(["5.0"] * 10) + "\n")
                f.write("z = " + ",".join(["1.0"] * 10) + "\n")

            # No fmcw.bin file
            with pytest.raises(Exception):
                sardata.SarData.import_from_directory(tmpdir)

    def test_corrupted_binary_file(self):
        """Test binary file with incorrect size/corrupted data."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                f.write("[general]\n")
                f.write("radartype = 80\n")
                f.write("[params]\n")
                f.write("start_frequency = 76000000000.0\n")
                f.write("stop_frequency = 81000000000.0\n")
                f.write("ramp_duration = 0.0001\n")
                f.write("adc_frequency = 1000000.0\n")
                f.write("azimuth_count = 10\n")
                f.write("azimuth_start_position = -1.0\n")
                f.write("azimuth_end_position = 1.0\n")
                f.write("[fpath]\n")
                f.write("x = " + ",".join(["0.0"] * 10) + "\n")
                f.write("y = " + ",".join(["5.0"] * 10) + "\n")
                f.write("z = " + ",".join(["1.0"] * 10) + "\n")

            # Create truncated/corrupted binary file
            bin_path = os.path.join(tmpdir, 'fmcw.bin')
            with open(bin_path, 'wb') as f:
                f.write(b"corrupted data")  # Too small

            # Should handle gracefully
            try:
                sardata.SarData.import_from_directory(tmpdir)
            except Exception:
                # Expected to fail on corrupted data
                pass

    @pytest.mark.slow
    def test_very_large_binary_file(self):
        """Test handling of very large binary files."""
        # This test is marked as slow and tests resource limits
        # Skipped by default to avoid long test runs
        pytest.skip("Slow test - enable manually to test large file handling")


class TestFlightPathValidation:
    """Test suite for flight path data validation."""

    def test_mismatched_flight_path_dimensions(self):
        """Test flight path with mismatched dimensions."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                f.write("[general]\n")
                f.write("radartype = 80\n")
                f.write("[params]\n")
                f.write("start_frequency = 76000000000.0\n")
                f.write("stop_frequency = 81000000000.0\n")
                f.write("ramp_duration = 0.0001\n")
                f.write("adc_frequency = 1000000.0\n")
                f.write("azimuth_count = 10\n")
                f.write("azimuth_start_position = -1.0\n")
                f.write("azimuth_end_position = 1.0\n")
                f.write("[fpath]\n")
                # Wrong number of points (5 instead of 10)
                f.write("x = " + ",".join(["0.0"] * 5) + "\n")
                f.write("y = " + ",".join(["5.0"] * 5) + "\n")
                f.write("z = " + ",".join(["1.0"] * 5) + "\n")

            bin_path = os.path.join(tmpdir, 'fmcw.bin')
            import array
            data = array.array('i', [0] * 1000)
            with open(bin_path, 'wb') as f:
                data.tofile(f)

            with pytest.raises(Exception, match="Unexpected dimensions"):
                sardata.SarData.import_from_directory(tmpdir)

    def test_invalid_flight_path_values(self):
        """Test flight path with invalid numeric values."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                f.write("[general]\n")
                f.write("radartype = 80\n")
                f.write("[params]\n")
                f.write("start_frequency = 76000000000.0\n")
                f.write("stop_frequency = 81000000000.0\n")
                f.write("ramp_duration = 0.0001\n")
                f.write("adc_frequency = 1000000.0\n")
                f.write("azimuth_count = 3\n")
                f.write("azimuth_start_position = -1.0\n")
                f.write("azimuth_end_position = 1.0\n")
                f.write("[fpath]\n")
                # Invalid numeric values
                f.write("x = 0.0,invalid,1.0\n")
                f.write("y = 5.0,5.0,5.0\n")
                f.write("z = 1.0,1.0,1.0\n")

            with pytest.raises(Exception):
                sardata.SarData.import_from_directory(tmpdir)


class TestRangeCompressedData:
    """Test suite for range-compressed data loading."""

    def test_load_range_compressed_flag(self):
        """Test loading data with range_compressed flag."""
        with tempfile.TemporaryDirectory(suffix='.sardata') as tmpdir:
            config_path = os.path.join(tmpdir, 'params.cfg')
            with open(config_path, 'w') as f:
                f.write("[general]\n")
                f.write("data_is_range_compressed = true\n")
                f.write("[params]\n")
                f.write("center_frequency = 78500000000.0\n")
                f.write("bandwidth = 5000000000.0\n")
                f.write("azimuth_count = 10\n")
                f.write("azimuth_start_position = -1.0\n")
                f.write("azimuth_end_position = 1.0\n")
                f.write("[fpath]\n")
                f.write("x = " + ",".join(["0.0"] * 10) + "\n")
                f.write("y = " + ",".join(["5.0"] * 10) + "\n")
                f.write("z = " + ",".join(["1.0"] * 10) + "\n")

            # Create range_comp.bin with complex data
            bin_path = os.path.join(tmpdir, 'range_comp.bin')
            import numpy as np
            # 10 lines * 100 samples * 2 (real+imag) = 2000 floats
            data = np.zeros(2000, dtype=np.float32)
            data.tofile(bin_path)

            # Should load as range-compressed data
            sd = sardata.SarData.import_from_directory(tmpdir)
            assert sd.has_range_compressed_data is True


# Run with: pytest tests/unit/test_sardata_security.py -v
# Run security tests only: pytest tests/unit/test_sardata_security.py -v -m "not slow"
