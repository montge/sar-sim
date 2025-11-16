import re
from typing import Tuple

_SI_PREFIX = [
    (1e12, "T"),
    (1e9, "G"),
    (1e6, "M"),
    (1e3, "k"),
    (1, ""),
    (1e-3, "m"),
    (1e-6, "u"),
    (1e-9, "n"),
    (1e-12, "p"),
    (1e-15, "f"),
]

# Mapping from prefix character to scale factor
_PREFIX_TO_SCALE = {
    "T": 1e12,
    "G": 1e9,
    "M": 1e6,
    "k": 1e3,
    "m": 1e-3,
    "u": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
}


def choose_si_scale(value: float, unit: str = "") -> Tuple[float, str]:
    """
    Chooses a proper SI prefix for the given unit to represent a value.
    Then: Take the unscaled value, divide by factor to get scaled value.
    :param value: The unscaled numeric value to represent
    :param unit: The base unit without prefix or None to get only the prefix
    :return: Tuple of scale factor and prefixed unit
    """
    for factor, name in _SI_PREFIX:
        if value >= factor:
            return factor, f"{name}{unit}"
    return 1, unit


def scale_si_unit(value: float, unit: str = "") -> Tuple[float, str]:
    factor, unit = choose_si_scale(value, unit)
    return value / factor, unit


def format_si_unit(value: float, unit: str = "") -> str:
    value, unit = scale_si_unit(value, unit)
    return f"{value:.3f} {unit}"


def si_scale_parse(value_str: str) -> float:
    """
    Parse a string with SI prefix into a numeric value.

    Examples:
        "1k" -> 1000.0
        "2.5M" -> 2500000.0
        "500m" -> 0.5
        "42" -> 42.0

    :param value_str: String representation with optional SI prefix
    :return: Numeric value
    """
    # Match number (with optional sign and decimal) followed by optional SI prefix
    match = re.match(r"^([+-]?\d+\.?\d*)\s*([TGMkmnpfu]?)$", value_str.strip())

    if not match:
        raise ValueError(f"Invalid SI scaled value: {value_str}")

    number_str, prefix = match.groups()
    number = float(number_str)

    if prefix:
        scale = _PREFIX_TO_SCALE.get(prefix, 1.0)
        return number * scale

    return number


def si_scale_format(value: float, precision: int = 1) -> str:
    """
    Format a numeric value with appropriate SI prefix.

    Examples:
        1000.0 -> "1.0k"
        2500000.0 -> "2.5M"
        0.5 -> "500.0m"

    :param value: Numeric value to format
    :param precision: Number of decimal places (default 1)
    :return: Formatted string with SI prefix
    """
    abs_value = abs(value)

    # Handle zero specially
    if abs_value == 0:
        return f"{0:.{precision}f}"

    # Find appropriate prefix
    for factor, prefix in _SI_PREFIX:
        if factor == 1:  # Skip the no-prefix entry for now
            continue
        if abs_value >= factor:
            scaled = value / factor
            return f"{scaled:.{precision}f}{prefix}"

    # No prefix needed
    return f"{value:.{precision}f}"
