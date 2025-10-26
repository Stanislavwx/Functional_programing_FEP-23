from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Mapping, NamedTuple, Tuple


class Item(NamedTuple):
    sku: str
    price: float
    qty: int

    @property
    def total(self) -> float:
        return self.price * self.qty


def make_meta(**kwargs: str) -> Mapping[str, str]:
    """Return a read-only mapping for metadata."""
    return MappingProxyType(dict(kwargs))


@dataclass(frozen=True, slots=True)
class Order:
    id: int
    paid: bool
    items: Tuple[Item, ...]
    tags: frozenset[str]
    # exclude meta from hashing/eq; MappingProxyType isn't hashable
    meta: Mapping[str, str] = field(compare=False, hash=False)

    def __deepcopy__(self, memo: dict[int, Any]) -> "Order":
        """Custom deepcopy to support MappingProxyType in meta on Python 3.13."""
        new_meta = MappingProxyType(dict(self.meta))
        new_obj = Order(id=self.id, paid=self.paid, items=self.items, tags=self.tags, meta=new_meta)
        memo[id(self)] = new_obj
        return new_obj

    # ---- pure methods: return NEW Order instances ----

    def subtotal(self) -> float:
        return sum(i.total for i in self.items)

    def add_tag(self, tag: str) -> "Order":
        return replace(self, tags=self.tags | frozenset({tag}))

    def with_item(self, item: Item) -> "Order":
        return replace(self, items=self.items + (item,))

    def pay(self) -> "Order":
        return self if self.paid else replace(self, paid=True)

    def with_meta(self, **patch: str) -> "Order":
        merged = dict(self.meta)
        merged.update(patch)
        return replace(self, meta=MappingProxyType(merged))
