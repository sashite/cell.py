"""Tests for CELL coordinate formatting (indices → string)."""

import pytest

from sashite_cell import Coordinate


class TestFormatBasic:
    """Basic formatting tests."""

    def test_format_1d_first_letter(self) -> None:
        """Format single dimension with first letter."""
        assert str(Coordinate(0)) == "a"

    def test_format_1d_last_single_letter(self) -> None:
        """Format single dimension with last single letter."""
        assert str(Coordinate(25)) == "z"

    def test_format_1d_first_double_letter(self) -> None:
        """Format single dimension with first double letter."""
        assert str(Coordinate(26)) == "aa"

    def test_format_1d_max_index(self) -> None:
        """Format single dimension with maximum index."""
        assert str(Coordinate(255)) == "iv"

    def test_format_2d_a1(self) -> None:
        """Format 2D coordinate a1."""
        assert str(Coordinate(0, 0)) == "a1"

    def test_format_2d_e4(self) -> None:
        """Format 2D coordinate e4."""
        assert str(Coordinate(4, 3)) == "e4"

    def test_format_2d_h8(self) -> None:
        """Format 2D coordinate h8."""
        assert str(Coordinate(7, 7)) == "h8"

    def test_format_2d_max_indices(self) -> None:
        """Format 2D coordinate with maximum indices."""
        assert str(Coordinate(255, 255)) == "iv256"

    def test_format_3d_a1a(self) -> None:
        """Format 3D coordinate a1A."""
        assert str(Coordinate(0, 0, 0)) == "a1A"

    def test_format_3d_b2b(self) -> None:
        """Format 3D coordinate b2B."""
        assert str(Coordinate(1, 1, 1)) == "b2B"

    def test_format_3d_c3c(self) -> None:
        """Format 3D coordinate c3C."""
        assert str(Coordinate(2, 2, 2)) == "c3C"

    def test_format_3d_max_indices(self) -> None:
        """Format 3D coordinate with maximum indices."""
        assert str(Coordinate(255, 255, 255)) == "iv256IV"


class TestFormatClassMethod:
    """Tests for Coordinate.format() class method."""

    def test_format_method_1d(self) -> None:
        """Format via class method for 1D."""
        assert Coordinate.format(0) == "a"

    def test_format_method_2d(self) -> None:
        """Format via class method for 2D."""
        assert Coordinate.format(4, 3) == "e4"

    def test_format_method_3d(self) -> None:
        """Format via class method for 3D."""
        assert Coordinate.format(0, 0, 0) == "a1A"


class TestFormatLetterConversion:
    """Tests for letter index conversion."""

    def test_single_letters(self) -> None:
        """All single letters map correctly."""
        expected = "abcdefghijklmnopqrstuvwxyz"
        for i, letter in enumerate(expected):
            assert str(Coordinate(i)) == letter

    def test_double_letter_aa(self) -> None:
        """Double letter aa maps to index 26."""
        assert str(Coordinate(26)) == "aa"

    def test_double_letter_ab(self) -> None:
        """Double letter ab maps to index 27."""
        assert str(Coordinate(27)) == "ab"

    def test_double_letter_az(self) -> None:
        """Double letter az maps to index 51."""
        assert str(Coordinate(51)) == "az"

    def test_double_letter_ba(self) -> None:
        """Double letter ba maps to index 52."""
        assert str(Coordinate(52)) == "ba"


class TestFormatIntegerConversion:
    """Tests for integer formatting (1-indexed output)."""

    def test_integer_one(self) -> None:
        """Index 0 formats to integer 1."""
        assert str(Coordinate(0, 0)) == "a1"

    def test_integer_ten(self) -> None:
        """Index 9 formats to integer 10."""
        assert str(Coordinate(0, 9)) == "a10"

    def test_integer_256(self) -> None:
        """Index 255 formats to integer 256."""
        assert str(Coordinate(0, 255)) == "a256"


class TestFormatUppercaseConversion:
    """Tests for uppercase letter formatting in 3D."""

    def test_uppercase_a(self) -> None:
        """Third dimension index 0 formats to A."""
        assert str(Coordinate(0, 0, 0)) == "a1A"

    def test_uppercase_z(self) -> None:
        """Third dimension index 25 formats to Z."""
        assert str(Coordinate(0, 0, 25)) == "a1Z"

    def test_uppercase_aa(self) -> None:
        """Third dimension index 26 formats to AA."""
        assert str(Coordinate(0, 0, 26)) == "a1AA"

    def test_uppercase_iv(self) -> None:
        """Third dimension index 255 formats to IV."""
        assert str(Coordinate(0, 0, 255)) == "a1IV"


class TestFormatErrors:
    """Tests for formatting error cases."""

    def test_no_indices(self) -> None:
        """Reject empty indices."""
        with pytest.raises(ValueError, match="at least one index required"):
            Coordinate()

    def test_too_many_dimensions(self) -> None:
        """Reject more than 3 dimensions."""
        with pytest.raises(ValueError, match="exceeds 3 dimensions"):
            Coordinate(0, 0, 0, 0)

    def test_negative_index(self) -> None:
        """Reject negative index."""
        with pytest.raises(ValueError, match="exceeds 255"):
            Coordinate(-1)

    def test_index_too_large(self) -> None:
        """Reject index > 255."""
        with pytest.raises(ValueError, match="exceeds 255"):
            Coordinate(256)

    def test_non_integer_index(self) -> None:
        """Reject non-integer index."""
        with pytest.raises(ValueError, match="must be an integer"):
            Coordinate("a")  # type: ignore[arg-type]

    def test_float_index(self) -> None:
        """Reject float index."""
        with pytest.raises(ValueError, match="must be an integer"):
            Coordinate(1.5)  # type: ignore[arg-type]

    def test_bool_index(self) -> None:
        """Reject boolean index (bool is subclass of int)."""
        with pytest.raises(ValueError, match="must be an integer"):
            Coordinate(True)  # type: ignore[arg-type]
