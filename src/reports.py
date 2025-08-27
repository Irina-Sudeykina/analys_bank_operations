import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

logging.basicConfig(filemode="w")

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)
    :param transactions: DataFrame с транзакциями
    :param category: название категории
    :param date: дата в виде строки формата 2021-08-20 14:05:37
    :return: DataFrame траты по заданной категории за последние три месяца
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
        logger.info(f"Используется текущая дата: {date}")

    dt = datetime.strptime(date, "%Y-%m-%d")
    logger.info(f"Объект datetime: {dt}")

    # Рассчитываем дату за 3 месяца назад
    past_date = dt - relativedelta(months=3)
    logger.info(f"Начало периода: {past_date}, конец периода: {dt}")

    # Выделяем группы с разными форматами дат
    index_dmy = transactions["Дата операции"].str.match(r"\d{2}.\d{2}.\d{4}")  # dd.mm.yyyy
    index_ymd = ~index_dmy  # yyyy-mm-dd

    # Парсим каждую группу отдельно
    transactions.loc[index_dmy, "DateTimeColumn"] = pd.to_datetime(
        transactions.loc[index_dmy, "Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )
    transactions.loc[index_ymd, "DateTimeColumn"] = pd.to_datetime(
        transactions.loc[index_ymd, "Дата операции"], format="%Y-%m-%d %H:%M:%S"
    )

    # Продолжаем дальше по обычной схеме
    filtered_transactions = transactions[
        (transactions["DateTimeColumn"] >= past_date) & (transactions["DateTimeColumn"] <= dt)
    ]
    logger.info(f"Записи после фильтрации по дате: {filtered_transactions.shape[0]}")

    # Фильтруем по категории
    final_result = filtered_transactions[filtered_transactions["Категория"].str.lower() == category.lower()]
    logger.info(f"Итоговый результат после фильтрации по категории: {final_result.shape[0]}")

    return final_result
