from config import TRANSACTION_PATH_EXCEL
from src.reports import spending_by_category, read_excel_df
from src.services import investment_bank
from src.views import main_views


def run_functionality1():
    """Функция для запуска модуля reports"""
    operations_data = read_excel_df(TRANSACTION_PATH_EXCEL)
    result = spending_by_category(operations_data, "Наличные", "20.07.2020")
    print("Результат функциональности 1:", result)


def run_functionality2():
    """Функция для запуска модуля services"""
    transactions = [
        {"Дата операции": "2023-10-01", "Сумма операции": 1712},
        {"Дата операции": "2023-10-05", "Сумма операции": 845},
        {"Дата операции": "2023-10-10", "Сумма операции": 123},
        {"Дата операции": "2023-10-15", "Сумма операции": 459},
    ]
    result = investment_bank("2023-10-15", transactions, limit=100)
    print("Результат функциональности 2:", result)


def run_functionality3():
    """Функция для запуска модуля views"""
    result = main_views("2020-10-10 15:30:00")
    print("Результат функциональности 3:", result)


if __name__ == "__main__":
    print("Запуск всех функциональностей проекта:")
    run_functionality1()
    run_functionality2()
    run_functionality3()
