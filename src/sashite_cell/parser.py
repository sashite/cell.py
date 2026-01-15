"""
Parser for CELL coordinates.

This module converts CELL string representations to index tuples.
"""

from __future__ import annotations

MAX_DIMENSIONS: int = 3
MAX_INDEX_VALUE: int = 255
MAX_STRING_LENGTH: int = 7


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
    if not isinstance(string, str):
        raise ValueError("input must be a string")

    if not string:
        raise ValueError("empty input")

    if len(string) > MAX_STRING_LENGTH:
        raise ValueError(f"input exceeds {MAX_STRING_LENGTH} characters")

    indices: list[int] = []
    pos = 0

    while pos < len(string):
        dimension_type = len(indices) % 3

        if dimension_type == 0:
            # Dimensions 1, 4, 7... -> lowercase letters
            index, consumed = _parse_lowercase(string, pos)
        elif dimension_type == 1:
            # Dimensions 2, 5, 8... -> positive integers
            index, consumed = _parse_integer(string, pos)
        else:
            # Dimensions 3, 6, 9... -> uppercase letters
            index, consumed = _parse_uppercase(string, pos)

        indices.append(index)
        pos += consumed

        if len(indices) > MAX_DIMENSIONS:
            raise ValueError(f"exceeds {MAX_DIMENSIONS} dimensions")

    return tuple(indices)


def _parse_lowercase(string: str, pos: int) -> tuple[int, int]:
    """
    Parse lowercase letter sequence starting at pos.

    Args:
        string: Input string.
        pos: Starting position.

    Returns:
        Tuple of (index, characters_consumed).

    Raises:
        ValueError: If no lowercase letter found or index out of range.
    """
    if pos >= len(string):
        raise ValueError("must start with lowercase letter")

    char = string[pos]
    if not (char.isascii() and char.islower()):
        raise ValueError("must start with lowercase letter")

    end = pos
    while end < len(string):
        char = string[end]
        if not (char.isascii() and char.islower()):
            break
        end += 1

    segment = string[pos:end]
    index = _letters_to_index(segment)

    if index > MAX_INDEX_VALUE:
        raise ValueError(f"index exceeds {MAX_INDEX_VALUE}")

    return index, end - pos


def _parse_integer(string: str, pos: int) -> tuple[int, int]:
    """
    Parse integer sequence starting at pos.

    Args:
        string: Input string.
        pos: Starting position.

    Returns:
        Tuple of (index, characters_consumed).

    Raises:
        ValueError: If invalid integer format or index out of range.
    """
    if pos >= len(string) or not (string[pos].isascii() and string[pos].isdigit()):
        raise ValueError("unexpected character")

    if string[pos] == "0":
        raise ValueError("leading zero")

    end = pos
    while end < len(string) and string[end].isascii() and string[end].isdigit():
        end += 1

    segment = string[pos:end]
    value = int(segment)
    index = value - 1  # Convert to 0-indexed

    if index < 0 or index > MAX_INDEX_VALUE:
        raise ValueError(f"index exceeds {MAX_INDEX_VALUE}")

    return index, end - pos


def _parse_uppercase(string: str, pos: int) -> tuple[int, int]:
    """
    Parse uppercase letter sequence starting at pos.

    Args:
        string: Input string.
        pos: Starting position.

    Returns:
        Tuple of (index, characters_consumed).

    Raises:
        ValueError: If no uppercase letter found or index out of range.
    """
    if pos >= len(string):
        raise ValueError("unexpected character")

    char = string[pos]
    if not (char.isascii() and char.isupper()):
        raise ValueError("unexpected character")

    end = pos
    while end < len(string):
        char = string[end]
        if not (char.isascii() and char.isupper()):
            break
        end += 1

    segment = string[pos:end]
    index = _letters_to_index(segment.lower())

    if index > MAX_INDEX_VALUE:
        raise ValueError(f"index exceeds {MAX_INDEX_VALUE}")

    return index, end - pos


def _letters_to_index(letters: str) -> int:
    """
    Convert letter sequence to 0-indexed integer.

    'a' -> 0, 'z' -> 25, 'aa' -> 26, 'ab' -> 27, etc.

    Args:
        letters: Lowercase letter sequence.

    Returns:
        0-indexed integer value.
    """
    index = 0
    for char in letters:
        index = index * 26 + (ord(char) - ord("a") + 1)
    return index - 1
