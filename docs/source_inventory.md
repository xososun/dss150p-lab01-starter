# Source Inventory

This inventory catalogs the main sources included in the starter repository and the likely characteristics that matter for ingestion, validation, and downstream pipeline design.

| Source name | Source-system type | Data format | Structured / semi-structured / unstructured | Expected update pattern | Likely acquisition method | Schema location or schema owner | Possible primary/business key | Potential schema-evolution risk | Potential data-quality risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| customers.csv | Customer master data export from a CRM or customer management system | CSV flat file | Structured | Batch refresh; likely nightly or periodic snapshot | File copy/import from local raw data directory | Header row in customers.csv; owner: customer master / CRM team | customer_id | Added or renamed columns, changes to date format, new segmentation categories | Missing values, duplicate customer IDs, inconsistent city/segment naming |
| orders.json | Order management / e-commerce transaction system | JSON document | Semi-structured | Append-only event feed or periodic export; updated as orders are created/fulfilled | Read from raw JSON file or API feed into staging area | Top-level keys in orders.json and nested shipping object; owner: order management system | order_id (primary key), customer_id (business join key) | New nested fields, status changes, timestamp format drift, shipping object schema changes | Missing totals, null or malformed shipping data, duplicate order IDs, inconsistent currency/decimal handling |
| products.parquet | Product catalog / inventory system | Parquet columnar file | Structured | Low-frequency snapshot or scheduled inventory refresh | File-based ETL import from repository data/raw folder | Parquet schema inferred from columns; owner: product/inventory management | product_id | Column additions/removals, type changes in price/quantity/weight, category taxonomy changes | Stale stock counts, missing product names, outlier pricing, rounding issues in weight or unit_price |

## API Retrieval

API retrieval timestamp (UTC): 2026-08-24T14:08:32.333687+00:00

