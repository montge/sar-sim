"""Unit tests for simulation job execution module."""

import numpy as np
import pytest

from sarsim import operations, simjob, simscene, simstate


class TestSimResult:
    """Test suite for SimResult named tuple."""

    def test_simresult_creation(self):
        """Test creating a SimResult instance."""
        # Create mock data
        raw_data = np.random.rand(10, 10) + 1j * np.random.rand(10, 10)
        rc_data = np.random.rand(10, 10) + 1j * np.random.rand(10, 10)
        ac_data = np.random.rand(10, 10) + 1j * np.random.rand(10, 10)
        af_data = np.random.rand(10, 10) + 1j * np.random.rand(10, 10)
        fpath_exact = np.random.rand(10, 3)
        fpath_distorted = np.random.rand(10, 3)
        optimal_phases = np.random.rand(5, 10)

        # Create SimImage instances
        raw_img = simstate.SimImage(raw_data, 0.0, 0.0, 1.0, 1.0)
        rc_img = simstate.SimImage(rc_data, 0.0, 0.0, 1.0, 1.0)
        ac_img = simstate.SimImage(ac_data, 0.0, 0.0, 1.0, 1.0)
        af_img = simstate.SimImage(af_data, 0.0, 0.0, 1.0, 1.0)

        # Create SimResult
        result = simjob.SimResult(
            raw=raw_img,
            rc=rc_img,
            ac=ac_img,
            af=af_img,
            fpath_exact=fpath_exact,
            fpath_distorted=fpath_distorted,
            optimal_phases=optimal_phases,
        )

        # Verify all fields
        assert result.raw == raw_img
        assert result.rc == rc_img
        assert result.ac == ac_img
        assert result.af == af_img
        assert np.array_equal(result.fpath_exact, fpath_exact)
        assert np.array_equal(result.fpath_distorted, fpath_distorted)
        assert np.array_equal(result.optimal_phases, optimal_phases)

    def test_simresult_immutable(self):
        """Test that SimResult is immutable (NamedTuple)."""
        raw_data = np.random.rand(5, 5) + 1j * np.random.rand(5, 5)
        raw_img = simstate.SimImage(raw_data, 0.0, 0.0, 1.0, 1.0)
        rc_img = simstate.SimImage(raw_data, 0.0, 0.0, 1.0, 1.0)
        ac_img = simstate.SimImage(raw_data, 0.0, 0.0, 1.0, 1.0)
        af_img = simstate.SimImage(raw_data, 0.0, 0.0, 1.0, 1.0)

        result = simjob.SimResult(
            raw=raw_img,
            rc=rc_img,
            ac=ac_img,
            af=af_img,
            fpath_exact=np.zeros((5, 3)),
            fpath_distorted=np.zeros((5, 3)),
            optimal_phases=np.zeros((2, 5)),
        )

        # Attempt to modify should raise AttributeError
        with pytest.raises(AttributeError):
            result.raw = simstate.SimImage(raw_data, 1.0, 1.0, 2.0, 2.0)


