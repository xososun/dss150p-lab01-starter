# DSS150P Weeks 1-2: Multi-Source Data Inspection Laboratory

## Student information

- Full Name: **Xyl Santos**
- Student Number: **2024107865**

## Purpose

This laboratory introduces inspection of data from multiple source systems before
building a data pipeline. The repository contains flat files, semi-structured JSON,
Parquet, a PostgreSQL table, and a REST API. The exercises identify schemas, data
types, missing values, duplicates, keys, nested fields, and possible data-quality or
schema-evolution risks. The starter code is intentionally incomplete.

## Software requirements

- Windows 10 or later with PowerShell
- Python 3.10 or later
- Docker Desktop with Docker Compose
- Visual Studio Code (recommended)
- Internet access for the public REST API, unless the local fallback is used
- The Python packages listed in `requirements.txt`

## Reproduce the environment

Run these commands from the repository root in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
docker compose up -d
Get-Content .\sql\seed_support_tickets.sql | docker exec -i dss150p-postgres psql -U dss150p -d dss150p_lab
docker exec dss150p-postgres psql -U dss150p -d dss150p_lab -c "SELECT COUNT(*) FROM support_tickets;"
```

The final command should report `250`. If PowerShell blocks script activation,
run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the current
PowerShell window, then activate the environment again.

For the database-aware `src` scripts, set the Docker connection values in the
current PowerShell session because `src/config.py` has different starter defaults:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "5433"
$env:DB_NAME = "dss150p_lab"
$env:DB_USER = "dss150p"
$env:DB_PASSWORD = "dss150p_lab"
```

## Start and stop PostgreSQL

Start the PostgreSQL container:

```powershell
docker compose up -d
```

Stop it while preserving its data volume:

```powershell
docker compose stop postgres
```

Restart it later with `docker compose start postgres`. To stop it and remove the
container and network while retaining the named data volume, use:

```powershell
docker compose down
```

## Run the Python scripts

Run all commands from the repository root with the virtual environment activated.

| Command | Function |
| --- | --- |
| `python src/verify_environment.py` | Checks PostgreSQL connectivity and prints the server version and database name. |
| `python src/inspect_sources.py` | Prints basic CSV and JSON structure information for the customer and order files. |
| `python src/profile_sources.py` | Profiles raw customer, order, and product data: sizes, rows, columns, types, nulls, duplicates, distinct values, samples, numeric ranges, and date ranges. |
| `python src/fetch_api.py` | Fetches JSONPlaceholder `/posts`, saves `data/raw/api_snapshot.json`, and records the UTC retrieval time in `docs/source_inventory.md`. |
| `python src/db_inspect.py` | Connects to PostgreSQL and prints the `support_tickets` row count. Set the `DB_*` variables above first. |
| `python src/local_api_server.py` | Starts the fallback API at `http://localhost:8000/api/orders`; press `Ctrl+C` to stop it. |
| `python fetch_api.py` | Fetches the public API and prints its record count and a sample record. |
| `python inspect_sources.py` | Runs the simpler customer CSV and order JSON inspection in the root-level copy. |
| `python db_inspect.py` | Runs the root-level PostgreSQL row-count check; set the `DB_*` variables above first. |

The root-level scripts are starter copies. The `src` versions are the preferred
entry points because they use paths relative to the repository structure. The
`config.py` and `__init__.py` files provide support and are not standalone scripts.

## Source descriptions

| Source | Description |
| --- | --- |
| `data/customers.csv` | 250-row customer master export with `customer_id`, contact/location fields, signup date, and segment. Missing and duplicate values are deliberate. |
| `data/orders.json` | 250 order records with timestamps, numeric measures such as `total_amount`, categorical values, and a nested `shipping` object. |
| `data/products.parquet` | 200-row product and inventory snapshot with identifiers, categories, brands, prices, quantities, and weights. |
| `data/products_optional_compare.csv` and `data/products_optional_compare.json` | Alternative-format copies of the 200 product rows for format-size and read-performance comparison. |
| `sql/seed_support_tickets.sql` | SQL schema and seed data for the PostgreSQL `support_tickets` table, containing 250 support tickets. |
| JSONPlaceholder `/posts` | Public mock REST API used by `src/fetch_api.py`; normally returns 100 JSON objects. |
| Local `/api/orders` fallback | Standard-library HTTP server backed by `data/orders.json`, returning up to 100 records without authentication or internet access. |

The same raw inputs are also available under `data/raw/` for profiling and API
snapshot work. See `docs/source_inventory.md` for keys, update patterns, and risks.

## Known limitations and unresolved questions

- The repository has no `.env.example`; connection values must be set in the
  PowerShell session as shown above or supplied through another environment file.
- `src/config.py` defaults to port `5432`, database `dss150p`, and password
  `dss150p`, but `docker-compose.yml` uses port `5433`, database `dss150p_lab`,
  and password `dss150p_lab`. The explicit `DB_*` settings are currently required.
- The public API is an external mock service and may be unavailable, change, or
  return data unsuitable for production decisions. The local fallback avoids this
  dependency but serves only the bundled order data.
- The starter inspection scripts do not yet perform complete validation, type
  inference, deduplication, error handling, or pipeline loading.
- It is not yet defined whether `customer_id` and `order_id` are globally unique
  across future extracts, or how incremental changes and late-arriving updates
  should be handled.
- The product comparison files are described as mirrors, but no automated parity
  check currently proves that their rows and values match the Parquet source.
not copy a completed pipeline.

## Included sources
- `data/customers.csv`
- `data/orders.json`
- `data/products.parquet`
- optional `products_optional_compare.csv` and `.json`
- `sql/seed_support_tickets.sql`
- public REST API configured in `src/fetch_api.py`

## Quick start
1. `python -m venv .venv`
2. Activate the virtual environment.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`.
5. `docker compose up -d`
6. Load `sql/seed_support_tickets.sql` into PostgreSQL.
7. Run the starter scripts.
8. Extend the code only as required by the laboratory activity.

The starter files intentionally stop before a complete data pipeline.

## REST API choices
- Public: `https://jsonplaceholder.typicode.com/posts`
- Local fallback: run `python src/local_api_server.py`, then call
  `http://localhost:8000/api/orders`

The local option is useful when your internet access is unreliable.
