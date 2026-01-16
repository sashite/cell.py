"""Tests for the Coordinate class."""

import unittest

from sashite_cell import Coordinate


class TestCoordinateConstructor(unittest.TestCase):
    """Tests for Coordinate constructor."""

    def test_creates_1d_coordinate(self) -> None:
        coord = Coordinate(0)
        self.assertEqual(coord.dimensions, 1)
        self.assertEqual(coord.indices, (0,))

    def test_creates_2d_coordinate(self) -> None:
        coord = Coordinate(4, 3)
        self.assertEqual(coord.dimensions, 2)
        self.assertEqual(coord.indices, (4, 3))

    def test_creates_3d_coordinate(self) -> None:
        coord = Coordinate(0, 0, 0)
        self.assertEqual(coord.dimensions, 3)
        self.assertEqual(coord.indices, (0, 0, 0))

    def test_accepts_index_0(self) -> None:
        coord = Coordinate(0)
        self.assertEqual(coord.indices, (0,))

    def test_accepts_index_255(self) -> None:
        coord = Coordinate(255)
        self.assertEqual(coord.indices, (255,))

    def test_raises_on_no_indices(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate()
        self.assertIn("at least one index required", str(ctx.exception))

    def test_raises_on_more_than_3_indices(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate(0, 0, 0, 0)
        self.assertIn("exceeds 3 dimensions", str(ctx.exception))

    def test_raises_on_negative_index(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate(-1)
        self.assertIn("index exceeds 255", str(ctx.exception))

    def test_raises_on_index_greater_than_255(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate(256)
        self.assertIn("index exceeds 255", str(ctx.exception))

    def test_raises_on_float_index(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate(1.5)  # type: ignore[arg-type]
        self.assertIn("index must be an integer", str(ctx.exception))

    def test_raises_on_string_index(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate("a")  # type: ignore[arg-type]
        self.assertIn("index must be an integer", str(ctx.exception))

    def test_raises_on_none_index(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate(None)  # type: ignore[arg-type]
        self.assertIn("index must be an integer", str(ctx.exception))

    def test_raises_on_bool_index(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Coordinate(True)  # type: ignore[arg-type]
        self.assertIn("index must be an integer", str(ctx.exception))


class TestCoordinateDimensions(unittest.TestCase):
    """Tests for Coordinate.dimensions property."""

    def test_returns_1_for_1d_coordinate(self) -> None:
        self.assertEqual(Coordinate(5).dimensions, 1)

    def test_returns_2_for_2d_coordinate(self) -> None:
        self.assertEqual(Coordinate(4, 3).dimensions, 2)

    def test_returns_3_for_3d_coordinate(self) -> None:
        self.assertEqual(Coordinate(0, 0, 0).dimensions, 3)


class TestCoordinateIndices(unittest.TestCase):
    """Tests for Coordinate.indices property."""

    def test_returns_tuple(self) -> None:
        coord = Coordinate(4, 3)
        self.assertIsInstance(coord.indices, tuple)
        self.assertEqual(coord.indices, (4, 3))

    def test_returns_same_reference_on_multiple_calls(self) -> None:
        coord = Coordinate(4, 3)
        self.assertIs(coord.indices, coord.indices)


class TestCoordinateStr(unittest.TestCase):
    """Tests for Coordinate.__str__ (1D coordinates - lowercase letters)."""

    def test_encodes_index_0_as_a(self) -> None:
        self.assertEqual(str(Coordinate(0)), "a")

    def test_encodes_index_4_as_e(self) -> None:
        self.assertEqual(str(Coordinate(4)), "e")

    def test_encodes_index_25_as_z(self) -> None:
        self.assertEqual(str(Coordinate(25)), "z")

    def test_encodes_index_26_as_aa(self) -> None:
        self.assertEqual(str(Coordinate(26)), "aa")

    def test_encodes_index_27_as_ab(self) -> None:
        self.assertEqual(str(Coordinate(27)), "ab")

    def test_encodes_index_51_as_az(self) -> None:
        self.assertEqual(str(Coordinate(51)), "az")

    def test_encodes_index_52_as_ba(self) -> None:
        self.assertEqual(str(Coordinate(52)), "ba")

    def test_encodes_index_255_as_iv(self) -> None:
        self.assertEqual(str(Coordinate(255)), "iv")


class TestCoordinateStr2D(unittest.TestCase):
    """Tests for Coordinate.__str__ (2D coordinates - lowercase + integer)."""

    def test_encodes_0_0_as_a1(self) -> None:
        self.assertEqual(str(Coordinate(0, 0)), "a1")

    def test_encodes_4_3_as_e4(self) -> None:
        self.assertEqual(str(Coordinate(4, 3)), "e4")

    def test_encodes_7_7_as_h8(self) -> None:
        self.assertEqual(str(Coordinate(7, 7)), "h8")

    def test_encodes_0_255_as_a256(self) -> None:
        self.assertEqual(str(Coordinate(0, 255)), "a256")

    def test_encodes_255_255_as_iv256(self) -> None:
        self.assertEqual(str(Coordinate(255, 255)), "iv256")


class TestCoordinateStr3D(unittest.TestCase):
    """Tests for Coordinate.__str__ (3D coordinates - lowercase + integer + uppercase)."""

    def test_encodes_0_0_0_as_a1A(self) -> None:
        self.assertEqual(str(Coordinate(0, 0, 0)), "a1A")

    def test_encodes_4_3_1_as_e4B(self) -> None:
        self.assertEqual(str(Coordinate(4, 3, 1)), "e4B")

    def test_encodes_2_2_2_as_c3C(self) -> None:
        self.assertEqual(str(Coordinate(2, 2, 2)), "c3C")

    def test_encodes_0_0_25_as_a1Z(self) -> None:
        self.assertEqual(str(Coordinate(0, 0, 25)), "a1Z")

    def test_encodes_0_0_26_as_a1AA(self) -> None:
        self.assertEqual(str(Coordinate(0, 0, 26)), "a1AA")

    def test_encodes_0_0_255_as_a1IV(self) -> None:
        self.assertEqual(str(Coordinate(0, 0, 255)), "a1IV")

    def test_encodes_255_255_255_as_iv256IV(self) -> None:
        self.assertEqual(str(Coordinate(255, 255, 255)), "iv256IV")


class TestCoordinateEquality(unittest.TestCase):
    """Tests for Coordinate equality."""

    def test_equal_coordinates_are_equal(self) -> None:
        a = Coordinate(4, 3)
        b = Coordinate(4, 3)
        self.assertEqual(a, b)

    def test_different_coordinates_are_not_equal(self) -> None:
        a = Coordinate(4, 3)
        b = Coordinate(3, 4)
        self.assertNotEqual(a, b)

    def test_different_dimensions_are_not_equal(self) -> None:
        a = Coordinate(4, 3)
        b = Coordinate(4, 3, 0)
        self.assertNotEqual(a, b)

    def test_not_equal_to_tuple(self) -> None:
        a = Coordinate(4, 3)
        self.assertNotEqual(a, (4, 3))

    def test_not_equal_to_string(self) -> None:
        a = Coordinate(4, 3)
        self.assertNotEqual(a, "e4")


class TestCoordinateHash(unittest.TestCase):
    """Tests for Coordinate hashing."""

    def test_equal_coordinates_have_same_hash(self) -> None:
        a = Coordinate(4, 3)
        b = Coordinate(4, 3)
        self.assertEqual(hash(a), hash(b))

    def test_can_be_used_as_dict_key(self) -> None:
        coord = Coordinate(4, 3)
        d = {coord: "value"}
        lookup = Coordinate(4, 3)
        self.assertEqual(d[lookup], "value")

    def test_can_be_used_in_set(self) -> None:
        a = Coordinate(4, 3)
        b = Coordinate(4, 3)
        c = Coordinate(0, 0)
        s = {a, b, c}
        self.assertEqual(len(s), 2)


class TestCoordinateRepr(unittest.TestCase):
    """Tests for Coordinate.__repr__."""

    def test_returns_readable_representation(self) -> None:
        coord = Coordinate(4, 3)
        result = repr(coord)
        self.assertIn("Coordinate", result)
        self.assertIn("4", result)
        self.assertIn("3", result)

    def test_repr_format(self) -> None:
        coord = Coordinate(4, 3)
        self.assertEqual(repr(coord), "Coordinate(4, 3)")

    def test_repr_1d(self) -> None:
        coord = Coordinate(0)
        self.assertEqual(repr(coord), "Coordinate(0)")

    def test_repr_3d(self) -> None:
        coord = Coordinate(1, 2, 3)
        self.assertEqual(repr(coord), "Coordinate(1, 2, 3)")


class TestCoordinateParse(unittest.TestCase):
    """Tests for Coordinate.parse class method."""

    def test_parses_1d_coordinate(self) -> None:
        coord = Coordinate.parse("e")
        self.assertEqual(coord.indices, (4,))

    def test_parses_2d_coordinate(self) -> None:
        coord = Coordinate.parse("e4")
        self.assertEqual(coord.indices, (4, 3))

    def test_parses_3d_coordinate(self) -> None:
        coord = Coordinate.parse("a1A")
        self.assertEqual(coord.indices, (0, 0, 0))

    def test_raises_on_invalid_input(self) -> None:
        with self.assertRaises(ValueError):
            Coordinate.parse("a0")


class TestCoordinateFormat(unittest.TestCase):
    """Tests for Coordinate.format class method."""

    def test_formats_1d_coordinate(self) -> None:
        self.assertEqual(Coordinate.format(4), "e")

    def test_formats_2d_coordinate(self) -> None:
        self.assertEqual(Coordinate.format(4, 3), "e4")

    def test_formats_3d_coordinate(self) -> None:
        self.assertEqual(Coordinate.format(2, 2, 2), "c3C")

    def test_raises_on_invalid_indices(self) -> None:
        with self.assertRaises(ValueError):
            Coordinate.format(256)


class TestCoordinateValidate(unittest.TestCase):
    """Tests for Coordinate.validate class method."""

    def test_returns_none_for_valid_input(self) -> None:
        result = Coordinate.validate("e4")
        self.assertIsNone(result)

    def test_raises_for_invalid_input(self) -> None:
        with self.assertRaises(ValueError):
            Coordinate.validate("a0")


class TestCoordinateIsValid(unittest.TestCase):
    """Tests for Coordinate.is_valid class method."""

    def test_returns_true_for_valid_input(self) -> None:
        self.assertTrue(Coordinate.is_valid("e4"))

    def test_returns_false_for_invalid_input(self) -> None:
        self.assertFalse(Coordinate.is_valid("a0"))

    def test_returns_false_for_empty_input(self) -> None:
        self.assertFalse(Coordinate.is_valid(""))


if __name__ == "__main__":
    unittest.main()
