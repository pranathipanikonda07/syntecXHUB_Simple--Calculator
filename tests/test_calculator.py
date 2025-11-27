import unittest

from calculator import calculate, parse_input, CalculationError


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculate(2, '+', 3), 5)

    def test_subtract(self):
        self.assertEqual(calculate(5.5, '-', 1.5), 4.0)

    def test_multiply(self):
        self.assertEqual(calculate(-2, '*', -4), 8)

    def test_divide(self):
        self.assertAlmostEqual(calculate(7, '/', 2), 3.5)

    def test_divide_by_zero(self):
        with self.assertRaises(CalculationError):
            calculate(1, '/', 0)


class TestParseInput(unittest.TestCase):
    def test_valid_expr(self):
        op, a, _, b = parse_input('  12  +  3 ')
        self.assertEqual(op, '+')
        self.assertEqual(a, 12.0)
        self.assertEqual(b, 3.0)

    def test_invalid_format(self):
        with self.assertRaises(CalculationError):
            parse_input('not_an_expression')

    def test_invalid_number(self):
        with self.assertRaises(CalculationError):
            parse_input('12 + twelve')

    def test_clear_and_exit(self):
        self.assertEqual(parse_input('clear')[0], 'clear')
        self.assertEqual(parse_input('exit')[0], 'exit')


if __name__ == '__main__':
    unittest.main()
