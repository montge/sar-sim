"""Unit tests for simulation state parameter management."""

import pytest
import tempfile
import os
from sarsim import simstate
from sarsim.operations import SUPPORTED_WINDOWS


class TestSimParameterType:
    """Test suite for SimParameterType."""

    def test_parse_string_float(self):
        """Test parsing float values."""
        param_type = simstate.SimParameterType(float)
        assert param_type.parse_string("3.14") == pytest.approx(3.14)
        assert param_type.parse_string("100") == pytest.approx(100.0)
        assert param_type.parse_string("-5.5") == pytest.approx(-5.5)

    def test_parse_string_int(self):
        """Test parsing integer values."""
        param_type = simstate.SimParameterType(int)
        assert param_type.parse_string("42") == 42
        assert param_type.parse_string("-10") == -10

    def test_parse_string_bool(self):
        """Test parsing boolean values."""
        param_type = simstate.SimParameterType(bool)

        # True values
        assert param_type.parse_string("true") is True
        assert param_type.parse_string("True") is True
        assert param_type.parse_string("yes") is True
        assert param_type.parse_string("1") is True

        # False values
        assert param_type.parse_string("false") is False
        assert param_type.parse_string("False") is False
        assert param_type.parse_string("no") is False
        assert param_type.parse_string("0") is False

    def test_parse_string_bool_invalid(self):
        """Test parsing invalid boolean values raises ValueError."""
        param_type = simstate.SimParameterType(bool)

        with pytest.raises(ValueError, match="Not a boolean"):
            param_type.parse_string("maybe")

    def test_parse_string_enum(self):
        """Test parsing enum/choice values."""
        choices = {"option1": 1, "option2": 2, "option3": 3}
        param_type = simstate.SimParameterType(int, choices=choices)

        assert param_type.parse_string("option1") == 1
        assert param_type.parse_string("option2") == 2
        assert param_type.parse_string("option3") == 3

    def test_parse_string_enum_invalid(self):
        """Test parsing invalid enum value raises KeyError."""
        choices = {"option1": 1, "option2": 2}
        param_type = simstate.SimParameterType(int, choices=choices)

        with pytest.raises(KeyError):
            param_type.parse_string("invalid")

    def test_stringify_basic(self):
        """Test converting values to strings."""
        param_type = simstate.SimParameterType(float)
        assert param_type.stringify(3.14) == "3.14"
        assert param_type.stringify(100.0) == "100.0"

    def test_stringify_enum(self):
        """Test converting enum values to strings."""
        choices = {"option1": 1, "option2": 2}
        param_type = simstate.SimParameterType(int, choices=choices)

        assert param_type.stringify(1) == "option1"
        assert param_type.stringify(2) == "option2"

    def test_stringify_enum_invalid(self):
        """Test converting invalid enum value raises ValueError."""
        choices = {"option1": 1, "option2": 2}
        param_type = simstate.SimParameterType(int, choices=choices)

        with pytest.raises(ValueError, match="not a valid choise"):
            param_type.stringify(999)


class TestSimParameter:
    """Test suite for SimParameter."""

    def test_parameter_creation(self):
        """Test creating a SimParameter."""
        param_type = simstate.SimParameterType(float, unit='Hz', min=0, max=1e9)
        param = simstate.SimParameter(
            type=param_type,
            name='test_frequency',
            symbol='f_test',
            default=1000.0,
            info='Test frequency parameter',
            category='Test'
        )

        assert param.name == 'test_frequency'
        assert param.symbol == 'f_test'
        assert param.default == 1000.0
        assert param.info == 'Test frequency parameter'
        assert param.category == 'Test'

    def test_human_name(self):
        """Test converting parameter name to human-readable format."""
        param_type = simstate.SimParameterType(float)
        param = simstate.SimParameter(param_type, 'fmcw_start_frequency', 'f1')

        assert param.human_name() == 'Fmcw Start Frequency'

    def test_str_representation(self):
        """Test string representation of parameter."""
        param_type = simstate.SimParameterType(float, unit='Hz')
        param = simstate.SimParameter(param_type, 'frequency', 'f')

        str_repr = str(param)
        assert 'frequency' in str_repr


