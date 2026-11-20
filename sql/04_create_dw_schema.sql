CREATE SCHEMA IF NOT EXISTS dw;

SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = 'dw';