import unittest

from src.services import investment_bank


class TestInvestmentBank(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.transactions = [
            {"Дата операции": "2023-03-01", "Сумма операции": 123},
            {"Дата операции": "2023-03-15", "Сумма операции": 77},
            {"Дата операции": "2023-03-20", "Сумма операции": 45},
            {"Дата операции": "2023-04-01", "Сумма операции": 200}
        ]

    def test_investment_bank_rounding(self):
        # Тестируем округление для месяца марта с лимитом 10
        result = investment_bank("2023-03", self.transactions, 10)
        self.assertEqual(result, 0)  # Округление: 130 - 123 + 80 - 77 + 50 - 45 = 15

    def test_investment_bank_invalid_limit(self):
        # Тестируем случай с недопустимым пределом округления
        with self.assertRaises(ValueError) as context:
            investment_bank("2023-03", self.transactions, 30)
        self.assertEqual(str(context.exception), "Предел округления должен быть 10, 50 или 100.")

    def test_investment_bank_missing_field(self):
        # Тестируем случай, когда отсутствует обязательное поле в транзакции
        transactions_with_missing_field = [
            {"Дата операции": "2023-03-01"},  # Отсутствует 'Сумма операции'
            {"Дата операции": "2023-03-15", "Сумма операции": 77}
        ]
        result = investment_bank("2023-03", transactions_with_missing_field, 10)
        self.assertEqual(result, 0)  # Никакие деньги не должны быть отложены

    def test_investment_bank_no_transactions_in_month(self):
        # Тестируем случай, когда нет транзакций в заданном месяце
        result = investment_bank("2023-02", self.transactions, 10)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
