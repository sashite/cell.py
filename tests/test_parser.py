"""Tests for the parser module."""

import unittest

from sashite_cell.parser import parse_to_indices


class TestParseToIndices1D(unittest.TestCase):
    """Tests for valid 1D coordinates (lowercase letters)."""

    def test_parses_a_as_0(self) -> None:
        self.assertEqual(parse_to_indices("a"), (0,))

    def test_parses_e_as_4(self) -> None:
        self.assertEqual(parse_to_indices("e"), (4,))

    def test_parses_z_as_25(self) -> None:
        self.assertEqual(parse_to_indices("z"), (25,))

    def test_parses_aa_as_26(self) -> None:
        self.assertEqual(parse_to_indices("aa"), (26,))

    def test_parses_ab_as_27(self) -> None:
        self.assertEqual(parse_to_indices("ab"), (27,))

    def test_parses_az_as_51(self) -> None:
        self.assertEqual(parse_to_indices("az"), (51,))

    def test_parses_ba_as_52(self) -> None:
        self.assertEqual(parse_to_indices("ba"), (52,))

    def test_parses_iv_as_255(self) -> None:
        self.assertEqual(parse_to_indices("iv"), (255,))


class TestParseToIndices2D(unittest.TestCase):
    """Tests for valid 2D coordinates (lowercase + integer)."""

    def test_parses_a1_as_0_0(self) -> None:
        self.assertEqual(parse_to_indices("a1"), (0, 0))

    def test_parses_e4_as_4_3(self) -> None:
        self.assertEqual(parse_to_indices("e4"), (4, 3))

    def test_parses_h8_as_7_7(self) -> None:
        self.assertEqual(parse_to_indices("h8"), (7, 7))

    def test_parses_a256_as_0_255(self) -> None:
        self.assertEqual(parse_to_indices("a256"), (0, 255))

    def test_parses_iv256_as_255_255(self) -> None:
        self.assertEqual(parse_to_indices("iv256"), (255, 255))

    def test_parses_aa10_as_26_9(self) -> None:
        self.assertEqual(parse_to_indices("aa10"), (26, 9))


class TestParseToIndices3D(unittest.TestCase):
    """Tests for valid 3D coordinates (lowercase + integer + uppercase)."""

    def test_parses_a1A_as_0_0_0(self) -> None:
        self.assertEqual(parse_to_indices("a1A"), (0, 0, 0))

    def test_parses_e4B_as_4_3_1(self) -> None:
        self.assertEqual(parse_to_indices("e4B"), (4, 3, 1))

    def test_parses_c3C_as_2_2_2(self) -> None:
        self.assertEqual(parse_to_indices("c3C"), (2, 2, 2))

    def test_parses_a1Z_as_0_0_25(self) -> None:
        self.assertEqual(parse_to_indices("a1Z"), (0, 0, 25))

    def test_parses_a1AA_as_0_0_26(self) -> None:
        self.assertEqual(parse_to_indices("a1AA"), (0, 0, 26))

    def test_parses_a1IV_as_0_0_255(self) -> None:
        self.assertEqual(parse_to_indices("a1IV"), (0, 0, 255))

    def test_parses_iv256IV_as_255_255_255(self) -> None:
        self.assertEqual(parse_to_indices("iv256IV"), (255, 255, 255))


