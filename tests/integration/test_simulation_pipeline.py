"""Integration tests for the complete SAR simulation pipeline.

These tests validate end-to-end workflows and integration between components.
They are slower than unit tests but ensure the system works as a whole.
"""

import pytest
import numpy as np
from sarsim import simstate, simscene, simjob, profiling


class TestBasicSimulationPipeline:
    """Test complete simulation workflow from start to finish."""

    def test_simple_scene_simulation(self):
        """Test running a complete simulation with a simple scene."""
        # Create simulation state with simple parameters
        state = simstate.create_state()
        state.azimuth_count = 50  # Fewer points for faster test
        state.image_count_x = 50
        state.image_count_y = 50

        # Create simple scene
        scene = simscene.create_default_scene()

        # Run simulation (without GPU for CI compatibility)
        result = simjob.run_sim(
            state=state,
            scene=scene,
            timestamper=profiling.TimeStamper(report_tic_inline=False, report_toc_inline=False),
            progress_callback=None,
            loaded_data=None,
            gpu_id=0
        )

        # Verify results exist and have correct shapes
        assert result is not None
        assert result.raw is not None
        assert result.rc is not None
        assert result.ac is not None

        # Verify data shapes
        assert result.raw.data.shape[0] == state.azimuth_count
        assert result.ac.data.shape == (state.image_count_x, state.image_count_y)

        # Verify data is not all zeros (actual signal processing happened)
        assert not np.allclose(result.ac.data, 0)

    def test_parameter_modification_workflow(self):
        """Test modifying parameters and re-running simulation."""
        state = simstate.create_state()
        scene = simscene.create_default_scene()

        # Initial run with default frequency
        state.azimuth_count = 30
        state.image_count_x = 30
        state.image_count_y = 30
        original_freq = state.fmcw_start_frequency

        result1 = simjob.run_sim(
            state, scene,
            timestamper=profiling.TimeStamper(False, False),
            progress_callback=None
        )

        # Modify parameters
        state.fmcw_start_frequency = original_freq * 1.1

        result2 = simjob.run_sim(
            state, scene,
            timestamper=profiling.TimeStamper(False, False),
            progress_callback=None
        )

        # Results should differ
        assert not np.allclose(result1.ac.data, result2.ac.data)


class TestSceneConfiguration:
    """Test different scene configurations."""

    def test_single_reflector_scene(self):
        """Test simulation with single reflector."""
        state = simstate.create_state()
        state.azimuth_count = 30
        state.image_count_x = 30
        state.image_count_y = 30

        # Create scene with single reflector at origin
        scene = simscene.SimulationScene()
        scene += simscene.SimpleReflector(0, 0, 0, amplitude=1.0)

        result = simjob.run_sim(
            state, scene,
            timestamper=profiling.TimeStamper(False, False)
        )

        assert result is not None
        assert not np.allclose(result.ac.data, 0)

    def test_multiple_reflectors_scene(self):
        """Test simulation with multiple reflectors."""
        state = simstate.create_state()
        state.azimuth_count = 40
        state.image_count_x = 40
        state.image_count_y = 40

        # Create scene with multiple reflectors
        scene = simscene.SimulationScene()
        scene += simscene.SimpleReflector(-0.5, 0, 0, amplitude=1.0)
        scene += simscene.SimpleReflector(0, 0, 0, amplitude=0.8)
        scene += simscene.SimpleReflector(0.5, 0, 0, amplitude=1.2)

        result = simjob.run_sim(
            state, scene,
            timestamper=profiling.TimeStamper(False, False)
        )

        assert result is not None
        # Image should have stronger signal with more reflectors
        assert np.max(np.abs(result.ac.data)) > 0


@pytest.mark.slow
class TestCompressionStages:
    """Test individual compression stages."""

    def test_range_compression_only(self):
        """Test range compression stage."""
        state = simstate.create_state()
        state.azimuth_count = 30
        scene = simscene.create_default_scene()

        result = simjob.run_sim(
            state, scene,
            timestamper=profiling.TimeStamper(False, False)
        )

        # Range compressed data should exist and be complex
        assert result.rc.data.dtype == np.complex128 or result.rc.data.dtype == np.complex64
        assert result.rc.data.shape[0] == state.azimuth_count

    def test_flight_path_generation(self):
        """Test flight path generation."""
        state = simstate.create_state()
        state.azimuth_count = 50
        scene = simscene.create_default_scene()

        result = simjob.run_sim(
            state, scene,
            timestamper=profiling.TimeStamper(False, False)
        )

        # Flight paths should be generated
        assert result.fpath_exact is not None
        assert result.fpath_distorted is not None
        assert result.fpath_exact.shape[0] == state.azimuth_count
        assert result.fpath_exact.shape[1] == 3  # x, y, z coordinates


# Run with:
# pytest tests/integration/ -v
# pytest tests/integration/ -v -m "not slow"  # Skip slow tests