class TestFlightPathCreation:
    """Test suite for flight path creation functions."""

    def test_make_flight_path_basic(self):
        """Test basic flight path creation."""
        state = simstate.SarSimParameterState()
        state.azimuth_start_position = 0.0
        state.azimuth_stop_position = 100.0
        state.azimuth_count = 11
        state.flight_height = 1000.0
        state.flight_distance_to_scene_center = 5000.0
        state.flight_wiggle_global_scale = 0.0  # Disable wiggles for basic test

        flight_path = simjob._make_flight_path(state)

        # Check shape: should be [azimuth_count, 3] for (x, y, z)
        assert flight_path.shape == (11, 3)

        # Check z-coordinate (height) is constant
        assert np.allclose(flight_path[:, 2], state.flight_height)

        # Check y-coordinate (distance to scene, negative)
        assert np.allclose(flight_path[:, 1], -state.flight_distance_to_scene_center)

        # Check x-coordinate varies from start to stop
        assert flight_path[0, 0] == pytest.approx(state.azimuth_start_position)
        assert flight_path[-1, 0] == pytest.approx(state.azimuth_stop_position)

    def test_make_flight_path_negative_positions(self):
        """Test flight path with negative azimuth positions."""
        state = simstate.SarSimParameterState()
        state.azimuth_start_position = -50.0
        state.azimuth_stop_position = 50.0
        state.azimuth_count = 21
        state.flight_height = 500.0
        state.flight_distance_to_scene_center = 3000.0
        state.flight_wiggle_global_scale = 0.0  # Disable wiggles

        flight_path = simjob._make_flight_path(state)

        assert flight_path.shape == (21, 3)
        assert flight_path[0, 0] == pytest.approx(-50.0)
        assert flight_path[-1, 0] == pytest.approx(50.0)
        assert np.allclose(flight_path[:, 2], 500.0)

    def test_distort_path_with_zero_distortion(self):
        """Test path distortion with zero random factor."""
        state = simstate.SarSimParameterState()
        state.distortion_random_factor = 0.0
        state.distortion_sample_frequency = 1.0
        state.azimuth_start_position = 0.0
        state.azimuth_stop_position = 20.0

        exact_path = np.array([[0, 1000, -500], [10, 1000, -500], [20, 1000, -500]])

        distorted_path = simjob._distort_path(exact_path, state)

        # With zero random factor, paths should be similar (after interpolation)
        # Shape should be preserved
        assert distorted_path.shape == exact_path.shape

    def test_distort_path_with_random_factor(self):
        """Test path distortion with non-zero random factor."""
        state = simstate.SarSimParameterState()
        state.distortion_random_factor = 1.0
        state.distortion_sample_frequency = 0.5
        state.azimuth_start_position = 0.0
        state.azimuth_stop_position = 20.0

        exact_path = np.array([[0, 1000, -500], [10, 1000, -500], [20, 1000, -500]])

        distorted_path = simjob._distort_path(exact_path, state)

        # Distorted path should differ from exact path due to random noise
        assert not np.allclose(distorted_path, exact_path)

        # Shape should be preserved
        assert distorted_path.shape == exact_path.shape


class TestRangeCompression:
    """Test suite for range compression functions."""

    def test_range_compression_basic(self):
        """Test basic range compression."""
        state = simstate.SarSimParameterState()
        state.fmcw_start_frequency = 76.0e9
        state.fmcw_stop_frequency = 81.0e9
        state.fmcw_ramp_duration = 1e-3
        state.range_compression_window = operations.SUPPORTED_WINDOWS["Rect"]
        state.range_compression_window_parameter = 0.0

        # Create simple test data: 5 azimuth lines, 100 samples each
        fmcw_lines = [np.random.rand(100) + 1j * np.random.rand(100) for _ in range(5)]

        rc_lines = simjob._range_compression(state, fmcw_lines)

        # Check output shape
        assert rc_lines.shape[0] == 5  # same number of azimuth lines
        # Output range samples will be different due to FFT oversampling
        assert rc_lines.shape[1] > 100  # FFT oversampling increases sample count

        # Output should be complex
        assert rc_lines.dtype == complex

    def test_range_compression_window_functions(self):
        """Test range compression with different window functions."""
        state = simstate.SarSimParameterState()
        state.fmcw_start_frequency = 76.0e9
        state.fmcw_stop_frequency = 81.0e9
        state.fmcw_ramp_duration = 1e-3

        fmcw_lines = [np.random.rand(50) + 1j * np.random.rand(50) for _ in range(3)]

        # Test with different windows
        for window_name in ["Rect", "Hann", "Hamming"]:
            state.range_compression_window = operations.SUPPORTED_WINDOWS[window_name]
            state.range_compression_window_parameter = 0.0

            rc_lines = simjob._range_compression(state, fmcw_lines)

            assert rc_lines.shape[0] == 3  # same azimuth lines
            assert rc_lines.shape[1] > 50  # FFT oversampling
            assert rc_lines.dtype == complex


