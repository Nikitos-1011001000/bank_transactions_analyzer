from parsers import load_excel_transactions
from reports import generate_json_report


def main() -> None:
    """Полный пайплайн: Excel → JSON."""
    print("🚀 Анализатор транзакций запущен!")

    # 1. Загрузка Excel
    data = load_excel_transactions("data/operations.xlsx")

    if not data:
        print("❌ Нет данных для анализа")
        return

    # 2. JSON для веба
    generate_json_report(data)

    # 3. Статистика
    print(f"📊 Всего транзакций: {len(data)}")
    print("✅ Курсовая задача 1 выполнена!")


if __name__ == "__main__":
    main()
