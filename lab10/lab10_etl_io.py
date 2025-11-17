# -*- coding: utf-8 -*-
"""
Лабораторна 10 — Шар I/O
Файл: lab10_etl_io.py (читання/запис + склеювання з PURE CORE)

Залежить від: lab10_etl_core.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Iterable, List
import csv, json

from lab10_etl_core import Raw, Out, core_pipeline, core_collect

# ---------- Читання ----------

def read_csv(path: str | Path) -> Iterator[Raw]:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                "name": row.get("name",""),
                "age": row.get("age",""),
                "country": row.get("country",""),
                "email": row.get("email",""),
            }

def read_json(path: str | Path) -> Iterator[Raw]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for row in data:
        yield {
            "name": str(row.get("name","")),
            "age": str(row.get("age","")),
            "country": str(row.get("country","")),
            "email": str(row.get("email","")),
        }

# ---------- Запис ----------

def write_csv(path: str | Path, rows: Iterable[Out]) -> None:
    fields = ["name","age","email","segment"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def write_json(path: str | Path, rows: Iterable[Out]) -> None:
    data = list(rows)  # матеріалізуємо тільки на краю
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------- Повні ETL-обгортки ----------

def etl_csv_to_json(src_csv: str | Path, dst_json: str | Path) -> None:
    write_json(dst_json, core_pipeline(read_csv(src_csv)))

def etl_json_to_csv(src_json: str | Path, dst_csv: str | Path) -> None:
    write_csv(dst_csv, core_pipeline(read_json(src_json)))

# ---------- Демо ----------

def _demo(src_csv: str | Path, dst_json: str | Path) -> None:
    print(f"ETL CSV → JSON: {src_csv} → {dst_json}")
    etl_csv_to_json(src_csv, dst_json)
    print("Done.")

if __name__ == "__main__":
    # Невеличка демонстрація на файлах з каталогу /mnt/data
    base = Path(__file__).resolve().parent
    sample_csv = base / "lab10_sample.csv"
    out_json = base / "lab10_out.json"
    if sample_csv.exists():
        _demo(sample_csv, out_json)
        print(f"Результат записано в: {out_json}")
    else:
        print("Зразок CSV не знайдено. Спочатку згенеруйте його (див. ноутбук або скрипт створення).")
