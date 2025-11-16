"""Unit tests for SI units conversion module."""

import pytest
from sarsim import siunits


class TestSIUnitConversions:
    """Test suite for SI unit conversion functions."""

    def test_si_scale_parse_basic(self):
        """Test parsing of basic SI scale values."""
        # Test with common prefixes
        assert siunits.si_scale_parse("1k") == pytest.approx(1000.0)
        assert siunits.si_scale_parse("1M") == pytest.approx(1e6)
        assert siunits.si_scale_parse("1G") == pytest.approx(1e9)

    def test_si_scale_parse_milli(self):
        """Test parsing of milli prefix."""
        assert siunits.si_scale_parse("1m") == pytest.approx(0.001)
        assert siunits.si_scale_parse("500m") == pytest.approx(0.5)

    def test_si_scale_parse_micro(self):
        """Test parsing of micro prefix."""
        assert siunits.si_scale_parse("1u") == pytest.approx(1e-6)
        assert siunits.si_scale_parse("100u") == pytest.approx(1e-4)

    def test_si_scale_parse_no_prefix(self):
        """Test parsing values without prefix."""
        assert siunits.si_scale_parse("42") == pytest.approx(42.0)
        assert siunits.si_scale_parse("3.14") == pytest.approx(3.14)

    def test_si_scale_parse_negative(self):
        """Test parsing negative values."""
        assert siunits.si_scale_parse("-1k") == pytest.approx(-1000.0)
        assert siunits.si_scale_parse("-5M") == pytest.approx(-5e6)

    def test_si_scale_parse_decimal(self):
        """Test parsing decimal values with prefix."""
        assert siunits.si_scale_parse("1.5k") == pytest.approx(1500.0)
        assert siunits.si_scale_parse("2.5M") == pytest.approx(2.5e6)

    def test_si_scale_format_basic(self):
        """Test formatting of basic values."""
        assert siunits.si_scale_format(1000.0) == "1.0k"
        assert siunits.si_scale_format(1e6) == "1.0M"
        assert siunits.si_scale_format(1e9) == "1.0G"

    def test_si_scale_format_small(self):
        """Test formatting of small values."""
        assert siunits.si_scale_format(0.001) == "1.0m"
        assert siunits.si_scale_format(1e-6) == "1.0u"

    def test_si_scale_format_precision(self):
        """Test formatting with different precision."""
        # Default precision
        result = siunits.si_scale_format(1234.0)
        assert "k" in result

        # Should handle values that need rounding
        result = siunits.si_scale_format(1234567.89)
        assert "M" in result

    def test_roundtrip_conversion(self):
        """Test that parse(format(x)) approximately equals x."""
        test_values = [1.0, 10.0, 100.0, 1000.0, 1e6, 1e9, 0.001, 1e-6]

        for value in test_values:
            formatted = siunits.si_scale_format(value)
            parsed = siunits.si_scale_parse(formatted)
            assert parsed == pytest.approx(value, rel=1e-3)

    def test_si_scale_parse_invalid_format(self):
        """Test parsing of invalid format strings."""
        with pytest.raises(ValueError, match="Invalid SI scaled value"):
            siunits.si_scale_parse("abc")

        with pytest.raises(ValueError, match="Invalid SI scaled value"):
            siunits.si_scale_parse("12.3.4k")

        with pytest.raises(ValueError, match="Invalid SI scaled value"):
            siunits.si_scale_parse("k100")

    def test_si_scale_format_zero(self):
        """Test formatting zero value."""
        assert siunits.si_scale_format(0.0) == "0.0"
        assert siunits.si_scale_format(0.0, precision=2) == "0.00"

    def test_si_scale_format_very_small(self):
        """Test formatting values smaller than smallest prefix."""
        # Values smaller than femto (1e-15) should not get a prefix
        result = siunits.si_scale_format(1e-16)
        assert "f" not in result  # No femto prefix for values < 1e-15

    def test_si_scale_format_negative(self):
        """Test formatting negative values."""
        assert siunits.si_scale_format(-1000.0) == "-1.0k"
        assert siunits.si_scale_format(-0.001) == "-1.0m"

    def test_si_scale_format_custom_precision(self):
        """Test formatting with custom precision."""
        assert siunits.si_scale_format(1234.5, precision=2) == "1.23k"
        assert siunits.si_scale_format(1234.5, precision=0) == "1k"


