
from __future__ import annotations

import argparse

from core import Order, process_orders_pure


def sample_orders() -> list[Order]:
    return [
        {
            "id": 1,
            "paid": True,
            "items": [{"price": 50.0, "qty": 2}, {"price": 20.0, "qty": 1}],
        },
        {"id": 2, "paid": False, "items": [{"price": 200.0, "qty": 1}]},
        {"id": 3, "paid": True, "items": [{"price": 30.0, "qty": 3}]},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-total", type=float, default=100.0)
    parser.add_argument("--discount", type=float, default=0.1)
    parser.add_argument("--tax", type=float, default=0.2)
    args = parser.parse_args()

    result = process_orders_pure(
        sample_orders(),
        min_total=args.min_total,
        discount=args.discount,
        tax_rate=args.tax,
    )

    for o in result["orders"]:
        print(f"Processed id={o['id']} total={o['total']:.2f}")
    print(f"Revenue: {result['revenue']:.2f} Count: {result['count']}")


if __name__ == "__main__":
    main()
