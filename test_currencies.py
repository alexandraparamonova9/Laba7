import unittest

from currencies import get_currencies


class TestCurrencies(unittest.TestCase):
    def test_real_currency(self):
        result = get_currencies(["USD"])
        self.assertIn("USD", result)

    def test_invalid_url(self):
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://invalid")

    def test_missing_currency(self):
        with self.assertRaises(KeyError):
            get_currencies(["XXX"])


