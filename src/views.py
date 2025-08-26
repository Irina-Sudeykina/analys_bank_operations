import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from src import utils

logging.basicConfig(filemode="w")

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/views.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

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
    logger.info("Формируем приветствие")
    my_greeting = utils.get_greeting(date_time_str)

    logger.info(f"Читаем данные из файла {transactions_file}, формируем DataFrame")
    df = utils.load_transactions_xlsx_file(transactions_file)

    logger.info(f"Преобразуем дату {date_time_str} в объект Timestamp")
    target_date = pd.to_datetime(date_time_str)

    logger.info("Определяем начало месяца для заданной даты")
    first_day_of_target_month = target_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    logger.info("Приводим колонку 'Дата операции' к формату Timestamp")
    df["DateTimeColumn"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    logger.info("Фильтруем записи между первым числом месяца и целевой датой")
    df = df[(df["DateTimeColumn"] >= first_day_of_target_month) & (df["DateTimeColumn"] <= target_date)]

    logger.info("Получаем данные по картам")
    cards_info = utils.get_cards_info(df)

    logger.info("Получаем данные по последним 5 транзакциям")
    top_transactions = utils.get_top_transactions(df)

    logger.info("Получаем список валют")
    currencies_list = utils.load_currencies_json_file(settings_file)
    date_str = date_time_str[:10]
    logger.info(f"Получаем курсы валют на дату {date_str}")
    exchange_rate = utils.get_exchange_rate(date_str, currencies_list, "RUB")

    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Текущая дата: {today}")
    if date_str == today:
        # Преобразуем строку в объект datetime
        dt = datetime.strptime(date_str, "%Y-%m-%d")

        # Вычитаем один день
        new_dt = dt - timedelta(days=1)

        # Преобразуем обратно в строку нужного формата
        date_str = new_dt.strftime("%Y-%m-%d")
    logger.info("Получаем список акций")
    stock_prices_list = utils.load_prices_json_file(settings_file)
    logger.info(f"Получаем цены акций на дату {date_str}")
    stock_prices = utils.get_stock_prices(date_str, stock_prices_list)

    logger.info("Формируем json-ответ:")
    home_json = {
        "greeting": f"{my_greeting}",
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": exchange_rate,
        "stock_prices": stock_prices,
    }
    logger.info(f"{json.dumps(home_json, ensure_ascii=False, indent=4)}")
    return json.dumps(home_json, ensure_ascii=False, indent=4)
