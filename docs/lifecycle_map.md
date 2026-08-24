**Lifecycle Table**

| Lifecycle Element | What It Means | Example In This Lab | Primary Tool/Artifact | Possible Failure |
| --- | --- | --- | --- | --- |
| Source system | The is where raw data is generated or stored before entering the pipeline. | customers.csv, orders.json, products.parquet, PostgreSQL (support_tickets), REST API (JSONPlaceholder) | data\ directory files, SQL database, external API endpoints | Missing source files, API unavailability, database connection errors, corrupted files |
| Ingestion/Acquisition | Extract raw data from sources and bring it into a system we can control. | fetch_api.py retrieves data from REST API, CSV/JSON file loading, SQL seed_support_tickets.sql import into PostgreSQL | fetch_api.py, inspect_sources.py, docker-compose.yml (PostgreSQL setup) | Network timeouts, malformed JSON/CSV, schema mismatch, authentication issues, duplicate records |
| Storage | This is where the ingested data is stored for optimized access and querying. | data\ directory (raw files), PostgreSQL container, local cache of API responses | docker-compose.yml, PostgreSQL tables, data\raw\ directory | Disk space exhaustion, database connection failures, file permission errors, data corruption |
| Processing/Transformation | Clean, enrich, and restructure raw data into formats suitable for analysis. | inspect_sources.py examines data structure, db_inspect.py queries PostgreSQL, joining multiple datasets | inspect_sources.py, db_inspect.py, config.py | NULL values, data type mismatches, missing joins, duplicates not handled, inconsistent formats |
| Data Quality/Validation | Verify data accuracy, completeness, consistency, and conformance to business rules. | verify_environment.py checks system setup, schema validation against expected structure | verify_environment.py, validation scripts | Data drift, constraint violations, missing required fields, duplicate customer/order IDs |
| Delivery | Package cleaned data in formats ready for consumption or analysis. | Prepared datasets in data\evidence\ directory, normalized tables ready for queries | data\evidence\ directory, SQL views/tables | Format incompatibility, insufficient data for analysis, unmet SLAs, schema changes |
| Consumer | The end user, application, or system that uses the delivered data for decision-making or operations. | Data analysts running queries, BI dashboards, reporting applications | SQL queries, analytics notebooks, business intelligence tools | Incorrect interpretation of data, stale data consumption, missing context/documentation |


<br>

**Diagram**

| Start |  |  |  |  |  | End |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | 
| CSV |  |  |  |  |  |  |
| JSON |  | Data |  |  |  |  |
| Parquet | -->| Processing | --> | Storage | --> | Analyst/Consumer |
| REST API |  | Pipeline |  |  |  |  |
| PostgreSQL |  |  |  |  |  |  |