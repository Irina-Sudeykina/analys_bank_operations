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
    ],
    "top_transactions": [
        {
            "date": "31.12.2021",
            "amount": -160.89,
            "category": "Супермаркеты",
            "description": "Колхоз"
        },
        {
            "date": "31.12.2021",
            "amount": -64.0,
            "category": "Супермаркеты",
            "description": "Колхоз"
        },
        {
            "date": "31.12.2021",
            "amount": -118.12,
            "category": "Супермаркеты",
            "description": "Магнит"
        },
        {
            "date": "31.12.2021",
            "amount": -78.05,
            "category": "Супермаркеты",
            "description": "Колхоз"
        },
        {
            "date": "31.12.2021",
            "amount": -564.0,
            "category": "Различные товары",
            "description": "Ozon.ru"
        }
    ],
    "currency_rates": [
        {
            "currency": "USD",
            "rate": 80.66
        },
        {
            "currency": "EUR",
            "rate": 94.56
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


@pytest.fixture
def top_transactions_on_transactions_df() -> list[dict]:
    """
    Фикстура c последними транзакциями
    :return: список с последними транзакциями
    """
    return [
        {"date": "30.12.2021", "amount": -1411.4, "category": "Ж/д билеты", "description": "РЖД"},
        {"date": "26.12.2021", "amount": -218.07, "category": "Каршеринг", "description": "Ситидрайв"},
    ]


@pytest.fixture
def freecurrencyapi_20250820() -> dict:
    """
    Фикстура c курсами валют на 20.08.2025
    :return: список с последними транзакциями
    """
    return {
        "data": {
            "2025-08-20": {
                "AUD": 1.553620224,
                "BGN": 1.6749002447,
                "BRL": 5.4674905501,
                "CAD": 1.3869802438,
                "CHF": 0.8040101411,
                "CNY": 7.1703913399,
                "CZK": 20.9942726633,
                "DKK": 6.4047807772,
                "EUR": 0.8579101047,
                "GBP": 0.7426000981,
                "HKD": 7.8109609956,
                "HRK": 6.2864711723,
                "HUF": 338.0167080333,
                "IDR": 16233.387524701,
                "ILS": 3.4079804603,
                "INR": 86.9087146166,
                "ISK": 122.9315035067,
                "JPY": 147.2917634895,
                "KRW": 1395.1302453007,
                "MXN": 18.7677329679,
                "MYR": 4.2213507917,
                "NOK": 10.2336212546,
                "NZD": 1.7158203379,
                "PHP": 56.9162868308,
                "PLN": 3.6440505868,
                "RON": 4.3373207306,
                "RUB": 80.4473560133,
                "SEK": 9.5835516385,
                "SGD": 1.285100178,
                "THB": 32.5532833223,
                "TRY": 40.8887446728,
                "USD": 1,
                "ZAR": 17.6614829054,
            }
        }
    }


@pytest.fixture
def user_settings_json() -> dict:
    """
    Фикстура c настройками пользователя
    :return: словарь с настройками список валют и список акций
    """
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