class TestSarSimParameterState:
    """Test suite for SarSimParameterState."""

    def test_create_state(self):
        """Test creating a default state."""
        state = simstate.create_state()
        assert state is not None
        assert isinstance(state, simstate.SarSimParameterState)

    def test_default_values(self):
        """Test that parameters have correct default values."""
        state = simstate.create_state()

        # Test a few key defaults
        assert state.fmcw_start_frequency == 68e9
        assert state.fmcw_stop_frequency == 92e9
        assert state.azimuth_count == 201
        assert state.flight_height == 1.0
        assert state.signal_speed == simstate.suggested_c_speeds['Air']

    def test_get_set_value(self):
        """Test getting and setting parameter values."""
        state = simstate.create_state()
        params = state.get_parameters()

        # Find a specific parameter
        freq_param = next(p for p in params if p.name == 'fmcw_start_frequency')

        # Get value
        original = state.get_value(freq_param)
        assert original == 68e9

        # Set value
        state.set_value(freq_param, 70e9)
        assert state.get_value(freq_param) == 70e9

    def test_property_access(self):
        """Test accessing parameters as properties."""
        state = simstate.create_state()

        # Get via property
        freq = state.fmcw_start_frequency
        assert freq == 68e9

        # Set via property
        state.fmcw_start_frequency = 75e9
        assert state.fmcw_start_frequency == 75e9

    def test_get_parameters(self):
        """Test getting all parameters."""
        params = simstate.SarSimParameterState.get_parameters()

        assert len(params) > 0
        assert all(isinstance(p, simstate.SimParameter) for p in params)

        # Check some expected parameters exist
        param_names = [p.name for p in params]
        assert 'fmcw_start_frequency' in param_names
        assert 'azimuth_count' in param_names
        assert 'signal_speed' in param_names

    def test_window_parameter(self):
        """Test window type parameter."""
        state = simstate.create_state()

        # Default window
        assert state.range_compression_window == SUPPORTED_WINDOWS['Rect']

        # Change window
        state.range_compression_window = SUPPORTED_WINDOWS['Hann']
        assert state.range_compression_window == SUPPORTED_WINDOWS['Hann']

    def test_boolean_parameter(self):
        """Test boolean parameter."""
        state = simstate.create_state()

        # Default value
        assert state.enable_autofocus is False

        # Change value
        state.enable_autofocus = True
        assert state.enable_autofocus is True

    def test_parameter_categories(self):
        """Test that parameters have categories."""
        params = simstate.SarSimParameterState.get_parameters()

        categories = set(p.category for p in params if p.category)
        assert 'Acquisition' in categories
        assert 'Range Compression' in categories
        assert 'Azimuth Compression' in categories


class TestParameterPersistence:
    """Test suite for saving and loading parameter state."""

    def test_write_to_file(self):
        """Test writing state to file."""
        state = simstate.create_state()
        state.fmcw_start_frequency = 75e9
        state.azimuth_count = 150

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cfg') as f:
            filename = f.name

        try:
            state.write_to_file(filename)

            # Verify file exists and has content
            assert os.path.exists(filename)
            with open(filename, 'r') as f:
                content = f.read()
                assert 'fmcw_start_frequency' in content
                assert 'azimuth_count' in content
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_read_from_file(self):
        """Test reading state from file."""
        # Create and save a state
        state1 = simstate.create_state()
        state1.fmcw_start_frequency = 80e9
        state1.azimuth_count = 175
        state1.enable_autofocus = True

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cfg') as f:
            filename = f.name

        try:
            state1.write_to_file(filename)

            # Load the state
            state2 = simstate.SarSimParameterState.read_from_file(filename)

            assert state2.fmcw_start_frequency == 80e9
            assert state2.azimuth_count == 175
            assert state2.enable_autofocus is True
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_roundtrip_conversion(self):
        """Test that save and load preserves all values."""
        state1 = simstate.create_state()

        # Modify several parameters
        state1.fmcw_start_frequency = 77e9
        state1.fmcw_stop_frequency = 88e9
        state1.azimuth_count = 250
        state1.flight_height = 2.5
        state1.enable_autofocus = True
        state1.range_compression_window = SUPPORTED_WINDOWS['Hann']

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cfg') as f:
            filename = f.name

        try:
            state1.write_to_file(filename)
            state2 = simstate.SarSimParameterState.read_from_file(filename)

            # Verify all modified values match
            assert state2.fmcw_start_frequency == pytest.approx(77e9)
            assert state2.fmcw_stop_frequency == pytest.approx(88e9)
            assert state2.azimuth_count == 250
            assert state2.flight_height == pytest.approx(2.5)
            assert state2.enable_autofocus is True
            assert state2.range_compression_window == SUPPORTED_WINDOWS['Hann']
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_read_partial_file(self):
        """Test reading file with missing parameters uses defaults."""
        # Create minimal config file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cfg') as f:
            f.write("[params]\n")
            f.write("fmcw_start_frequency = 70000000000.0\n")
            filename = f.name

        try:
            state = simstate.SarSimParameterState.read_from_file(filename)

            # Modified parameter
            assert state.fmcw_start_frequency == pytest.approx(70e9)

            # Unspecified parameters should have defaults
            assert state.fmcw_stop_frequency == 92e9
            assert state.azimuth_count == 201
        finally:
            if os.path.exists(filename):
                os.unlink(filename)


