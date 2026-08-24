| table_scheman	| table_name |
| --- | --- |
| public	| support_tickets |

| column_name | data_typevarchar |	is_nullablevarchar |
| --- | --- | --- |
| ticket_id | 	integer | NO |
| customer_id |	character varying |	NO |
| category |	character varying |	NO |
| priority | 	character varying |	NO |
| assigned_agent | 	character varying	| YES |
| opened_at	| timestamp without time zone	| NO |
| resolved_at |	timestamp without time zone |	YES |
| status | character varying	| NO |

| constraint_name |	constraint_typevarchar |
| --- | --- |
| 2200_16419_1_not_null |	CHECK |
| 2200_16419_2_not_null |	CHECK |
| 2200_16419_3_not_null |	CHECK |
| 2200_16419_4_not_null |   CHECK |
| 2200_16419_6_not_null |	CHECK |
| 2200_16419_8_not_null |	CHECK |
| support_tickets_pkey |	PRIMARY KEY |

| row_count bigint |
| --- |
| 250 |

| ticket_idinteger	| customer_idvarchar |	categoryvarchar |	priorityvarchar |	assigned_agentvarchar |	opened_attimestamp |	resolved_attimestamp |	statusvarchar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |	C0246 |	Technical |	High | 	J. Reyes |	JSON"2026-06-18T20:00:00.000Z" |	JSON"2026-06-21T05:00:00.000Z" |	Resolved |
| 2	| C0130 |	Product	| Medium |	J. Reyes |	JSON"2026-05-25T23:00:00.000Z"	| JSON"2026-05-26T15:00:00.000Z" |	Closed |
| 3	| C0094 |	Delivery | 	Medium | 	J. Reyes |	JSON"2026-03-28T01:00:00.000Z" |	JSON"2026-03-31T09:00:00.000Z"	| Closed |
| 4	| C0057 |	Technical | High |	L. Tan |	JSON"2026-04-25T11:00:00.000Z" |	NULL	| In Progress |
| 5	| C0120 |	Delivery	| High |	R. Cruz |	JSON"2026-01-19T18:00:00.000Z" |	JSON"2026-01-22T13:00:00.000Z" |	Resolved |