# Лабораторна робота 4: Рекурсія та мемоізація в Python

## Що реалізовано
- `quicksort(xs)`: рекурсивне сортування з випадковим pivot (чисте, без мутацій).
- `Node` та обходи дерева: `preorder`, `inorder`, `postorder` (рекурсивно), `bfs_level_order`, `dfs_preorder_iter` (ітеративно).
- `fib` з `@lru_cache(maxsize=None)` та ітеративний `fib_iter`.
- Тести `pytest` для всіх частин.
- Налаштування `black/ruff/mypy` в `pyproject.toml`.

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pytest -q
pytest -q --durations=5

mypy lab04
black --check lab04
ruff check lab04
```