class TestFMCWSimulation:
    """Test suite for FMCW simulation functions."""

    def test_fmcw_sim_basic(self, simple_scene):
        """Test basic FMCW simulation."""
        # Create simple flight path
        flight_path = np.array([[0, 5000, -1000], [10, 5000, -1000], [20, 5000, -1000]])

        fmcw_samples = 100
        signal_speed = 3e8
        fmcw_start_freq = 76e9
        fmcw_slope = 5e12  # 5 THz/s
        fmcw_t = np.linspace(0, 1e-3, fmcw_samples)
        azimuth_3db_angle_deg = 30.0

        fmcw_lines = simjob._fmcw_sim(
            flight_path, fmcw_samples, simple_scene, signal_speed, fmcw_start_freq, fmcw_slope, fmcw_t, azimuth_3db_angle_deg
        )

        # Check output structure
        assert len(fmcw_lines) == 3  # one per flight path position
        assert all(len(line) == fmcw_samples for line in fmcw_lines)
        # Check that lines contain complex data (may be ndarray with complex dtype)
        assert all(isinstance(line, np.ndarray) for line in fmcw_lines)

    def test_fmcw_sim_empty_scene(self):
        """Test FMCW simulation with empty scene."""
        empty_scene = simscene.SimulationScene()

        flight_path = np.array([[0, 5000, -1000], [10, 5000, -1000]])
        fmcw_samples = 50
        signal_speed = 3e8
        fmcw_start_freq = 76e9
        fmcw_slope = 5e12
        fmcw_t = np.linspace(0, 1e-3, fmcw_samples)
        azimuth_3db_angle_deg = 30.0

        fmcw_lines = simjob._fmcw_sim(
            flight_path, fmcw_samples, empty_scene, signal_speed, fmcw_start_freq, fmcw_slope, fmcw_t, azimuth_3db_angle_deg
        )

        # Should return data even for empty scene (just noise/zeros)
        assert len(fmcw_lines) == 2
        assert all(len(line) == fmcw_samples for line in fmcw_lines)


@pytest.mark.slow
class TestSimulationExecution:
    """Test suite for full simulation execution."""

    def test_run_sim_basic(self, default_state, simple_scene):
        """Test basic simulation run."""
        # Configure for minimal simulation
        default_state.azimuth_count = 5
        default_state.image_count_x = 10
        default_state.image_count_y = 10
        default_state.enable_autofocus = False

        result = simjob.run_sim(default_state, simple_scene)

        # Verify result structure
        assert isinstance(result, simjob.SimResult)
        assert result.raw.data.shape[0] == 5  # azimuth lines
        assert result.rc.data.shape[0] == 5
        assert result.ac.data.shape == (10, 10)  # image dimensions
        assert result.af.data.shape == (10, 10)
        assert result.fpath_exact.shape[0] == 5
        assert result.fpath_distorted.shape[0] == 5

    def test_run_sim_with_autofocus(self, default_state, simple_scene):
        """Test simulation with autofocus enabled."""
        default_state.azimuth_count = 5
        default_state.image_count_x = 10
        default_state.image_count_y = 10
        default_state.enable_autofocus = True
        default_state.autofocus_rounds = 1
        default_state.autofocus_samples = 4  # Must be even
        default_state.autofocus_iterations = 2

        result = simjob.run_sim(default_state, simple_scene)

        # Autofocus should produce non-zero AF image
        assert isinstance(result, simjob.SimResult)
        assert result.af.data.shape == (10, 10)
        # Optimal phases should be computed
        assert result.optimal_phases.shape[1] == 5  # azimuth lines

    def test_run_sim_with_distorted_path(self, default_state, simple_scene):
        """Test simulation with distorted flight path."""
        default_state.azimuth_count = 5
        default_state.image_count_x = 10
        default_state.image_count_y = 10
        default_state.enable_autofocus = False
        default_state.use_distorted_path = True
        default_state.path_distortion_x_amplitude = 1.0

        result = simjob.run_sim(default_state, simple_scene)

        # Exact and distorted paths should differ
        assert not np.allclose(result.fpath_exact, result.fpath_distorted)

    def test_run_sim_with_progress_callback(self, default_state, simple_scene):
        """Test simulation with progress callback."""
        default_state.azimuth_count = 5
        default_state.image_count_x = 10
        default_state.image_count_y = 10
        default_state.enable_autofocus = False

        progress_updates = []

        def progress_callback(progress, message):
            progress_updates.append((progress, message))

        result = simjob.run_sim(default_state, simple_scene, progress_callback=progress_callback)

        # Should have received progress updates
        assert len(progress_updates) > 0
        # Progress should go from 0 to 1
        assert progress_updates[0][0] == pytest.approx(0.0)
        assert progress_updates[-1][0] == pytest.approx(1.0)
        assert progress_updates[-1][1] == "Finished"

    def test_run_sim_different_window_functions(self, default_state, simple_scene):
        """Test simulation with different windowing functions."""
        default_state.azimuth_count = 5
        default_state.image_count_x = 10
        default_state.image_count_y = 10
        default_state.enable_autofocus = False

        for window_name in ["Rect", "Hann", "Hamming"]:
            default_state.range_compression_window = operations.SUPPORTED_WINDOWS[window_name]
            default_state.azimuth_compression_window = operations.SUPPORTED_WINDOWS[window_name]

            result = simjob.run_sim(default_state, simple_scene)

            assert isinstance(result, simjob.SimResult)
            assert result.ac.data.shape == (10, 10)


