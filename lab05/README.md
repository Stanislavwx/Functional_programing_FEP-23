# ЛР 5 — Ліниві обчислення: генератори та `itertools`

## Цілі
- розібратися з генераторними виразами, `yield`/`yield from`, ітераторами та поняттям лінивої оцінки;
- безпечно працювати з нескінченними послідовностями;
- опанувати будівельні блоки з `itertools`: `islice`, `takewhile`, `dropwhile`, `accumulate`, `count`, `cycle`, `repeat`;
- реалізувати нескінченний стрім Фібоначчі, `sliding_window`, практики `take`/`drop`/`accumulate`.

## Швидкий старт
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt

pytest -v          # запустити тести з детальним підсумком
python main.py     # продемонструвати роботу
```
