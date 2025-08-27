from datetime import datetime
from unittest.mock import MagicMock, patch

from src import views


def test_get_home_json(home_json: str) -> None:
    """
    Проверка функции get_home_json, которая
    принимающет на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающет JSON-ответ с данными
    :param home_json: Фикстура содержимого JSON-ответа с данными
    :return: JSON-ответ с соответствующими данными
    """

    datetime_str = "2021-08-20 14:05:37"

    # Выполняем тестирование
    result = views.get_home_json(datetime_str)

    assert result == home_json


@patch("src.views.datetime")
def test_get_home_json_datetime_now(mock_datetime: MagicMock) -> None:
    """
    Проверка функции get_home_json, которая
    принимающет на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающет JSON-ответ с данными
    :param mock_datetime: Фикстура заменяющая src.views.datetime
    :return: JSON-ответ с соответствующими данными
    """

    datetime_str = "2021-08-20 14:05:37"

    home_json_datetame_now = """{
    "greeting": "Добрый день",
    "cards": [
        {
            "last_digits": "4556",
            "total_spent": 3361.7,
            "cashback": 154.0
        },
        {
            "last_digits": "7197",
            "total_spent": 6773.49,
            "cashback": 0.0
        }
    ],
    "top_transactions": [
        {
            "date": "20.08.2021",
            "amount": -226.7,
            "category": "Супермаркеты",
            "description": "Магнит"
        },
        {
            "date": "19.08.2021",
            "amount": -40.0,
            "category": "Фастфуд",
            "description": "Rumyanyj Khleb"
        },
        {
            "date": "18.08.2021",
            "amount": -115.98,
            "category": "Супермаркеты",
            "description": "Магнит"
        },
        {
            "date": "18.08.2021",
            "amount": -7632.84,
            "category": "ЖКХ",
            "description": "ЖКУ Квартира"
        },
        {
            "date": "18.08.2021",
            "amount": -112.26,
            "category": "Другое",
            "description": "Kvartplata.Info"
        }
    ],
    "currency_rates": [
        {
            "currency": "USD",
            "rate": 80.61
        },
        {
            "currency": "EUR",
            "rate": 93.87
        }
    ],
    "stock_prices": [
        {
            "stock": "AAPL",
            "price": 0
        },
        {
            "stock": "AMZN",
            "price": 0
        },
        {
            "stock": "GOOGL",
            "price": 0
        },
        {
            "stock": "MSFT",
            "price": 0
        },
        {
            "stock": "TSLA",
            "price": 0
        }
    ]
}"""

    # Эмулируем текущую дату, совпадающую с предоставленной датой
    mock_datetime.now.return_value = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    # Выполняем тестовую функцию
    result = views.get_home_json(datetime_str)

    assert result == home_json_datetame_now
