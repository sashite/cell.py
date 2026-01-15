"""Tests for CELL coordinate validation."""

import pytest

from sashite_cell import Coordinate


class TestIsValidTrue:
    """Tests for valid coordinates returning True."""

    def test_1d_single_letter(self) -> None:
        """Single letter is valid."""
        assert Coordinate.is_valid("a") is True
        assert Coordinate.is_valid("z") is True

    def test_1d_double_letter(self) -> None:
        """Double letter is valid."""
        assert Coordinate.is_valid("aa") is True
        assert Coordinate.is_valid("iv") is True

    def test_2d_basic(self) -> None:
        """Basic 2D coordinates are valid."""
        assert Coordinate.is_valid("a1") is True
        assert Coordinate.is_valid("e4") is True
        assert Coordinate.is_valid("h8") is True

    def test_2d_extended(self) -> None:
        """Extended 2D coordinates are valid."""
        assert Coordinate.is_valid("aa10") is True
        assert Coordinate.is_valid("iv256") is True

    def test_3d_basic(self) -> None:
        """Basic 3D coordinates are valid."""
        assert Coordinate.is_valid("a1A") is True
        assert Coordinate.is_valid("b2B") is True
        assert Coordinate.is_valid("c3C") is True

    def test_3d_extended(self) -> None:
        """Extended 3D coordinates are valid."""
        assert Coordinate.is_valid("a1AA") is True
        assert Coordinate.is_valid("iv256IV") is True


class TestIsValidFalse:
    """Tests for invalid coordinates returning False."""

    def test_empty_string(self) -> None:
        """Empty string is invalid."""
        assert Coordinate.is_valid("") is False

    def test_too_long(self) -> None:
        """String exceeding 7 characters is invalid."""
        assert Coordinate.is_valid("iv256IVx") is False

    def test_starts_with_digit(self) -> None:
        """String starting with digit is invalid."""
        assert Coordinate.is_valid("1") is False
        assert Coordinate.is_valid("1a") is False

    def test_starts_with_uppercase(self) -> None:
        """String starting with uppercase is invalid."""
        assert Coordinate.is_valid("A") is False
        assert Coordinate.is_valid("A1") is False

    def test_leading_zero(self) -> None:
        """Leading zero in integer is invalid."""
        assert Coordinate.is_valid("a0") is False
        assert Coordinate.is_valid("a01") is False

    def test_missing_dimension(self) -> None:
        """Missing dimension is invalid."""
        assert Coordinate.is_valid("aA") is False
        assert Coordinate.is_valid("a1a") is False

    def test_exceeds_dimensions(self) -> None:
        """More than 3 dimensions is invalid."""
        assert Coordinate.is_valid("a1Aa") is False

    def test_index_out_of_range(self) -> None:
        """Index exceeding 255 is invalid."""
        assert Coordinate.is_valid("a257") is False
        assert Coordinate.is_valid("iw") is False

    def test_symbols(self) -> None:
        """Symbols are invalid."""
        assert Coordinate.is_valid("*") is False
        assert Coordinate.is_valid("a*") is False
        assert Coordinate.is_valid("a1*") is False

    def test_whitespace(self) -> None:
        """Whitespace is invalid."""
        assert Coordinate.is_valid(" ") is False
        assert Coordinate.is_valid(" a1") is False
        assert Coordinate.is_valid("a1 ") is False
        assert Coordinate.is_valid("a 1") is False

    def test_unicode(self) -> None:
        """Unicode characters are invalid."""
        assert Coordinate.is_valid("ä1") is False
        assert Coordinate.is_valid("а1") is False  # noqa: RUF001


class TestIsValidReturnType:
    """Tests for is_valid() return type."""

    def test_returns_bool_true(self) -> None:
        """Returns exactly True, not truthy value."""
        result = Coordinate.is_valid("a1")
        assert result is True
        assert isinstance(result, bool)

    def test_returns_bool_false(self) -> None:
        """Returns exactly False, not falsy value."""
        result = Coordinate.is_valid("")
        assert result is False
        assert isinstance(result, bool)


