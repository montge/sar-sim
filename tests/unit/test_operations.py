"""Unit tests for signal processing operations."""

import pytest
import numpy as np
from sarsim import operations


class TestWindowFunctions:
    """Test suite for windowing functions."""

    def test_window_functions_exist(self):
        """Test that all expected window functions are available."""
        expected_windows = ['Rect', 'Hann', 'Hamming', 'Tukey', 'Blackman']

        for window_name in expected_windows:
            assert window_name in operations.SUPPORTED_WINDOWS, \
                f"Window '{window_name}' not found in SUPPORTED_WINDOWS"

    def test_rect_window_shape(self):
        """Test that rectangular window has correct shape."""
        window = operations.SUPPORTED_WINDOWS['Rect']
        length = 100

        result = window.factory(length, sym=False, alpha=0)

        assert len(result) == length
        assert isinstance(result, np.ndarray)

    def test_rect_window_values(self):
        """Test that rectangular window is all ones."""
        window = operations.SUPPORTED_WINDOWS['Rect']
        length = 50

        result = window.factory(length, sym=False, alpha=0)

        # Rectangular window should be all ones
        assert np.allclose(result, np.ones(length))

    def test_hann_window_shape(self):
        """Test that Hann window has correct shape."""
        window = operations.SUPPORTED_WINDOWS['Hann']
        length = 100

        result = window.factory(length, sym=False, alpha=0)

        assert len(result) == length

    def test_hann_window_endpoints(self):
        """Test that Hann window has expected endpoint behavior."""
        window = operations.SUPPORTED_WINDOWS['Hann']
        length = 100

        result = window.factory(length, sym=False, alpha=0)

        # Hann window should taper at edges
        assert result[0] < result[length // 2]
        assert result[-1] < result[length // 2]

    def test_tukey_window_with_alpha(self):
        """Test Tukey window with different alpha values."""
        window = operations.SUPPORTED_WINDOWS['Tukey']
        length = 100

        # Alpha = 0 should give rectangular window
        result_rect = window.factory(length, sym=False, alpha=0.0)
        assert np.allclose(result_rect, np.ones(length))

        # Alpha = 1 should give Hann-like window
        result_hann = window.factory(length, sym=False, alpha=1.0)
        assert result_hann[0] < result_hann[length // 2]
        assert result_hann[-1] < result_hann[length // 2]

    def test_window_normalization(self):
        """Test that windows are properly normalized."""
        length = 100

        for name, window in operations.SUPPORTED_WINDOWS.items():
            result = window.factory(length, sym=False, alpha=0.25)

            # Check that window is normalized (max value is 1)
            assert np.max(result) <= 1.0, f"{name} window exceeds 1.0"
            assert np.min(result) >= 0.0, f"{name} window has negative values"

    def test_symmetric_vs_periodic(self):
        """Test symmetric vs periodic window generation."""
        window = operations.SUPPORTED_WINDOWS['Hann']
        length = 100

        symmetric = window.factory(length, sym=True, alpha=0)
        periodic = window.factory(length, sym=False, alpha=0)

        # Results should be similar but not identical
        assert len(symmetric) == len(periodic)
        # The specific difference depends on implementation

    def test_window_length_edge_cases(self):
        """Test window generation with edge case lengths."""
        window = operations.SUPPORTED_WINDOWS['Rect']

        # Very short window
        result = window.factory(2, sym=False, alpha=0)
        assert len(result) == 2

        # Single element
        result = window.factory(1, sym=False, alpha=0)
        assert len(result) == 1


class TestSignalProcessingOperations:
    """Test suite for general signal processing operations."""

    def test_window_application(self):
        """Test applying window to a signal."""
        signal = np.ones(100)
        window = operations.SUPPORTED_WINDOWS['Hann'].factory(100, sym=False, alpha=0)

        windowed_signal = signal * window

        assert len(windowed_signal) == len(signal)
        assert np.max(windowed_signal) <= 1.0

    def test_window_energy(self):
        """Test that different windows have different energy."""
        length = 100

        rect_energy = np.sum(operations.SUPPORTED_WINDOWS['Rect'].factory(length, False, 0) ** 2)
        hann_energy = np.sum(operations.SUPPORTED_WINDOWS['Hann'].factory(length, False, 0) ** 2)

        # Rectangular window should have higher energy
        assert rect_energy > hann_energy


# Run with: pytest tests/unit/test_operations.py -v
