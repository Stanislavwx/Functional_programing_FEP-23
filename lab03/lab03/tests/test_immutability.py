from __future__ import annotations

from copy import deepcopy
from typing import Any, cast

import pytest

from lab03.core import add_item, freeze, top_expensive_items
from lab03.model import Item, Order, make_meta


def make_sample_order() -> Order:
    items = (Item("A1", 50.0, 2), Item("B2", 20.0, 1))
    tags = frozenset({"delhi", "priority"})
    meta = make_meta(source="fb_ads", campaign="summer")
    return Order(id=10, paid=False, items=items, tags=tags, meta=meta)


def test_no_mutation_on_add_item() -> None:
    o1 = make_sample_order()
    o1_copy = deepcopy(o1)
    o2 = add_item(o1, "C3", 15.0, 2)

    # original is unchanged
    assert o1 == o1_copy
    # new object returned
    assert o2 is not o1
    # business effect preserved
    assert pytest.approx(o2.subtotal(), rel=1e-9) == o1.subtotal() + 30.0


def test_mappingproxy_is_read_only() -> None:
    o = make_sample_order()
    with pytest.raises(TypeError):
        cast(Any, o.meta)["source"] = "changed"  # MappingProxyType forbids assignment


def test_hashability_and_set_usage() -> None:
    o1 = make_sample_order()
    o2 = add_item(o1, "C3", 15.0, 2)
    orders_set = {o1, o2}
    assert len(orders_set) == 2  # frozen dataclass + hashable fields


def test_tuple_and_frozenset_types() -> None:
    o = make_sample_order()
    assert isinstance(o.items, tuple)
    assert isinstance(o.tags, frozenset)


def test_top_expensive_items() -> None:
    o = make_sample_order()
    top = top_expensive_items(o.items, n=1)
    assert len(top) == 1
    assert top[0].sku == "A1"


def test_freeze_deep() -> None:
    deep = {"a": [1, 2, {"k": {1, 2}}], "b": {"x": 1}}
    f = freeze(deep)
    with pytest.raises(TypeError):
        cast(Any, f["b"])["x"] = 2  # inner mapping is read-only
