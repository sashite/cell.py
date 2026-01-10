"""CELL (Coordinate Encoding for Layered Locations) implementation for Python.

CELL is a standardized format for representing coordinates on multi-dimensional
game boards using a cyclical ASCII character system.

Format
------
CELL uses a cyclical three-character-set system:

| Dimension       | Condition | Character Set             |
|-----------------|-----------|---------------------------|
| 1st, 4th, 7th…  | n % 3 = 1 | Latin lowercase (`a`-`z`) |
| 2nd, 5th, 8th…  | n % 3 = 2 | Positive integers         |
| 3rd, 6th, 9th…  | n % 3 = 0 | Latin uppercase (`A`-`Z`) |

Examples
--------
>>> is_valid("a1")
True
>>> is_valid("a1A")
True
>>> parse("e4")
['e', '4']
>>> to_indices("e4")
(4, 3)
>>> from_indices((4, 3))
'e4'

See the `CELL Specification <https://sashite.dev/specs/cell/1.0.0/>`_ for details.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = [
    "dimensions",
    "from_indices",
    "is_valid",
    "parse",
    "regex",
    "to_indices",
]

# Regular expression from CELL Specification v1.0.0
# Note: Line breaks must be rejected separately (see is_valid)
_CELL_REGEX = re.compile(r"^[a-z]+(?:[1-9][0-9]*[A-Z]+[a-z]+)*(?:[1-9][0-9]*[A-Z]*)?$")

# Component extraction patterns
_LOWERCASE_REGEX = re.compile(r"^[a-z]+")
_NUMERIC_REGEX = re.compile(r"^[1-9][0-9]*")
_UPPERCASE_REGEX = re.compile(r"^[A-Z]+")


class _DimensionType(Enum):
    """Dimension type in the cyclical system."""

    LOWERCASE = 1
    NUMERIC = 2
    UPPERCASE = 3


# --- Validation ---


def is_valid(s: str) -> bool:
    """Check if a string represents a valid CELL coordinate.

    Implements full-string matching as required by the CELL specification.
    Rejects any input containing line breaks (``\\r`` or ``\\n``).

    Parameters
    ----------
    s : str
        The string to validate.

    Returns
    -------
    bool
        True if the string is a valid CELL coordinate, False otherwise.

    Examples
    --------
    >>> is_valid("a1")
    True
    >>> is_valid("a1A")
    True
    >>> is_valid("e4")
    True
    >>> is_valid("a0")
    False
    >>> is_valid("")
    False
    >>> is_valid("1a")
    False
    >>> is_valid("a1\\n")
    False
    """
    if not s or not isinstance(s, str):
        return False
    if "\r" in s or "\n" in s:
        return False
    return _CELL_REGEX.match(s) is not None


def regex() -> re.Pattern[str]:
    """Return the validation regular expression from CELL specification v1.0.0.

    Note: This regex alone does not guarantee full compliance. The :func:`is_valid`
    function additionally rejects strings containing line breaks, as required
    by the specification's anchoring requirements.

    Returns
    -------
    re.Pattern[str]
        The compiled regular expression pattern.

    Examples
    --------
    >>> regex().pattern
    '^[a-z]+(?:[1-9][0-9]*[A-Z]+[a-z]+)*(?:[1-9][0-9]*[A-Z]*)?$'
    """
    return _CELL_REGEX


# --- Parsing ---


def parse(s: str) -> list[str]:
    """Parse a CELL coordinate string into dimensional components.

    Parameters
    ----------
    s : str
        The CELL coordinate string to parse.

    Returns
    -------
    list[str]
        A list of dimensional components.

    Raises
    ------
    ValueError
        If the string is not a valid CELL coordinate.

    Examples
    --------
    >>> parse("a1")
    ['a', '1']
    >>> parse("a1A")
    ['a', '1', 'A']
    >>> parse("h8Hh8")
    ['h', '8', 'H', 'h', '8']
    >>> parse("foobar")
    ['foobar']
    >>> parse("invalid!")
    Traceback (most recent call last):
        ...
    ValueError: Invalid CELL coordinate: invalid!
    """
    if not is_valid(s):
        raise ValueError(f"Invalid CELL coordinate: {s}")
    return _parse_recursive(s, 1)


# --- Dimensional Analysis ---


def dimensions(s: str) -> int:
    """Return the number of dimensions in a CELL coordinate.

    Parameters
    ----------
    s : str
        The CELL coordinate string.

    Returns
    -------
    int
        The number of dimensions, or 0 for invalid coordinates.

    Examples
    --------
    >>> dimensions("a")
    1
    >>> dimensions("a1")
    2
    >>> dimensions("a1A")
    3
    >>> dimensions("h8Hh8")
    5
    >>> dimensions("1nvalid")
    0
    """
    if not is_valid(s):
        return 0
    return len(_parse_recursive(s, 1))


# --- Coordinate Conversion ---


def to_indices(s: str) -> tuple[int, ...]:
    """Convert a CELL coordinate to a tuple of 0-indexed integers.

    Parameters
    ----------
    s : str
        The CELL coordinate string.

    Returns
    -------
    tuple[int, ...]
        A tuple of 0-indexed integers.

    Raises
    ------
    ValueError
        If the string is not a valid CELL coordinate.

    Examples
    --------
    >>> to_indices("a1")
    (0, 0)
    >>> to_indices("e4")
    (4, 3)
    >>> to_indices("a1A")
    (0, 0, 0)
    >>> to_indices("z26Z")
    (25, 25, 25)
    >>> to_indices("aa1AA")
    (26, 0, 26)
    >>> to_indices("1nvalid")
    Traceback (most recent call last):
        ...
    ValueError: Invalid CELL coordinate: 1nvalid
    """
    components = parse(s)
    indices = []
    for i, component in enumerate(components):
        dimension = i + 1
        dim_type = _get_dimension_type(dimension)
        indices.append(_component_to_index(component, dim_type))
    return tuple(indices)


def from_indices(indices: Sequence[int]) -> str:
    """Convert a sequence of 0-indexed integers to a CELL coordinate.

    Parameters
    ----------
    indices : Sequence[int]
        A sequence of 0-indexed integers (tuple, list, etc.).

    Returns
    -------
    str
        The CELL coordinate string.

    Raises
    ------
    ValueError
        If the indices are empty, contain negative values, or would
        generate an invalid CELL coordinate.

    Examples
    --------
    >>> from_indices((0, 0))
    'a1'
    >>> from_indices((4, 3))
    'e4'
    >>> from_indices((0, 0, 0))
    'a1A'
    >>> from_indices((25, 25, 25))
    'z26Z'
    >>> from_indices((26, 0, 26))
    'aa1AA'
    >>> from_indices(())
    Traceback (most recent call last):
        ...
    ValueError: Cannot convert empty sequence to CELL coordinate
    >>> from_indices((-1, 0))
    Traceback (most recent call last):
        ...
    ValueError: Negative index not allowed: -1
    """
    if not indices:
        raise ValueError("Cannot convert empty sequence to CELL coordinate")

    parts = []
    for i, index in enumerate(indices):
        if index < 0:
            raise ValueError(f"Negative index not allowed: {index}")
        dimension = i + 1
        dim_type = _get_dimension_type(dimension)
        parts.append(_index_to_component(index, dim_type))

    result = "".join(parts)
    if not is_valid(result):
        raise ValueError(f"Generated invalid CELL coordinate: {result}")

    return result


# --- Private Functions ---


def _parse_recursive(s: str, dimension: int) -> list[str]:
    """Recursively parse a coordinate string into components.

    Follows the strict CELL specification cyclical pattern.
    """
    if not s:
        return []

    dim_type = _get_dimension_type(dimension)
    component, remaining = _extract_component(s, dim_type)
    if not component:
        return []

    return [component, *_parse_recursive(remaining, dimension + 1)]


def _get_dimension_type(dimension: int) -> _DimensionType:
    """Determine the character set type for a given dimension.

    Following CELL specification cyclical system: dimension n % 3 determines character set.
    """
    remainder = dimension % 3
    if remainder == 1:
        return _DimensionType.LOWERCASE
    elif remainder == 2:
        return _DimensionType.NUMERIC
    else:  # remainder == 0
        return _DimensionType.UPPERCASE


def _extract_component(s: str, dim_type: _DimensionType) -> tuple[str, str]:
    """Extract the next component from a string based on expected type."""
    if dim_type == _DimensionType.LOWERCASE:
        pattern = _LOWERCASE_REGEX
    elif dim_type == _DimensionType.NUMERIC:
        pattern = _NUMERIC_REGEX
    else:
        pattern = _UPPERCASE_REGEX

    match = pattern.match(s)
    if not match:
        return "", s
    component = match.group()
    return component, s[len(component) :]


def _component_to_index(component: str, dim_type: _DimensionType) -> int:
    """Convert a component to its 0-indexed position."""
    if dim_type == _DimensionType.LOWERCASE:
        return _letters_to_index(component)
    elif dim_type == _DimensionType.NUMERIC:
        return int(component) - 1
    else:  # UPPERCASE
        return _letters_to_index(component.lower())


def _index_to_component(index: int, dim_type: _DimensionType) -> str:
    """Convert a 0-indexed position to a component."""
    if dim_type == _DimensionType.LOWERCASE:
        return _index_to_letters(index)
    elif dim_type == _DimensionType.NUMERIC:
        return str(index + 1)
    else:  # UPPERCASE
        return _index_to_letters(index).upper()


def _letters_to_index(letters: str) -> int:
    """Convert a letter sequence to a 0-indexed position.

    Extended alphabet per CELL specification:
    a=0, b=1, ..., z=25, aa=26, ab=27, ..., zz=701, aaa=702, etc.
    """
    length = len(letters)

    # Add positions from shorter sequences
    base_offset: int = sum((26**exp for exp in range(1, length)), start=0)

    # Add position within current length
    position_in_length = 0
    for i, char in enumerate(letters):
        char_value = ord(char) - ord("a")
        place_value = 26 ** (length - i - 1)
        position_in_length += char_value * place_value

    return base_offset + position_in_length


def _index_to_letters(index: int) -> str:
    """Convert a 0-indexed position to a letter sequence.

    Extended alphabet per CELL specification:
    0=a, 1=b, ..., 25=z, 26=aa, 27=ab, ..., 701=zz, 702=aaa, etc.
    """
    # Find the length of the result
    length, base = _find_length_and_base(index)

    # Convert within the found length
    adjusted_index = index - base
    return _build_letters(adjusted_index, length)


def _find_length_and_base(index: int) -> tuple[int, int]:
    """Find the length and base offset for a given index."""
    length = 1
    base = 0
    while True:
        range_size = 26**length
        if index < base + range_size:
            return length, base
        base += range_size
        length += 1


def _build_letters(index: int, length: int) -> str:
    """Build the letter string from an adjusted index."""
    result = []
    for _ in range(length):
        result.append(chr(ord("a") + index % 26))
        index //= 26
    return "".join(reversed(result))
