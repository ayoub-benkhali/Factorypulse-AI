BEGIN;

CREATE TABLE IF NOT EXISTS dw.dim_product (
    product_key  integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id   text NOT NULL UNIQUE,
    product_type text NOT NULL CHECK (product_type IN ('L', 'M', 'H'))
);

CREATE TABLE IF NOT EXISTS dw.dim_tool_wear_band (
    wear_band_key smallint PRIMARY KEY,
    label         text NOT NULL UNIQUE,
    min_minutes   integer NOT NULL,
    max_minutes   integer,
    CHECK (max_minutes IS NULL OR max_minutes > min_minutes)
);

CREATE TABLE IF NOT EXISTS dw.dim_speed_band (
    speed_band_key smallint PRIMARY KEY,
    label          text NOT NULL UNIQUE,
    min_rpm        integer NOT NULL,
    max_rpm        integer,
    CHECK (max_rpm IS NULL OR max_rpm > min_rpm)
);

CREATE TABLE IF NOT EXISTS dw.dim_torque_band (
    torque_band_key smallint PRIMARY KEY,
    label           text NOT NULL UNIQUE,
    min_nm          numeric NOT NULL,
    max_nm          numeric,
    CHECK (max_nm IS NULL OR max_nm > min_nm)
);

CREATE TABLE IF NOT EXISTS dw.dim_temperature_gap_band (
    temperature_gap_band_key smallint PRIMARY KEY,
    label                    text NOT NULL UNIQUE,
    min_gap_k                numeric NOT NULL,
    max_gap_k                numeric,
    CHECK (max_gap_k IS NULL OR max_gap_k > min_gap_k)
);

COMMIT;