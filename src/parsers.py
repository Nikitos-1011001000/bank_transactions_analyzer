from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def load_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из Excel для анализа."""
    path = Path(file_path)
    if not path.exists():
        print(f"❌ Файл не найден: {file_path}")
        return []

    df = pd.read_excel(file_path)
    return df.to_dict('records')
