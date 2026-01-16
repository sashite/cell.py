"""
Constants for CELL (Coordinate Encoding for Layered Locations).

This module defines the implementation constraints for CELL coordinates.
"""

from typing import Final

# Maximum number of dimensions supported by a CELL coordinate.
# Sufficient for 1D, 2D, and 3D game boards.
MAX_DIMENSIONS: Final[int] = 3

# Maximum value for a single coordinate index.
# Fits in an 8-bit unsigned integer (0-255).
MAX_INDEX_VALUE: Final[int] = 255

# Maximum length of a CELL string representation.
# Corresponds to "iv256IV" (worst case for all dimensions at 255).
MAX_STRING_LENGTH: Final[int] = 7
