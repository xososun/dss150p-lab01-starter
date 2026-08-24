# Laboratory Reflection

## 1. Easiest source to integrate

The easiest source to integrate into a future pipeline is `products.parquet`. Parquet is a structured, columnar format whose schema and physical data types are stored with the file. That makes it easier to load consistently than CSV, where types must be inferred from text, or JSON, where records may contain different fields and nesting. The product source also has a clear candidate key, `product_id`, and predictable fields such as `category`, `brand`, `unit_price`, `stock_quantity`, and `weight_kg`. Its 200 rows are suitable for batch ingestion and validation. The optional CSV and JSON copies could be used to compare formats and confirm that the logical schema is preserved.

## 2. Greatest risk

The public JSONPlaceholder API presents the greatest combined schema and data-quality risk. It is externally controlled, may be unavailable, and is explicitly a mock service rather than a production source. Its response can change without this team's approval, with risks including payload drift, endpoint deprecation, rate limiting, missing fields, and unstable availability. The JSON order source is also risky because it contains nested `shipping` data and may experience timestamp, status, or numeric-format changes. Among local sources, the customer CSV has direct evidence of quality problems: the data contract reports three duplicate `customer_id` groups and missing `email` and `city` values.

## 3. Consequences of skipping schema and contract analysis

If a pipeline is built before the schema and contract are understood, it may infer identifiers as numbers, discard leading zeros, misread dates, or flatten nested fields incorrectly. Duplicate customers could multiply rows during joins, while null or malformed values could reach reports and decisions. A renamed API field or changed status value could silently produce incomplete output instead of a visible failure. Without agreed freshness, ownership, duplicate handling, and schema-evolution policies, the team cannot reliably distinguish a legitimate source change from a broken load.

## 4. Reproducibility practices

Git preserves code, SQL, documentation, and configuration history, making changes reviewable and recoverable. Virtual environments isolate Python dependencies so team members run compatible package versions without altering system Python. Containers provide a repeatable PostgreSQL version, credentials, port mapping, and data volume across machines. Documentation records prerequisites, commands, source assumptions, and known limitations, allowing another engineer to rebuild the environment and understand not only how to run it, but also why the pipeline behaves as it does.
