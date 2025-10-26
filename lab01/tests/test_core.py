from __future__ import annotations

from copy import deepcopy

import pytest

import core


@pytest.fixture()
def sample_orders() -> list[core.Order]:
    return [
        {
            "id": 1,
            "paid": True,
            "items": [{"price": 50.0, "qty": 2}, {"price": 20.0, "qty": 1}],
        },  # subtotal 120
        {"id": 2, "paid": False, "items": [{"price": 200.0, "qty": 1}]},  # unpaid
        {"id": 3, "paid": True, "items": [{"price": 30.0, "qty": 3}]},  # subtotal 90
    ]


def test_referential_transparency(sample_orders: list[core.Order]) -> None:
    args = dict(min_total=100, discount=0.1, tax_rate=0.2)
    r1 = core.process_orders_pure(sample_orders, **args)
    r2 = core.process_orders_pure(sample_orders, **args)
    assert r1 == r2  # той самий вхід → той самий вихід


def test_no_mutation(sample_orders: list[core.Order]) -> None:
    original = deepcopy(sample_orders)
    core.process_orders_pure(sample_orders, min_total=0, discount=0.0, tax_rate=0.0)
    assert sample_orders == original  # вхід не змінюється


def test_callable_policies(sample_orders: list[core.Order]) -> None:
    # accept: лише замовлення з subtotal >= 100
    accept = lambda s: s >= 100
    # 10% знижка
    apply_discount = lambda s: s * 0.9
    # 20% податок
    apply_tax = lambda a: a * 1.2

    processor = core.make_processor(
        accept=accept, apply_discount=apply_discount, apply_tax=apply_tax
    )
    result = processor(sample_orders)

    # Ручний розрахунок: тільки order id=1 (subtotal 120)
    # після знижки 10% -> 108, після податку 20% -> 129.6
    assert result["count"] == 1
    assert pytest.approx(result["revenue"], rel=1e-9) == 129.6
    assert isinstance(result["orders"], list)
    assert result["orders"][0]["id"] == 1
    assert pytest.approx(result["orders"][0]["total"], rel=1e-9) == 129.6