class TestAzimuthCompression:
    """Test suite for azimuth compression functions."""

    def test_azimuth_compression_cpu(self, default_state):
        """Test azimuth compression on CPU."""
        # Create simple test data
        flight_path = np.array([[0, 5000, -1000], [10, 5000, -1000], [20, 5000, -1000]])
        rc_lines = np.random.rand(3, 50) + 1j * np.random.rand(3, 50)

        default_state.image_count_x = 5
        default_state.image_count_y = 5

        image_x, image_y, image, r_vector = simjob._azimuth_compression(
            default_state, ac_use_cuda=False, flight_path=flight_path, rc_lines=rc_lines, use_fmcw=True
        )

        # Check outputs
        assert len(image_x) == 5
        assert len(image_y) == 5
        assert image.shape == (5, 5)
        assert image.dtype == complex
        assert len(r_vector) == 50

    def test_azimuth_compression_single_pulse_mode(self, default_state):
        """Test azimuth compression in single pulse mode."""
        flight_path = np.array([[0, 5000, -1000]])
        rc_lines = np.random.rand(1, 50) + 1j * np.random.rand(1, 50)

        default_state.image_count_x = 5
        default_state.image_count_y = 5

        image_x, image_y, image, r_vector = simjob._azimuth_compression(
            default_state,
            ac_use_cuda=False,
            flight_path=flight_path,
            rc_lines=rc_lines,
            single_pulse_mode=True,
            use_fmcw=True,
        )

        assert image.shape == (5, 5)


@pytest.mark.slow
class TestLoadedDataScenarios:
    """Test suite for simulation with pre-loaded data."""

    def test_run_sim_with_loaded_fmcw_data(self, default_state, simple_scene):
        """Test simulation using loaded FMCW data."""
        from sarsim import sardata

        # Create minimal loaded data
        loaded_data = sardata.SarData()
        loaded_data.flight_path = np.array([[0, 5000, -1000], [10, 5000, -1000], [20, 5000, -1000]])
        loaded_data.fmcw_lines = [np.random.rand(100) + 1j * np.random.rand(100) for _ in range(3)]

        default_state.azimuth_count = 3
        default_state.image_count_x = 5
        default_state.image_count_y = 5
        default_state.enable_autofocus = False

        result = simjob.run_sim(default_state, simple_scene, loaded_data=loaded_data)

        # Should use the loaded flight path
        assert isinstance(result, simjob.SimResult)
        assert result.fpath_exact.shape[0] == 3

    def test_run_sim_with_loaded_range_compressed_data(self, default_state, simple_scene):
        """Test simulation using loaded range-compressed data."""
        from sarsim import sardata

        # Create loaded data with range-compressed data
        loaded_data = sardata.SarData()
        loaded_data.flight_path = np.array([[0, 5000, -1000], [10, 5000, -1000]])
        loaded_data.rg_comp_data = np.random.rand(2, 50) + 1j * np.random.rand(2, 50)
        loaded_data.has_range_compressed_data = True  # Required flag

        default_state.azimuth_count = 2
        default_state.image_count_x = 5
        default_state.image_count_y = 5
        default_state.enable_autofocus = False

        result = simjob.run_sim(default_state, simple_scene, loaded_data=loaded_data)

        # Should skip FMCW simulation and range compression
        assert isinstance(result, simjob.SimResult)
        assert result.ac.data.shape == (5, 5)


