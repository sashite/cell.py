# cell.py

[![PyPI](https://img.shields.io/pypi/v/sashite-cell.svg)](https://pypi.org/project/sashite-cell/)
[![Python](https://img.shields.io/pypi/pyversions/sashite-cell.svg)](https://pypi.org/project/sashite-cell/)
[![License](https://img.shields.io/pypi/l/sashite-cell.svg)](https://github.com/sashite/cell.py/blob/main/LICENSE)

> **CELL** (Coordinate Encoding for Layered Locations) implementation for Python.

## What is CELL?

CELL (Coordinate Encoding for Layered Locations) is a standardized format for representing coordinates on multi-dimensional game boards using a cyclical ASCII character system. CELL supports unlimited dimensional coordinate systems through the systematic repetition of three distinct character sets.

This library implements the [CELL Specification v1.0.0](https://sashite.dev/specs/cell/1.0.0/).

## Installation

```bash
pip install sashite-cell
```

Or with uv:

```bash
uv add sashite-cell
```

## CELL Format

CELL uses a cyclical three-character-set system that repeats indefinitely based on dimensional position:

| Dimension | Condition | Character Set | Examples |
|-----------|-----------|---------------|----------|
| 1st, 4th, 7th… | n % 3 = 1 | Latin lowercase (`a`–`z`) | `a`, `e`, `aa`, `file` |
| 2nd, 5th, 8th… | n % 3 = 2 | Positive integers | `1`, `8`, `10`, `256` |
| 3rd, 6th, 9th… | n % 3 = 0 | Latin uppercase (`A`–`Z`) | `A`, `C`, `AA`, `LAYER` |

## Usage

```python
from cell import Cell

# Validation
Cell.valid("a1")       # True (2D coordinate)
Cell.valid("a1A")      # True (3D coordinate)
Cell.valid("e4")       # True (2D coordinate)
Cell.valid("h8Hh8")    # True (5D coordinate)
Cell.valid("*")        # False (not a CELL coordinate)
Cell.valid("a0")       # False (invalid numeral)
Cell.valid("")         # False (empty string)

# Dimensional analysis
Cell.dimensions("a1")     # 2
Cell.dimensions("a1A")    # 3
Cell.dimensions("h8Hh8")  # 5
Cell.dimensions("foobar") # 1

# Parse coordinate into dimensional components
Cell.parse("a1A")      # ["a", "1", "A"]
Cell.parse("h8Hh8")    # ["h", "8", "H", "h", "8"]
Cell.parse("foobar")   # ["foobar"]
Cell.parse("1nvalid")  # raises ValueError

# Convert coordinates to 0-indexed integer tuples
Cell.to_indices("a1")    # (0, 0)
Cell.to_indices("e4")    # (4, 3)
Cell.to_indices("a1A")   # (0, 0, 0)
Cell.to_indices("b2B")   # (1, 1, 1)

# Convert 0-indexed integer tuples back to CELL coordinates
Cell.from_indices((0, 0))      # "a1"
Cell.from_indices((4, 3))      # "e4"
Cell.from_indices((0, 0, 0))   # "a1A"
Cell.from_indices((1, 1, 1))   # "b2B"

# Round-trip conversion
Cell.from_indices(Cell.to_indices("e4"))  # "e4"
```

## Format Specification

### Dimensional Patterns

| Dimensions | Pattern | Examples |
|------------|---------|----------|
| 1D | `<lower>` | `a`, `e`, `file` |
| 2D | `<lower><integer>` | `a1`, `e4`, `aa10` |
| 3D | `<lower><integer><upper>` | `a1A`, `e4B` |
| 4D | `<lower><integer><upper><lower>` | `a1Ab`, `e4Bc` |
| 5D | `<lower><integer><upper><lower><integer>` | `a1Ab2` |

### Regular Expression

```regex
^[a-z]+(?:[1-9][0-9]*[A-Z]+[a-z]+)*(?:[1-9][0-9]*[A-Z]*)?$
```

### Valid Examples

| Coordinate | Dimensions | Description |
|------------|------------|-------------|
| `a` | 1D | Single file |
| `a1` | 2D | Standard chess-style |
| `e4` | 2D | Chess center |
| `a1A` | 3D | 3D tic-tac-toe |
| `h8Hh8` | 5D | Multi-dimensional |
| `aa1AA` | 3D | Extended alphabet |

### Invalid Examples

| String | Reason |
|--------|--------|
| `""` | Empty string |
| `1` | Starts with digit |
| `A` | Starts with uppercase |
| `a0` | Zero is not a valid positive integer |
| `a01` | Leading zero in numeric dimension |
| `aA` | Missing numeric dimension |
| `a1a` | Missing uppercase dimension |
| `a1A1` | Numeric after uppercase without lowercase |

## API Reference

### Validation

```python
Cell.valid(s: str) -> bool
Cell.regex() -> re.Pattern[str]
```

### Parsing

```python
Cell.parse(s: str) -> list[str]  # raises ValueError on invalid input
```

### Dimensional Analysis

```python
Cell.dimensions(s: str) -> int  # returns 0 for invalid coordinates
```

### Coordinate Conversion

```python
Cell.to_indices(s: str) -> tuple[int, ...]  # raises ValueError on invalid input
Cell.from_indices(indices: tuple[int, ...]) -> str  # raises ValueError on invalid input
```

## Game Examples

### Chess (8×8)

```python
from cell import Cell

# Standard chess coordinates
chess_squares = [f"{chr(file)}{rank}" for file in range(ord('a'), ord('h') + 1) for rank in range(1, 9)]

# All are valid
all(Cell.valid(square) for square in chess_squares)  # True

# Convert position
Cell.to_indices("e4")  # (4, 3)
Cell.to_indices("h8")  # (7, 7)
```

### Shōgi (9×9)

```python
from cell import Cell

# Shōgi board positions
Cell.valid("e5")  # True (center)
Cell.valid("i9")  # True (corner)

Cell.to_indices("e5")  # (4, 4)
```

### 3D Tic-Tac-Toe (3×3×3)

```python
from cell import Cell

# Three-dimensional coordinates
Cell.valid("a1A")  # True
Cell.valid("b2B")  # True
Cell.valid("c3C")  # True

# Winning diagonal
diagonal = ["a1A", "b2B", "c3C"]
[Cell.to_indices(coord) for coord in diagonal]
# [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
```

## Extended Alphabet

CELL supports extended alphabet notation for large boards:

```python
from cell import Cell

# Single letters: a-z (positions 0-25)
Cell.to_indices("z1")   # (25, 0)

# Double letters: aa-zz (positions 26-701)
Cell.to_indices("aa1")  # (26, 0)
Cell.to_indices("ab1")  # (27, 0)
Cell.to_indices("zz1")  # (701, 0)

# And so on...
Cell.from_indices((702, 0))  # "aaa1"
```

## Properties

- **Multi-dimensional**: Supports unlimited dimensional coordinate systems
- **Cyclical**: Uses systematic three-character-set repetition
- **ASCII-based**: Pure ASCII characters for universal compatibility
- **Unambiguous**: Each coordinate maps to exactly one location
- **Scalable**: Extends naturally from 1D to unlimited dimensions
- **Rule-agnostic**: Independent of specific game mechanics

## Related Specifications

- [Game Protocol](https://sashite.dev/game-protocol/) — Conceptual foundation
- [CELL Specification](https://sashite.dev/specs/cell/1.0.0/) — Official specification

## License

Available as open source under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

## About

Maintained by [Sashité](https://sashite.com/) — promoting chess variants and sharing the beauty of board game cultures.
