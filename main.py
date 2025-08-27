import os
from pathlib import Path

from src import reports, services, utils, views

# Задаём корневой путь проекта.
project_root = Path(__file__).resolve().parents[0]

transactions_file = os.path.join(project_root, r"data\operations.xlsx")  # Используем raw-string
settings_file = os.path.join(project_root, r"data\user_settings.json")  # Используем raw-string


def main() -> None:
    print("""Добро пожаловать в приложение для анализа банковских операций""")
    datetime_str = "2021-08-20 14:05:37"
    result_home = views.get_home_json(datetime_str)
    print(result_home)

    df = utils.load_transactions_xlsx_file(transactions_file)
    
    is_increased_cashback = input("Расчитать повышеный кэшбэк? Да/Нет\n").lower()
    if is_increased_cashback == "да":
        year = int(input("Ведите год для расчета:\n"))
        month = int(input("Ведите месяц для расчета:\n"))
        result_increased_cashback = services.get_increased_cashback(df, year, month)
        print(result_increased_cashback)

    is_spending_by_category = input("Показать траты по категории за последние 3 месяца? Да/Нет\n").lower()
    if is_spending_by_category == "да":
        category = input("Ведите интерисующую категорию:\n")
        date_and = input("Ведите дату в формате 2021-08-20:\n")
        result_spending_by_category = reports.spending_by_category(df, category, date_and)
        print(result_spending_by_category)


if __name__ == "__main__":
    main()
