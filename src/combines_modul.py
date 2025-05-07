import json
import logging
from datetime import datetime, timedelta

import pandas as pd

from config import TRANSACTION_PATH_EXCEL
from src.reports import read_excel_df

logger = logging.getLogger("combines_modul.py")
file_handler = logging.FileHandler('../logs/combines_modul.log', 'w', encoding="utf8")
file_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def filter_by_category_date(transactions: pd.DataFrame, category: str, start_date: str) -> json:
    """
    Фильтрация  по категории и дате, выводит уже отфильтрованные транзакции
    """
    end_date = datetime.strptime(start_date, "%d.%m.%Y") + timedelta(days=90)
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] < end_date.strftime("d.%m.%Y"))]
    return filtered_transactions.to_dict("records")


def main_reports() -> None:
    """
    функция обеденяющея весь модуль reports(ВСЕ ФУНКЦИИ МОДУЛЯ REPORTS)
    """
    operations = read_excel_df(TRANSACTION_PATH_EXCEL)
    category = input("Напишите категорию: ")
    start_date = input("Напишите дату (от которой надо считать) 3-месячного периода (например 01.01.2001): ")

    filtered_operations = filter_by_category_date(operations, category, start_date)

    with open("operations_data.json", "w", encoding="utf-8") as f:
        json.dump(filtered_operations, f, indent=4, ensure_ascii=False)

    logger.info("Отфильтрованные операции записаны сюда ../logs/combines_modul.log")
    print("Отфильтрованные операции записаны сюда ../logs/combines_modul.log")
