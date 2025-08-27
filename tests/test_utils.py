import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
from pandas.testing import assert_frame_equal

from src import utils

# Задаём корневой путь проекта.
root_path = Path(__file__).resolve().parents[1]
file_of_names = os.path.join(root_path, "data\\user_settings.json")
bad_json_file = os.path.join(root_path, "data\\bad_json_file.json")


def test_get_greeting() -> None:
    """
    Проверка функции get_greeting, которая
    принимает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращает строку с приветствием
    :return: строка с приветствием
    """
    datetime_str = "2025-08-20 09:05:37"
    result = utils.get_greeting(datetime_str)
    assert result == "Доброе утро"

    datetime_str = "2025-08-20 14:05:37"
    result = utils.get_greeting(datetime_str)
    assert result == "Добрый день"

    datetime_str = "2025-08-20 19:05:37"
    result = utils.get_greeting(datetime_str)
    assert result == "Добрый вечер"

    datetime_str = "2025-08-20 02:05:37"
    result = utils.get_greeting(datetime_str)
    assert result == "Доброй ночи"

    datetime_str = "2025-08-20"
    result = utils.get_greeting(datetime_str)
    assert result == ""


@patch("pandas.read_excel")
def test_load_transactions_xlsx_file(mock_read_excel: MagicMock) -> None:
    """
    Проверка работы функции load_transactions_xlsx_file,
    которая считывает финансовые операции из XLSX
    :param mock_read_excel: Мокируемый объект pandas.read_excel
    :return: DataFrame с финансовыми операциями
    """
    # Подготавливаем пример DataFrame
    sample_data = {
        "Статус": ["OK"],
        "Сумма операции": [-1000],  # Можно добавить любые поля, необходимые для теста
    }
    expected_df = pd.DataFrame(sample_data)

    # Настройка макета: имитируем загрузку реального DataFrame
    mock_read_excel.return_value = expected_df

    # Тестируем функцию загрузки
    result = utils.load_transactions_xlsx_file("test.xlsx")

    # Теперь сравниваем фактический результат с ожиданием
    pd.testing.assert_frame_equal(result, expected_df)


@patch("pandas.read_excel")
def test_load_transactions_xlsx_error(mock_read_excel: MagicMock) -> None:
    """
    Проверка работы функции load_transactions_xlsx_file,
    которая считывает финансовые операции из XLSX
    ловим ошибки
    :param mock_read_excel: Моксированный объект pandas.read_excel
    :return: DataFrame с финансовыми операциями
    """
    empty_data: dict[str, list[Any]] = {
        "Дата операции": [],
        "Дата платежа": [],
        "Номер карты": [],
        "Статус": [],
        "Сумма операции": [],
        "Валюта операции": [],
        "Сумма платежа": [],
        "Валюта платежа": [],
        "Кэшбэк": [],
        "Категория": [],
        "MCC": [],
        "Описание": [],
        "Бонусы (включая кэшбэк)": [],
        "Округление на инвесткопилку": [],
        "Сумма операции с округлением": [],
    }
    expected_empty_df = pd.DataFrame(empty_data)

    mock_read_excel.side_effect = Exception
    result = utils.load_transactions_xlsx_file("test.xlsx")

    # Проверяем, что пустой dataframe совпадает с ожидаемым
    assert_frame_equal(result, expected_empty_df)


def test_get_cards_info(transactions_df: pd.DataFrame, cards_info_on_transactions_df: list[dict]) -> None:
    """
    Проверка функции get_cards_info, которая
    принимает DataFrame с банковскими операциями
    и возвращает список с информацией по каждой карте
    :param transactions_df: Фикстура DataFrame с финансовыми операциями
    :param cards_info_on_transactions_df: Фикстура с данными по картам
    :return: список с информацией по каждой карте
    """
    assert utils.get_cards_info(transactions_df) == cards_info_on_transactions_df


def test_get_top_transactions(transactions_df: pd.DataFrame, top_transactions_on_transactions_df: list[dict]) -> None:
    """
    Проверка функции get_top_transactions, которая
    принимает DataFrame с банковскими операциями
    и возвращает список с 5-ю последними транзакциями
    :param transactions_df: Фикстура DataFrame с финансовыми операциями
    :param top_transactions_on_transactions_df: Фикстура с данными по картам
    :return: список с информацией по каждой карте
    """
    assert utils.get_top_transactions(transactions_df) == top_transactions_on_transactions_df


