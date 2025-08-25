import json
import os
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

# Получить текущую дату и время
now = datetime.now()

# Отформатировать в строку YYYY-MM-DD HH:MM:SS
formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")


def get_greeting(datetime_str: str) -> str:
    """
    Функция принимает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращает строку с приветствием
    :param datetime_str: строка датой и временем в формате YYYY-MM-DD HH:MM:SS
    :return: строка с приветствием
    """
    try:
        my_hour = int(datetime_str[11:13])

        if (my_hour >= 0) and (my_hour <= 4):
            my_greeting = "Доброй ночи"
        elif (my_hour >= 5) and (my_hour <= 11):
            my_greeting = "Доброе утро"
        elif (my_hour >= 12) and (my_hour <= 16):
            my_greeting = "Добрый день"
        else:
            my_greeting = "Добрый вечер"

    except Exception:
        print("Что-то пошло не так при обработке даты и времени")
        my_greeting = ""

    return my_greeting


def load_transactions_xlsx_file(transactions_file: str) -> pd.DataFrame:
    """
    Функция принимает путь к XLSX-файлу с банковскими операциями
    и возвращает DataFrame с банковскими операциями
    :param transactions_file: страка содержащая путь к XLSX-файллу
    :return: DataFrame с банковскими операциями
    """
    try:
        df = pd.read_excel(transactions_file)
    except Exception:
        data: dict[str, list[Any]] = {
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
        df = pd.DataFrame(data)
    return df


def get_cards_info(transactions: pd.DataFrame) -> list[dict]:
    """
    Функция принимает DataFrame с банковскими операциями
    и возвращает список с информацией по каждой карте:
        последние 4 цифры карты;
        общая сумма расходов;
        кешбэк (1 рубль на каждые 100 рублей).
    :param transactions:
    :return:
    """
    transactions = transactions.loc[(transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)]
    cards_df = transactions.groupby("Номер карты")
    cards_df_res = cards_df[["Сумма операции", "Кэшбэк"]].sum().abs()
    result_list = []
    for card_number, group_data in cards_df_res.iterrows():
        last_four_digits = str(card_number)[-4:]
        total_spent = group_data["Сумма операции"]
        cashback = group_data["Кэшбэк"]

        result_list.append({"last_digits": last_four_digits, "total_spent": total_spent, "cashback": cashback})
    return result_list


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """
    Функция принимает DataFrame с банковскими операциями
    и возвращает список с 5ю последними транзакциями
    :param transactions: DataFrame с банковскими операциями
    :return: список с 5ю последними транзакциями
    """
    transactions = transactions.sort_values(by="Дата операции", ascending=False)
    transactions = transactions.head(5)
    result_list = []
    for card_number, group_data in transactions.iterrows():
        result_list.append(
            {
                "date": group_data["Дата платежа"],
                "amount": group_data["Сумма операции"],
                "category": group_data["Категория"],
                "description": group_data["Описание"],
            }
        )

    return result_list


def load_currencies_json_file(settings_file: str) -> list[str]:
    """
    Функция принимает путь к json-файлу с настройками пользователя
    и возвращает список валют
    :param settings_file: страка содержащая путь к json-файлу
    :return: список валют
    """
    try:
        with open(settings_file, mode="r", encoding="utf-8") as currencies_file:
            try:
                user_settings = json.load(currencies_file)
                currencies_result = []
                for i in user_settings["user_currencies"]:
                    if len(i) != 0:
                        currencies_result.append(i)
            except json.JSONDecodeError:
                return ["USD", "EUR"]
    except FileNotFoundError:
        return ["USD", "EUR"]

    return currencies_result


def get_exchange_rate(date_str: str, currency_from: list[str], currency_to: str) -> list[dict]:
    """
    Функция принимает дату в формате 2025-08-20, список кодов валюты и код валюты обмена
    и возвращает список курсов обмена на дату
    :param date_str: дата в формате 2025-08-20
    :param currency_from: список кодов валюты - например USD, EUR
    :param currency_to: код валюты обмена - например RUB
    :return: список курсов обмена на дату
    """
    load_dotenv()
    API_KEY = str(os.getenv("API_KEY"))
    BASE_URL = "https://api.freecurrencyapi.com/v1/latest"  # Для текущих курсов

    result_list = []

    for i in currency_from:
        try:
            response = requests.get(BASE_URL, params={"apikey": API_KEY, "base_currency": i, "date": date_str})

            if response.status_code == 200:
                data = response.json()
                result_rate = round(data["data"].get(currency_to, 0.0), 2)
            else:
                result_rate = 0.0
        except Exception:
            result_rate = 0.0

        result_list.append({"currency": i, "rate": result_rate})

    return result_list


def load_prices_json_file(settings_file: str) -> list[str]:
    """
    Функция принимает путь к json-файлу с настройками пользователя
    и возвращает список акций
    :param settings_file: страка содержащая путь к json-файлу
    :return: список акций
    """
    try:
        with open(settings_file, mode="r", encoding="utf-8") as currencies_file:
            try:
                user_settings = json.load(currencies_file)
                currencies_result = []
                for i in user_settings["user_stocks"]:
                    if len(i) != 0:
                        currencies_result.append(i)
            except json.JSONDecodeError:
                return ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    except FileNotFoundError:
        return ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

    return currencies_result


def get_stock_prices(date_str: str, stock_prices_list: list[str]) -> list[dict]:
    """
    Функция принимает дату в формате 2025-08-20 список тикеров акций
    и возвращает список акций
    :param date_str: страка содержащая дату в формате 2025-08-20
    :param stock_prices_list: список тикеров акций
    :return: список акций
    """
    try:
        # Преобразуем строку в объект datetime
        dt = datetime.strptime(date_str, "%Y-%m-%d")

        # Вычитаем один день
        new_dt = dt - timedelta(days=1)

        # Преобразуем обратно в строку нужного формата
        date_str2 = new_dt.strftime("%Y-%m-%d")

        result_list = []

        for i in stock_prices_list:
            # Загружаем тикер например AAPL
            aapl = yf.Ticker(i)

            # Запрашиваем исторические данные за одну точку — нужную нам дату
            data = aapl.history(start=date_str2, end=date_str)  # Важно указывать следующий день окончания периода!

            # Извлекаем цену закрытия на нашу дату
            close_price = data["Close"].values[0]
            close_price = round(close_price, 2)

            result_list.append({"stock": i, "price": close_price})
    except Exception:
        result_list = [
            {"stock": "AAPL", "price": 0},
            {"stock": "AMZN", "price": 0},
            {"stock": "GOOGL", "price": 0},
            {"stock": "MSFT", "price": 0},
            {"stock": "TSLA", "price": 0},
        ]

    return result_list
