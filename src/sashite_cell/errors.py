"""
Error messages for CELL (Coordinate Encoding for Layered Locations).

This module defines the error messages used during parsing and validation.
All parsing and validation errors raise ValueError with these messages.
"""

from typing import Final


class Messages:
    """Error messages for validation failures."""

    EMPTY_INPUT: Final[str] = "empty input"
    INPUT_TOO_LONG: Final[str] = "input exceeds 7 characters"
    INVALID_START: Final[str] = "must start with lowercase letter"
    UNEXPECTED_CHARACTER: Final[str] = "unexpected character"
    LEADING_ZERO: Final[str] = "leading zero"
    TOO_MANY_DIMENSIONS: Final[str] = "exceeds 3 dimensions"
    INDEX_OUT_OF_RANGE: Final[str] = "index exceeds 255"
    NO_INDICES: Final[str] = "at least one index required"
    INVALID_INDEX_TYPE: Final[str] = "index must be an integer"
