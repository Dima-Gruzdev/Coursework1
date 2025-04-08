import json
import logging
from datetime import datetime
from typing import List, Dict, Any


logger = logging.getLogger("services.py")
file_handler = logging.FileHandler('../logs/services.log', 'w', encoding="utf8")
file_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> json:
    """Функция в которой траты будут округляться, и разница между фактической
    суммой трат по карте и суммой округления будет попадать на счет Инвесткопилки."""
    if limit not in {10, 50, 100}:
        logger.error(f"Недопустимый предел округления: {limit}. Допустимые значения: 10, 50, 100.")
        raise ValueError("Предел округления должен быть 10, 50 или 100.")
    piggy_bank = 0
    for transaction in transactions:
        try:
            operation_date = datetime.strptime(transaction["Дата операции"], "%Y-%m-%d")
            transaction_month = operation_date.strftime("%Y-%m-%d")
            if transaction_month == month:
                amount = transaction["Сумма операции"]
                rounded_amount = ((amount + limit - 1) // limit) * limit
                accumulation = rounded_amount - amount
                piggy_bank += accumulation
                logger.info(
                    f"Транзакция на {amount} руб. округлена до {rounded_amount} руб. "
                    f"Отложено в копилку: {accumulation} руб."
                )
        except KeyError as e:
            logger.error(f"Отсутствует обязательное поле в транзакции: {e}")
        except Exception as e:
            logger.error(f"Ошибка при обработке транзакции: {e}")
    logger.info(f"Итого отложено в «Инвесткопилку» за {month}: {piggy_bank} руб.")
    return piggy_bank

if __name__ == "__main__":
    transactions = [
        {"Дата операции": "2023-10-01", "Сумма операции": 1712},
        {"Дата операции": "2023-10-05", "Сумма операции": 845},
        {"Дата операции": "2023-10-10", "Сумма операции": 123},
        {"Дата операции": "2023-10-15", "Сумма операции": 459},
    ]
    savings = investment_bank("2023-10-15", transactions, limit=100)
    savings = json.dumps(savings)
    print(f"Сумма в копилке: {savings} руб.")
