from collections import defaultdict
from typing import Any, Dict, List


def aggregate_by_month(
    transactions: List[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:
    """Группировка по месяцам YYYY-MM."""
    monthly: Dict[str, float] = defaultdict(lambda: {"total": 0.0, "count": 0})
    for t in transactions:
        month = t["date"][:7]  # 2025-01
        monthly[month]["total"] += t["amount"]
        monthly[month]["count"] += 1
    return dict(monthly)


def aggregate_by_category(
    transactions: List[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:
    """Группировка по категориям."""
    category_stats = defaultdict(lambda: {"total": 0.0, "count": 0})
    for t in transactions:
        cat = t.get("category", "другое")
        category_stats[cat]["total"] += t["amount"]
        category_stats[cat]["count"] += 1
    return dict(category_stats)
