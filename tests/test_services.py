import pytest

from src.services import investment_bank


def test_correct_invest(correct_check, data_test):
    result = investment_bank(data_test, correct_check, limit=100)
    assert result == 41


def test_error_invest(invest_empty_key, data_test):
    result = investment_bank(invest_empty_key, data_test, limit=100)
    assert result == 0


def test_no_limit(data_test, correct_check):
    with pytest.raises(ValueError):
        investment_bank(data_test, correct_check, 0)
