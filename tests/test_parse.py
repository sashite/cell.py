"""Tests for CELL coordinate parsing (string → indices)."""

import pytest

from sashite_cell import Coordinate


class TestParseBasic:
    """Basic parsing tests."""

    def test_parse_1d_first_letter(self) -> None:
        """Parse single letter a."""
        coord = Coordinate.parse("a")
        assert coord.indices == (0,)

    def test_parse_1d_last_single_letter(self) -> None:
        """Parse single letter z."""
        coord = Coordinate.parse("z")
        assert coord.indices == (25,)

    def test_parse_1d_double_letter(self) -> None:
        """Parse double letter aa."""
        coord = Coordinate.parse("aa")
        assert coord.indices == (26,)

    def test_parse_1d_max_index(self) -> None:
        """Parse iv (index 255)."""
        coord = Coordinate.parse("iv")
        assert coord.indices == (255,)

    def test_parse_2d_a1(self) -> None:
        """Parse 2D coordinate a1."""
        coord = Coordinate.parse("a1")
        assert coord.indices == (0, 0)

    def test_parse_2d_e4(self) -> None:
        """Parse 2D coordinate e4."""
        coord = Coordinate.parse("e4")
        assert coord.indices == (4, 3)

    def test_parse_2d_h8(self) -> None:
        """Parse 2D coordinate h8."""
        coord = Coordinate.parse("h8")
        assert coord.indices == (7, 7)

    def test_parse_2d_max_indices(self) -> None:
        """Parse 2D coordinate with maximum indices."""
        coord = Coordinate.parse("iv256")
        assert coord.indices == (255, 255)

    def test_parse_3d_a1a(self) -> None:
        """Parse 3D coordinate a1A."""
        coord = Coordinate.parse("a1A")
        assert coord.indices == (0, 0, 0)

    def test_parse_3d_b2b(self) -> None:
        """Parse 3D coordinate b2B."""
        coord = Coordinate.parse("b2B")
        assert coord.indices == (1, 1, 1)

    def test_parse_3d_c3c(self) -> None:
        """Parse 3D coordinate c3C."""
        coord = Coordinate.parse("c3C")
        assert coord.indices == (2, 2, 2)

    def test_parse_3d_max_indices(self) -> None:
        """Parse 3D coordinate with maximum indices."""
        coord = Coordinate.parse("iv256IV")
        assert coord.indices == (255, 255, 255)


class TestParseDimensions:
    """Tests for dimension count after parsing."""

    def test_dimensions_1d(self) -> None:
        """1D coordinate has 1 dimension."""
        coord = Coordinate.parse("e")
        assert coord.dimensions == 1

    def test_dimensions_2d(self) -> None:
        """2D coordinate has 2 dimensions."""
        coord = Coordinate.parse("e4")
        assert coord.dimensions == 2

    def test_dimensions_3d(self) -> None:
        """3D coordinate has 3 dimensions."""
        coord = Coordinate.parse("e4B")
        assert coord.dimensions == 3


class TestParseLetterConversion:
    """Tests for letter to index conversion."""

    def test_single_letters(self) -> None:
        """All single letters parse correctly."""
        expected = "abcdefghijklmnopqrstuvwxyz"
        for i, letter in enumerate(expected):
            coord = Coordinate.parse(letter)
            assert coord.indices == (i,)

    def test_double_letter_aa(self) -> None:
        """Double letter aa parses to index 26."""
        coord = Coordinate.parse("aa")
        assert coord.indices == (26,)

    def test_double_letter_ab(self) -> None:
        """Double letter ab parses to index 27."""
        coord = Coordinate.parse("ab")
        assert coord.indices == (27,)

    def test_double_letter_az(self) -> None:
        """Double letter az parses to index 51."""
        coord = Coordinate.parse("az")
        assert coord.indices == (51,)

    def test_double_letter_ba(self) -> None:
        """Double letter ba parses to index 52."""
        coord = Coordinate.parse("ba")
        assert coord.indices == (52,)


class TestParseIntegerConversion:
    """Tests for integer parsing (1-indexed input)."""

    def test_integer_one(self) -> None:
        """Integer 1 parses to index 0."""
        coord = Coordinate.parse("a1")
        assert coord.indices[1] == 0

    def test_integer_ten(self) -> None:
        """Integer 10 parses to index 9."""
        coord = Coordinate.parse("a10")
        assert coord.indices[1] == 9

    def test_integer_256(self) -> None:
        """Integer 256 parses to index 255."""
        coord = Coordinate.parse("a256")
        assert coord.indices[1] == 255


class TestParseUppercaseConversion:
    """Tests for uppercase letter parsing in 3D."""

    def test_uppercase_a(self) -> None:
        """Uppercase A parses to index 0."""
        coord = Coordinate.parse("a1A")
        assert coord.indices[2] == 0

    def test_uppercase_z(self) -> None:
        """Uppercase Z parses to index 25."""
        coord = Coordinate.parse("a1Z")
        assert coord.indices[2] == 25

    def test_uppercase_aa(self) -> None:
        """Uppercase AA parses to index 26."""
        coord = Coordinate.parse("a1AA")
        assert coord.indices[2] == 26

    def test_uppercase_iv(self) -> None:
        """Uppercase IV parses to index 255."""
        coord = Coordinate.parse("a1IV")
        assert coord.indices[2] == 255