class TestChooseSiScale:
    """Test suite for choose_si_scale function."""

    def test_choose_si_scale_basic(self):
        """Test choosing SI scale for basic values."""
        factor, unit = siunits.choose_si_scale(1000.0, "m")
        assert factor == 1e3
        assert unit == "km"

    def test_choose_si_scale_mega(self):
        """Test choosing mega scale."""
        factor, unit = siunits.choose_si_scale(1e6, "Hz")
        assert factor == 1e6
        assert unit == "MHz"

    def test_choose_si_scale_milli(self):
        """Test choosing milli scale."""
        factor, unit = siunits.choose_si_scale(0.001, "s")
        assert factor == 1e-3
        assert unit == "ms"

    def test_choose_si_scale_no_unit(self):
        """Test choosing scale without unit."""
        factor, prefix = siunits.choose_si_scale(1000.0, "")
        assert factor == 1e3
        assert prefix == "k"

    def test_choose_si_scale_small_value(self):
        """Test choosing scale for small value (sub-unit)."""
        # 0.5 is < 1, so it gets milli prefix
        factor, unit = siunits.choose_si_scale(0.5, "V")
        assert factor == 1e-3
        assert unit == "mV"

    def test_choose_si_scale_value_near_one(self):
        """Test choosing scale for value near 1."""
        # Values >= 1 but < 1000 should get no prefix
        factor, unit = siunits.choose_si_scale(50.0, "V")
        assert factor == 1
        assert unit == "V"


class TestScaleSiUnit:
    """Test suite for scale_si_unit function."""

    def test_scale_si_unit_basic(self):
        """Test scaling basic values."""
        value, unit = siunits.scale_si_unit(1000.0, "m")
        assert value == pytest.approx(1.0)
        assert unit == "km"

    def test_scale_si_unit_mega(self):
        """Test scaling to mega."""
        value, unit = siunits.scale_si_unit(2.5e6, "Hz")
        assert value == pytest.approx(2.5)
        assert unit == "MHz"

    def test_scale_si_unit_milli(self):
        """Test scaling to milli."""
        value, unit = siunits.scale_si_unit(0.005, "s")
        assert value == pytest.approx(5.0)
        assert unit == "ms"


class TestFormatSiUnit:
    """Test suite for format_si_unit function."""

    def test_format_si_unit_basic(self):
        """Test formatting with unit."""
        result = siunits.format_si_unit(1000.0, "m")
        assert result == "1.000 km"

    def test_format_si_unit_mega(self):
        """Test formatting mega values."""
        result = siunits.format_si_unit(2.5e6, "Hz")
        assert result == "2.500 MHz"

    def test_format_si_unit_milli(self):
        """Test formatting milli values."""
        result = siunits.format_si_unit(0.005, "s")
        assert result == "5.000 ms"

    def test_format_si_unit_no_prefix_needed(self):
        """Test formatting when no prefix needed."""
        result = siunits.format_si_unit(50.0, "V")
        assert result == "50.000 V"


class TestRangeUtilities:
    """Test suite for range-related utility functions."""

    def test_range_in_bounds(self):
        """Test that values within range are accepted."""
        # This test assumes there's a range validation function
        # Adapt based on actual implementation
        pass

    def test_range_out_of_bounds(self):
        """Test that out-of-range values are rejected."""
        # This test assumes there's a range validation function
        # Adapt based on actual implementation
        pass


# Example of how to run specific tests:
# pytest tests/unit/test_siunits.py -v
# pytest tests/unit/test_siunits.py::TestSIUnitConversions::test_si_scale_parse_basic
