from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

customers = pd.read_csv(RAW / "customers.csv")
orders = pd.read_json(RAW / "orders.json")
products = pd.read_parquet(RAW / "products.parquet")


def make_hashable(value):
    if isinstance(value, (dict, list, set, tuple)):
        return json.dumps(value, sort_keys=True, default=str)
    return value


for name, df in {
    "customers.csv": customers,
    "orders.json": orders,
    "products.parquet": products,
}.items():
    path = RAW / name
    print(f"\n=== {name} ===")
    print("file size (bytes):", path.stat().st_size)
    print("rows:", len(df))
    print("columns:", len(df.columns))
    print("column names:", list(df.columns))
    print("inferred data types:")
    for column in df.columns:
        print(f"  {column}: {df[column].dtype}")
    print("missing/null values per column:")
    for column in df.columns:
        print(f"  {column}: {df[column].isna().sum()}")
    hashable_df = df.apply(lambda column: column.map(make_hashable))
    print("fully duplicated rows:", hashable_df.duplicated().sum())
    print("distinct values per column:")
    for column in df.columns:
        print(f"  {column}: {hashable_df[column].nunique(dropna=False)}")

    print("first five records:")
    print(df.head(5).to_string(index=False))

    numeric_columns = df.select_dtypes(include="number").columns
    if len(numeric_columns):
        print("numeric minimum and maximum values:")
        for column in numeric_columns:
            print(f"  {column}: min={df[column].min()}, max={df[column].max()}")

    date_columns = [
        column
        for column in df.columns
        if pd.api.types.is_datetime64_any_dtype(df[column])
        or any(part in str(column).lower() for part in ("date", "time", "timestamp"))
    ]
    if date_columns:
        print("date/time earliest and latest values:")
        for column in date_columns:
            parsed = pd.to_datetime(df[column], errors="coerce", format="mixed")
            valid = parsed.dropna()
            if valid.empty:
                print(f"  {column}: no safely parsed values")
            else:
                print(f"  {column}: earliest={valid.min()}, latest={valid.max()}")