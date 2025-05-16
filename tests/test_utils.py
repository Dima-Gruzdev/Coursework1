from unittest.mock import patch
from datetime import datetime

import pytest

from src.utils import exchange_rate, get_greeting, calcul_total_expen, card_info, top_wastes_trans, \
    reading_transactions_excel


def test_get_greeting_morning():
    date_time = "2023-10-01 08:00:00"
    assert get_greeting(date_time) == "Доброе утро!"


def test_get_greeting_afternoon():
    date_time = "2023-10-01 14:00:00"
    assert get_greeting(date_time) == "Добрый день!"


def test_get_greeting_evening():
    date_time = "2023-10-01 19:00:00"
    assert get_greeting(date_time) == "Добрый вечер!"


def test_get_greeting_night():
    date_time = "2023-10-01 23:00:00"
    assert get_greeting(date_time) == "Доброй ночи!"


def test_get_greeting_invalid_format():
    date_time = "2023/10/01 08:00:00"
    assert get_greeting(date_time) is None


def test_get_greeting_none():
    result = get_greeting(None)
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        assert result == "Доброе утро!"
    elif 12 <= current_hour < 18:
        assert result == "Добрый день!"
    elif 18 <= current_hour < 23:
        assert result == "Добрый вечер!"
    else:
        assert result == "Доброй ночи!"


def test_calcul_total_expen_basic():
    transactions = [
        {"Сумма операции": -50},
        {"Сумма операции": -100},
        {"Сумма операции": 200},
    ]
    assert calcul_total_expen(transactions) == 150.0


def test_calcul_total_expen_no_expenses():
    transactions = [
        {"Сумма операции": 100},
        {"Сумма операции": 200},
    ]
    assert calcul_total_expen(transactions) == 0.0


def test_calcul_total_expen_empty_list():
    transactions = []
    assert calcul_total_expen(transactions) == 0.0


def test_calcul_total_expen_mixed_transactions():
    transactions = [
        {"Сумма операции": -20},
        {"Сумма операции": 50},
        {"Сумма операции": -30},
        {"Сумма операции": -10},
    ]
    assert calcul_total_expen(transactions) == 60.0


def test_calcul_total_expen_single_negative_transaction():
    transactions = [
        {"Сумма операции": -75},
    ]
    assert calcul_total_expen(transactions) == 75.0


def test_calcul_total_expen_single_positive_transaction():
    transactions = [
        {"Сумма операции": 100},
    ]
    assert calcul_total_expen(transactions) == 0.0


def test_calcul_total_expen_negative_and_zero_transactions():
    transactions = [
        {"Сумма операции": -50},
        {"Сумма операции": 0},
        {"Сумма операции": -100},
    ]
    assert calcul_total_expen(transactions) == 150.0


def test_card_info_basic():
    card_total = [
        {"Номер карты": "*1234", "Сумма операции": -50, "Бонусы (включая кэшбэк)": 5.0},
        {"Номер карты": "*1234", "Сумма операции": -100, "Бонусы (включая кэшбэк)": 10.0},
        {"Номер карты": "*5678", "Сумма операции": -200, "Бонусы (включая кэшбэк)": 20.0},
    ]
    expected_output = [
        {"last_digits": "1234", "total_spent": 150.0, "cashback": 15.0},
        {"last_digits": "5678", "total_spent": 200.0, "cashback": 20.0},
    ]
    assert card_info(card_total) == expected_output


def test_card_info_single_card():
    card_total = [
        {"Номер карты": "*4321", "Сумма операции": -75, "Бонусы (включая кэшбэк)": 7.5},
    ]
    expected_output = [
        {"last_digits": "4321", "total_spent": 75.0, "cashback": 7.5},
    ]
    assert card_info(card_total) == expected_output


def test_card_info_multiple_cards():
    card_total = [
        {"Номер карты": "*1111", "Сумма операции": -50, "Бонусы (включая кэшбэк)": 5.0},
        {"Номер карты": "*2222", "Сумма операции": -100, "Бонусы (включая кэшбэк)": 10.0},
        {"Номер карты": "*1111", "Сумма операции": -150, "Бонусы (включая кэшбэк)": 15.0},
    ]
    expected_output = [
        {"last_digits": "1111", "total_spent": 200.0, "cashback": 20.0},
        {"last_digits": "2222", "total_spent": 100.0, "cashback": 10.0},
    ]
    assert card_info(card_total) == expected_output


