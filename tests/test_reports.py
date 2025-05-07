import unittest
from datetime import datetime

import pandas as pd

from src.reports import spending_by_category


class TestSpendingByCategory(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        data = {
            "Дата операции": [
                "01-01-2023", "15-01-2023", "10-02-2023",
                "05-03-2023", "20-03-2023", "25-03-2023",
                "01-04-2023"
            ],
            "Категория": [
                "Еда", "Еда", "Транспорт",
                "Еда", "Развлечения", "Транспорт",
                "Еда"
            ],
            "Сумма платежа": [100, 200, 50, 150, 300, 75, 100]
        }
        self.transactions = pd.DataFrame(data)

    def test_spending_in_category(self):
        # Тестируем траты по категории 'Еда'
        result = spending_by_category(self.transactions, 'Еда', '01-04-2023')
        self.assertEqual(result, 550)  # 100 + 200 + 150 + 100 = 450

    def test_no_transactions_in_category(self):
        # Тестируем случай, когда нет транзакций в категории 'Одежда'
        result = spending_by_category(self.transactions, 'Одежда', '01-04-2023')
        self.assertEqual(result, 0)

    def test_spending_with_no_date(self):
        # Тестируем без передачи даты (должна использовать текущую дату)
        today = datetime.now().strftime("%d-%m-%Y")
        result = spending_by_category(self.transactions, 'Еда')
        # Сравниваем с ожидаемым результатом на основе текущей даты
        expected_sum = 450 if today <= '01-04-2023' else 0  # Зависит от текущей даты
        self.assertEqual(result, expected_sum)

    def test_spending_with_various_date_formats(self):
        # Тестируем с разными форматами дат
        result1 = spending_by_category(self.transactions, 'Еда', '15-03-2023')
        self.assertEqual(result1, 450)  # 100 + 200 + 150 = 450

        result2 = spending_by_category(self.transactions, 'Еда', '10-03-2023')
        self.assertEqual(result2, 450)  # 100 + 200 + 150 + 100 = 300
