import io
import unittest

from logger import logger


class TestLogger(unittest.TestCase):
    """
    Тестирование параметризуемого декоратора logger.
    Проверяются логи и проброс исключений.
    """

    def setUp(self):
        # Используем StringIO, чтобы перехватывать вывод
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def double(x):
            return x * 2

        @logger(handle=self.stream)
        def broken():
            raise ValueError("boom")

        self.double = double
        self.broken = broken

    def test_success_logging(self):
        """Проверка логов при успешном выполнении функции"""
        result = self.double(5)
        logs = self.stream.getvalue()

        self.assertEqual(result, 10)
        self.assertIn("INFO", logs)
        self.assertIn("Calling double", logs)
        self.assertIn("double finished successfully", logs)
        self.assertIn("result=10", logs)

    def test_error_logging(self):
        """Проверка логов при выбросе исключения"""
        with self.assertRaises(ValueError):
            self.broken()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("boom", logs)

