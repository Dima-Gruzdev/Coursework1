import unittest
from datetime import datetime

from src.views import get_greet, calcul_total_expen, card_info, top_transactions_5


class TestGetGreet(unittest.TestCase):

    def test_good_morning(self):
        # Тестируем утреннее время
        date_time = "2023-03-01 07:30:00"
        result = get_greet(date_time)
        self.assertEqual(result, "Доброе утро!")

    def test_good_day(self):
        # Тестируем дневное время
        date_time = "2023-03-01 14:00:00"
        result = get_greet(date_time)
        self.assertEqual(result, "Добрый день!")

    def test_good_evening(self):
        # Тестируем вечернее время
        date_time = "2023-03-01 19:00:00"
        result = get_greet(date_time)
        self.assertEqual(result, "Добрый вечер!")

    def test_good_night(self):
        # Тестируем ночное время
        date_time = "2023-03-01 02:00:00"
        result = get_greet(date_time)
        self.assertEqual(result, "Доброй ночи!")


    def test_no_argument(self):
        # Тестируем случай, когда аргумент не передан (должно использовать текущее время)
        result = get_greet(None)
        current_hour = datetime.now().hour

        if 5 <= current_hour < 12:
            self.assertEqual(result, "Доброе утро!")
        elif 12 <= current_hour < 18:
            self.assertEqual(result, "Добрый день!")
        elif 18 <= current_hour < 23:
            self.assertEqual(result, "Добрый вечер!")
        else:
            self.assertEqual(result, "Доброй ночи!")


class TestCalculTotalExpen(unittest.TestCase):

    def test_no_expenses(self):
        transactions = [{"Сумма операции": 100}, {"Сумма операции": 200}]
        result = calcul_total_expen(transactions)
        self.assertEqual(result, 0.0)

    def test_only_expenses(self):
        transactions = [{"Сумма операции": -50}, {"Сумма операции": -100}]
        result = calcul_total_expen(transactions)
        self.assertEqual(result, 150.0)

    def test_mixed_transactions(self):
        transactions = [{"Сумма операции": -50}, {"Сумма операции": 100}, {"Сумма операции": -200}]
        result = calcul_total_expen(transactions)
        self.assertEqual(result, 250.0)


class TestCardInfo(unittest.TestCase):

    def test_empty_operations(self):
        """Тест на отсутствие операций"""
        result = card_info([])
        self.assertEqual(result, [])

    def test_no_expenses(self):
        """Тест на операции без расходов"""
        operations = [
            {"Номер карты": "*1234", "Сумма операции": 100, "Бонусы (включая кэшбэк)": 10.0},
            {"Номер карты": "*1234", "Сумма операции": 200, "Бонусы (включая кэшбэк)": 20.0}
        ]
        result = card_info(operations)
        self.assertEqual(result, [{"last_digits": "1234", "total_spent": 0.0, "cashback": 30.0}])

    def test_expenses_and_cashback(self):
        """Тест на операции с расходами и кэшбэком"""
        operations = [
            {"Номер карты": "*1234", "Сумма операции": -100, "Бонусы (включая кэшбэк)": 10.0},
            {"Номер карты": "*1234", "Сумма операции": -200, "Бонусы (включая кэшбэк)": 20.0}
        ]
        result = card_info(operations)
        self.assertEqual(result, [{"last_digits": "1234", "total_spent": 300.0, "cashback": 30.0}])

    def test_multiple_cards(self):
        """Тест на несколько карт"""
        operations = [
            {"Номер карты": "*1234", "Сумма операции": -100, "Бонусы (включая кэшбэк)": 10.0},
            {"Номер карты": "*5678", "Сумма операции": -200, "Бонусы (включая кэшбэк)": 20.0},
            {"Номер карты": "*5678", "Сумма операции": -50, "Бонусы (включая кэшбэк)": 5.0}
        ]
        result = card_info(operations)
        expected_result = [
            {"last_digits": "1234", "total_spent": 100.0, "cashback": 10.0},
            {"last_digits": "5678", "total_spent": 250.0, "cashback": 25.0}
        ]
        self.assertEqual(result, expected_result)


class TestTopTransactions(unittest.TestCase):

    def test_empty_transactions(self):
        """Тест на пустой список транзакций"""
        result = top_transactions_5([])
        self.assertEqual(result, [])

    def test_less_than_five_transactions(self):
        """Тест с менее чем 5 транзакциями"""
        transactions = [
            {"Сумма операции": 100},
            {"Сумма операции": 200},
            {"Сумма операции": 50}
        ]
        result = top_transactions_5(transactions)
        self.assertEqual(result, [
            {"Сумма операции": 200},
            {"Сумма операции": 100},
            {"Сумма операции": 50}
        ])

    def test_exactly_five_transactions(self):
        """Тест с ровно 5 транзакциями"""
        transactions = [
            {"Сумма операции": 100},
            {"Сумма операции": 200},
            {"Сумма операции": 150},
            {"Сумма операции": 300},
            {"Сумма операции": 250}
        ]
        result = top_transactions_5(transactions)
        self.assertEqual(result, [
            {"Сумма операции": 300},
            {"Сумма операции": 250},
            {"Сумма операции": 200},
            {"Сумма операции": 150},
            {"Сумма операции": 100}
        ])

    def test_more_than_five_transactions(self):
        """Тест с более чем 5 транзакциями"""
        transactions = [
            {"Сумма операции": 100},
            {"Сумма операции": 200},
            {"Сумма операции": 150},
            {"Сумма операции": 300},
            {"Сумма операции": 250},
            {"Сумма операции": 400},
            {"Сумма операции": 350}
        ]
        result = top_transactions_5(transactions)
        self.assertEqual(result, [
            {"Сумма операции": 400},
            {"Сумма операции": 350},
            {"Сумма операции": 300},
            {"Сумма операции": 250},
            {"Сумма операции": 200}
        ])

    def test_identical_sums(self):
        """Тест на одинаковые суммы"""
        transactions = [
            {"Сумма операции": 100},
            {"Сумма операции": 100},
            {"Сумма операции": 200},
            {"Сумма операции": 200},
            {"Сумма операции": 150}
        ]
        result = top_transactions_5(transactions)
        self.assertEqual(result, [
            {"Сумма операции": 200},
            {"Сумма операции": 200},
            {"Сумма операции": 150},
            {"Сумма операции": 100},
            {"Сумма операции": 100}
        ])


if __name__ == '__main__':
    unittest.main()
