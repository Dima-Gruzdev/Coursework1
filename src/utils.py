import json

from typing import Any

import pandas as pd


def reading_transactions_excel(filename: str) -> list[dict]:
    """Функция чтения Excel файла транзакции"""
    try:
        return pd.read_excel(filename).to_dict(orient='records')
    except (FileNotFoundError, ValueError) as err:
        print(err)
        return []


def write_json(file_path: str, data: Any) -> None:
    """ Открытие и запись json данных"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
