import json
import os
from datetime import datetime

from typing import Any
import yfinance as yf

import pandas as pd
import requests
import logging

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

logger = logging.getLogger("utils.py")
file_handler = logging.FileHandler('logs/utils.log', 'w', encoding="utf8")
file_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_greeting(date_time: Any) -> str | None:
    """
    Функция принимает строку с date и time (либо жми enter , будет текущее время)
    после выводит приветствие в зависимости от чего вы вели.
    """
    try:
        if date_time is None:
            date_time = datetime.now()
        else:
            date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        hour = date_time.hour
        if 5 <= hour < 12:
            logger.info("Доброе утро!")
            return "Доброе утро!"
        elif 12 <= hour < 18:
            logger.info("Добрый день!")
            return "Добрый день!"
        elif 18 <= hour < 23:
            logger.info("Добрый вечер!")
            return "Добрый вечер!"
        else:
            logger.info("Доброй ночи!")
            return "Доброй ночи!"
    except ValueError as er:
        print(f"Неверный формат ошибка {er}")
        logger.info(f"Неверный формат ошибка {er}")


def calcul_total_expen(transactions_sum: list[dict[str, Any]]) -> float:
    """
    Функция считает сумму расходов по списку транзакций.
    """
    total_expenses = 0.0
    for transaction in transactions_sum:
        if transaction["Сумма операции"] < 0:
            total_expenses += transaction["Сумма операции"]
    logger.info(f'{total_expenses * -1}')
    return total_expenses * -1


def card_info(card_total: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Функция обрабатывает данные о картах из списка"""
    card_data = {}
    for operation in card_total:
        if isinstance(operation["Номер карты"], str) and operation["Номер карты"].startswith("*"):
            last_digits = operation["Номер карты"][-4:]
            if last_digits not in card_data:
                card_data[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
        if operation["Сумма операции"] < 0:
            card_data[last_digits]["total_spent"] += round(operation["Сумма операции"] * -1, 1)
        card_data[last_digits]["cashback"] += operation.get("Бонусы (включая кэшбэк)", 0.0)
    logger.info(f"{card_data.values()}")
    return list(card_data.values())


def top_wastes_trans(transactions: [dict]) -> list[dict]:
    """Функция возвращает топ 5 транзакций"""
    transactions.sort(key=lambda x: x["Сумма операции"], reverse=True)
    logger.info(f"{transactions[:5]}")
    return transactions[:5]


def exchange_rate(currency: str) -> Any:
    """ Функция получение курса валют."""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY}, timeout=40)
    response_data = response.json()
    logger.info(f"{response_data["rates"]["RUB"]}")
    return response_data["rates"]["RUB"]


def yf_tick_stoc_cur(stock: str) -> Any:
    """Функция получает акции с помощью Yahoo Finance"""
    stock_data = yf.Ticker(stock)
    todays_data = stock_data.history(period="1d")
    logger.info(f"{todays_data["High"].iloc[0]}")
    return todays_data["High"].iloc[0]


def reading_transactions_excel(filename: str) -> list[dict]:
    """Функция чтения Excel файла транзакции"""
    try:
        logger.info(f"{pd.read_excel(filename).to_dict(orient='records')}")
        return pd.read_excel(filename).to_dict(orient='records')
    except (FileNotFoundError, ValueError) as err:
        logger.info(f"{err}")
        return []


def write_json(file_path: str, data: Any) -> None:
    """ Открытие и запись json данных"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(file_path: str) -> Any:
    """Функция чтения json файла"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
