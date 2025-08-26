import os
from pathlib import Path

from src import views

# Задаём корневой путь проекта.
project_root = Path(__file__).resolve().parents[0]

transactions_file = os.path.join(project_root, r"data\operations.xlsx")  # Используем raw-string
settings_file = os.path.join(project_root, r"data\user_settings.json")  # Используем raw-string


def main() -> None:
    datetime_str = "2021-08-20 14:05:37"
    result = views.get_home_json(datetime_str)
    print(result)


if __name__ == "__main__":
    main()
