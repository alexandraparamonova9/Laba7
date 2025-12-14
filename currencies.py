"""
Модуль получения курсов валют с API ЦБ РФ.
"""

from typing import Dict, List
import requests

from logger import logger


@logger()
def get_currencies(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
) -> Dict[str, float]:
    """
    Получает курсы валют по кодам.

    :param currency_codes: список кодов валют (например ["USD", "EUR"])
    :param url: URL API
    :return: словарь {код: курс}
    :raises ConnectionError: если API недоступен
    :raises ValueError: если JSON некорректен
    :raises KeyError: если отсутствуют нужные ключи
    :raises TypeError: если курс имеет неверный тип
    """

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError("API is unavailable") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError("Invalid JSON") from exc

    if "Valute" not in data:
        raise KeyError("Key 'Valute' not found")

    valutes = data["Valute"]
    result: Dict[str, float] = {}

    for code in currency_codes:
        if code not in valutes:
            raise KeyError(f"Currency {code} not found")

        value = valutes[code].get("Value")
        if not isinstance(value, (int, float)):
            raise TypeError(f"Invalid value type for {code}")

        result[code] = float(value)

    return result
