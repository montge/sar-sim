"""Pytest configuration and shared fixtures."""

import pytest
import numpy as np
from sarsim import simstate, simscene


@pytest.fixture
def default_state():
    """Create a default simulation state for testing."""
    return simstate.create_state()


@pytest.fixture
def simple_scene():
    """Create a simple test scene with a few reflectors."""
    return simscene.create_default_scene()


@pytest.fixture
def sample_fmcw_params():
    """Return a dictionary of typical FMCW parameters for testing."""
    return {
        'start_frequency': 76.0e9,  # 76 GHz
        'stop_frequency': 81.0e9,   # 81 GHz
        'ramp_duration': 100e-6,    # 100 microseconds
        'adc_frequency': 1.0e6,     # 1 MHz
    }


@pytest.fixture
def sample_flight_path():
    """Generate a simple flight path for testing."""
    azimuth_positions = np.linspace(-5, 5, 100)
    return np.array([
        [x, -10.0, 5.0]  # x, y, z coordinates
        for x in azimuth_positions
    ])


@pytest.fixture
def mock_rc_lines():
    """Create mock range-compressed data for testing."""
    num_azimuth = 100
    num_range = 512
    # Simple mock data with some signal
    data = np.random.randn(num_azimuth, num_range) + 1j * np.random.randn(num_azimuth, num_range)
    return data * 0.1  # Scale down
