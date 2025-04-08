import json

from datetime import datetime, time
from typing import Any

import pandas as pd



def read_excel(filename: str, datetime_to_timestamp: bool = True) -> pd.DataFrame:
    """Функция для чтения excel файла"""
    operations_df = pd.read_excel(filename)
    if datetime_to_timestamp:
        operations_df["Дата операции"] = pd.to_datetime(operations_df["Дата операции"], dayfirst=True)
    return operations_df


def write_json(file_path: str, data: Any) -> None:
    """ Открытие и запись json данных"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# def greeting()-> str:
#     """Функция приветсвия в зависимости от времени суток"""
#     date_now = datetime.now().time()
#     if time(hour=22) <= date_now < time(hour=23, minute=59, second=59) or time(hour=0) <= date_now < time(hour=6):
#         return "Доброй ночи"
#     elif time(hour=6) <= date_now < time(hour=12):
#         return "Доброе утро"
#     elif time(hour=12) <= date_now < time(hour=17):
#         return "Добрый день"
#     else:
#         return "Добрый вечер"

