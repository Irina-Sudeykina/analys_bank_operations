# Проект "Приложение для анализа банковских операций"

## Описание:
 Проект "Приложение для анализа банковских операций" - это проект на Python, 
 содержащий функции для работы с банковскими операциями
 
## Установка:
 1. Клонируйте репозиторий:
 ```
 git clone https://github.com/Irina-Sudeykina/analys_bank_operations.git
 
 ```

 1. Установите зависимости:
 ```
 pip install -r requirements.txt
 ```

## Использование:
 
 ### Функция **get_home_json**(date_time_str: str) -> str
  Главная функция, принимающет на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
  и возвращающет JSON-ответ со следующими данными:
    Приветствие
    Информация по каждой карте
    Топ-5 транзакций по сумме платежа
    Курс валют
    Стоимость акций из S&P500

 #### Пример использования: 
```
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from src import utils

project_root = Path(__file__).resolve().parent.parent
transactions_file = os.path.join(project_root, r"data\operations.xlsx")  # Используем raw-string
settings_file = os.path.join(project_root, r"data\user_settings.json")
 
datetime_str = "2021-08-20 14:05:37"
print(get_home_json(datetime_str))

 ```
 #### Пример работы:
 ```
{
    "greeting": "Добрый день",
    "cards": [
        {
            "last_digits": "4556",
            "total_spent": 3361.7,
            "cashback": 154.0
        },
        {
            "last_digits": "7197",
            "total_spent": 6773.49,
            "cashback": 0.0
        }
    ],
    "top_transactions": [
        {
            "date": "20.08.2021",
            "amount": -226.7,
            "category": "Супермаркеты",
            "description": "Магнит"
        },
        {
            "date": "19.08.2021",
            "amount": -40.0,
            "category": "Фастфуд",
            "description": "Rumyanyj Khleb"
        },
        {
            "date": "18.08.2021",
            "amount": -115.98,
            "category": "Супермаркеты",
            "description": "Магнит"
        },
        {
            "date": "18.08.2021",
            "amount": -7632.84,
            "category": "ЖКХ",
            "description": "ЖКУ Квартира"
        },
        {
            "date": "18.08.2021",
            "amount": -112.26,
            "category": "Другое",
            "description": "Kvartplata.Info"
        }
    ],
    "currency_rates": [
        {
            "currency": "USD",
            "rate": 80.59
        },
        {
            "currency": "EUR",
            "rate": 94.41
        }
    ],
    "stock_prices": [
        {
            "stock": "AAPL",
            "price": 143.62
        },
        {
            "stock": "AMZN",
            "price": 159.39
        },
        {
            "stock": "GOOGL",
            "price": 134.87
        },
        {
            "stock": "MSFT",
            "price": 287.16
        },
        {
            "stock": "TSLA",
            "price": 224.49
        }
    ]
}
 ```

 
 ### Функция **get_greeting**(datetime_str: str) -> str
  Функция принимает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
  и возвращает строку с приветствием

 #### Пример использования: 
 ```
date_time_str = "2021-08-20 14:05:37"
my_greeting = utils.get_greeting(date_time_str)
print(my_greeting)
 ```
 #### Пример работы:
 ```
"Добрый день"
 ```
 
 
 ### Функция **load_transactions_xlsx_file**(transactions_file: str) -> pd.DataFrame
  Функция принимает путь к XLSX-файлу с банковскими операциями
  и возвращает DataFrame с банковскими операциями

 #### Пример использования: 
 ```
df = utils.load_transactions_xlsx_file(operations.xlsx)
print(df.head())
 ```
 #### Пример работы:
 ```
         Дата операции Дата платежа  ... Округление на инвесткопилку Сумма операции с округлением
0  29.12.2021 22:32:24   30.12.2021  ...                           0                      1411.40
1  25.12.2021 22:21:49   26.12.2021  ...                           0                       218.07

[2 rows x 15 columns]
 ```
  
 
 ### Функция **get_cards_info**(transactions: pd.DataFrame) -> list[dict]
  Функция принимает DataFrame с банковскими операциями
  и возвращает список с информацией по каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей).

 #### Пример использования: 
 ```
df = utils.load_transactions_xlsx_file(operations.xlsx)
    
# Преобразуем дату в объект Timestamp
target_date = pd.to_datetime(date_time_str)

# Начало месяца для заданной даты
first_day_of_target_month = target_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# Приводим колонку дат к формату Timestamp
df['DateTimeColumn'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

# Фильтруем записи между первым числом месяца и целевой датой
df = df[
    (df['DateTimeColumn'] >= first_day_of_target_month) &
    (df['DateTimeColumn'] <= target_date)
]

cards_info = utils.get_cards_info(df)
 ```
 #### Пример работы:
 ```
[
    {
        "last_digits": "4556",
        "total_spent": 3361.7,
        "cashback": 154.0
    },
    {
        "last_digits": "7197",
        "total_spent": 6773.49,
        "cashback": 0.0
    }
]
 ```
  
 
 ### Функция **get_top_transactions**(transactions: pd.DataFrame) -> list[dict]
  Функция принимает DataFrame с банковскими операциями
  и возвращает список с 5ю последними транзакциями

 #### Пример использования: 
 ```
df = utils.load_transactions_xlsx_file(operations.xlsx)
top_transactions = utils.get_top_transactions(df)
print(top_transactions)
 ```
 #### Пример работы:
 ```
[
    {
        "date": "20.08.2021",
        "amount": -226.7,
        "category": "Супермаркеты",
        "description": "Магнит"
    },
    {
        "date": "19.08.2021",
        "amount": -40.0,
        "category": "Фастфуд",
        "description": "Rumyanyj Khleb"
    },
    {
        "date": "18.08.2021",
        "amount": -115.98,
        "category": "Супермаркеты",
        "description": "Магнит"
    },
    {
        "date": "18.08.2021",
        "amount": -7632.84,
        "category": "ЖКХ",
        "description": "ЖКУ Квартира"
    },
    {
        "date": "18.08.2021",
        "amount": -112.26,
        "category": "Другое",
        "description": "Kvartplata.Info"
    }
]
 ```
  
 
 ### Функция **load_currencies_json_file**(settings_file: str) -> list[str]
  Функция принимает путь к json-файлу с настройками пользователя
  и возвращает список валют

 #### Пример использования: 
 ```
currencies_list = utils.load_currencies_json_file(user_settings.json)
print(currencies_list)
 ```
 #### Пример работы:
 ```
["USD", "EUR"]
 ```


 ### Функция **get_exchange_rate**(date_str: str, currency_from: list[str], currency_to: str) -> list[dict]
  Функция принимает дату в формате 2025-08-20, список кодов валюты и код валюты обмена
  и возвращает список курсов обмена на дату

 #### Пример использования: 
 ```
exchange_rate = utils.get_exchange_rate("2025-08-20", ["USD", "EUR"], "RUB")
print(exchange_rate)
 ```
 #### Пример работы:
 ```
[
    {
        "currency": "USD",
        "rate": 80.59
    },
    {
        "currency": "EUR",
        "rate": 94.41
    }
]
 ```


 ### Функция **load_prices_json_file**(settings_file: str) -> list[str]
  Функция принимает путь к json-файлу с настройками пользователя
  и возвращает список акций

 #### Пример использования: 
 ```
stock_prices_list = utils.load_prices_json_file(user_settings.json)
print(stock_prices_list)
 ```
 #### Пример работы:
 ```
["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
 ```


 ### Функция **get_stock_prices**(date_str: str, stock_prices_list: list[str]) -> list[dict]
  Функция принимает дату в формате 2025-08-20 список тикеров акций
  и возвращает список словарей со стоимостью акций

 #### Пример использования: 
 ```
stock_prices = utils.get_stock_prices(2025-08-20, ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
print(stock_prices)
 ```
 #### Пример работы:
 ```
[
    {
        "stock": "AAPL",
        "price": 143.62
    },
    {
        "stock": "AMZN",
        "price": 159.39
    },
    {
        "stock": "GOOGL",
        "price": 134.87
    },
    {
        "stock": "MSFT",
        "price": 287.16
    },
    {
        "stock": "TSLA",
        "price": 224.49
    }
]
 ```


## Декораторы:
 
 ### Декоратор **log**(filename: str | None = None) -> Any
  Декоратор, который логирует работу функции и ее результат в файл

 #### Пример использования: 
```
import decorators

file_of_names = "my_log.txt"

@decorators.log(file_of_names)
def add_numbers(a: int | float, b: int | float) -> int | float:
    """
    Функция для тестирования декоратора
    Просто складывает два числа
    :param a: первое число
    :param b: второе число
    :return: сумма чисел a и b
    """
    return a + b
 
result = add_numbers(3, 5)
 ```
 
 #### Пример работы:
 ```

2025-08-03 15:53:58:
Function add_numbers called with args: (3, 5) and kwargs: {}.
Execution time: 0:00:00.0010. Result: 8

 ```

 ## Тестирование:
Проект покрыт тестами фреймворка pytest. Для их запуска выполните команду:
```
pytest
```
Для выгрузки отчета о покрытии проекта тестами выполните команду:
```
pytest --cov=src --cov-report=html
```

 ## Логирование:
Работа проекта логируется.
Логи соханяются в папку logs и презаписываются при каждом запуске приложения.

 ## Документация:

 ## Лицензия:
 Проект распространяется под [лицензией MIT](LICENSE).
 