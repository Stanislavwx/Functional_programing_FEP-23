# Лабораторна робота 2: Функції вищого порядку, композиція, map/filter/reduce

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# тести
pytest -q

# демо
python -m lab2.main --data lab2/sample_data.json --top 3 --boost-city Delhi --factor 1.1

# додаткові перевірки
mypy lab2
black --check lab2
ruff check lab2
```
