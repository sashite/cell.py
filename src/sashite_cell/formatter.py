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
            parts.append(_encode_to_lower(index))
        elif dimension_type == 1:
            parts.append(_encode_to_number(index))
        else:
            parts.append(_encode_to_upper(index))

    return "".join(parts)


def _encode_to_lower(index: int) -> str:
    """
    Encode index (0-255) as lowercase letters (a-z, aa-iv).

    Args:
        index: 0-indexed value (0-255).

    Returns:
        Lowercase letter sequence.

    Example:
        >>> _encode_to_lower(0)
        'a'
        >>> _encode_to_lower(25)
        'z'
        >>> _encode_to_lower(26)
        'aa'
        >>> _encode_to_lower(255)
        'iv'
    """
    return _encode_to_letters(index, base=ord("a"))


def _encode_to_upper(index: int) -> str:
    """
    Encode index (0-255) as uppercase letters (A-Z, AA-IV).

    Args:
        index: 0-indexed value (0-255).

    Returns:
        Uppercase letter sequence.

    Example:
        >>> _encode_to_upper(0)
        'A'
        >>> _encode_to_upper(25)
        'Z'
        >>> _encode_to_upper(26)
        'AA'
        >>> _encode_to_upper(255)
        'IV'
    """
    return _encode_to_letters(index, base=ord("A"))


def _encode_to_letters(index: int, base: int) -> str:
    """
    Encode index to letter sequence.

    Args:
        index: 0-indexed value (0-255).
        base: Base character code (ord('a') or ord('A')).

    Returns:
        Letter sequence.
    """
    if index < 26:
        return chr(base + index)
    else:
        adjusted = index - 26
        first = adjusted // 26
        second = adjusted % 26
        return chr(base + first) + chr(base + second)


def _encode_to_number(index: int) -> str:
    """
    Encode index (0-255) as 1-based positive integer string.

    Args:
        index: 0-indexed value (0-255).

    Returns:
        Number string (1-indexed).

    Example:
        >>> _encode_to_number(0)
        '1'
        >>> _encode_to_number(255)
        '256'
    """
    return str(index + 1)
