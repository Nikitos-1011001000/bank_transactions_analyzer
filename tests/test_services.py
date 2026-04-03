import json

import pytest

from services import save_cashback_analysis_json
from utils import cards_to_json_safe, validate_json_serializable


def test_save_cashback_analysis_json(tmp_path):
    """Тест сохранения отчёта."""
    transactions = [{"amount": 100, "category": "Еда",  "date": "2025-01-15"}]
    path = tmp_path / "test.json"
    save_cashback_analysis_json(transactions, 2025, 1, str(path))
    assert path.exists()


def test_other_service_functions():
    """Базовые сервисы."""
    pass


def test_services_functions(tmp_path):
    """Массовый тест сервисов."""
    transactions = [{"id": 1, "amount": 100, "date": "2025-01-15"}]
    # services.py
    save_cashback_analysis_json(transactions, 2025, 1, str(tmp_path / "test.json"))

    # utils.py
    validate_json_serializable(transactions)
    cards_to_json_safe(transactions)

    assert True


@pytest.mark.parametrize("year,month,expected_count", [
    (2025, 1, 1),  # Январь 2025 — 1 транзакция
    (2025, 2, 0),  # Февраль 2025 — 0 транзакций
])
def test_save_cashback_analysis_json_parametrized(
        tmp_path,
        year,
        month,
        expected_count,
):
    """Параметризованный тест сохранения."""
    transactions = [{"amount": 100, "category": "Еда", "date": "2025-01-15"}]
    path = tmp_path / "test.json"

    save_cashback_analysis_json(transactions, year, month, str(path))

    # Читаем результат
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == expected_count
