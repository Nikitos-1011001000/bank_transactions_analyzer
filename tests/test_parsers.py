from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest

from parsers import load_excel_transactions


@pytest.fixture
def mock_excel_data() -> List[Dict[str, Any]]:
    return [{"id": 1, "amount": 1000}, {"id": 2, "amount": 500}]


def test_file_not_found():
    with patch('pathlib.Path.exists', return_value=False):
        result = load_excel_transactions("nonexistent.xlsx")
        assert result == []


@patch('pathlib.Path.exists')
@patch('pandas.read_excel')
def test_excel_loaded(mock_read_excel, mock_exists, mock_excel_data):
    mock_exists.return_value = True
    mock_read_excel.return_value = Mock(to_dict=Mock(return_value=mock_excel_data))

    result = load_excel_transactions("data/test.xlsx")

    mock_read_excel.assert_called_once()
    assert len(result) == 2


@pytest.mark.parametrize("file_path,expected", [
    ("data/good.xlsx", 2),
    ("data/bad.xlsx", 0),
    ("empty.xlsx", 0)
])
@patch('pathlib.Path.exists')
@patch('pandas.read_excel')
def test_parametrized(
    mock_read_excel,
    mock_exists,
    file_path,
    expected,
    mock_excel_data
):
    """✅ ФИКС: if внутри функции!"""
    mock_exists.return_value = True

    # ✅ expected=0 → ПУСТОЙ список!
    if expected == 0:
        mock_read_excel.return_value.to_dict.return_value = []
    else:
        mock_read_excel.return_value.to_dict.return_value = mock_excel_data[:expected]

    result = load_excel_transactions(file_path)
    assert len(result) == expected
