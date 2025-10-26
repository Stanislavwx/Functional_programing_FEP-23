# ЛР1. Основи функціонального програмування у Python

## Цілі
- Чисті функції та референтна прозорість
- Виявлення й ізоляція побічних ефектів
- Перепис імперативного фрагмента у функціональному стилі
- Параметризація обчислень через `typing.Callable`

## Структура
```
lab01/
  README.md
  core.py          # чисте ядро (без I/O)
  app.py           # оболонка побічних ефектів (I/O)
  tests/
    test_core.py   # pytest-тести до чистого ядра
  requirements.txt # інструменти
  pyproject.toml   # налаштування black/ruff
  mypy.ini         # налаштування типів
  .gitignore
```

## Встановлення
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск
- Тести: `pytest -q`
- Статика типів: `mypy .`
- Форматування: `black .`
- Лінт: `ruff check .`

## Приклад
```bash
python app.py --min-total 100 --discount 0.1 --tax 0.2
```

## Завдання
1. Перепишіть імперативний код у `core.py:process_orders_pure` на чисті функції (вже дано приклад) і не змінюйте вхідні дані.
2. Параметризуйте політику фільтрації/знижок/податків через `Callable` (див. `make_processor`).
3. Перенесіть усі `print/IO/random/time` в оболонку (`app.py`).

## Оцінювання (10 балів)
- Коректність: 4
- Функціональний стиль/чистота: 3
- Тести+типи: 2
- Читабельність/структура: 1
