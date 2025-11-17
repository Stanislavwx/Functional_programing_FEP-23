# Лабораторна робота №8 — ADT в Python (Union • Literal • Protocol • match/case)

## Вміст
- `expr.py` — AST: `Expr = Num | Add | Mul` (та альтернативний варіант із `Literal`).
- `eval_.py` — чистий `eval_expr` через `match/case`, захист від переповнення.
- `pretty.py` — рендер AST у рядок.
- `main.py` — демо запуск.
- `tests/test_expr.py` — pytest-тести.
- `mypy.ini` — строгий режим типізації.
- `pyproject.toml` — мінімальні налаштування pytest.

## Швидкий старт
```bash
python -m pip install mypy pytest
mypy --strict .
pytest
python main.py
```

## Пояснення
- ADT моделюємо як `Union` із `@dataclass`-вузлами.
- `match/case` дає структурний розбір: `case Add(left=a, right=b)`.
- `Literal` показує, як звузити значення оператора до конкретних символів: `Literal["+", "*"]`.
- `Protocol` (див. `expr.py`) — приклад структурного інтерфейсу (duck typing з mypy).

Успіхів!
