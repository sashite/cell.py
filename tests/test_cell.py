"""Tests for the CELL (Coordinate Encoding for Layered Locations) implementation."""

import re

import pytest

import cell


class TestIsValid:
    """Tests for the is_valid function."""

    @pytest.mark.parametrize(
        "coord",
        [
            "a",  # 1D single letter
            "foobar",  # 1D multiple letters
            "a1",  # 2D standard chess
            "e4",  # 2D chess center
            "h8",  # 2D corner
            "aa1",  # 2D extended file
            "a10",  # 2D large rank
            "aa10",  # 2D extended both
            "a1A",  # 3D basic
            "e4B",  # 3D extended
            "aa1AA",  # 3D all extended
            "a1Ab",  # 4D basic
            "e4Bc",  # 4D extended
            "a1Ab2",  # 5D basic
            "h8Hh8",  # 5D complex
            "e5",  # shogi center
            "i9",  # shogi corner
            "b2B",  # 3D tic-tac-toe
            "z26Z",  # large board
        ],
    )
    def test_valid_coordinates(self, coord: str) -> None:
        """Test that valid CELL coordinates are recognized."""
        assert cell.is_valid(coord) is True

    @pytest.mark.parametrize(
        ("coord", "reason"),
        [
            ("", "empty string"),
            ("1", "starts with digit"),
            ("A", "starts with uppercase"),
            ("a0", "zero rank"),
            ("a01", "leading zero"),
            ("aA", "missing numeric"),
            ("a1a", "missing uppercase"),
            ("a1A1", "numeric after uppercase without lowercase"),
            ("1a", "starts with digit then letter"),
            ("*", "special character"),
            ("a1!", "invalid character"),
            ("a 1", "space in coordinate"),
            ("a1\n", "newline in coordinate"),
            ("a1\r", "carriage return"),
            ("a\t1", "tab character"),
            ("α1", "unicode letter"),  # noqa: RUF001
            ("aB1", "mixed case in dimension"),
        ],
    )
    def test_invalid_coordinates(self, coord: str, reason: str) -> None:
        """Test that invalid CELL coordinates are rejected."""
        assert cell.is_valid(coord) is False, f"Should reject: {reason}"

    def test_non_string_input(self) -> None:
        """Test that non-string inputs return False."""
        assert cell.is_valid(None) is False  # type: ignore[arg-type]
        assert cell.is_valid(123) is False  # type: ignore[arg-type]
        assert cell.is_valid([]) is False  # type: ignore[arg-type]


class TestRegex:
    """Tests for the regex function."""

    def test_returns_compiled_pattern(self) -> None:
        """Test that regex returns a compiled pattern."""
        pattern = cell.regex()
        assert isinstance(pattern, re.Pattern)

    def test_pattern_matches_specification(self) -> None:
        """Test that the regex pattern matches the CELL specification."""
        expected = r"^[a-z]+(?:[1-9][0-9]*[A-Z]+[a-z]+)*(?:[1-9][0-9]*[A-Z]*)?$"
        assert cell.regex().pattern == expected