class TestParseEmptyInput:
    """Tests for empty input handling."""

    def test_empty_string(self) -> None:
        """Reject empty string."""
        with pytest.raises(ValueError, match="empty input"):
            Coordinate.parse("")


class TestParseInputTooLong:
    """Tests for input length limit."""

    def test_max_length_valid(self) -> None:
        """Accept 7 character input (maximum)."""
        coord = Coordinate.parse("iv256IV")
        assert coord.indices == (255, 255, 255)

    def test_exceeds_max_length(self) -> None:
        """Reject input exceeding 7 characters."""
        with pytest.raises(ValueError, match="exceeds 7 characters"):
            Coordinate.parse("iv256IVx")

    def test_way_too_long(self) -> None:
        """Reject very long input."""
        with pytest.raises(ValueError, match="exceeds 7 characters"):
            Coordinate.parse("a" * 100)


class TestParseInvalidStart:
    """Tests for invalid starting character."""

    def test_starts_with_digit(self) -> None:
        """Reject string starting with digit."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("1")

    def test_starts_with_uppercase(self) -> None:
        """Reject string starting with uppercase."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("A")

    def test_starts_with_symbol(self) -> None:
        """Reject string starting with symbol."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("*")

    def test_starts_with_space(self) -> None:
        """Reject string starting with space."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse(" a1")


class TestParseLeadingZero:
    """Tests for leading zero rejection."""

    def test_zero_alone(self) -> None:
        """Reject zero as integer part."""
        with pytest.raises(ValueError, match="leading zero"):
            Coordinate.parse("a0")

    def test_leading_zero(self) -> None:
        """Reject leading zero in integer part."""
        with pytest.raises(ValueError, match="leading zero"):
            Coordinate.parse("a01")

    def test_leading_zeros(self) -> None:
        """Reject multiple leading zeros."""
        with pytest.raises(ValueError, match="leading zero"):
            Coordinate.parse("a001")


class TestParseUnexpectedCharacter:
    """Tests for unexpected character in sequence."""

    def test_missing_integer(self) -> None:
        """Reject missing integer between lowercase and uppercase."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.parse("aA")

    def test_missing_uppercase(self) -> None:
        """Reject missing uppercase between integer and lowercase."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.parse("a1a")

    def test_symbol_after_lowercase(self) -> None:
        """Reject symbol after lowercase."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.parse("a*")

    def test_symbol_after_integer(self) -> None:
        """Reject symbol after integer."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.parse("a1*")


class TestParseDimensionLimit:
    """Tests for dimension limit."""

    def test_exceeds_3_dimensions(self) -> None:
        """Reject more than 3 dimensions."""
        with pytest.raises(ValueError, match="exceeds 3 dimensions"):
            Coordinate.parse("a1Aa")


class TestParseIndexOutOfRange:
    """Tests for index value limits."""

    def test_integer_too_large(self) -> None:
        """Reject integer > 256 (index > 255)."""
        with pytest.raises(ValueError, match="exceeds 255"):
            Coordinate.parse("a257")

    def test_lowercase_index_too_large(self) -> None:
        """Reject lowercase letters exceeding index 255."""
        with pytest.raises(ValueError, match="exceeds 255"):
            Coordinate.parse("iw")  # index 256

    def test_uppercase_index_too_large(self) -> None:
        """Reject uppercase letters exceeding index 255."""
        with pytest.raises(ValueError, match="exceeds 255"):
            Coordinate.parse("a1IW")  # index 256


class TestParseNonStringInput:
    """Tests for non-string input rejection."""

    def test_integer_input(self) -> None:
        """Reject integer input."""
        with pytest.raises(ValueError, match="input must be a string"):
            Coordinate.parse(123)  # type: ignore[arg-type]

    def test_none_input(self) -> None:
        """Reject None input."""
        with pytest.raises(ValueError, match="input must be a string"):
            Coordinate.parse(None)  # type: ignore[arg-type]

    def test_list_input(self) -> None:
        """Reject list input."""
        with pytest.raises(ValueError, match="input must be a string"):
            Coordinate.parse(["a", "1"])  # type: ignore[arg-type]


class TestParseUnicodeRejection:
    """Tests for Unicode character rejection (ASCII only)."""

    def test_unicode_letter(self) -> None:
        """Reject Unicode letter."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("ä1")

    def test_unicode_digit(self) -> None:
        """Reject Unicode digit."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.parse("a①")

    def test_fullwidth_letter(self) -> None:
        """Reject fullwidth letter."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("ａ1")  # noqa: RUF001

    def test_cyrillic_lookalike(self) -> None:
        """Reject Cyrillic lookalike."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("а1")  # noqa: RUF001


class TestParseMaliciousInput:
    """Tests for potentially malicious input."""

    def test_null_byte(self) -> None:
        """Reject null byte in input."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("\x00a1")

    def test_newline(self) -> None:
        """Reject newline in input."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("\na1")

    def test_tab(self) -> None:
        """Reject tab in input."""
        with pytest.raises(ValueError, match="must start with lowercase letter"):
            Coordinate.parse("\ta1")

    def test_trailing_space(self) -> None:
        """Reject trailing space."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.parse("a1 ")

    def test_embedded_space(self) -> None:
        """Reject embedded space."""
        with pytest.raises(ValueError, match="unexpected character"):
            Coordinate.parse("a 1")
