import pytest

from aggregator import aggregate_by_category, aggregate_by_month


@pytest.fixture
def transactions():
    return [
        {"id": 1, "amount": 1000, "date": "2025-01-15", "category": "еда"},
        {"id": 2, "amount": -500, "date": "2025-01-20", "category": "еда"},
        {"id": 3, "amount": 2000, "date": "2025-02-10", "category": "транспорт"}
    ]


def test_aggregate_by_month(transactions):
    """Тест: группировка по месяцам."""
    result = aggregate_by_month(transactions)

    assert len(result) == 2
    assert result["2025-01"]["total"] == 500.0  # 1000 + (-500)
    assert result["2025-01"]["count"] == 2
    assert result["2025-02"]["total"] == 2000.0
    assert result["2025-02"]["count"] == 1


def test_aggregate_by_category(transactions):
    """Тест: группировка по категориям."""
    result = aggregate_by_category(transactions)

    assert len(result) == 2
    assert result["еда"]["total"] == 500.0  # 1000 + (-500)
    assert result["еда"]["count"] == 2
    assert result["транспорт"]["total"] == 2000.0
    assert result["транспорт"]["count"] == 1


def test_aggregate_empty():
    """Тест: пустой список."""
    result_month = aggregate_by_month([])
    result_cat = aggregate_by_category([])
    assert result_month == {}
    assert result_cat == {}
