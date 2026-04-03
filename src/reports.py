import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def report_to_json(
        data: List[Dict[str, Any]],
        output_path: str = "reports/web_data.json"
) -> None:
    """Совместимо с тестами."""
    Path(output_path).parent.mkdir(exist_ok=True, parents=True)

    report_data = {
        "total_transactions": len(data),
        "total_amount": sum(item["amount"] for item in data),
        "data": data
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)


def json_report(default_filename: str = "reports/report_{timestamp}.json"):
    """Декоратор: сохраняет отчет в JSON."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, output_file: Optional[str] = None, **kwargs) -> Any:
            result = func(*args, **kwargs)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = output_file or default_filename.format(timestamp=timestamp)
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"✅ Отчет сохранен: {filename}")
            return result
        return wrapper
    return decorator


@json_report()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Траты по категории за последние 3 месяца.

    >>> df = pd.DataFrame({
    ...     'date': ['2025-01-15', '2025-02-10', '2025-03-05'],
    ...     'amount': [-1000, -500, -200],
    ...     'category': ['Супермаркеты', 'Транспорт', 'Супермаркеты']
    ... })
    >>> spending_by_category(df, 'Супермаркеты')
    """
    # Текущая дата или переданная
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    # 3 месяца назад
    start_date = end_date - timedelta(days=90)

    # Фильтр по периоду + категории + расходам (amount < 0)
    mask = (
            (pd.to_datetime(transactions['date']) >= start_date) &
            (pd.to_datetime(transactions['date']) <= end_date) &
            (transactions['category'] == category) &
            (transactions['amount'] < 0)
    )

    result = transactions[mask].copy()
    result = (
        result[['date', 'amount', 'description']]
        .sort_values('date', ascending=False)
    )

    logger.info(
        f"📊 {category}: {len(result)} трат за 3 мес. "
        f"на сумму {abs(result['amount'].sum()):.2f}₽"
    )

    # JSON сериализуемый результат
    return result.reset_index(drop=True)


@json_report()
def spending_by_category_summary(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> Dict[str, Any]:
    """JSON сводка по категории."""
    df = spending_by_category(transactions, category, date)
    total_spent = abs(df['amount'].sum()) if not df.empty else 0
    avg_spent = abs(df['amount'].mean()) if not df.empty else 0

    return {
        "category": category,
        "period_3_months": True,
        "total_transactions": len(df),
        "total_spent": round(total_spent, 2),
        "average_transaction": round(avg_spent, 2),
        "transactions": df.to_dict('records')
    }


# Утилита для Pandas DataFrame из транзакций
def df_from_transactions(transactions: List[Dict[str, Any]]) -> pd.DataFrame:
    """Конвертер list[dict] → DataFrame."""
    return pd.DataFrame(transactions)
