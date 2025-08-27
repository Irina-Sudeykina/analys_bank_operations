from datetime import datetime

import pandas as pd

from src import reports


def test_spending_by_category(transactions_df: pd.DataFrame, transactions_category: pd.DataFrame) -> None:
    """
    Тестирование функции spending_by_category, которая
    возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    # Запускаем функцию и получаем результат
    result = reports.spending_by_category(transactions_df, "Каршеринг", "2021-12-31")

    # Убираем лишнюю колонку DateTimeColumn
    result.drop(columns=["DateTimeColumn"], errors="ignore", inplace=True)

    # Приводим отсутствующие значения к NA
    result.fillna(value=pd.NA, inplace=True)
    transactions_category.fillna(value=pd.NA, inplace=True)

    # Сбрасываем индексы
    result_reset = result.reset_index(drop=True)
    transactions_category_reset = transactions_category.reset_index(drop=True)

    # Сортируем оба DataFrame
    result_sorted = result_reset.sort_values(by=list(result_reset.columns)).reset_index(drop=True)
    transactions_category_sorted = transactions_category_reset.sort_values(
        by=list(transactions_category_reset.columns)
    ).reset_index(drop=True)

    # Проверка близости значений
    pd.testing.assert_frame_equal(result_sorted, transactions_category_sorted, check_dtype=False, atol=1e-8)


def test_spending_by_category_without_date() -> None:
    """
    Тестирование функции spending_by_category без передачи конкретной даты,
    используя текущую дату.
    """
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Создаем данные, относящиеся к последнему месяцу
    data = {
        "Дата операции": [
            f"{current_year}-{current_month - 1}-29 22:32:24",
            f"{current_year}-{current_month - 1}-25 22:21:49",
        ],
        "Дата платежа": [f"{current_year}-{current_month}-30", f"{current_year}-{current_month}-26"],
        "Номер карты": ["*4556", "*5091"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-1411.4, -218.07],
        "Валюта операции": ["RUB", "RUB"],
        "Сумма платежа": [-1411.4, -218.07],
        "Валюта платежа": ["RUB", "RUB"],
        "Кэшбэк": [70.0, 0.0],
        "Категория": ["Ж/д билеты", "Каршеринг"],
        "MCC": [4112, 7512],
        "Описание": ["РЖД", "Ситидрайв"],
        "Бонусы (включая кэшбэк)": [70, 10],
        "Округление на инвесткопилку": [0, 0],
        "Сумма операции с округлением": [1411.4, 218.07],
    }
    df_all = pd.DataFrame(data)

    # Ожидаемый результат
    expected_data = {
        "Дата операции": [f"{current_year}-{current_month - 1}-25 22:21:49"],
        "Дата платежа": [f"{current_year}-{current_month}-26"],
        "Номер карты": ["*5091"],
        "Статус": ["OK"],
        "Сумма операции": [-218.07],
        "Валюта операции": ["RUB"],
        "Сумма платежа": [-218.07],
        "Валюта платежа": ["RUB"],
        "Кэшбэк": [0.0],
        "Категория": ["Каршеринг"],
        "MCC": [7512],
        "Описание": ["Ситидрайв"],
        "Бонусы (включая кэшбэк)": [10],
        "Округление на инвесткопилку": [0],
        "Сумма операции с округлением": [218.07],
    }
    df_expected = pd.DataFrame(expected_data)

    # Запускаем функцию без даты
    result = reports.spending_by_category(df_all, "Каршеринг")

    # Чистка результатов
    result.drop(columns=["DateTimeColumn"], errors="ignore", inplace=True)
    result.fillna(value=pd.NA, inplace=True)
    df_expected.fillna(value=pd.NA, inplace=True)

    # Проверка размеров
    assert len(result) == len(df_expected), f"Ошибочный размер результата: {len(result)} vs {len(df_expected)}"

    # Установка одинакового порядка столбцов
    result = result[list(df_expected.columns)]

    # Проверка
    result_sorted = result.sort_values(by=list(result.columns)).reset_index(drop=True)
    df_expected_sorted = df_expected.sort_values(by=list(df_expected.columns)).reset_index(drop=True)

    # Основное утверждение
    pd.testing.assert_frame_equal(result_sorted, df_expected_sorted, check_dtype=False, atol=1e-8)
