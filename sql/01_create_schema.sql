-- Customer source schema for the laboratory.
-- The table is dropped and recreated so this script can be rerun cleanly.
CREATE SCHEMA IF NOT EXISTS lab;

DROP TABLE IF EXISTS lab.customers;

CREATE TABLE lab.customers (
	customer_id VARCHAR(5) NOT NULL,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(80) NOT NULL,
	email VARCHAR(254),
	city VARCHAR(100),
	signup_date DATE NOT NULL,
	customer_segment VARCHAR(20) NOT NULL,
	CONSTRAINT customers_customer_segment_check
		CHECK (customer_segment IN ('Professional', 'Retail', 'SME', 'Student'))
);

-- customer_id is not a primary key because the source contains duplicate IDs
-- (C0036, C0090, and C0145); no reliable row-level key is provided.

-- Confirm the deployed columns match the definitions above.
WITH expected (ordinal_position, column_name, data_type, character_maximum_length, is_nullable) AS (
	VALUES
		(1, 'customer_id', 'character varying', 5, 'NO'),
		(2, 'first_name', 'character varying', 50, 'NO'),
		(3, 'last_name', 'character varying', 80, 'NO'),
		(4, 'email', 'character varying', 254, 'YES'),
		(5, 'city', 'character varying', 100, 'YES'),
		(6, 'signup_date', 'date', NULL, 'NO'),
		(7, 'customer_segment', 'character varying', 20, 'NO')
), actual AS (
	SELECT ordinal_position, column_name, data_type,
		   character_maximum_length, is_nullable
	FROM information_schema.columns
	WHERE table_schema = 'lab'
	  AND table_name = 'customers'
)
SELECT NOT EXISTS (
	SELECT 1
	FROM expected
	FULL OUTER JOIN actual USING (ordinal_position)
	WHERE expected.column_name IS NULL
	   OR actual.column_name IS NULL
	   OR expected.column_name <> actual.column_name
	   OR expected.data_type <> actual.data_type
	   OR expected.character_maximum_length IS DISTINCT FROM actual.character_maximum_length
	   OR expected.is_nullable <> actual.is_nullable
) AS schema_matches_sql_file;

