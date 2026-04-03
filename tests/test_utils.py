from src.utils import extract_card_last_digits, format_top_transaction, get_greeting


# 1. get_greeting (строки 16-25) — 100% покрытие!
def test_get_greeting_morning():
    assert get_greeting("2026-04-03 08:00:00") == "Доброе утро"


def test_get_greeting_day():
    assert get_greeting("2026-04-03 14:00:00") == "Добрый день"


def test_get_greeting_evening():
    assert get_greeting("2026-04-03 20:00:00") == "Добрый вечер"


def test_get_greeting_night():
    assert get_greeting("2026-04-03 02:00:00") == "Доброй ночи"


# 2. extract_card_last_digits (строка 34)
def test_extract_card_last_digits():
    assert extract_card_last_digits("Карта ****1234") == "1234"
    assert extract_card_last_digits("Без карты") == "****"


# 3. format_top_transaction (строки 46-53)
def test_format_top_transaction():
    transaction = {
        "date": "2026-04-03",
        "amount": 123.456,
        "category": "Еда",
        "description": "Длинное описание транзакции больше 50 символов..."
    }
    result = format_top_transaction(transaction)
    assert result["date"] == "03.04.2026"
    assert result["amount"] == 123.46
