import pandas as pd
import pytest


@pytest.fixture
def greeting() -> str:
    """
    Фикстура приветствия
    :return: строка приветствия
    """
    return "Доброе утро"


@pytest.fixture
def cards_info() -> list[dict]:
    """
    Фикстура с данными по картам
    :return: список с данными по картам
    """
    return [
        {"last_digits": "4556", "total_spent": 1006659.05, "cashback": 8959.0},
        {"last_digits": "5091", "total_spent": 17367.5, "cashback": 0.0},
        {"last_digits": "7197", "total_spent": 2380912.73, "cashback": 0.0},
    ]


@pytest.fixture
def home_json() -> str:
    """
    Фикстура содержимого JSON-ответа с данными
    :return: JSON-ответ
    """
    return """{
    "greeting": "Доброе утро",
    "cards": [
        {
            "last_digits": "4556",
            "total_spent": 1006659.05,
            "cashback": 8959.0
        },
        {
            "last_digits": "5091",
            "total_spent": 17367.5,
            "cashback": 0.0
        },
        {
            "last_digits": "7197",
            "total_spent": 2380912.73,
            "cashback": 0.0
        }
    ]
}"""


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    """
    Фикстура DataFrame с финансовыми операциями
    :return: DataFrame
    """
    data = {
        "Дата операции": ["29.12.2021 22:32:24", "25.12.2021 22:21:49"],
        "Дата платежа": ["30.12.2021", "26.12.2021"],
        "Номер карты": ["*4556", "*5091"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-1411.4, -218.07],
        "Валюта операции": ["RUB", "RUB"],
        "Сумма платежа": [-1411.4, -218.07],
        "Валюта платежа": ["RUB", "RUB"],
        "Кэшбэк": [70.0, None],
        "Категория": ["Ж/д билеты", "Каршеринг"],
        "MCC": [4112, 7512],
        "Описание": ["РЖД", "Ситидрайв"],
        "Бонусы (включая кэшбэк)": [70, 10],
        "Округление на инвесткопилку": [0, 0],
        "Сумма операции с округлением": [1411.4, 218.07],
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def cards_info_on_transactions_df() -> list[dict]:
    """
    Фикстура с данными по картам
    :return: список с данными по картам
    """
    return [
        {"last_digits": "4556", "total_spent": 1411.4, "cashback": 70.0},
        {"last_digits": "5091", "total_spent": 218.07, "cashback": 0.0},
    ]
