"""Tests for the errors module."""

import unittest

from sashite_cell.errors import Messages


class TestMessagesConstants(unittest.TestCase):
    """Tests for Messages constants."""

    def test_empty_input_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.EMPTY_INPUT, "empty input")

    def test_input_too_long_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.INPUT_TOO_LONG, "input exceeds 7 characters")

    def test_invalid_start_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.INVALID_START, "must start with lowercase letter")

    def test_unexpected_character_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.UNEXPECTED_CHARACTER, "unexpected character")

    def test_leading_zero_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.LEADING_ZERO, "leading zero")

    def test_too_many_dimensions_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.TOO_MANY_DIMENSIONS, "exceeds 3 dimensions")

    def test_index_out_of_range_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.INDEX_OUT_OF_RANGE, "index exceeds 255")

    def test_no_indices_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.NO_INDICES, "at least one index required")

    def test_invalid_index_type_is_defined_correctly(self) -> None:
        self.assertEqual(Messages.INVALID_INDEX_TYPE, "index must be an integer")


class TestMessagesUsage(unittest.TestCase):
    """Tests for Messages usage with ValueError."""

    def test_messages_can_be_used_to_raise_errors(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            raise ValueError(Messages.EMPTY_INPUT)
        self.assertEqual(str(ctx.exception), "empty input")

    def test_messages_are_strings(self) -> None:
        self.assertIsInstance(Messages.EMPTY_INPUT, str)
        self.assertIsInstance(Messages.INPUT_TOO_LONG, str)
        self.assertIsInstance(Messages.INVALID_START, str)
        self.assertIsInstance(Messages.UNEXPECTED_CHARACTER, str)
        self.assertIsInstance(Messages.LEADING_ZERO, str)
        self.assertIsInstance(Messages.TOO_MANY_DIMENSIONS, str)
        self.assertIsInstance(Messages.INDEX_OUT_OF_RANGE, str)
        self.assertIsInstance(Messages.NO_INDICES, str)
        self.assertIsInstance(Messages.INVALID_INDEX_TYPE, str)


if __name__ == "__main__":
    unittest.main()