class TestPhaseCorrection:
    """Test suite for phase correction parameters."""

    def test_inverted_phase_correction(self, default_state, simple_scene):
        """Test simulation with inverted phase correction."""
        default_state.azimuth_count = 3
        default_state.image_count_x = 5
        default_state.image_count_y = 5
        default_state.enable_autofocus = False
        default_state.inverted_phase_correction = True

        result = simjob.run_sim(default_state, simple_scene)

        assert isinstance(result, simjob.SimResult)
        assert result.ac.data.shape == (5, 5)

    def test_normal_phase_correction(self, default_state, simple_scene):
        """Test simulation with normal phase correction."""
        default_state.azimuth_count = 3
        default_state.image_count_x = 5
        default_state.image_count_y = 5
        default_state.enable_autofocus = False
        default_state.inverted_phase_correction = False

        result = simjob.run_sim(default_state, simple_scene)

        assert isinstance(result, simjob.SimResult)
        assert result.ac.data.shape == (5, 5)


class TestNonFMCWMode:
    """Test suite for non-FMCW data processing."""

    def test_azimuth_compression_non_fmcw(self, default_state):
        """Test azimuth compression with non-FMCW data."""
        flight_path = np.array([[0, 5000, -1000], [10, 5000, -1000]])
        rc_lines = np.random.rand(2, 50) + 1j * np.random.rand(2, 50)

        default_state.image_count_x = 5
        default_state.image_count_y = 5

        image_x, image_y, image, r_vector = simjob._azimuth_compression(
            default_state,
            ac_use_cuda=False,
            flight_path=flight_path,
            rc_lines=rc_lines,
            use_fmcw=False,  # Non-FMCW mode
        )

        assert image.shape == (5, 5)
        assert len(r_vector) == 50


class TestFlightPathWiggles:
    """Test suite for flight path wiggle parameters."""

    def test_make_flight_path_with_wiggles(self):
        """Test flight path creation with wiggle perturbations."""
        state = simstate.SarSimParameterState()
        state.azimuth_start_position = 0.0
        state.azimuth_stop_position = 100.0
        state.azimuth_count = 11
        state.flight_height = 1000.0
        state.flight_distance_to_scene_center = 5000.0
        state.flight_wiggle_global_scale = 1.0
        state.flight_wiggle_amplitude_azimuth = 1.0
        state.flight_wiggle_amplitude_range = 0.5
        state.flight_wiggle_amplitude_height = 0.2
        state.flight_wiggle_frequency_azimuth = 0.1
        state.flight_wiggle_frequency_range = 0.1
        state.flight_wiggle_frequency_height = 0.1

        flight_path = simjob._make_flight_path(state)

        assert flight_path.shape == (11, 3)
        # With wiggles, the path should not be perfectly straight
        # But still start and end at the right positions
        assert flight_path[0, 0] == pytest.approx(state.azimuth_start_position, abs=1.0)
        assert flight_path[-1, 0] == pytest.approx(state.azimuth_stop_position, abs=1.0)


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    def test_minimal_simulation_configuration(self, simple_scene):
        """Test simulation with minimal configuration."""
        state = simstate.SarSimParameterState()
        state.azimuth_count = 2  # Minimum viable count
        state.image_count_x = 2
        state.image_count_y = 2
        state.enable_autofocus = False

        result = simjob.run_sim(state, simple_scene)

        assert isinstance(result, simjob.SimResult)
        assert result.ac.data.shape == (2, 2)

    def test_simulation_with_timestamper(self, default_state, simple_scene):
        """Test simulation with custom timestamper."""
        from sarsim import profiling

        timestamper = profiling.TimeStamper()

        default_state.azimuth_count = 3
        default_state.image_count_x = 5
        default_state.image_count_y = 5
        default_state.enable_autofocus = False

        result = simjob.run_sim(default_state, simple_scene, timestamper=timestamper)

        assert isinstance(result, simjob.SimResult)
        # Timestamper should have been used (verified by no errors)
        assert result.ac.data.shape == (5, 5)


class TestCUDAAvailability:
    """Test suite for CUDA availability detection."""

    def test_cuda_availability_flag(self):
        """Test that CUDA availability flag is set."""
        # Should be either True or False, not None
        assert isinstance(simjob.CUDA_NUMBA_AVAILABLE, bool)


# Example of how to run specific tests:
# pytest tests/unit/test_simjob.py -v
# pytest tests/unit/test_simjob.py::TestSimulationExecution::test_run_sim_basic -v
# pytest tests/unit/test_simjob.py -m "not slow" -v
