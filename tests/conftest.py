import pandas as pd
import pytest


@pytest.fixture
def correct_check():
    return [
        {"Дата операции": "2023-10-01", "Сумма операции": 1712},
        {"Дата операции": "2023-10-05", "Сумма операции": 845},
        {"Дата операции": "2023-10-10", "Сумма операции": 123},
        {"Дата операции": "2023-10-15", "Сумма операции": 459},
    ]


@pytest.fixture
def data_test():
    return "2023-10-15"


@pytest.fixture
def invest_empty_key():
    return [
        {"Дата операции": "2023-10-01", "": 1712},
        {"Дата операции": "2023-10-05", "": 845},
        {"Дата операции": "2023-10-10", "": 123},
        {"Дата операции": "2023-10-15", "": 459},
    ]


@pytest.fixture
def transactions_data():
    data = {
        "Дата операции": ["01.05.2020", "15.06.2020", "20.07.2020", "10.08.2020", "15.09.2020"],
        "Категория": ["Наличные", "Наличные", "Кредитка", "Наличные", "Кредитка"],
        "Сумма платежа": [100, 200, 300, 400, 500]
    }
    return pd.DataFrame(data)


@pytest.fixture
def create_test_excel_file(tmp_path):
    data = {
        'TransactionID': [1, 2],
        'Amount': [100.0, 200.0],
        'Date': ['2023-01-01', '2023-01-02']
    }
    df = pd.DataFrame(data)

    test_file = tmp_path / "test_transactions.xlsx"
    df.to_excel(test_file, index=False)

    return str(test_file)
