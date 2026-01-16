"""
Parser for CELL coordinates.

This module converts CELL string representations to index tuples.

Security considerations:
- Character-by-character parsing (no regex, no ReDoS risk)
- Fail-fast on invalid input
- Bounded iteration (max 7 characters)
- Explicit ASCII validation
"""

from __future__ import annotations

from sashite_cell.constants import MAX_DIMENSIONS, MAX_INDEX_VALUE, MAX_STRING_LENGTH
from sashite_cell.errors import Messages


def parse_to_indices(string: str) -> tuple[int, ...]:
    """
    Parse a CELL string into a tuple of indices.

    Args:
        string: CELL coordinate string.

    Returns:
        Tuple of 0-indexed integers.

    Raises:
        ValueError: With descriptive message if invalid.

    Example:
        >>> parse_to_indices("e4")
        (4, 3)
        >>> parse_to_indices("a1A")
        (0, 0, 0)
    """
    if not string:
        raise ValueError(Messages.EMPTY_INPUT)

    if len(string) > MAX_STRING_LENGTH:
        raise ValueError(Messages.INPUT_TOO_LONG)

    first_char = string[0]
    if not _is_lowercase(first_char):
        raise ValueError(Messages.INVALID_START)

    indices: list[int] = []
    pos = 0
    dimension_type = 0  # 0: lowercase, 1: integer, 2: uppercase

    while pos < len(string):
        if len(indices) >= MAX_DIMENSIONS:
            raise ValueError(Messages.TOO_MANY_DIMENSIONS)

        if dimension_type == 0:
            value, consumed = _parse_lowercase(string, pos)
            indices.append(value)
            pos += consumed
            dimension_type = 1
        elif dimension_type == 1:
            value, consumed = _parse_integer(string, pos)
            indices.append(value)
            pos += consumed
            dimension_type = 2
        else:
            value, consumed = _parse_uppercase(string, pos)
            indices.append(value)
            pos += consumed
            dimension_type = 0

    return tuple(indices)


def _is_lowercase(char: str) -> bool:
    """Check if character is ASCII lowercase letter (a-z)."""
    return len(char) == 1 and "a" <= char <= "z"


def _is_uppercase(char: str) -> bool:
    """Check if character is ASCII uppercase letter (A-Z)."""
    return len(char) == 1 and "A" <= char <= "Z"


def _is_digit(char: str) -> bool:
    """Check if character is ASCII digit (0-9)."""
    return len(char) == 1 and "0" <= char <= "9"


def _parse_lowercase(string: str, pos: int) -> tuple[int, int]:
    """
    Parse lowercase letters starting at position.

    Args:
        string: Input string.
        pos: Starting position.

    Returns:
        Tuple of (decoded_value, characters_consumed).

    Raises:
        ValueError: If parsing fails.
    """
    if pos >= len(string) or not _is_lowercase(string[pos]):
        raise ValueError(Messages.UNEXPECTED_CHARACTER)

    end = pos
    while end < len(string) and _is_lowercase(string[end]):
        end += 1

    value = _decode_lowercase(string[pos:end])
    if value > MAX_INDEX_VALUE:
        raise ValueError(Messages.INDEX_OUT_OF_RANGE)

    return value, end - pos


def _parse_integer(string: str, pos: int) -> tuple[int, int]:
    """
    Parse positive integer starting at position.

    Args:
        string: Input string.
        pos: Starting position.

    Returns:
        Tuple of (decoded_value, characters_consumed).

    Raises:
        ValueError: If parsing fails.
    """
    if pos >= len(string) or not _is_digit(string[pos]):
        raise ValueError(Messages.UNEXPECTED_CHARACTER)

    if string[pos] == "0":
        raise ValueError(Messages.LEADING_ZERO)

    end = pos
    while end < len(string) and _is_digit(string[end]):
        end += 1

    value = _decode_integer(string[pos:end])
    if value < 0 or value > MAX_INDEX_VALUE:
        raise ValueError(Messages.INDEX_OUT_OF_RANGE)

    return value, end - pos


def _parse_uppercase(string: str, pos: int) -> tuple[int, int]:
    """
    Parse uppercase letters starting at position.

    Args:
        string: Input string.
        pos: Starting position.

    Returns:
        Tuple of (decoded_value, characters_consumed).

    Raises:
        ValueError: If parsing fails.
    """
    if pos >= len(string) or not _is_uppercase(string[pos]):
        raise ValueError(Messages.UNEXPECTED_CHARACTER)

    end = pos
    while end < len(string) and _is_uppercase(string[end]):
        end += 1

    value = _decode_uppercase(string[pos:end])
    if value > MAX_INDEX_VALUE:
        raise ValueError(Messages.INDEX_OUT_OF_RANGE)

    return value, end - pos


def _decode_lowercase(segment: str) -> int:
    """
    Decode lowercase letter segment to index.

    Args:
        segment: Lowercase letter sequence.

    Returns:
        Decoded index (0-255).

    Example:
        >>> _decode_lowercase("a")
        0
        >>> _decode_lowercase("z")
        25
        >>> _decode_lowercase("aa")
        26
        >>> _decode_lowercase("iv")
        255
    """
    if len(segment) == 1:
        return ord(segment[0]) - ord("a")
    else:
        first = ord(segment[0]) - ord("a")
        second = ord(segment[1]) - ord("a")
        return 26 + (first * 26) + second


def _decode_uppercase(segment: str) -> int:
    """
    Decode uppercase letter segment to index.

    Args:
        segment: Uppercase letter sequence.

    Returns:
        Decoded index (0-255).

    Example:
        >>> _decode_uppercase("A")
        0
        >>> _decode_uppercase("Z")
        25
        >>> _decode_uppercase("AA")
        26
        >>> _decode_uppercase("IV")
        255
    """
    if len(segment) == 1:
        return ord(segment[0]) - ord("A")
    else:
        first = ord(segment[0]) - ord("A")
        second = ord(segment[1]) - ord("A")
        return 26 + (first * 26) + second


def _decode_integer(segment: str) -> int:
    """
    Decode digit segment to index (1-based to 0-based).

    Args:
        segment: Digit sequence.

    Returns:
        Decoded index (0-255).

    Example:
        >>> _decode_integer("1")
        0
        >>> _decode_integer("256")
        255
    """
    return int(segment) - 1
