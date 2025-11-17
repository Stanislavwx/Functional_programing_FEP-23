# -*- coding: utf-8 -*-

from pathlib import Path
import json, csv

from lab10_etl_core import Raw, Out, Ok, Err, normalize, validate_all, core_pipeline, core_collect

def test_core() -> None:
    demo: list[Raw] = [
        {"name":"   aLiCe  ", "age":"19", "country":" ua ", "email":"Alice@EXAMPLE.com"},
        {"name":"Bob",       "age":"17", "country":" IN",  "email":"bad_at"},
        {"name":"Carol",     "age":"21", "country":"IT",   "email":"c@ex.io"},
        {"name":"EmptyAge",  "age":"  ", "country":"UA",   "email":"fail@example.com"},
    ]
    
    n0_result = normalize(demo[0])
    assert isinstance(n0_result, Ok)
    n0 = n0_result.value
    
    assert n0 == {"name":"Alice","age":19,"country":"UA","email":"alice@example.com"}
    
    assert isinstance(validate_all(n0_result), Ok)
    
    assert isinstance(validate_all(normalize(demo[1])), Err) 
    
    assert isinstance(validate_all(normalize(demo[3])), Err) 

    out = list(core_pipeline(demo))
    assert [r["name"] for r in out] == ["Alice", "Carol"]

def test_io(tmpdir: Path | None = None) -> None:
    base = Path(__file__).resolve().parent
    csv_path = base / "lab10_sample.csv"
    json_path = base / "lab10_sample.json"
    out_csv = base / "lab10_out.csv"
    out_json = base / "lab10_out.json"

    if not csv_path.exists():
        sample_csv_content = """name,age,country,email
 aLiCe ,19, ua ,Alice@EXAMPLE.com
Bob,17, IN,bad_at
Carol,21,IT,c@ex.io
Denis,20,GR,denis@example.gr
, ,UA,empty@example.com"""
        csv_path.write_text(sample_csv_content, encoding="utf-8")
        
    if not json_path.exists():
        sample_json_content = """[
{"name":"Alice","age":"19","country":"UA","email":"alice@example.com"},
{"name":"Bob","age":"17","country":"IN","email":"bad_at"}
]"""
        json_path.write_text(sample_json_content, encoding="utf-8")

    from lab10_etl_io import read_csv, read_json, write_csv, write_json, etl_csv_to_json, etl_json_to_csv

    rows_out = list(core_pipeline(read_csv(csv_path)))
    write_json(out_json, rows_out)
    back = list(read_json(out_json))
    assert out_json.exists() and len(back) >= 1

    etl_json_to_csv(json_path, out_csv)
    assert out_csv.exists()
    
    with open(out_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        hdr = reader.fieldnames or []
        assert set(hdr) == {"name","age","email","segment"}

if __name__ == "__main__":
    test_core()
    try:
        test_io()
        print("✅ Lab 10 tests passed.")
    except Exception as e:
        print(f"❌ Lab 10 tests failed during I/O: {e}")