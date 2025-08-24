from src import views


def test_get_home_json(home_json: str) -> None:
    """
    Проверка функции get_home_json, которая
    принимающет на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающет JSON-ответ с данными
    :param greeting: Фикстура приветствия
    :param home_json: Фикстура содержимого JSON-ответа с данными
    :return: JSON-ответ с соответствующими данными
    """

    datetime_str = "2025-08-20 09:05:37"

    # Выполняем тестирование
    result = views.get_home_json(datetime_str)

    assert result == home_json
