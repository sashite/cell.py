"""
Coordinate class for CELL (Coordinate Encoding for Layered Locations).

This module provides the core Coordinate type that delegates parsing
and formatting to specialized modules.
"""

from __future__ import annotations

from typing import Final

from sashite_cell.formatter import format_indices
from sashite_cell.parser import parse_to_indices


class Coordinate:
    """
    Represents a parsed CELL coordinate with up to 3 dimensions.

    A Coordinate holds 0-indexed integer values for each dimension.
    Coordinates are immutable and hashable.

    Example:
        >>> coord = Coordinate(4, 3)
        >>> coord.indices
        (4, 3)
        >>> str(coord)
        'e4'
    """

    MAX_DIMENSIONS: Final[int] = 3
    MAX_INDEX_VALUE: Final[int] = 255
    MAX_STRING_LENGTH: Final[int] = 7

    __slots__ = ("_indices",)

    def __init__(self, *indices: int) -> None:
        """
        Creates a Coordinate from 1 to 3 indices.

        Args:
            *indices: 0-indexed coordinate values (0-255).

        Raises:
            ValueError: If no indices provided, more than 3, or out of range.
        """
        if not indices:
            raise ValueError("at least one index required")

        if len(indices) > self.MAX_DIMENSIONS:
            raise ValueError(f"exceeds {self.MAX_DIMENSIONS} dimensions")

        for i, index in enumerate(indices):
            if not isinstance(index, int) or isinstance(index, bool):
                raise ValueError(f"index {i} must be an integer")
            if index < 0 or index > self.MAX_INDEX_VALUE:
                raise ValueError(f"index {i} exceeds {self.MAX_INDEX_VALUE}")

        self._indices: tuple[int, ...] = tuple(indices)

    @property
    def indices(self) -> tuple[int, ...]:
        """Returns the coordinate indices as a tuple."""
        return self._indices

    @property
    def dimensions(self) -> int:
        """Returns the number of dimensions (1, 2, or 3)."""
        return len(self._indices)

    def __str__(self) -> str:
        """Returns the CELL string representation."""
        return format_indices(self._indices)

    def __repr__(self) -> str:
        """Returns a debug representation."""
        indices_str = ", ".join(str(i) for i in self._indices)
        return f"Coordinate({indices_str})"

    def __eq__(self, other: object) -> bool:
        """Compares two coordinates for equality."""
        if not isinstance(other, Coordinate):
            return NotImplemented
        return self._indices == other._indices

    def __hash__(self) -> int:
        """Returns hash for use in sets and dicts."""
        return hash(self._indices)

    @classmethod
    def parse(cls, string: str) -> Coordinate:
        """
        Parses a CELL string into a Coordinate.

        Args:
            string: CELL coordinate string.

        Returns:
            Coordinate object.

        Raises:
            ValueError: If the string is not valid.
        """
        indices = parse_to_indices(string)
        return cls(*indices)

    @classmethod
    def format(cls, *indices: int) -> str:
        """
        Formats indices into a CELL string.

        Convenience method equivalent to str(Coordinate(*indices)).

        Args:
            *indices: 0-indexed coordinate values.

        Returns:
            CELL string representation.

        Raises:
            ValueError: If indices are invalid.
        """
        return str(cls(*indices))

    @classmethod
    def validate(cls, string: str) -> None:
        """
        Validates a CELL string.

        Args:
            string: CELL coordinate string.

        Raises:
            ValueError: With descriptive message if invalid.
        """
        parse_to_indices(string)

    @classmethod
    def is_valid(cls, string: str) -> bool:
        """
        Reports whether string is a valid CELL coordinate.

        Args:
            string: CELL coordinate string.

        Returns:
            True if valid, False otherwise.
        """
        try:
            parse_to_indices(string)
            return True
        except ValueError:
            return False
