import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_with_date(transactions_data):
    result = spending_by_category(transactions_data, "Наличные", "20.07.2020")
    assert result == 300


def test_spending_by_category_without_date(transactions_data):
    result = spending_by_category(transactions_data, "Наличные")
    assert result == 0


def test_spending_by_category_no_transactions(transactions_data):
    result = spending_by_category(transactions_data, "Неизвестная категория", "20.07.2020")
    assert result == 0


def test_spending_by_category_empty_dataframe():
    empty_df = pd.DataFrame(columns=["Дата операции", "Категория", "Сумма платежа"])
    result = spending_by_category(empty_df, "Наличные", "20.07.2020")
    assert result == 0


def test_spending_by_category_with_future_date(transactions_data):
    future_date = "01.01.2021"
    result = spending_by_category(transactions_data, "Наличные", future_date)
    assert result == 0
