import io
import unittest

from logger import logger
from currencies import get_currencies


class TestLoggerStringIO(unittest.TestCase):
    """
    Тестирование работы декоратора с потоком io.StringIO.
    Проверяются логи при успешном вызове и при ошибках.
    """

    def setUp(self):
        # Создаём StringIO, чтобы перехватывать вывод
        self.stream = io.StringIO()

        # Декорируем функцию get_currencies с недоступным URL для проверки ошибки
        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(["USD"], url="https://invalid.url")

        self.wrapped = wrapped

        # Простая тестовая функция для успешного вызова
        @logger(handle=self.stream)
        def test_func(x):
            return x * 2

        self.test_func = test_func

    def test_logging_success(self):
        """Проверка логов при успешном вызове функции"""
        result = self.test_func(5)
        logs = self.stream.getvalue()

        self.assertEqual(result, 10)
        self.assertIn("INFO", logs)
        self.assertIn("Calling test_func", logs)
        self.assertIn("test_func finished successfully", logs)
        self.assertIn("result=10", logs)

    def test_logging_error(self):
        """Проверка логов при возникновении ошибки"""
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)

