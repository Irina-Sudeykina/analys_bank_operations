import pandas as pd

from src import services


def test_get_increased_cashback(transactions_df: pd.DataFrame) -> None:
    """
    Проверка работы функции get_increased_cashback для анализа выгодности категорий повышенного кешбэка
    принимает данные для анализа, год и месяц
    и возвращает JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года
    :param transactions_df: Фикстура DataFrame с финансовыми операциями
    :return: JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года
    """

    assert services.get_increased_cashback(transactions_df, 2021, 12) == {"Ж/д билеты": 70.0, "Каршеринг": 10.0}
