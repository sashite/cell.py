"""
Formatter for CELL coordinates.

This module converts index tuples to CELL string representations.
"""

from __future__ import annotations


def format_indices(indices: tuple[int, ...]) -> str:
    """
    Format indices tuple to CELL string.

    Args:
        indices: Tuple of 0-indexed integers (already validated).

    Returns:
        CELL string representation.

    Example:
        >>> format_indices((4, 3))
        'e4'
        >>> format_indices((0, 0, 0))
        'a1A'
    """
    parts: list[str] = []

    for i, index in enumerate(indices):
        dimension_type = i % 3

        if dimension_type == 0:
            # Dimensions 1, 4, 7... -> lowercase letters
            parts.append(_index_to_letters(index, lowercase=True))
        elif dimension_type == 1:
            # Dimensions 2, 5, 8... -> positive integers (1-indexed)
            parts.append(str(index + 1))
        else:
            # Dimensions 3, 6, 9... -> uppercase letters
            parts.append(_index_to_letters(index, lowercase=False))

    return "".join(parts)


def _index_to_letters(index: int, *, lowercase: bool) -> str:
    """
    Convert 0-indexed integer to letter sequence.

    0 -> 'a', 25 -> 'z', 26 -> 'aa', 27 -> 'ab', etc.

    Args:
        index: 0-indexed integer value.
        lowercase: If True, return lowercase letters; otherwise uppercase.

    Returns:
        Letter sequence representing the index.
    """
    result: list[str] = []
    value = index + 1  # Convert to 1-indexed for calculation

    while value > 0:
        value, remainder = divmod(value - 1, 26)
        char = chr(ord("a") + remainder)
        result.append(char)

    letters = "".join(reversed(result))
    return letters if lowercase else letters.upper()
