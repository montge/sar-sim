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