class TestValidateSuccess:
    """Tests for validate() with valid input (no exception)."""

    def test_1d_valid(self) -> None:
        """Valid 1D coordinate does not raise."""
        Coordinate.validate("a")
        Coordinate.validate("z")
        Coordinate.validate("iv")

    def test_2d_valid(self) -> None:
        """Valid 2D coordinate does not raise."""
        Coordinate.validate("a1")
        Coordinate.validate("e4")
        Coordinate.validate("iv256")

    def test_3d_valid(self) -> None:
        """Valid 3D coordinate does not raise."""
        Coordinate.validate("a1A")
        Coordinate.validate("b2B")
        Coordinate.validate("iv256IV")

    def test_returns_none(self) -> None:
        """validate() returns None on success."""
        result = Coordinate.validate("e4")
        assert result is None


class TestValidateErrors:
    """Tests for validate() error messages."""

    def test_empty_input_message(self) -> None:
        """Empty input raises with correct message."""
        with pytest.raises(ValueError, match="empty input"):
            Coordinate.validate("")

    def test_too_long_message(self) -> None:
        """Too long input raises with correct message."""
        with pytest.raises(ValueError, match="exceeds 7 characters"):
            Coordinate.validate("iv256IVx")

    def test_invalid_start_message(self) -> None:
        """Invalid start raises with correct message."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.validate("1a")

    def test_leading_zero_message(self) -> None:
        """Leading zero raises with correct message."""
        with pytest.raises(ValueError, match="leading zero"):
            Coordinate.validate("a0")

    def test_unexpected_char_message(self) -> None:
        """Unexpected character raises with correct message."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.validate("aA")

    def test_exceeds_dimensions_message(self) -> None:
        """Exceeding dimensions raises with correct message."""
        with pytest.raises(ValueError, match="exceeds 3 dimensions"):
            Coordinate.validate("a1Aa")

    def test_index_out_of_range_message(self) -> None:
        """Index out of range raises with correct message."""
        with pytest.raises(ValueError, match="exceeds 255"):
            Coordinate.validate("a257")


class TestValidateVsIsValid:
    """Tests ensuring validate() and is_valid() are consistent."""

    @pytest.mark.parametrize(
        "string",
        [
            "a",
            "z",
            "aa",
            "iv",
            "a1",
            "e4",
            "h8",
            "iv256",
            "a1A",
            "b2B",
            "iv256IV",
        ],
    )
    def test_valid_strings_consistent(self, string: str) -> None:
        """Valid strings: is_valid returns True, validate does not raise."""
        assert Coordinate.is_valid(string) is True
        Coordinate.validate(string)  # Should not raise

    @pytest.mark.parametrize(
        "string",
        [
            "",
            "1",
            "A",
            "a0",
            "a01",
            "aA",
            "a1a",
            "a1Aa",
            "a257",
            "iw",
            "*",
            " ",
            "a1 ",
        ],
    )
    def test_invalid_strings_consistent(self, string: str) -> None:
        """Invalid strings: is_valid returns False, validate raises."""
        assert Coordinate.is_valid(string) is False
        with pytest.raises(ValueError):
            Coordinate.validate(string)


class TestValidateEdgeCases:
    """Edge case tests for validation."""

    def test_max_valid_length(self) -> None:
        """7 characters is valid (maximum length)."""
        assert Coordinate.is_valid("iv256IV") is True
        Coordinate.validate("iv256IV")

    def test_min_valid_length(self) -> None:
        """1 character is valid (minimum length)."""
        assert Coordinate.is_valid("a") is True
        Coordinate.validate("a")

    def test_boundary_index_255(self) -> None:
        """Index 255 is valid (maximum)."""
        assert Coordinate.is_valid("iv") is True
        assert Coordinate.is_valid("a256") is True
        assert Coordinate.is_valid("a1IV") is True

    def test_boundary_index_256(self) -> None:
        """Index 256 is invalid (exceeds maximum)."""
        assert Coordinate.is_valid("iw") is False
        assert Coordinate.is_valid("a257") is False
        assert Coordinate.is_valid("a1IW") is False
