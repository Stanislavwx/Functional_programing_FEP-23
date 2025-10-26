# Звіт по ЛР1: Основи функціонального програмування у Python

## Що зроблено
- Реалізовано чисте ядро `core.py` без I/O.
- Додано параметризований конвеєр `make_processor(...)` з прийманням політик як `Callable`.
- Реалізовано зручну обгортку `process_orders_pure(...)`.
- I/O винесено в `app.py`: парсинг аргументів, друк результатів, демо-дані.
- Дотримано принципу референтної прозорості: вхідні дані не мутуються.

## API
### Типи
```py
class Item(TypedDict):
    price: float
    qty: int

class Order(TypedDict, total=False):
    id: int
    paid: bool
    items: List[Item]

class ProcessedOrder(TypedDict):
    id: int
    total: float

class Result(TypedDict):
    count: int
    revenue: float
    orders: List[ProcessedOrder]
```

### Чисті функції
- `subtotal(items)` — сума `price * qty`.
- `accept_min_total_paid(min_total)` — будує фільтр: лише оплачені замовлення з достатнім `subtotal`.
- `apply_discount_rate(rate)` — застосовує знижку.
- `apply_tax_rate(rate)` — застосовує податок.
- `compose(f, g)` — композиція функцій.

### Конвеєр
- `make_processor(accept, apply_discount, apply_tax)` повертає функцію `process(orders) -> Result`.
- `process_orders_pure(orders, *, min_total, discount, tax_rate)` — готова політика: accept=оплачено+поріг, discount/tax — ставки.

## Як працює конвеєр
1. **Фільтрація**: `accept(order)`.
2. **Проміжна сума**: `subtotal(order.items)`.
3. **Знижка → Податок**: `compose(apply_tax, apply_discount)` над gross.
4. **Агрегація**: список `{id, total}` і `revenue = sum(total)`.
5. **Іммутованість**: робимо `deepcopy` вхідних замовлень і не змінюємо їх.

## Перевірка на прикладі
Вхід:
```
id=1: items=[(50×2),(20×1)] subtotal=120 → після 10%:108 → після 20%:129.6
id=2: unpaid → відкидається
id=3: subtotal=90 < 100 → відкидається
```
Результат: `count=1`, `revenue=129.6`, orders=`[{id:1,total:129.6}]`.

## Як запускати
```bash
python app.py --min-total 100 --discount 0.1 --tax 0.2
```
Або без параметрів — усі за замовчуванням 0.

## Тести і типізація
- Тести можна запускати так: `pytest -q` (якщо доступний `pytest`).
- Перевірка типів: `mypy .`
- Форматування: `black .`
- Лінт: `ruff check .`

## Чому це функціональний стиль
- Вся бізнес-логіка в чистих функціях, без побічних ефектів.
- Вся взаємодія зі світом (I/O) в одному місці — `app.py`.
- Параметризація поведінки через передавання функцій.
- Композиція `apply_tax ∘ apply_discount` замість проміжних змінних.

## Як адаптувати під інші політики
- Міняти фільтр: наприклад, приймати не лише `paid`, а ще `id ∈ whitelist`.
- Інша знижка: купон, ступінчата шкала, функція від `subtotal`.
- Інша податкова модель: після знижки чи перед нею, фіксована сума тощо.
- Просто передайте ваші функції у `make_processor(...)`.
