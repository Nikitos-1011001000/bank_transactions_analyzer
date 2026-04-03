import json
import logging
from datetime import datetime
from functools import reduce
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def filter_by_month(
        transactions: List[Dict[str, Any]],
        year: int,
        month: int,
) -> List[Dict[str, Any]]:
    """Фильтр транзакций по году/месяцу (чистая функция)."""

    def is_target_month(t: Dict[str, Any]) -> bool:
        tx_date = datetime.strptime(t["date"][:7], "%Y-%m")  # "2026-03" → datetime
        return tx_date.year == year and tx_date.month == month

    return list(filter(is_target_month, transactions))


def group_by_category(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Группировка расходов по категориям (reduce)."""

    def reducer(acc: Dict[str, float], t: Dict[str, Any]) -> Dict[str, float]:
        cat = t.get("category", "Неизвестно")
        amount = abs(t["amount"])  # только расходы
        acc[cat] = acc.get(cat, 0.0) + amount
        return acc

    return reduce(reducer, transactions, {})


def calculate_cashback_amounts(category_totals: Dict[str, float]) -> Dict[str, float]:
    """Кешбэк 1% (map)."""
    return {cat: round(total / 100, 2) for cat, total in category_totals.items()}


def analyze_cashback_categories(
        data: List[Dict[str, Any]],
        year: int,
        month: int
) -> Dict[str, float]:
    """
    Главный сервис: анализ выгодных категорий кешбэка.

    >>> analyze_cashback_categories([
    ...     {"date": "2025-01-15", "amount": 10000, "category": "Супермаркеты"},
    ...     {"date": "2025-01-20", "amount": 5000, "category": "Транспорт"}
    ... ], 2025, 1)
    {'Супермаркеты': 100.0, 'Транспорт': 50.0}
    """
    logger.info(f"🔍 Анализ кешбэка {year}-{month:02d}: {len(data)} транзакций")  # ← +1

    monthly_data = filter_by_month(data, year, month)
    logger.info(f"📅 Март: {len(monthly_data)} транзакций")  # ← +2

    category_totals = group_by_category(monthly_data)
    cashback = calculate_cashback_amounts(category_totals)

    result = dict(sorted(cashback.items(), key=itemgetter(1), reverse=True))
    logger.info(f"🏆 Категорий кешбэка: {len(result)}")  # ← +3

    return result


def save_cashback_analysis_json(
        transactions: List[Dict[str, Any]],
        year: int,
        month: int,
        output_path: str = "reports/cashback_analysis.json"
) -> None:
    """Сохраняет анализ в JSON."""
    result = analyze_cashback_categories(transactions, year, month)
    Path(output_path).parent.mkdir(exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Анализ кешбэка: {output_path}")

    if result:  # Проверка на пустой dict
        print(f"📊 Топ категория: {max(result.items(), key=itemgetter(1))}")
    else:
        print("📊 Нет данных для анализа")
