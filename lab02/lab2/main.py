from __future__ import annotations

import argparse
import json
from typing import List

from .lab2 import Record, build_pipeline, reduce_stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 2: HOF pipeline demo")
    parser.add_argument("--data", required=True, help="Path to JSON list of records")
    parser.add_argument("--top", type=int, default=3, help="Top-N to take")
    parser.add_argument("--boost-city", default="Delhi", help="City to boost totals for")
    parser.add_argument("--factor", type=float, default=1.1, help="Boost factor")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with open(args.data, "r", encoding="utf-8") as f:
        data: List[Record] = json.load(f)

    pipeline = build_pipeline(top_n=args.top, city=args.boost_city, factor=args.factor)
    top = pipeline(data)
    stats = reduce_stats(top)

    print("Top records:")
    for r in top:
        print(json.dumps(r, ensure_ascii=False))

    print("\nStats:", json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()
