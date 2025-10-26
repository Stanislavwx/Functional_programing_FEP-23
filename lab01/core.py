from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict


# === Типи даних ===============================================================

class Item(TypedDict):
    price: float
    qty: int


class Order(TypedDict):
    id: int
    items: list[Item]
    paid: bool


class ProcessedOrder(TypedDict):
    id: int
    total: float


class Result(TypedDict):
    orders: list[ProcessedOrder]
    revenue: float
    count: int


# === Чисті утиліти ============================================================

def subtotal(order: Order) -> float:
    """Сума по товарах (без знижок і податків)."""
    return sum(item["price"] * item["qty"] for item in order["items"])


# === Будівники політик (higher-order functions) ===============================

def accept_min_total(min_total: float) -> Callable[[float], bool]:
    """Приймати замовлення з subtotal ≥ min_total."""
    return lambda s: s >= min_total


def apply_discount_rate(rate: float) -> Callable[[float], float]:
    """Знижка rate (0.1 = 10%)."""
    def _apply(s: float) -> float:
        return s * (1 - rate)
    return _apply


def apply_tax_rate(rate: float) -> Callable[[float], float]:
    """Податок rate (0.2 = 20%)."""
    def _apply(a: float) -> float:
        return a * (1 + rate)
    return _apply


# === Конвеєр обробки ==========================================================

def make_processor(
    accept: Callable[[float], bool],
    apply_discount: Callable[[float], float],
    apply_tax: Callable[[float], float],
) -> Callable[[list[Order]], Result]:
    """
    Повертає чисту функцію process(orders) -> Result.

    Ланцюжок:
      1) тільки оплачені замовлення;
      2) subtotal;
      3) accept(subtotal);
      4) знижка → податок;
      5) підсумок revenue і count.
    """
    def process(orders: list[Order]) -> Result:
        processed: list[ProcessedOrder] = []

        for o in orders:
            if not o.get("paid"):
                continue

            s = subtotal(o)
            if not accept(s):
                continue

            total = apply_tax(apply_discount(s))
            processed.append({"id": o["id"], "total": total})

        revenue = sum(p["total"] for p in processed)
        return {"orders": processed, "revenue": revenue, "count": len(processed)}

    return process


# === Зручна обгортка (типова політика) ========================================

def process_orders_pure(
    orders: list[Order],
    *,
    min_total: float,
    discount: float,
    tax_rate: float,
) -> Result:
    """Готова конфігурація конвеєра під методичку."""
    processor = make_processor(
        accept=accept_min_total(min_total),
        apply_discount=apply_discount_rate(discount),
        apply_tax=apply_tax_rate(tax_rate),
    )
    return processor(orders)
