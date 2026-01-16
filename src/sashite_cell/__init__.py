"""
CELL (Coordinate Encoding for Layered Locations) implementation for Python.

This library implements the CELL Specification v1.0.0.
See: https://sashite.dev/specs/cell/1.0.0/

Example usage:
    >>> from sashite_cell import Coordinate
    >>> coord = Coordinate.parse("e4")
    >>> coord.indices
    (4, 3)
    >>> str(coord)
    'e4'

Constants are available in the constants module:
    >>> from sashite_cell.constants import MAX_DIMENSIONS, MAX_INDEX_VALUE
"""

from sashite_cell.coordinate import Coordinate

__all__ = ["Coordinate"]
__version__ = "3.0.0"
