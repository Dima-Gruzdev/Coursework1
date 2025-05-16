import json
import logging
from datetime import datetime
from typing import Optional, Any
import pandas as pd

from config import TRANSACTION_PATH_EXCEL

logger = logging.getLogger("reports.py")
file_handler = logging.FileHandler('logs/reports.log', 'w', encoding="utf8")
file_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_excel_df(path: Any) -> pd.DataFrame:
    """Функция считывания эксель файла"""
    df_trans = pd.read_excel(path)
    return df_trans


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date, dayfirst=True)

    start_date = date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)]

    sum_category = filtered_transactions["Сумма платежа"].sum()
    logger.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.\n"
                f"Потрачено: {sum_category}")

    return sum_category


if __name__ == "__main__":
    operations_data = read_excel_df(TRANSACTION_PATH_EXCEL)
    total = json.dumps(spending_by_category(operations_data, "Наличные", "20.07.2020"))
    print(total)
