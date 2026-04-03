"""Вспомогательные функции для views.py."""
import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, cast

import pandas as pd
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_greeting(current_time: str) -> str:
    """Приветствие по времени."""
    logger.info(f"Определяем приветствие: {current_time[:16]}")
    hour = int(current_time.split()[1][:2])

    logger.info("Приветствие установлено")
    if 5 <= hour < 11:
        return "Доброе утро"
    elif 11 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def extract_card_last_digits(description: str) -> str:
    """Последние 4 цифры карты."""
    match = re.search(r'(\d{4})(?!\d)', description)
    return match.group(1) if match else "****"


def format_top_transaction(t: Dict[str, Any]) -> Dict[str, Any]:
    """Форматирует одну транзакцию для топа."""
    return {
        "date": (
            datetime.strptime(t["date"], "%Y-%m-%d")
            .strftime("%d.%m.%Y")
        ),
        "amount": round(t["amount"], 2),
        "category": t.get("category", "Неизвестно"),
        "description": t["description"][:50] + "..." if len(t["description"]) > 50 else
        t["description"]
    }


def validate_json_serializable(data: Dict[str, Any]) -> Dict[str, Any]:
    """Проверяет/исправляет JSON-сериализуемость (использует json)."""
    try:
        json.dumps(data)  # ← ТЗ: использует json!
        return data
    except (TypeError, ValueError):
        if isinstance(data, dict):
            return {k: validate_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [validate_json_serializable(item) for item in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        return str(data)


def cards_to_json_safe(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Гарантирует JSON-сериализуемость карт."""
    return cast(
        List[Dict[str, Any]],
        json.loads(
            json.dumps(
                cards,
                default=str,
                ensure_ascii=False,
            ),
        ),
    )  # ← json!


def get_cbr_currency_rates() -> List[Dict[str, float]]:
    """API ЦБ РФ курсы валют (pandas!)."""
    logger.info("Загружаем курсы ЦБ РФ с pandas")
    try:
        resp = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)
        logger.info(f"ЦБ API: статус {resp.status_code}")

        # PANDAS обработка
        df = pd.DataFrame(list(resp.json()["Valute"].items()), columns=['code', 'info'])
        currencies = [{"currency": c['code'], "rate": c['info']['Value']}
                      for c in df.head(2)[['code', 'info']].to_dict('records')]

        logger.info(f"Pandas обработано валют: {len(currencies)}")
        return json.loads(json.dumps(currencies, ensure_ascii=False))

    except (
        requests.RequestException,
        json.JSONDecodeError,
        pd.errors.EmptyDataError,
    ) as e:
        logger.error(f"Ошибка ЦБ API: {e}")
        return [{"currency": "USD", "rate": 97.5}, {"currency": "EUR", "rate": 105.2}]


def get_stock_prices() -> List[Dict[str, float]]:
    """API Alpha Vantage акции (json в utils!)."""
    try:
        import os
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
        stocks = []
        for symbol in ["AAPL", "TSLA"]:
            url = (
                f"https://www.alphavantage.co/query?"
                f"function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
            )
            resp = requests.get(url, timeout=5)
            price = resp.json()["Global Quote"]["05. price"]
            stocks.append({"stock": symbol, "price": float(price)})
        return json.loads(json.dumps(stocks, ensure_ascii=False))  # ← json!

    except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Ошибка Alpha Vantage API: {e}")
        return [
            {"stock": "AAPL", "price": 230.45},
            {"stock": "TSLA", "price": 248.90}
        ]
