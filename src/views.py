import json
import os
from datetime import datetime
from typing import List, Any
import requests
import yfinance as yf

from dotenv import load_dotenv

from config import TRANSACTION_PATH_EXCEL
from src.utils import read_excel, write_json, read_json

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_greet(date_time: Any) -> str:
    """
    Функция принимает строку с date и time (либо жми энтер если в падлу)
    после выводит приветствие в зависимости от чего вы вели .
    """
    if date_time is None:
        date_time = datetime.now()
    else:
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    hour = date_time.hour
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def sum_expenses_transactions(transactions_sum: List[dict]) -> float:
    """Функция считает сумму расходов по списку"""
    result_expens = 0
    for transaction in transactions_sum:
        if transaction["Сумма операции"] < 0:
            result_expens += transaction["Сумма операции"]
    return result_expens * -1


def card_info(operations: List[dict]) -> List[dict]:
    """Функция обрабатывает данные о картах из списка"""
    card_data = {}
    for operation in operations:
        if isinstance(operation["Номер карты"], str) and operation["Номер карты"].startswith("*"):
            last_digits = operation["Номер карты"][-4:]
            if last_digits not in card_data:
                card_data[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
        if operation["Сумма операции"] < 0:
            card_data[last_digits]["total_spent"] += round(operation["Сумма операции"] * -1, 1)
            card_data[last_digits]["cashback"] += operation.get("Бонусы (включая кэшбэк)", 0.0)
    return list(card_data.values())


def top_transactions_5(transactions: List[dict]) -> List[dict]:
    """Функция возвращает топ 5 транзакций"""
    transactions.sort(key=lambda x: x["Сумма операции"], reverse=True)
    return transactions[:5]


def get_cur_rate(currency: str) -> Any:
    """ Функция получение курса валют."""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY}, timeout=40)
    response_data = json.loads(response.text)
    return response_data["rates"]["RUB"]


def get_stoc_cur(stock: str, yf=None) -> Any:
    """Функция получает акции с помощью Yahoo Finance"""
    stock_data = yf.Ticker(stock)
    todays_data = stock_data.history(period="1d")
    return todays_data["High"].iloc[0]


def main_views() -> None:
    """
    Главная функция программы, запускающая все функции модулей.
    """
    user_input = input(
        "Введите дату и время в формате YYYY-MM-DD HH:MM:SS " "или нажмите Enter для использования на вашем устройстве:"
    )
    greeting = get_greet(user_input if user_input else None)
    transactions = read_excel(TRANSACTION_PATH_EXCEL)
    total_expenses = sum_expenses_transactions(transactions)
    card_data = card_info(transactions)
    top_trans = top_transactions_5(transactions)
    currency_rates = [
        {"currency": "USD", "rate": get_cur_rate("USD")},
        {"currency": "EUR", "rate": get_cur_rate("EUR")},
    ]
    stock_prices = [
        {"stock": "AAPL", "price": get_stoc_cur("AAPL")},
        {"stock": "AMZN", "price": get_stoc_cur("AMZN")},
        {"stock": "GOOGL", "price": get_stoc_cur("GOOGL")},
        {"stock": "MSFT", "price": get_stoc_cur("MSFT")},
        {"stock": "TSLA", "price": get_stoc_cur("TSLA")},
    ]
    output_data = {
        "greeting": greeting,
        "total_expenses": total_expenses,
        "card_data": card_data,
        "top_transactions": top_trans,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    output_file = "operations_data.json"
    write_json(output_file, output_data)
    print(read_json(output_file))


if __name__ == "__main__":
    main_views()
