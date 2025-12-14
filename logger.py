import functools
import logging
import sys
from typing import Any, Callable, Optional


def logger(
    func: Optional[Callable] = None, *, handle: Any = sys.stdout
) -> Callable:
    """
    Параметризуемый декоратор логирования.
    Логирует:
    - старт вызова функции и аргументы (INFO);
    - успешное завершение и результат (INFO);
    - ошибки и тип исключения (ERROR).

    В зависимости от типа handle:
    - logging.Logger -> log.info / log.error
    - файловый поток / StringIO -> handle.write()

    :param func: декорируемая функция
    :param handle: поток вывода или logging.Logger
    :return: обёрнутая функция
    """

    def decorator(inner_func: Callable) -> Callable:
        @functools.wraps(inner_func)
        def wrapper(*args, **kwargs):
            def log_info(message: str) -> None:
                if isinstance(handle, logging.Logger):
                    handle.info(message)
                else:
                    handle.write(f"INFO: {message}\n")

            def log_error(message: str) -> None:
                if isinstance(handle, logging.Logger):
                    handle.error(message)
                else:
                    handle.write(f"ERROR: {message}\n")

            log_info(
                f"Calling {inner_func.__name__} "
                f"args={args}, kwargs={kwargs}"
            )

            try:
                result = inner_func(*args, **kwargs)
                log_info(
                    f"{inner_func.__name__} finished successfully, "
                    f"result={result}"
                )
                return result
            except Exception as exc:
                log_error(
                    f"{inner_func.__name__} failed with "
                    f"{type(exc).__name__}: {exc}"
                )
                raise

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator
