# ЛР6. Замикання та декоратори як HOF

**Цілі**
- Створення замикань (closures): утримання стану, інʼєкція залежностей.
- Параметризовані декоратори як фабрики: коректний `@wraps`, `ParamSpec`, `TypeVar`.
- Завдання: **таймінг**, **ретраї**, **кеш** із **інвалідацією**.

## Структура
```
lab06/
  README.md
  decorators.py       # timed, retries, cached (+ утиліти)
  closures.py         # приклади замикань
  tests/
    test_timed.py
    test_retries.py
    test_cached.py
  requirements.txt
  pyproject.toml
  mypy.ini
  .gitignore
```

## Швидкий старт
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

## Нотатки
- Декоратори інʼєктують залежності (`clock/sleep/logger/time_fn`) — це робить тести стабільними.
- Порядок декораторів важливий: кеш → ретраї → таймінг (знизу вгору).
- Використовуйте `functools.wraps` для збереження метаданих функції.
