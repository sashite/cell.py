# cell.py

[![PyPI](https://img.shields.io/pypi/v/sashite-cell.svg)](https://pypi.org/project/sashite-cell/)
[![Python](https://img.shields.io/pypi/pyversions/sashite-cell.svg)](https://pypi.org/project/sashite-cell/)
[![License](https://img.shields.io/pypi/l/sashite-cell.svg)](https://github.com/sashite/cell.py/blob/main/LICENSE)

> **CELL** (Coordinate Encoding for Layered Locations) implementation for Python.

## Overview

This library implements the [CELL Specification v1.0.0](https://sashite.dev/specs/cell/1.0.0/).

### Implementation Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max dimensions | 3 | Sufficient for 1D, 2D, 3D boards |
| Max index value | 255 | Covers 256×256×256 boards |
| Max string length | 7 | `"iv256IV"` (max for all dimensions at 255) |

These constraints enable bounded memory usage, safe parsing, and protection against malicious input in networked applications.

## Installation

```bash
pip install sashite-cell
```

Or with uv:

```bash
uv add sashite-cell
```

## Usage

### Parsing (String → Coordinate)

Convert a CELL string into a `Coordinate` object.

```python
from sashite_cell import Coordinate

# Standard parsing (raises on error)
coord = Coordinate.parse("e4")
coord.indices     # => (4, 3)
coord.dimensions  # => 2

# 3D coordinate
coord = Coordinate.parse("a1A")
coord.indices  # => (0, 0, 0)

# Invalid input raises ValueError
Coordinate.parse("a0")  # => raises ValueError
```

### Formatting (Coordinate → String)

Convert a `Coordinate` back to a CELL string.

```python
# From Coordinate object
coord = Coordinate(4, 3)
str(coord)  # => "e4"

# Direct formatting (convenience)
Coordinate.format(2, 2, 2)  # => "c3C"
```

### Validation

```python
from sashite_cell import Coordinate

# Boolean check
Coordinate.is_valid("e4")  # => True
Coordinate.is_valid("a0")  # => False

# Detailed error
Coordinate.validate("a0")  # => raises ValueError("leading zero")
```

### Accessing Coordinate Data

```python
coord = Coordinate.parse("e4")

# Get dimensions count
coord.dimensions  # => 2

# Get indices as tuple
coord.indices  # => (4, 3)

# Access individual index
coord.indices[0]  # => 4
coord.indices[1]  # => 3

# Round-trip conversion
str(Coordinate.parse("e4"))  # => "e4"
```

## API Reference

### Types

```python
class Coordinate:
    """
    Represents a parsed CELL coordinate with up to 3 dimensions.

    Attributes:
        indices: Tuple of 0-indexed integers (0-255).
        dimensions: Number of dimensions (1, 2, or 3).
    """

    def __init__(self, *indices: int) -> None:
        """
        Creates a Coordinate from 1 to 3 indices.

        Args:
            *indices: 0-indexed coordinate values (0-255).

        Raises:
            ValueError: If no indices provided, more than 3, or out of range.
        """

    @property
    def dimensions(self) -> int:
        """Returns the number of dimensions (1, 2, or 3)."""

    @property
    def indices(self) -> tuple[int, ...]:
        """Returns the coordinate indices as a tuple."""

    def __str__(self) -> str:
        """Returns the CELL string representation."""

    def __repr__(self) -> str:
        """Returns a debug representation."""

    def __eq__(self, other: object) -> bool:
        """Compares two coordinates for equality."""

    def __hash__(self) -> int:
        """Returns hash for use in sets and dicts."""
```

### Constants

```python
Coordinate.MAX_DIMENSIONS: int = 3
Coordinate.MAX_INDEX_VALUE: int = 255
Coordinate.MAX_STRING_LENGTH: int = 7
```

### Parsing

```python
@classmethod
def parse(cls, string: str) -> "Coordinate":
    """
    Parses a CELL string into a Coordinate.

    Args:
        string: CELL coordinate string.

    Returns:
        Coordinate object.

    Raises:
        ValueError: If the string is not valid.
    """
```

### Formatting

```python
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
```

### Validation

```python
@classmethod
def validate(cls, string: str) -> None:
    """
    Validates a CELL string.

    Args:
        string: CELL coordinate string.

    Raises:
        ValueError: With descriptive message if invalid.
    """

@classmethod
def is_valid(cls, string: str) -> bool:
    """
    Reports whether string is a valid CELL coordinate.

    Args:
        string: CELL coordinate string.

    Returns:
        True if valid, False otherwise.
    """
```

### Errors

All parsing and validation errors raise `ValueError` with descriptive messages:

| Message | Cause |
|---------|-------|
| `"empty input"` | String length is 0 |
| `"input exceeds 7 characters"` | String too long |
| `"must start with lowercase letter"` | Invalid first character |
| `"unexpected character"` | Character violates the cyclic sequence |
| `"leading zero"` | Numeric part starts with '0' |
| `"exceeds 3 dimensions"` | More than 3 dimensions |
| `"index exceeds 255"` | Decoded value out of range |

## Design Principles

- **Bounded values**: Index validation (0-255) prevents overflow and DoS attacks
- **Input length limits**: Maximum 7 characters protects against malicious input
- **Object-oriented**: `Coordinate` class enables methods and encapsulation
- **Python idioms**: `is_valid()` predicate, `__str__` conversion, `ValueError` for invalid input
- **Immutable coordinates**: Tuple indices prevent mutation
- **Hashable**: Coordinates can be used in sets and as dict keys
- **Type hints**: Full type annotations for IDE support and static analysis
- **No dependencies**: Pure Python standard library only

## Related Specifications

- [Game Protocol](https://sashite.dev/game-protocol/) — Conceptual foundation
- [CELL Specification](https://sashite.dev/specs/cell/1.0.0/) — Official specification
- [CELL Examples](https://sashite.dev/specs/cell/1.0.0/examples/) — Usage examples

## License

Available as open source under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).