def test_load_currencies_json_file() -> None:
    """
    Проверка работы функции load_currencies_json_file,
    которая принимает на вход путь до JSON-файла
    и возвращает список валют
    :return: список валют
    """
    assert utils.load_currencies_json_file(file_of_names) == ["USD", "EUR"]

    assert os.path.exists(file_of_names)

    assert utils.load_currencies_json_file("test") == ["USD", "EUR"]
    assert utils.load_currencies_json_file(bad_json_file) == ["USD", "EUR"]


@patch("requests.get")
def test_get_exchange_rate_success(mock_get: Any) -> None:
    """
    Проверка функции get_exchange_rate, которая
    принимает дату в формате 2025-08-20, список кодов валюты и код валюты обмена
    и возвращает список курсов обмена на дату
    :param mock_get: Фикстура заменяющая requests.get
    :return: список курсов обмена на дату
    """
    # Создаём фиктивный ответ от API
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"USD": 0.0, "EUR": 0.0}, "status_code": 200}
    mock_get.return_value = mock_response  # Подменяем реальный вызов requests.get фиктивным объектом

    currency_from = ["USD", "EUR"]
    currency_to = "RUB"
    date_str = "2025-08-20"

    # Выполняем тестируемую функцию
    result = utils.get_exchange_rate(date_str, currency_from, currency_to)

    # Проверяем результат
    assert result == [{"currency": "USD", "rate": 0.0}, {"currency": "EUR", "rate": 0.0}]


@patch("requests.get")
def test_get_exchange_rate_failure(mock_get: Any) -> None:
    """
    Проверка функции get_exchange_rate, конвертирующей сумму из одной валюты в другую
    Отлавливаем ошибки
    :param mock_get: Фикстура заменяющая requests.get
    :return: список курсов обмена
    """
    # Моделируем ошибку при получении данных
    mock_get.side_effect = Exception("Искусственная ошибка при обращении к API")

    # Выполнение тестируемой функции
    result = utils.get_exchange_rate("2025-08-20", ["USD", "EUR"], "RUB")

    # Ожидается, что при ошибке API вернутся нулевые значения
    assert result == [{"currency": "USD", "rate": 0.0}, {"currency": "EUR", "rate": 0.0}]


def test_load_prices_json_file() -> None:
    """
    Проверка работы функции load_prices_json_file,
    которая принимает на вход путь до JSON-файла
    и возвращает список акций
    :return: список акций
    """
    assert utils.load_prices_json_file(file_of_names) == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

    assert os.path.exists(file_of_names)

    assert utils.load_prices_json_file("test") == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    assert utils.load_prices_json_file(bad_json_file) == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def test_get_stock_prices() -> None:
    """
    Проверка работы функции get_stock_prices,
    которая принимает дату в формате 2025-08-20 список тикеров акций
    и возвращает список словарей со стоимостью акций
    :return: список акций
    """
    stock_prices_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    date_str = "2025-08-20"
    assert utils.get_stock_prices(date_str, stock_prices_list) == [
        {"stock": "AAPL", "price": 230.56},
        {"stock": "AMZN", "price": 228.01},
        {"stock": "GOOGL", "price": 201.57},
        {"stock": "MSFT", "price": 508.93},
        {"stock": "TSLA", "price": 329.31},
    ]

    assert utils.get_stock_prices("2025-08-40", stock_prices_list) == [
        {"stock": "AAPL", "price": 0},
        {"stock": "AMZN", "price": 0},
        {"stock": "GOOGL", "price": 0},
        {"stock": "MSFT", "price": 0},
        {"stock": "TSLA", "price": 0},
    ]
    assert utils.get_stock_prices(date_str, ["test"]) == [
        {"stock": "AAPL", "price": 0},
        {"stock": "AMZN", "price": 0},
        {"stock": "GOOGL", "price": 0},
        {"stock": "MSFT", "price": 0},
        {"stock": "TSLA", "price": 0},
    ]