class TestParseToIndicesEmptyInput(unittest.TestCase):
    """Tests for empty input."""

    def test_raises_on_empty_string(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("")
        self.assertIn("empty input", str(ctx.exception))


class TestParseToIndicesInputTooLong(unittest.TestCase):
    """Tests for input too long."""

    def test_raises_on_8_characters(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("iv256IVa")
        self.assertIn("input exceeds 7 characters", str(ctx.exception))

    def test_raises_on_very_long_input(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("abcdefghijklmnop")
        self.assertIn("input exceeds 7 characters", str(ctx.exception))


class TestParseToIndicesInvalidStart(unittest.TestCase):
    """Tests for must start with lowercase."""

    def test_raises_on_uppercase_start(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("A")
        self.assertIn("must start with lowercase letter", str(ctx.exception))

    def test_raises_on_digit_start(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("1")
        self.assertIn("must start with lowercase letter", str(ctx.exception))

    def test_raises_on_space_start(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices(" a1")
        self.assertIn("must start with lowercase letter", str(ctx.exception))

    def test_raises_on_special_character_start(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("@a1")
        self.assertIn("must start with lowercase letter", str(ctx.exception))


class TestParseToIndicesUnexpectedCharacter(unittest.TestCase):
    """Tests for unexpected character."""

    def test_raises_on_uppercase_after_lowercase(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("aA")
        self.assertIn("unexpected character", str(ctx.exception))

    def test_raises_on_special_character_in_middle(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a@1")
        self.assertIn("unexpected character", str(ctx.exception))

    def test_raises_on_space_in_middle(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a 1")
        self.assertIn("unexpected character", str(ctx.exception))


class TestParseToIndicesLeadingZero(unittest.TestCase):
    """Tests for leading zero."""

    def test_raises_on_zero_as_integer(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a0")
        self.assertIn("leading zero", str(ctx.exception))

    def test_raises_on_01(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a01")
        self.assertIn("leading zero", str(ctx.exception))

    def test_raises_on_007(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a007")
        self.assertIn("leading zero", str(ctx.exception))


class TestParseToIndicesTooManyDimensions(unittest.TestCase):
    """Tests for exceeds 3 dimensions."""

    def test_raises_on_4d_coordinate(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a1Aa")
        self.assertIn("exceeds 3 dimensions", str(ctx.exception))


class TestParseToIndicesIndexOutOfRange(unittest.TestCase):
    """Tests for index out of range."""

    def test_raises_on_integer_257(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a257")
        self.assertIn("index exceeds 255", str(ctx.exception))

    def test_raises_on_integer_999(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a999")
        self.assertIn("index exceeds 255", str(ctx.exception))

    def test_raises_on_lowercase_iw(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("iw")
        self.assertIn("index exceeds 255", str(ctx.exception))

    def test_raises_on_uppercase_IW(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_to_indices("a1IW")
        self.assertIn("index exceeds 255", str(ctx.exception))


class TestParseToIndicesSecurity(unittest.TestCase):
    """Tests for security (malicious inputs)."""

    def test_rejects_null_byte_injection(self) -> None:
        with self.assertRaises(ValueError):
            parse_to_indices("a\x00")

    def test_rejects_newline_injection(self) -> None:
        with self.assertRaises(ValueError):
            parse_to_indices("a\n1")

    def test_rejects_carriage_return_injection(self) -> None:
        with self.assertRaises(ValueError):
            parse_to_indices("a\r1")

    def test_rejects_tab_injection(self) -> None:
        with self.assertRaises(ValueError):
            parse_to_indices("a\t1")

    def test_rejects_unicode_letter_lookalikes(self) -> None:
        # Cyrillic small letter A (U+0430) looks like Latin 'a'
        with self.assertRaises(ValueError):
            parse_to_indices("\u0430")

    def test_rejects_full_width_characters(self) -> None:
        # Full-width 'a' (U+FF41)
        with self.assertRaises(ValueError):
            parse_to_indices("\uff41")

    def test_rejects_combining_characters(self) -> None:
        with self.assertRaises(ValueError):
            parse_to_indices("a\u0301")

    def test_rejects_zero_width_characters(self) -> None:
        with self.assertRaises(ValueError):
            parse_to_indices("a\u200b1")

    def test_handles_maximum_valid_input(self) -> None:
        result = parse_to_indices("iv256IV")
        self.assertEqual(result, (255, 255, 255))


class TestParseToIndicesRoundTrip(unittest.TestCase):
    """Tests for round-trip (parse -> format -> parse)."""

    def test_round_trips_e4(self) -> None:
        from sashite_cell.formatter import format_indices

        indices = parse_to_indices("e4")
        formatted = format_indices(indices)
        reparsed = parse_to_indices(formatted)
        self.assertEqual(reparsed, indices)

    def test_round_trips_iv256IV(self) -> None:
        from sashite_cell.formatter import format_indices

        indices = parse_to_indices("iv256IV")
        formatted = format_indices(indices)
        reparsed = parse_to_indices(formatted)
        self.assertEqual(reparsed, indices)

    def test_round_trips_aa27AA(self) -> None:
        from sashite_cell.formatter import format_indices

        indices = parse_to_indices("aa27AA")
        formatted = format_indices(indices)
        reparsed = parse_to_indices(formatted)
        self.assertEqual(reparsed, indices)


if __name__ == "__main__":
    unittest.main()
