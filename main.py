import os
from pathlib import Path

from src import reports, services, utils, views

# Задаём корневой путь проекта.
project_root = Path(__file__).resolve().parents[0]

transactions_file = os.path.join(project_root, r"data\operations.xlsx")  # Используем raw-string
settings_file = os.path.join(project_root, r"data\user_settings.json")  # Используем raw-string


def main() -> None:
    datetime_str = "2021-08-20 14:05:37"
    result_home = views.get_home_json(datetime_str)
    print(result_home)

    df = utils.load_transactions_xlsx_file(transactions_file)
    result_increased_cashback = services.get_increased_cashback(df, 2021, 8)
    print(result_increased_cashback)

    result_spending_by_category = reports.spending_by_category(df, "Супермаркеты", "2021-08-20")
    print(result_spending_by_category)


if __name__ == "__main__":
    main()
