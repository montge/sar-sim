"""Unit tests for simulation scene creation."""

import pytest
from sarsim import simscene


class TestSimpleReflector:
    """Test suite for SimpleReflector."""

    def test_create_reflector(self):
        """Test creating a simple reflector."""
        reflector = simscene.SimpleReflector(
            x=1.0,
            y=2.0,
            z=0.5,
            amplitude=10.0
        )

        assert reflector.x == 1.0
        assert reflector.y == 2.0
        assert reflector.z == 0.5
        assert reflector.amplitude == 10.0

    def test_reflector_is_named_tuple(self):
        """Test that SimpleReflector is a NamedTuple."""
        reflector = simscene.SimpleReflector(0, 0, 0, 1.0)

        # Named tuple properties
        assert reflector[0] == 0  # Access by index
        assert reflector.x == 0  # Access by name
        assert len(reflector) == 4  # Has 4 fields

    def test_reflector_defaults(self):
        """Test reflector creation with typical values."""
        reflector = simscene.SimpleReflector(
            x=0.0,
            y=3.0,
            z=0.0,
            amplitude=1.0
        )

        assert reflector.amplitude > 0


class TestSimulationScene:
    """Test suite for SimulationScene."""

    def test_create_empty_scene(self):
        """Test creating an empty scene."""
        scene = simscene.SimulationScene()

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) == 0

    def test_create_scene_with_reflectors(self):
        """Test creating a scene with reflectors."""
        scene = simscene.SimulationScene()
        scene += simscene.SimpleReflector(0, 0, 0, 1.0)
        scene += simscene.SimpleReflector(1, 1, 0, 1.0)
        scene += simscene.SimpleReflector(-1, 2, 0, 0.5)

        result = list(scene.get_simple_reflectors())
        assert len(result) == 3

    def test_scene_get_reflectors_returns_generator(self):
        """Test that get_simple_reflectors returns a generator."""
        scene = simscene.SimulationScene()
        scene += simscene.SimpleReflector(0, 0, 0, 1.0)

        result = scene.get_simple_reflectors()
        # get_simple_reflectors is a generator
        result_list = list(result)
        assert len(result_list) == 1

    def test_hash_method(self):
        """Test that scene has a hash method."""
        scene = simscene.SimulationScene()

        # Should be hashable (for caching in simjob)
        hash_value = hash(scene)
        assert isinstance(hash_value, int)

    def test_hash_consistency(self):
        """Test that identical scenes have same hash."""
        scene1 = simscene.SimulationScene()
        scene1 += simscene.SimpleReflector(0, 0, 0, 1.0)
        scene1 += simscene.SimpleReflector(1, 1, 0, 1.0)

        scene2 = simscene.SimulationScene()
        scene2 += simscene.SimpleReflector(0, 0, 0, 1.0)
        scene2 += simscene.SimpleReflector(1, 1, 0, 1.0)

        assert hash(scene1) == hash(scene2)


class TestDefaultScene:
    """Test suite for default scene creation."""

    def test_create_default_scene(self):
        """Test creating the default scene."""
        scene = simscene.create_default_scene()

        assert scene is not None
        assert isinstance(scene, simscene.SimulationScene)

    def test_default_scene_has_reflectors(self):
        """Test that default scene contains reflectors."""
        scene = simscene.create_default_scene()

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) > 0

    def test_default_scene_reflector_properties(self):
        """Test that default scene reflectors have valid properties."""
        scene = simscene.create_default_scene()

        reflectors = list(scene.get_simple_reflectors())
        for reflector in reflectors:
            assert isinstance(reflector, simscene.SimpleReflector)
            assert reflector.amplitude > 0
            # Position values should be reasonable (not NaN, not infinite)
            assert abs(reflector.x) < 1000
            assert abs(reflector.y) < 1000
            assert abs(reflector.z) < 1000


class TestSceneManipulation:
    """Test suite for scene manipulation."""

    def test_scene_with_single_reflector(self):
        """Test scene with single reflector."""
        reflector = simscene.SimpleReflector(0, 5, 0, 2.0)
        scene = simscene.SimulationScene()
        scene += reflector

        result = list(scene.get_simple_reflectors())
        assert len(result) == 1
        assert result[0] == reflector

    def test_scene_with_varying_amplitudes(self):
        """Test scene with reflectors of different amplitudes."""
        scene = simscene.SimulationScene()
        scene += simscene.SimpleReflector(0, 0, 0, 1.0)
        scene += simscene.SimpleReflector(1, 0, 0, 0.5)
        scene += simscene.SimpleReflector(2, 0, 0, 2.0)

        result = list(scene.get_simple_reflectors())
        assert len(result) == 3
        assert result[0].amplitude == 1.0
        assert result[1].amplitude == 0.5
        assert result[2].amplitude == 2.0

    def test_scene_with_3d_positions(self):
        """Test scene with reflectors at different heights."""
        scene = simscene.SimulationScene()
        scene += simscene.SimpleReflector(0, 5, 0, 1.0)      # Ground level
        scene += simscene.SimpleReflector(0, 5, 0.5, 1.0)    # Elevated
        scene += simscene.SimpleReflector(0, 5, -0.5, 1.0)   # Below ground

        result = list(scene.get_simple_reflectors())
        assert result[0].z == 0
        assert result[1].z == 0.5
        assert result[2].z == -0.5


