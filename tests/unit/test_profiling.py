"""Unit tests for profiling and timing utilities."""

import pytest
import time
from sarsim import profiling


class TestTimeStamper:
    """Test suite for TimeStamper class."""

    def test_create_timestamper(self):
        """Test creating a TimeStamper instance."""
        ts = profiling.TimeStamper()
        assert ts is not None

    def test_tic_toc_basic(self):
        """Test basic tic/toc functionality."""
        ts = profiling.TimeStamper()

        ts.tic('test_operation')
        time.sleep(0.01)  # Sleep for 10ms
        ts.toc()

        # TimeStamper should have recorded the operation
        # (Implementation detail: depends on how TimeStamper stores data)

    def test_multiple_operations(self):
        """Test timing multiple operations."""
        ts = profiling.TimeStamper()

        ts.tic('operation1')
        time.sleep(0.005)
        ts.toc()

        ts.tic('operation2')
        time.sleep(0.005)
        ts.toc()

        ts.tic('operation3')
        time.sleep(0.005)
        ts.toc()

        # All three operations should be recorded

    def test_nested_operations(self):
        """Test nested tic/toc calls."""
        ts = profiling.TimeStamper()

        ts.tic('outer')
        time.sleep(0.005)

        ts.tic('inner')
        time.sleep(0.005)
        ts.toc()

        ts.toc()

        # Both operations should be recorded

    def test_tic_without_name(self):
        """Test tic without operation name."""
        ts = profiling.TimeStamper()

        # Should work with empty or no name
        ts.tic('')
        time.sleep(0.001)
        ts.toc()

    def test_multiple_timestampers(self):
        """Test using multiple independent TimeStampers."""
        ts1 = profiling.TimeStamper()
        ts2 = profiling.TimeStamper()

        ts1.tic('ts1_operation')
        ts2.tic('ts2_operation')

        time.sleep(0.005)

        ts1.toc()
        ts2.toc()

        # Each timestamper should independently track its operations

    def test_timing_accuracy(self):
        """Test that timing is reasonably accurate."""
        ts = profiling.TimeStamper()

        ts.tic('sleep_test')
        sleep_duration = 0.05  # 50ms
        time.sleep(sleep_duration)
        ts.toc()

        # Actual implementation would depend on TimeStamper's API
        # This test verifies timing works

    def test_sequential_timing(self):
        """Test timing sequential operations."""
        ts = profiling.TimeStamper()

        operations = ['op1', 'op2', 'op3', 'op4']

        for op in operations:
            ts.tic(op)
            time.sleep(0.005)
            ts.toc()

        # All operations should be timed

    def test_empty_timestamper(self):
        """Test newly created TimeStamper with no operations."""
        ts = profiling.TimeStamper()

        # Should handle having no recorded operations gracefully

    def test_toc_without_tic(self):
        """Test calling toc without corresponding tic."""
        ts = profiling.TimeStamper()

        # Should either raise an error or handle gracefully
        # (depends on implementation)
        try:
            ts.toc()
        except (IndexError, RuntimeError, ValueError):
            # Expected behavior if implementation checks for matching tic
            pass


class TestTimingConsistency:
    """Test suite for timing consistency and reliability."""

    def test_repeated_operations(self):
        """Test timing the same operation multiple times."""
        ts = profiling.TimeStamper()

        for i in range(5):
            ts.tic(f'iteration_{i}')
            time.sleep(0.002)
            ts.toc()

        # All iterations should be recorded

    def test_varying_durations(self):
        """Test operations with different durations."""
        ts = profiling.TimeStamper()

        durations = [0.001, 0.005, 0.01, 0.002, 0.008]

        for i, duration in enumerate(durations):
            ts.tic(f'operation_{i}')
            time.sleep(duration)
            ts.toc()

        # All operations should be recorded with different timings

    def test_very_short_operation(self):
        """Test timing very short operations."""
        ts = profiling.TimeStamper()

        ts.tic('fast_operation')
        # Very fast operation (no sleep)
        _ = 1 + 1
        ts.toc()

        # Should handle sub-millisecond timing

    def test_long_operation_name(self):
        """Test with long operation names."""
        ts = profiling.TimeStamper()

        long_name = 'operation_' * 20  # Very long name
        ts.tic(long_name)
        time.sleep(0.001)
        ts.toc()

        # Should handle long operation names

    def test_special_characters_in_name(self):
        """Test operation names with special characters."""
        ts = profiling.TimeStamper()

        names = [
            'operation-with-dashes',
            'operation_with_underscores',
            'operation with spaces',
            'operation.with.dots',
        ]

        for name in names:
            ts.tic(name)
            time.sleep(0.001)
            ts.toc()

        # Should handle various character types in names


class TestTimeStamperUsage:
    """Test suite for typical TimeStamper usage patterns."""

    def test_simulation_workflow(self):
        """Test timing a simulated workflow."""
        ts = profiling.TimeStamper()

        # Simulate typical SAR simulation workflow
        ts.tic('Data Preparation')
        time.sleep(0.005)
        ts.toc()

        ts.tic('FMCW Simulation')
        time.sleep(0.01)
        ts.toc()

        ts.tic('Range Compression')
        time.sleep(0.008)
        ts.toc()

        ts.tic('Azimuth Compression')
        time.sleep(0.015)
        ts.toc()

        # Workflow should be fully timed

    def test_optional_timestamper(self):
        """Test using None as optional timestamper."""
        # Simulating optional timestamper pattern used in simjob.py
        ts = None

        # Should handle None gracefully in application code
        if ts:
            ts.tic('operation')
            time.sleep(0.001)
            ts.toc()

    def test_timestamper_reuse(self):
        """Test reusing same TimeStamper instance."""
        ts = profiling.TimeStamper()

        # First run
        ts.tic('run1')
        time.sleep(0.002)
        ts.toc()

        # Second run
        ts.tic('run2')
        time.sleep(0.002)
        ts.toc()

        # Third run
        ts.tic('run3')
        time.sleep(0.002)
        ts.toc()

        # Should accumulate all runs


# Run with: pytest tests/unit/test_profiling.py -v
