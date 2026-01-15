"""Tests for CELL coordinate round-trip conversion."""

import pytest

from sashite_cell import Coordinate


class TestRoundTripStringToString:
    """Tests for string → Coordinate → string round-trip."""

    def test_1d_single_letter(self) -> None:
        """Round-trip single letter."""
        assert str(Coordinate.parse("a")) == "a"
        assert str(Coordinate.parse("e")) == "e"
        assert str(Coordinate.parse("z")) == "z"

    def test_1d_double_letter(self) -> None:
        """Round-trip double letter."""
        assert str(Coordinate.parse("aa")) == "aa"
        assert str(Coordinate.parse("ab")) == "ab"
        assert str(Coordinate.parse("az")) == "az"
        assert str(Coordinate.parse("ba")) == "ba"
        assert str(Coordinate.parse("iv")) == "iv"

    def test_2d_chess_squares(self) -> None:
        """Round-trip chess-style squares."""
        assert str(Coordinate.parse("a1")) == "a1"
        assert str(Coordinate.parse("e4")) == "e4"
        assert str(Coordinate.parse("h8")) == "h8"

    def test_2d_extended(self) -> None:
        """Round-trip extended 2D coordinates."""
        assert str(Coordinate.parse("aa10")) == "aa10"
        assert str(Coordinate.parse("iv256")) == "iv256"

    def test_3d_basic(self) -> None:
        """Round-trip 3D coordinates."""
        assert str(Coordinate.parse("a1A")) == "a1A"
        assert str(Coordinate.parse("b2B")) == "b2B"
        assert str(Coordinate.parse("c3C")) == "c3C"

    def test_3d_extended(self) -> None:
        """Round-trip extended 3D coordinates."""
        assert str(Coordinate.parse("a1AA")) == "a1AA"
        assert str(Coordinate.parse("iv256IV")) == "iv256IV"


class TestRoundTripIndicesToIndices:
    """Tests for indices → Coordinate → indices round-trip."""

    def test_1d_indices(self) -> None:
        """Round-trip 1D indices."""
        assert Coordinate(0).indices == (0,)
        assert Coordinate(25).indices == (25,)
        assert Coordinate(26).indices == (26,)
        assert Coordinate(255).indices == (255,)

    def test_2d_indices(self) -> None:
        """Round-trip 2D indices."""
        assert Coordinate(0, 0).indices == (0, 0)
        assert Coordinate(4, 3).indices == (4, 3)
        assert Coordinate(7, 7).indices == (7, 7)
        assert Coordinate(255, 255).indices == (255, 255)

    def test_3d_indices(self) -> None:
        """Round-trip 3D indices."""
        assert Coordinate(0, 0, 0).indices == (0, 0, 0)
        assert Coordinate(1, 1, 1).indices == (1, 1, 1)
        assert Coordinate(255, 255, 255).indices == (255, 255, 255)


class TestRoundTripFullCycle:
    """Tests for complete round-trip: string → indices → string → indices."""

    def test_full_cycle_1d(self) -> None:
        """Full cycle for 1D coordinate."""
        original = "e"
        coord1 = Coordinate.parse(original)
        formatted = str(coord1)
        coord2 = Coordinate.parse(formatted)
        assert formatted == original
        assert coord2.indices == coord1.indices

    def test_full_cycle_2d(self) -> None:
        """Full cycle for 2D coordinate."""
        original = "e4"
        coord1 = Coordinate.parse(original)
        formatted = str(coord1)
        coord2 = Coordinate.parse(formatted)
        assert formatted == original
        assert coord2.indices == coord1.indices

    def test_full_cycle_3d(self) -> None:
        """Full cycle for 3D coordinate."""
        original = "b2B"
        coord1 = Coordinate.parse(original)
        formatted = str(coord1)
        coord2 = Coordinate.parse(formatted)
        assert formatted == original
        assert coord2.indices == coord1.indices

    def test_full_cycle_max(self) -> None:
        """Full cycle for maximum coordinate."""
        original = "iv256IV"
        coord1 = Coordinate.parse(original)
        formatted = str(coord1)
        coord2 = Coordinate.parse(formatted)
        assert formatted == original
        assert coord2.indices == coord1.indices


class TestRoundTripIndicesToString:
    """Tests for indices → string → indices round-trip."""

    def test_indices_to_string_1d(self) -> None:
        """Round-trip 1D via string."""
        original = (4,)
        coord = Coordinate(*original)
        parsed = Coordinate.parse(str(coord))
        assert parsed.indices == original

    def test_indices_to_string_2d(self) -> None:
        """Round-trip 2D via string."""
        original = (4, 3)
        coord = Coordinate(*original)
        parsed = Coordinate.parse(str(coord))
        assert parsed.indices == original

    def test_indices_to_string_3d(self) -> None:
        """Round-trip 3D via string."""
        original = (1, 1, 1)
        coord = Coordinate(*original)
        parsed = Coordinate.parse(str(coord))
        assert parsed.indices == original


class TestRoundTripAllSingleLetters:
    """Round-trip all single letters (a-z)."""

    @pytest.mark.parametrize("index", range(26))
    def test_single_letter_round_trip(self, index: int) -> None:
        """Each single letter round-trips correctly."""
        coord = Coordinate(index)
        assert Coordinate.parse(str(coord)).indices == (index,)


class TestRoundTripChessBoard:
    """Round-trip all chess board squares."""

    @pytest.mark.parametrize("file", range(8))
    @pytest.mark.parametrize("rank", range(8))
    def test_chess_square_round_trip(self, file: int, rank: int) -> None:
        """Each chess square round-trips correctly."""
        coord = Coordinate(file, rank)
        assert Coordinate.parse(str(coord)).indices == (file, rank)


class TestRoundTripBoundaryValues:
    """Round-trip boundary values."""

    def test_min_indices_1d(self) -> None:
        """Minimum 1D index."""
        assert Coordinate.parse(str(Coordinate(0))).indices == (0,)

    def test_max_indices_1d(self) -> None:
        """Maximum 1D index."""
        assert Coordinate.parse(str(Coordinate(255))).indices == (255,)

    def test_min_indices_2d(self) -> None:
        """Minimum 2D indices."""
        assert Coordinate.parse(str(Coordinate(0, 0))).indices == (0, 0)

    def test_max_indices_2d(self) -> None:
        """Maximum 2D indices."""
        assert Coordinate.parse(str(Coordinate(255, 255))).indices == (255, 255)

    def test_min_indices_3d(self) -> None:
        """Minimum 3D indices."""
        assert Coordinate.parse(str(Coordinate(0, 0, 0))).indices == (0, 0, 0)

    def test_max_indices_3d(self) -> None:
        """Maximum 3D indices."""
        assert Coordinate.parse(str(Coordinate(255, 255, 255))).indices == (
            255,
            255,
            255,
        )

    def test_mixed_boundary_values(self) -> None:
        """Mixed min/max values."""
        assert Coordinate.parse(str(Coordinate(0, 255))).indices == (0, 255)
        assert Coordinate.parse(str(Coordinate(255, 0))).indices == (255, 0)
        assert Coordinate.parse(str(Coordinate(0, 255, 0))).indices == (0, 255, 0)
        assert Coordinate.parse(str(Coordinate(255, 0, 255))).indices == (255, 0, 255)