class TestSimImage:
    """Test suite for SimImage."""

    def test_create_sim_image(self):
        """Test creating a SimImage."""
        import numpy as np

        data = np.zeros((100, 200))
        img = simstate.SimImage(
            data=data,
            x0=-1.0,
            y0=-2.0,
            dx=0.01,
            dy=0.02
        )

        assert img.data.shape == (100, 200)
        assert img.x0 == -1.0
        assert img.y0 == -2.0
        assert img.dx == 0.01
        assert img.dy == 0.02

    def test_sim_image_is_named_tuple(self):
        """Test that SimImage behaves as a NamedTuple."""
        import numpy as np

        data = np.ones((50, 50))
        img = simstate.SimImage(data, 0, 0, 0.1, 0.1)

        # Named tuple properties
        assert img[0] is data  # Access by index
        assert img.data is data  # Access by name
        assert len(img) == 5  # Has 5 fields


class TestParameterValidation:
    """Test suite for parameter range validation."""

    def test_parameter_ranges(self):
        """Test that parameters have reasonable ranges defined."""
        params = simstate.SarSimParameterState.get_parameters()

        # Find frequency parameter
        freq_param = next(p for p in params if p.name == 'fmcw_start_frequency')

        # Should have min and max
        assert freq_param.type.min is not None
        assert freq_param.type.max is not None
        assert freq_param.type.min < freq_param.type.max

    def test_count_parameter_ranges(self):
        """Test that count parameters have positive ranges."""
        params = simstate.SarSimParameterState.get_parameters()

        # Find count parameter
        count_param = next(p for p in params if p.name == 'azimuth_count')

        assert count_param.type.min >= 1
        assert count_param.type.max > count_param.type.min


class TestStubFileGeneration:
    """Test suite for stub file generation."""

    def test_write_stub_file(self):
        """Test generating a stub file for IDE support."""
        import tempfile
        import shutil
        import os

        # Create a temporary copy of the simstate module
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy simstate.py to temp directory
            temp_simstate = os.path.join(tmpdir, 'simstate_test.py')
            shutil.copy(simstate.__file__, temp_simstate)

            # Temporarily replace __file__ to point to our temp file
            original_file = simstate.__file__
            simstate.__file__ = temp_simstate

            try:
                # Call the stub file generator
                simstate.write_simstate_stub_file()

                # Check that stub file was created
                stub_file = temp_simstate + 'i'
                assert os.path.exists(stub_file), "Stub file should be created"

                # Read and verify stub file contents
                with open(stub_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Should contain auto-generated notice
                    assert 'Auto-Generated Stub File' in content
                    assert 'DO NOT EDIT THIS FILE DIRECTLY' in content

                    # Should contain dynamic properties section
                    assert 'BEGIN OF ADDED DYNAMIC PROPERTIES' in content
                    assert 'END OF ADDED DYNAMIC PROPERTIES' in content

                    # Should contain some parameter definitions
                    assert 'fmcw_start_frequency' in content
                    assert 'azimuth_count' in content

            finally:
                # Restore original __file__
                simstate.__file__ = original_file


# Run with: pytest tests/unit/test_simstate.py -v
