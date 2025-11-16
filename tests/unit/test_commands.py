"""Unit tests for commands module."""

import argparse
import os
import tempfile
from datetime import datetime
from io import StringIO
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from sarsim import commands, simscene, simstate


class TestCommandParsing:
    """Test suite for command parsing functionality."""

    def test_run_command_with_comment(self, capsys):
        """Test that comments are ignored."""
        pstate = create_test_pstate()
        commands.run_command("# This is a comment", pstate)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_run_command_with_empty_line(self, capsys):
        """Test that empty lines are ignored."""
        pstate = create_test_pstate()
        commands.run_command("", pstate)
        commands.run_command("   ", pstate)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_run_command_with_assignment(self):
        """Test parameter assignment."""
        pstate = create_test_pstate()
        initial_value = pstate.simstate.flight_height

        # Change the flight height parameter
        commands.run_command("flight_height=1500.0", pstate)

        assert pstate.simstate.flight_height != initial_value
        assert pstate.simstate.flight_height == 1500.0

    def test_run_command_with_unknown_parameter(self, capsys):
        """Test that unknown parameters are handled gracefully."""
        pstate = create_test_pstate()
        commands.run_command("unknown_param=123", pstate)

        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_run_command_with_action(self, capsys):
        """Test calling an action command."""
        pstate = create_test_pstate()
        commands.run_command("print_date", pstate)

        captured = capsys.readouterr()
        assert "Current Time:" in captured.out

    def test_run_command_with_action_and_params(self, capsys):
        """Test calling an action with parameters."""
        pstate = create_test_pstate()
        commands.run_command("echo test_message", pstate)

        captured = capsys.readouterr()
        assert "test_message" in captured.out

    def test_run_command_with_unknown_action(self, capsys):
        """Test that unknown actions are handled gracefully."""
        pstate = create_test_pstate()
        commands.run_command("unknown_action", pstate)

        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()


class TestScriptCommandDecorator:
    """Test suite for @script_command decorator."""

    def test_script_command_registers_function(self):
        """Test that decorator registers functions in commands dict."""
        # Check that known commands are registered
        assert "print_date" in commands.commands
        assert "echo" in commands.commands
        assert "run_sim" in commands.commands

    def test_script_command_callable(self):
        """Test that registered commands are callable."""
        pstate = create_test_pstate()

        # Should not raise an exception
        commands.commands["print_date"](pstate)

    def test_custom_script_command(self):
        """Test creating and using a custom script command."""

        @commands.script_command
        def test_command(pstate: commands.ProgramState):
            pstate.color_preset = "test_value"

        pstate = create_test_pstate()
        test_command(pstate)

        assert pstate.color_preset == "test_value"
        assert "test_command" in commands.commands


class TestPrintDateCommand:
    """Test suite for print_date command."""

    def test_print_date_output(self, capsys):
        """Test that print_date outputs current time."""
        pstate = create_test_pstate()
        commands.print_date(pstate)

        captured = capsys.readouterr()
        assert "Current Time:" in captured.out

        # Check that output contains year (as simple validation)
        current_year = str(datetime.now().year)
        assert current_year in captured.out


class TestEchoCommand:
    """Test suite for echo command."""

    def test_echo_simple_string(self, capsys):
        """Test echoing a simple string."""
        pstate = create_test_pstate()
        commands.echo(pstate, "Hello World")

        captured = capsys.readouterr()
        assert "Hello World" in captured.out

    def test_echo_empty_string(self, capsys):
        """Test echoing an empty string."""
        pstate = create_test_pstate()
        commands.echo(pstate, "")

        captured = capsys.readouterr()
        assert captured.out == "\n"


class TestColorPresetCommand:
    """Test suite for set_color_preset command."""

    def test_set_color_preset(self):
        """Test setting color preset."""
        pstate = create_test_pstate()
        assert pstate.color_preset == "jet"  # default

        commands.set_color_preset(pstate, "viridis")
        assert pstate.color_preset == "viridis"

    def test_set_color_preset_multiple_times(self):
        """Test changing color preset multiple times."""
        pstate = create_test_pstate()

        commands.set_color_preset(pstate, "plasma")
        assert pstate.color_preset == "plasma"

        commands.set_color_preset(pstate, "magma")
        assert pstate.color_preset == "magma"


class TestUnloadCaptureCommand:
    """Test suite for unload_capture command."""

    def test_unload_capture_clears_dataset(self):
        """Test that unload_capture clears loaded dataset."""
        pstate = create_test_pstate()
        pstate.loaded_dataset = MagicMock()  # Simulate loaded data

        commands.unload_capture(pstate)

        assert pstate.loaded_dataset is None

    def test_unload_capture_resets_simstate(self):
        """Test that unload_capture creates new simstate."""
        pstate = create_test_pstate()
        old_state = pstate.simstate

        # Modify state to verify it gets reset
        pstate.simstate.flight_height = 9999.0

        commands.unload_capture(pstate)

        # Should be a new state object
        assert pstate.simstate is not old_state
        assert pstate.simstate.flight_height != 9999.0