class TestParse:
    """Tests for the parse function."""

    @pytest.mark.parametrize(
        ("coord", "expected"),
        [
            ("a", ["a"]),
            ("foobar", ["foobar"]),
            ("a1", ["a", "1"]),
            ("e4", ["e", "4"]),
            ("aa10", ["aa", "10"]),
            ("a1A", ["a", "1", "A"]),
            ("aa1AA", ["aa", "1", "AA"]),
            ("a1Ab", ["a", "1", "A", "b"]),
            ("h8Hh8", ["h", "8", "H", "h", "8"]),
        ],
    )
    def test_parse_valid_coordinates(self, coord: str, expected: list[str]) -> None:
        """Test parsing valid CELL coordinates."""
        assert cell.parse(coord) == expected

    @pytest.mark.parametrize(
        "coord",
        [
            "",
            "1a",
            "a1!",
            "A1",
        ],
    )
    def test_parse_invalid_coordinates(self, coord: str) -> None:
        """Test that parsing invalid coordinates raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CELL coordinate"):
            cell.parse(coord)


class TestDimensions:
    """Tests for the dimensions function."""

    @pytest.mark.parametrize(
        ("coord", "expected"),
        [
            ("a", 1),
            ("foobar", 1),
            ("a1", 2),
            ("e4", 2),
            ("a1A", 3),
            ("a1Ab", 4),
            ("h8Hh8", 5),
        ],
    )
    def test_dimensions_valid_coordinates(self, coord: str, expected: int) -> None:
        """Test dimension counting for valid coordinates."""
        assert cell.dimensions(coord) == expected

    @pytest.mark.parametrize(
        "coord",
        [
            "",
            "1nvalid",
            "a!",
        ],
    )
    def test_dimensions_invalid_coordinates(self, coord: str) -> None:
        """Test that invalid coordinates return 0 dimensions."""
        assert cell.dimensions(coord) == 0


class TestToIndices:
    """Tests for the to_indices function."""

    @pytest.mark.parametrize(
        ("coord", "expected"),
        [
            # Basic conversions
            ("a1", (0, 0)),
            ("e4", (4, 3)),
            ("h8", (7, 7)),
            ("a1A", (0, 0, 0)),
            ("b2B", (1, 1, 1)),
            ("z26Z", (25, 25, 25)),
            # Extended alphabet
            ("aa1", (26, 0)),
            ("ab1", (27, 0)),
            ("az1", (51, 0)),
            ("ba1", (52, 0)),
            ("zz1", (701, 0)),
            ("aa1AA", (26, 0, 26)),
            # Shogi
            ("e5", (4, 4)),
            ("i9", (8, 8)),
            # 3D tic-tac-toe diagonal
            ("a1A", (0, 0, 0)),
            ("b2B", (1, 1, 1)),
            ("c3C", (2, 2, 2)),
            # 1D
            ("a", (0,)),
            ("z", (25,)),
            ("aa", (26,)),
        ],
    )
    def test_to_indices_valid_coordinates(
        self, coord: str, expected: tuple[int, ...]
    ) -> None:
        """Test conversion of valid coordinates to indices."""
        assert cell.to_indices(coord) == expected

    @pytest.mark.parametrize(
        "coord",
        [
            "",
            "1nvalid",
        ],
    )
    def test_to_indices_invalid_coordinates(self, coord: str) -> None:
        """Test that invalid coordinates raise ValueError."""
        with pytest.raises(ValueError, match="Invalid CELL coordinate"):
            cell.to_indices(coord)


class TestFromIndices:
    """Tests for the from_indices function."""

    @pytest.mark.parametrize(
        ("indices", "expected"),
        [
            # Basic conversions
            ((0, 0), "a1"),
            ((4, 3), "e4"),
            ((7, 7), "h8"),
            ((0, 0, 0), "a1A"),
            ((1, 1, 1), "b2B"),
            ((25, 25, 25), "z26Z"),
            # Extended alphabet
            ((26, 0), "aa1"),
            ((27, 0), "ab1"),
            ((51, 0), "az1"),
            ((52, 0), "ba1"),
            ((701, 0), "zz1"),
            ((702, 0), "aaa1"),
            ((26, 0, 26), "aa1AA"),
            # 1D
            ((0,), "a"),
            ((25,), "z"),
            ((26,), "aa"),
            # 4D and 5D
            ((0, 0, 0, 0), "a1Aa"),
            ((0, 0, 0, 0, 0), "a1Aa1"),
        ],
    )
    def test_from_indices_valid(self, indices: tuple[int, ...], expected: str) -> None:
        """Test conversion of valid indices to coordinates."""
        assert cell.from_indices(indices) == expected

    def test_from_indices_accepts_list(self) -> None:
        """Test that from_indices accepts a list as input."""
        assert cell.from_indices([4, 3]) == "e4"
        assert cell.from_indices([0, 0, 0]) == "a1A"

    def test_from_indices_empty_sequence(self) -> None:
        """Test that empty sequence raises ValueError."""
        with pytest.raises(ValueError, match="Cannot convert empty sequence"):
            cell.from_indices(())

    def test_from_indices_negative_index(self) -> None:
        """Test that negative indices raise ValueError."""
        with pytest.raises(ValueError, match="Negative index not allowed"):
            cell.from_indices((-1, 0))
        with pytest.raises(ValueError, match="Negative index not allowed"):
            cell.from_indices((0, -1))


class TestRoundTrip:
    """Tests for round-trip conversion."""

    @pytest.mark.parametrize(
        "coord",
        [
            "a",
            "z",
            "aa",
            "az",
            "ba",
            "zz",
            "aaa",
            "a1",
            "e4",
            "h8",
            "aa10",
            "zz99",
            "a1A",
            "b2B",
            "c3C",
            "z26Z",
            "aa1AA",
            "a1Ab",
            "e4Bc",
            "a1Ab2",
            "h8Hh8",
        ],
    )
    def test_round_trip_from_coordinate(self, coord: str) -> None:
        """Test that coordinate -> indices -> coordinate preserves value."""
        indices = cell.to_indices(coord)
        result = cell.from_indices(indices)
        assert result == coord

    @pytest.mark.parametrize(
        "indices",
        [
            (0,),
            (25,),
            (26,),
            (701,),
            (702,),
            (0, 0),
            (4, 3),
            (7, 7),
            (25, 25),
            (26, 0),
            (0, 0, 0),
            (1, 1, 1),
            (25, 25, 25),
            (26, 0, 26),
            (0, 0, 0, 0),
            (1, 2, 3, 4),
            (0, 0, 0, 0, 0),
            (7, 7, 7, 7, 7),
        ],
    )
    def test_round_trip_from_indices(self, indices: tuple[int, ...]) -> None:
        """Test that indices -> coordinate -> indices preserves value."""
        coord = cell.from_indices(indices)
        result = cell.to_indices(coord)
        assert result == indices


class TestExtendedAlphabet:
    """Tests for extended alphabet conversion."""

    @pytest.mark.parametrize(
        ("letters", "index"),
        [
            # Single letters: 0-25
            ("a", 0),
            ("b", 1),
            ("z", 25),
            # Double letters: 26-701
            ("aa", 26),
            ("ab", 27),
            ("az", 51),
            ("ba", 52),
            ("bz", 77),
            ("za", 676),
            ("zz", 701),
            # Triple letters: 702+
            ("aaa", 702),
            ("aab", 703),
            ("aba", 728),
            ("azz", 1377),
            ("baa", 1378),
        ],
    )
    def test_extended_alphabet_conversion(self, letters: str, index: int) -> None:
        """Test the extended alphabet index calculations."""
        # Test via 1D coordinate (just the letters)
        assert cell.to_indices(letters) == (index,)
        assert cell.from_indices((index,)) == letters


class TestChessBoard:
    """Tests for chess board coordinates."""

    def test_all_chess_squares_valid(self) -> None:
        """Test that all 64 chess squares are valid."""
        for file in "abcdefgh":
            for rank in range(1, 9):
                coord = f"{file}{rank}"
                assert cell.is_valid(coord), f"Chess square {coord} should be valid"

    @pytest.mark.parametrize(
        ("coord", "expected"),
        [
            ("a1", (0, 0)),  # white rook
            ("e1", (4, 0)),  # white king
            ("d1", (3, 0)),  # white queen
            ("e4", (4, 3)),  # classic opening
            ("d5", (3, 4)),  # center
            ("h8", (7, 7)),  # black rook
        ],
    )
    def test_chess_positions(self, coord: str, expected: tuple[int, int]) -> None:
        """Test specific chess positions."""
        assert cell.to_indices(coord) == expected


class TestShogiBoard:
    """Tests for shogi board coordinates."""

    def test_all_shogi_squares_valid(self) -> None:
        """Test that all 81 shogi squares are valid."""
        for file in "abcdefghi":
            for rank in range(1, 10):
                coord = f"{file}{rank}"
                assert cell.is_valid(coord), f"Shogi square {coord} should be valid"

    @pytest.mark.parametrize(
        ("coord", "expected"),
        [
            ("e1", (4, 0)),  # sente king initial
            ("e9", (4, 8)),  # gote king initial
            ("e5", (4, 4)),  # center
            ("a1", (0, 0)),  # corner
            ("i9", (8, 8)),  # opposite corner
        ],
    )
    def test_shogi_positions(self, coord: str, expected: tuple[int, int]) -> None:
        """Test specific shogi positions."""
        assert cell.to_indices(coord) == expected


class TestTicTacToe3D:
    """Tests for 3D tic-tac-toe coordinates."""

    def test_all_positions_valid(self) -> None:
        """Test that all 27 positions are valid."""
        for file in "abc":
            for rank in range(1, 4):
                for level in "ABC":
                    coord = f"{file}{rank}{level}"
                    assert cell.is_valid(coord), f"3D position {coord} should be valid"

    def test_winning_diagonal(self) -> None:
        """Test the main 3D diagonal."""
        diagonal = [
            ("a1A", (0, 0, 0)),
            ("b2B", (1, 1, 1)),
            ("c3C", (2, 2, 2)),
        ]
        for coord, expected in diagonal:
            assert cell.to_indices(coord) == expected
