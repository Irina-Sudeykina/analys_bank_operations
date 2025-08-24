from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
from pandas.testing import assert_frame_equal

from src import utils


def test_get_greeting() -> None:
    """
    Приверка функции get_greeting, которая
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
    Приверка функции get_cards_info, которая
    принимает DataFrame с банковскими операциями
    и возвращает список с информацией по каждой карте
    :param transactions_df: Фикстура DataFrame с финансовыми операциями
    :param cards_info_on_transactions_df: Фикстура с данными по картам
    :return: список с информацией по каждой карте
    """
    assert utils.get_cards_info(transactions_df) == cards_info_on_transactions_df
