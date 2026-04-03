import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .parsers import load_excel_transactions
from .utils import (  # ← utils!
    extract_card_last_digits,
    format_top_transaction,
    get_cbr_currency_rates,
    get_greeting,
    get_stock_prices,
)


def main_page_json(file_path: str, current_datetime: str = None) -> Dict[str, Any]:
    """Главная страница JSON (использует utils)."""
    if current_datetime is None:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Загрузка
    transactions = load_excel_transactions(file_path)

    # Карты (utils)
    cards = {}
    for t in transactions:
        card_digits = extract_card_last_digits(t["description"])
        total = abs(t["amount"])
        if card_digits not in cards:
            cards[card_digits] = 0.0
        cards[card_digits] += total

    cards_list = [
        {
            "last_digits": card,
            "total_spent": round(total, 2),
            "cashback": round(total / 100, 2)
        }
        for card, total in cards.items()
    ][:2]

    # Топ-5 (utils)
    top_transactions = (
        sorted(transactions, key=lambda t: abs(t["amount"]), reverse=True)[:5]
    )
    top_formatted = [format_top_transaction(t) for t in top_transactions]

    # Фиксированные данные
    currencies = get_cbr_currency_rates()  # ← API + json!
    stocks = get_stock_prices()

    return {
        "greeting": get_greeting(current_datetime),
        "cards": cards_list,
        "top_transactions": top_formatted,
        "currency_rates": currencies,
        "stock_prices": stocks,
        "total_balance": round(sum(t["amount"] for t in transactions), 2),
        "total_transactions": len(transactions),
        "datetime": current_datetime
    }


def save_main_page_json(file_path: str, output_path: str = "reports/main_page.json"):
    """Сохраняет JSON главной страницы."""
    data = main_page_json(file_path)
    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Главная страница JSON: {output_path}")
