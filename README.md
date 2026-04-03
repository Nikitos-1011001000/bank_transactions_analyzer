\# 💳 Bank Transactions Analyzer



\## 🚀 Описание

\*\*Анализатор банковских транзакций\*\* — Python CLI приложение для:

\- Анализа CSV выписок банков

\- Отслеживания кэшбэка и топ-тратах

\- Конвертации валют по API ЦБ РФ

\- Мониторинга акций (AAPL/TSLA) через Alpha Vantage

\- Генерации JSON отчетов с декораторами



\*\*Тех стек:\*\* `pandas` `requests` `pytest` `mypy` `poetry` `flake8`



\## 🛠 Установка \& Запуск



1\. \*\*Клонируй репозиторий:\*\*

```bash

git clone https://github.com/твой\_username/bank\_transactions\_analyzer.git

cd bank\_transactions\_analyzer

```



2\. \*\*Установи зависимости:\*\*

```bash

poetry install

\# или

pip install -r requirements.txt

```



3\. \*\*Запусти тесты:\*\*

```bash

poetry run pytest --cov=src --cov-report=html

```



4\. \*\*Запуск анализа:\*\*

```bash

poetry run python src/main.py transactions.csv

```



\## 🔧 Локальная разработка

```bash

\# Линтинг

poetry run flake8 src tests



\# Форматирование

poetry run isort src tests

```



\## 📄 Лицензия

\[MIT](LICENSE)



\## Автор

\*\*Никита Рукин\*\*