class TestReflectorArrayScene:
    """Test suite for reflector array scene creation."""

    def test_create_reflector_array_basic(self):
        """Test creating a basic reflector array."""
        scene = simscene.create_reflector_array_scene(
            count_x=2,
            count_y=2,
            start_x=0.0,
            start_y=0.0,
            spacing_x=1.0,
            spacing_y=1.0,
            amplitude=1.0,
            z=0.0
        )

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) == 4  # 2x2 grid

    def test_create_reflector_array_single(self):
        """Test creating a single reflector array."""
        scene = simscene.create_reflector_array_scene(
            count_x=1,
            count_y=1,
            start_x=5.0,
            start_y=10.0,
            amplitude=2.0,
            z=1.0
        )

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) == 1
        assert reflectors[0].x == pytest.approx(5.0)
        assert reflectors[0].y == pytest.approx(10.0)
        assert reflectors[0].z == pytest.approx(1.0)
        assert reflectors[0].amplitude == pytest.approx(2.0)

    def test_create_reflector_array_positions(self):
        """Test that reflector array positions are correct."""
        scene = simscene.create_reflector_array_scene(
            count_x=3,
            count_y=2,
            start_x=0.0,
            start_y=0.0,
            spacing_x=0.5,
            spacing_y=0.5,
            amplitude=1.0
        )

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) == 6  # 3x2 grid

        # First reflector at start position
        assert reflectors[0].x == pytest.approx(0.0)
        assert reflectors[0].y == pytest.approx(0.0)

        # Second reflector in first column
        assert reflectors[1].x == pytest.approx(0.0)
        assert reflectors[1].y == pytest.approx(0.5)

        # First reflector in second column
        assert reflectors[2].x == pytest.approx(0.5)
        assert reflectors[2].y == pytest.approx(0.0)

    def test_create_reflector_array_with_defaults(self):
        """Test creating reflector array with default parameters."""
        scene = simscene.create_reflector_array_scene()

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) == 1  # Default is 1x1
        assert reflectors[0].amplitude == 1.0
        assert reflectors[0].z == 0.0

    def test_create_reflector_array_large(self):
        """Test creating a larger reflector array."""
        scene = simscene.create_reflector_array_scene(
            count_x=5,
            count_y=5,
            spacing_x=0.1,
            spacing_y=0.1
        )

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) == 25  # 5x5 grid

    def test_create_reflector_array_negative_start(self):
        """Test creating reflector array with negative start position."""
        scene = simscene.create_reflector_array_scene(
            count_x=2,
            count_y=2,
            start_x=-1.0,
            start_y=-1.0,
            spacing_x=1.0,
            spacing_y=1.0
        )

        reflectors = list(scene.get_simple_reflectors())
        assert len(reflectors) == 4
        assert reflectors[0].x == pytest.approx(-1.0)
        assert reflectors[0].y == pytest.approx(-1.0)


class TestSceneGeometry:
    """Test suite for scene geometry."""

    def test_reflector_positions(self):
        """Test reflector position coordinates."""
        reflector = simscene.SimpleReflector(
            x=1.5,
            y=2.5,
            z=0.5,
            amplitude=1.0
        )

        assert reflector.x == pytest.approx(1.5)
        assert reflector.y == pytest.approx(2.5)
        assert reflector.z == pytest.approx(0.5)

    def test_negative_coordinates(self):
        """Test reflectors with negative coordinates."""
        reflector = simscene.SimpleReflector(
            x=-1.0,
            y=-2.0,
            z=-0.5,
            amplitude=1.0
        )

        assert reflector.x == -1.0
        assert reflector.y == -2.0
        assert reflector.z == -0.5

    def test_origin_reflector(self):
        """Test reflector at origin."""
        reflector = simscene.SimpleReflector(0, 0, 0, 1.0)

        assert reflector.x == 0
        assert reflector.y == 0
        assert reflector.z == 0


# Run with: pytest tests/unit/test_simscene.py -v
