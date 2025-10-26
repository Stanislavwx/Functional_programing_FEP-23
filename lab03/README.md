# Лабораторна робота 3: Незмінні структури даних у Python

## Що реалізовано
- `Item`: NamedTuple (незмінний), властивість `total`.
- `Order`: `@dataclass(frozen=True, slots=True)`:
  - поля: `items: tuple[Item, ...]`, `tags: frozenset[str]`, `meta: Mapping[str, str]` (read-only через `MappingProxyType`).
  - чисті методи: `subtotal`, `add_tag`, `with_item`, `pay`, `with_meta`.
  - кастомний `__deepcopy__` для `MappingProxyType` на Python 3.13.
- `core.py`: чисті операції `add_item`, `add_tag`, `pay`; читальна `top_expensive_items`; утиліта `freeze`.

## Команди перевірки
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest -q
mypy lab03
black --check lab03
ruff check lab03

pytest --durations=5 -q
```