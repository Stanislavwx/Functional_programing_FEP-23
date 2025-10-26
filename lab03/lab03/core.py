from __future__ import annotations

from collections.abc import Mapping as ABMapping
from types import MappingProxyType
from typing import Any, Sequence, Tuple

from .model import Item, Order


# ---- pure update functions (no in-place mutation) ----
def add_item(order: Order, sku: str, price: float, qty: int) -> Order:
    return order.with_item(Item(sku, price, qty))


def add_tag(order: Order, tag: str) -> Order:
    return order.add_tag(tag)


def pay(order: Order) -> Order:
    return order.pay()


# ---- read helpers ----
def top_expensive_items(items: Sequence[Item], n: int = 3) -> Tuple[Item, ...]:
    return tuple(sorted(items, key=lambda i: i.total, reverse=True)[:n])


# ---- optional: deep freeze utility ----
def freeze(obj: Any) -> Any:
    """Deep-freeze: Mapping→MappingProxyType; set→frozenset; list/tuple→tuple."""
    if isinstance(obj, ABMapping):
        frozen_inner = {k: freeze(v) for k, v in obj.items()}
        return MappingProxyType(frozen_inner)
    if isinstance(obj, set):
        return frozenset(freeze(x) for x in obj)
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(x) for x in obj)
    return obj
