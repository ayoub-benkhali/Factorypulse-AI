CREATE TABLE IF NOT EXISTS dw.fact_machine_observation (
    observation_id integer PRIMARY KEY,

    product_key integer NOT NULL
        REFERENCES dw.dim_product (product_key),
    wear_band_key smallint NOT NULL
        REFERENCES dw.dim_tool_wear_band (wear_band_key),
    speed_band_key smallint NOT NULL
        REFERENCES dw.dim_speed_band (speed_band_key),
    torque_band_key smallint NOT NULL
        REFERENCES dw.dim_torque_band (torque_band_key),
    temperature_gap_band_key smallint NOT NULL
        REFERENCES dw.dim_temperature_gap_band (temperature_gap_band_key),

    air_temp_k           numeric NOT NULL,
    process_temp_k       numeric NOT NULL,
    rotational_speed_rpm integer NOT NULL,
    torque_nm            numeric NOT NULL,
    tool_wear_min        integer NOT NULL,
    machine_failure      smallint NOT NULL CHECK (machine_failure IN (0, 1))
);