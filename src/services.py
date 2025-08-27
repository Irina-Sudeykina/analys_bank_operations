import logging

import pandas as pd

logging.basicConfig(filemode="w")

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_increased_cashback(data: pd.DataFrame, year: int, month: int) -> dict:
    """
    Функция для анализа выгодности категорий повышенного кешбэка
    принимает данные для анализа, год и месяц
    и возвращает JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года
    :param data: данные с транзакциями
    :param year: год, за который проводится анализ
    :param month: месяц, за который проводится анализ
    :return: JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года
    """
    # Отфильтровываем данные
    logger.info("Отфильтровываем данные")
    filtered_data = data.loc[
        (data["Статус"] == "OK")
        & (data["Сумма операции"] < 0)
        & (~data["Категория"].isin(["Переводы", "Услуги банка", "Другое"]))
    ]

    # Добавляем дополнительные столбцы
    logger.info("Добавляем дополнительные столбцы")
    filtered_data["год"] = filtered_data["Дата операции"].str.slice(6, 10).astype(int)
    filtered_data["месяц"] = filtered_data["Дата операции"].str.slice(3, 5).astype(int)

    # Оставляем только интересующие нас данные
    logger.info("Оставляем только интересующие нас данные")
    filtered_data = filtered_data.loc[(filtered_data["год"] == year) & (filtered_data["месяц"] == month)]

    # Рассчитываем повышенный кэшбэк
    logger.info("Рассчитываем повышенный кэшбэк")
    filtered_data["Повышенный кэшбэк"] = filtered_data["Сумма операции"].abs() * 0.05 // 1

    # Агрегируем и сортируем по убыванию
    logger.info("Агрегируем и сортируем по убыванию")
    aggregated_data = filtered_data.groupby("Категория").agg({"Повышенный кэшбэк": "sum"}).reset_index()
    sorted_data = aggregated_data.sort_values(by="Повышенный кэшбэк", ascending=False)

    # Готовим результирующий словарь
    logger.info("Готовим результирующий словарь")
    result_dict = dict(zip(sorted_data["Категория"], sorted_data["Повышенный кэшбэк"]))

    logger.info(f"Результат: {result_dict}")

    return result_dict