def test_card_info_no_cashback():
    card_total = [
        {"Номер карты": "*9999", "Сумма операции": -30, "Бонусы (включая кэшбэк)": 0.0},
        {"Номер карты": "*9999", "Сумма операции": -70, "Бонусы (включая кэшбэк)": 0.0},
    ]
    expected_output = [
        {"last_digits": "9999", "total_spent": 100.0, "cashback": 0.0},
    ]
    assert card_info(card_total) == expected_output


def test_top_wastes_trans_basic():
    transactions = [
        {"Номер карты": "*1234", "Сумма операции": -50},
        {"Номер карты": "*5678", "Сумма операции": -100},
        {"Номер карты": "*1111", "Сумма операции": -200},
        {"Номер карты": "*2222", "Сумма операции": -150},
        {"Номер карты": "*3333", "Сумма операции": -75},
        {"Номер карты": "*4444", "Сумма операции": -25},
    ]
    expected_output = [
        {"Номер карты": "*4444", "Сумма операции": -25},
        {"Номер карты": "*1234", "Сумма операции": -50},
        {"Номер карты": "*3333", "Сумма операции": -75},
        {"Номер карты": "*5678", "Сумма операции": -100},
        {"Номер карты": "*2222", "Сумма операции": -150},
    ]
    assert top_wastes_trans(transactions) == expected_output


def test_top_wastes_trans_less_than_five():
    transactions = [
        {"Номер карты": "*1234", "Сумма операции": -50},
        {"Номер карты": "*5678", "Сумма операции": -100},
    ]
    expected_output = [
        {"Номер карты": "*1234", "Сумма операции": -50},
        {"Номер карты": "*5678", "Сумма операции": -100},
    ]
    assert top_wastes_trans(transactions) == expected_output


def test_top_wastes_trans_empty():
    transactions = []
    expected_output = []
    assert top_wastes_trans(transactions) == expected_output


def test_top_wastes_trans_identical_values():
    transactions = [
        {"Номер карты": "*1111", "Сумма операции": -100},
        {"Номер карты": "*2222", "Сумма операции": -100},
        {"Номер карты": "*3333", "Сумма операции": -100},
        {"Номер карты": "*4444", "Сумма операции": -100},
        {"Номер карты": "*5555", "Сумма операции": -100},
        {"Номер карты": "*6666", "Сумма операции": -100},
    ]
    expected_output = [
        {"Номер карты": "*1111", "Сумма операции": -100},
        {"Номер карты": "*2222", "Сумма операции": -100},
        {"Номер карты": "*3333", "Сумма операции": -100},
        {"Номер карты": "*4444", "Сумма операции": -100},
        {"Номер карты": "*5555", "Сумма операции": -100},
    ]
    assert top_wastes_trans(transactions) == expected_output


def test_reading_transactions_excel_success(create_test_excel_file):
    result = reading_transactions_excel(create_test_excel_file)
    expected_result = [
        {'TransactionID': 1, 'Amount': 100.0, 'Date': '2023-01-01'},
        {'TransactionID': 2, 'Amount': 200.0, 'Date': '2023-01-02'}
    ]
    assert result == expected_result


@patch('pandas.read_excel')
def test_reading_transactions_excel_file_not_found(mock_read_excel):
    # Тестируем ситуацию, когда файл не найден
    mock_read_excel.side_effect = FileNotFoundError("File not found.")
    result = reading_transactions_excel("non_existent_file.xlsx")
    assert result == []


@patch('pandas.read_excel')
def test_reading_transactions_excel_value_error(mock_read_excel):
    mock_read_excel.side_effect = ValueError("Invalid file format.")
    result = reading_transactions_excel("invalid_file.xlsx")
    assert result == []


@patch("requests.get")
def test_correct_exchange(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 100}}
    assert exchange_rate("USD") == 100
    mock_get.assert_called_once()


@patch("requests.get")
def test_error_exchange(mock_get):
    mock_get.return_value.json.return_value = {"test": {"test": 100}}
    with pytest.raises(KeyError):
        exchange_rate("USD")
    mock_get.assert_called_once()
