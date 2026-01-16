"""Tests for the formatter module."""

import unittest

from sashite_cell.formatter import format_indices


class TestFormatIndices1D(unittest.TestCase):
    """Tests for 1D coordinates (lowercase letters)."""

    def test_formats_index_0_as_a(self) -> None:
        self.assertEqual(format_indices((0,)), "a")

    def test_formats_index_4_as_e(self) -> None:
        self.assertEqual(format_indices((4,)), "e")

    def test_formats_index_25_as_z(self) -> None:
        self.assertEqual(format_indices((25,)), "z")

    def test_formats_index_26_as_aa(self) -> None:
        self.assertEqual(format_indices((26,)), "aa")

    def test_formats_index_27_as_ab(self) -> None:
        self.assertEqual(format_indices((27,)), "ab")

    def test_formats_index_51_as_az(self) -> None:
        self.assertEqual(format_indices((51,)), "az")

    def test_formats_index_52_as_ba(self) -> None:
        self.assertEqual(format_indices((52,)), "ba")

    def test_formats_index_255_as_iv(self) -> None:
        self.assertEqual(format_indices((255,)), "iv")


class TestFormatIndices2D(unittest.TestCase):
    """Tests for 2D coordinates (lowercase + integer)."""

    def test_formats_0_0_as_a1(self) -> None:
        self.assertEqual(format_indices((0, 0)), "a1")

    def test_formats_4_3_as_e4(self) -> None:
        self.assertEqual(format_indices((4, 3)), "e4")

    def test_formats_7_7_as_h8(self) -> None:
        self.assertEqual(format_indices((7, 7)), "h8")

    def test_formats_0_255_as_a256(self) -> None:
        self.assertEqual(format_indices((0, 255)), "a256")

    def test_formats_255_255_as_iv256(self) -> None:
        self.assertEqual(format_indices((255, 255)), "iv256")

    def test_formats_26_9_as_aa10(self) -> None:
        self.assertEqual(format_indices((26, 9)), "aa10")


class TestFormatIndices3D(unittest.TestCase):
    """Tests for 3D coordinates (lowercase + integer + uppercase)."""

    def test_formats_0_0_0_as_a1A(self) -> None:
        self.assertEqual(format_indices((0, 0, 0)), "a1A")

    def test_formats_4_3_1_as_e4B(self) -> None:
        self.assertEqual(format_indices((4, 3, 1)), "e4B")

    def test_formats_2_2_2_as_c3C(self) -> None:
        self.assertEqual(format_indices((2, 2, 2)), "c3C")

    def test_formats_0_0_25_as_a1Z(self) -> None:
        self.assertEqual(format_indices((0, 0, 25)), "a1Z")

    def test_formats_0_0_26_as_a1AA(self) -> None:
        self.assertEqual(format_indices((0, 0, 26)), "a1AA")

    def test_formats_0_0_255_as_a1IV(self) -> None:
        self.assertEqual(format_indices((0, 0, 255)), "a1IV")

    def test_formats_255_255_255_as_iv256IV(self) -> None:
        self.assertEqual(format_indices((255, 255, 255)), "iv256IV")


class TestFormatIndicesOutputProperties(unittest.TestCase):
    """Tests for output properties."""

    def test_returns_string(self) -> None:
        result = format_indices((4, 3))
        self.assertIsInstance(result, str)

    def test_returns_new_string_each_time(self) -> None:
        result1 = format_indices((4, 3))
        result2 = format_indices((4, 3))
        self.assertEqual(result1, result2)


class TestFormatIndicesBoundaryValues(unittest.TestCase):
    """Tests for boundary values."""

    def test_formats_minimum_values_0(self) -> None:
        self.assertEqual(format_indices((0,)), "a")

    def test_formats_maximum_1d_value_255(self) -> None:
        self.assertEqual(format_indices((255,)), "iv")

    def test_formats_minimum_3d_values_0_0_0(self) -> None:
        self.assertEqual(format_indices((0, 0, 0)), "a1A")

    def test_formats_maximum_3d_values_255_255_255(self) -> None:
        self.assertEqual(format_indices((255, 255, 255)), "iv256IV")

    def test_formats_boundary_value_25(self) -> None:
        self.assertEqual(format_indices((25, 25, 25)), "z26Z")

    def test_formats_boundary_value_26(self) -> None:
        self.assertEqual(format_indices((26, 26, 26)), "aa27AA")


class TestFormatIndicesEmptyInput(unittest.TestCase):
    """Tests for empty input."""

    def test_formats_empty_tuple_as_empty_string(self) -> None:
        self.assertEqual(format_indices(()), "")


if __name__ == "__main__":
    unittest.main()
