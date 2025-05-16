from typing import Any

from config import TRANSACTION_PATH_EXCEL
import src.utils


def main_views(data_main_time: Any) -> None:
    """
    Главная функция программы, запускающая все функции модулей.
    """
    greeting = src.utils.get_greeting(data_main_time if data_main_time else None)
    transactions = src.utils.reading_transactions_excel(TRANSACTION_PATH_EXCEL)
    total_expenses = src.utils.calcul_total_expen(transactions)
    card_data = src.utils.card_info(transactions)
    top_trans = src.utils.top_wastes_trans(transactions)
    currency_rates = [
        {"currency": "USD", "rate": src.utils.exchange_rate("USD")},
        {"currency": "EUR", "rate": src.utils.exchange_rate("EUR")},
    ]
    stock_prices = [
        {"stock": "AAPL", "price": src.utils.yf_tick_stoc_cur("AAPL")},
        {"stock": "AMZN", "price": src.utils.yf_tick_stoc_cur("AMZN")},
        {"stock": "GOOGL", "price": src.utils.yf_tick_stoc_cur("GOOGL")},
        {"stock": "MSFT", "price": src.utils.yf_tick_stoc_cur("MSFT")},
        {"stock": "TSLA", "price": src.utils.yf_tick_stoc_cur("TSLA")},
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
    src.utils.write_json(output_file, output_data)
    return src.utils.read_json(output_file)


if __name__ == "__main__":
    main_views("2020-10-10 15:30:00")
