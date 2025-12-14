"""
Демонстрационный пример работы декоратора.
"""

import math
import logging

from logger import logger

log = logging.getLogger("quadratic")
logging.basicConfig(level=logging.INFO)


@logger(handle=log)
def solve_quadratic(a: float, b: float, c: float):
    """
    Решает квадратное уравнение ax^2 + bx + c = 0.
    """

    if not all(isinstance(x, (int, float)) for x in (a, b, c)):
        raise TypeError("Coefficients must be numbers")

    if a == 0 and b == 0:
        log.critical("Impossible equation: a=b=0")
        raise ValueError("Invalid equation")

    if a == 0:
        return (-c / b,)

    d = b ** 2 - 4 * a * c

    if d < 0:
        log.warning("Discriminant < 0, no real roots")
        return ()

    sqrt_d = math.sqrt(d)
    return (
        (-b + sqrt_d) / (2 * a),
        (-b - sqrt_d) / (2 * a),
    )