class TestParameterFileCommands:
    """Test suite for load_param_file and save_param_file commands."""

    def test_save_and_load_param_file(self):
        """Test saving and loading parameter file."""
        pstate = create_test_pstate()

        # Modify some parameters
        pstate.simstate.flight_height = 2500.0
        pstate.simstate.azimuth_count = 512

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_file = f.name

        try:
            # Save parameters
            commands.save_param_file(pstate, temp_file)
            assert os.path.exists(temp_file)

            # Create new state and load parameters
            pstate2 = create_test_pstate()
            commands.load_param_file(pstate2, temp_file)

            # Verify loaded parameters match
            assert pstate2.simstate.flight_height == 2500.0
            assert pstate2.simstate.azimuth_count == 512

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_load_param_file_replaces_state(self):
        """Test that loading param file replaces current state."""
        pstate = create_test_pstate()
        original_state = pstate.simstate

        # Modify and save
        pstate.simstate.flight_height = 3000.0

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_file = f.name

        try:
            commands.save_param_file(pstate, temp_file)

            # Create new state with different values
            pstate2 = create_test_pstate()
            pstate2.simstate.flight_height = 1000.0

            # Load should replace the state
            commands.load_param_file(pstate2, temp_file)

            assert pstate2.simstate.flight_height == 3000.0

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestExportNumpyHelper:
    """Test suite for _export_numpy helper function."""

    def test_export_numpy_creates_file(self):
        """Test that export_numpy creates a file."""
        data = np.array([[1, 2, 3], [4, 5, 6]])

        with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
            temp_file = f.name

        try:
            commands._export_numpy(temp_file, data)

            assert os.path.exists(temp_file)

            # Verify data can be loaded
            loaded = np.load(temp_file)
            np.testing.assert_array_equal(loaded, data)

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_export_numpy_overwrites_existing_file(self):
        """Test that export_numpy overwrites existing files."""
        data1 = np.array([1, 2, 3])
        data2 = np.array([4, 5, 6, 7, 8])

        with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
            temp_file = f.name

        try:
            # Save first data
            commands._export_numpy(temp_file, data1)
            size1 = os.path.getsize(temp_file)

            # Overwrite with second data
            commands._export_numpy(temp_file, data2)
            size2 = os.path.getsize(temp_file)

            # File sizes should differ
            assert size1 != size2

            # Loaded data should be the second dataset
            loaded = np.load(temp_file)
            np.testing.assert_array_equal(loaded, data2)

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestExportCommands:
    """Test suite for export commands."""

    def test_export_ac_numpy(self, capsys):
        """Test exporting azimuth compressed data."""
        pstate = create_test_pstate()

        # Mock simulation result
        ac_data = np.random.rand(100, 100)
        pstate.sim_result = MagicMock()
        pstate.sim_result.ac.data = ac_data

        with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
            temp_file = f.name

        try:
            commands.export_ac_numpy(pstate, temp_file)

            # Verify file exists and contains correct data
            assert os.path.exists(temp_file)
            loaded = np.load(temp_file)
            np.testing.assert_array_equal(loaded, ac_data)

            # Check output message
            captured = capsys.readouterr()
            assert "exported" in captured.out.lower()

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_export_af_numpy(self, capsys):
        """Test exporting autofocused data."""
        pstate = create_test_pstate()

        # Mock simulation result
        af_data = np.random.rand(100, 100)
        pstate.sim_result = MagicMock()
        pstate.sim_result.af.data = af_data

        with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
            temp_file = f.name

        try:
            commands.export_af_numpy(pstate, temp_file)

            # Verify file exists and contains correct data
            assert os.path.exists(temp_file)
            loaded = np.load(temp_file)
            np.testing.assert_array_equal(loaded, af_data)

            # Check output message
            captured = capsys.readouterr()
            assert "exported" in captured.out.lower()

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestProgramState:
    """Test suite for ProgramState dataclass."""

    def test_program_state_creation(self):
        """Test creating ProgramState."""
        args = argparse.Namespace(gui=False, gpu=0)
        state = simstate.create_state()
        scene = simscene.create_default_scene()

        pstate = commands.ProgramState(args, state, scene)

        assert pstate.args == args
        assert pstate.simstate == state
        assert pstate.scene == scene
        assert pstate.loaded_dataset is None
        assert pstate.sim_result is None
        assert pstate.color_preset == "jet"

    def test_program_state_with_custom_defaults(self):
        """Test ProgramState with custom default values."""
        args = argparse.Namespace(gui=True, gpu=1)
        state = simstate.create_state()
        scene = simscene.create_default_scene()

        pstate = commands.ProgramState(
            args=args, simstate=state, scene=scene, color_preset="viridis"
        )

        assert pstate.color_preset == "viridis"


# Helper function to create test ProgramState
def create_test_pstate():
    """Create a ProgramState for testing."""
    args = argparse.Namespace(gui=False, gpu=0)
    state = simstate.create_state()
    scene = simscene.create_default_scene()
    return commands.ProgramState(args, state, scene)


# Run with: pytest tests/unit/test_commands.py -v
