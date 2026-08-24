## Source profile

### `customers.csv`

- Treat the customer identifier as a candidate business key, but validate uniqueness before using it for joins; repeated IDs would multiply rows downstream.
- CSV types are not self-describing, so parse identifiers as strings (to preserve leading zeroes) and explicitly coerce numeric fields. Blank values should remain null rather than being treated as zero or the string `"null"`.

### `orders.json`

- JSON may contain nested objects or arrays (for example, line items), so normalize those structures into related tables instead of flattening them into a single ambiguous row.
- Order IDs and customer IDs should be checked for missing or duplicate values, and references should be validated against the customer source before joining.
- Parse order dates explicitly and standardize timezone and representation; do not assume that all records use the same date format.

### `products.parquet`

- Parquet preserves physical types, but the product identifier still needs a uniqueness check before it is treated as a dimension key; duplicate products can create many-to-many joins.
- Preserve nullable columns and inspect the stored schema before casting. In particular, distinguish numeric measures from categorical codes and avoid converting missing values to defaults without a business rule.
