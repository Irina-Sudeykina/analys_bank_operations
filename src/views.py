import json
import os
from pathlib import Path

from src import utils

project_root = Path(__file__).resolve().parent.parent
transactions_file = os.path.join(project_root, r"data\operations.xlsx")  # Используем raw-string
settings_file = os.path.join(project_root, r"data\user_settings.json")  # Используем raw-string


def get_home_json(date_time_str: str) -> str:
    """
    Главная функция, принимающет на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающет JSON-ответ со следующими данными:
        Приветствие
        Информация по каждой карте
        Топ-5 транзакций по сумме платежа
        Курс валют
        Стоимость акций из S&P500
    :param date_time_str: строка датой и временем в формате YYYY-MM-DD HH:MM:SS
    :return: JSON-ответ с соответствующими данными
    """
    my_greeting = utils.get_greeting(date_time_str)

    df = utils.load_transactions_xlsx_file(transactions_file)

    cards_info = utils.get_cards_info(df)
    top_transactions = utils.get_top_transactions(df)

    currencies_list = utils.load_currencies_json_file(settings_file)
    date_str = date_time_str[:10]
    exchange_rate = utils.get_exchange_rate(date_str, currencies_list, "RUB")

    home_json = {
        "greeting": f"{my_greeting}",
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": exchange_rate,
    }
    return json.dumps(home_json, ensure_ascii=False, indent=4)


datetime_str = utils.formatted_datetime  # "2025-08-20 14:05:37"
print(get_home_json(datetime_str))
