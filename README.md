Bank Transactions Analyzer



Описание

Анализатор банковских транзакций — приложение для:

\- Анализа CSV выписок банков

\- Генерации JSON отчетов с декораторами



###Тех стек:

`pandas` `requests` `pytest` `mypy` `poetry` `flake8`



\###Установка \& Запуск

1\. Клонирование репозитория:

```bash

git clone https://github.com/Nikitos-1011001000/bank_transactions_analyzer

2\. Установка зависимости:

```bash

poetry install

\# или

pip install -r requirements.txt

```

3\. Запуск тестов:

```bash

poetry run pytest --cov=src --cov-report=html

```

4\. Запуск анализа:

```bash

poetry run python main.py

```
5\. Пример вывода:

Анализатор транзакций запущен!
Всего транзакций: 6705


\## Локальная разработка

```bash

\# Линтинг

poetry run flake8 src tests

\## Автор

\*\*Никита Рукин\*\*

=======
# bank_transactions_analyzer
