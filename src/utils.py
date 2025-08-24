from datetime import datetime

import pandas as pd

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
    my_hour = int(datetime_str[11:13])

    if (my_hour >= 0) and (my_hour <= 4):
        my_greeting = "Доброй ночи"
    elif (my_hour >= 5) and (my_hour <= 11):
        my_greeting = "Доброе утро"
    elif (my_hour >= 12) and (my_hour <= 16):
        my_greeting = "Добрый день"
    else:
        my_greeting = "Добрый вечер"

    return my_greeting


def load_transactions_xlsx_file(transactions_file: str) -> pd.DataFrame:
    """
    Функция принимает путь к XLSX-файлу с банковскими операциями
    и возвращает DataFrame с банковскими операциями
    :param transactions_file: страка содержащая путь к XLSX-файллу
    :return: DataFrame с банковскими операциями
    """
    df = pd.read_excel(transactions_file)
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
