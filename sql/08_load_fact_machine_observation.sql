INSERT INTO dw.fact_machine_observation (
    observation_id, product_key, wear_band_key, speed_band_key,
    torque_band_key, temperature_gap_band_key,
    air_temp_k, process_temp_k, rotational_speed_rpm,
    torque_nm, tool_wear_min, machine_failure
)
SELECT
    s.observation_id,

    (SELECT p.product_key
     FROM dw.dim_product AS p
     WHERE p.product_id = s.product_id),

    (SELECT w.wear_band_key
     FROM dw.dim_tool_wear_band AS w
     WHERE s.tool_wear_min >= w.min_minutes
       AND (s.tool_wear_min < w.max_minutes OR w.max_minutes IS NULL)),

    (SELECT v.speed_band_key
     FROM dw.dim_speed_band AS v
     WHERE s.rotational_speed_rpm >= v.min_rpm
       AND (s.rotational_speed_rpm < v.max_rpm OR v.max_rpm IS NULL)),

    (SELECT t.torque_band_key
     FROM dw.dim_torque_band AS t
     WHERE s.torque_nm >= t.min_nm
       AND (s.torque_nm < t.max_nm OR t.max_nm IS NULL)),

    (SELECT g.temperature_gap_band_key
     FROM dw.dim_temperature_gap_band AS g
     WHERE (s.process_temp_k - s.air_temp_k) >= g.min_gap_k
       AND ((s.process_temp_k - s.air_temp_k) < g.max_gap_k
            OR g.max_gap_k IS NULL)),

    s.air_temp_k, s.process_temp_k, s.rotational_speed_rpm,
    s.torque_nm, s.tool_wear_min, s.machine_failure
FROM public.machine_observations AS s
ON CONFLICT (observation_id) DO UPDATE SET
    product_key              = EXCLUDED.product_key,
    wear_band_key            = EXCLUDED.wear_band_key,
    speed_band_key           = EXCLUDED.speed_band_key,
    torque_band_key          = EXCLUDED.torque_band_key,
    temperature_gap_band_key = EXCLUDED.temperature_gap_band_key,
    air_temp_k               = EXCLUDED.air_temp_k,
    process_temp_k           = EXCLUDED.process_temp_k,
    rotational_speed_rpm     = EXCLUDED.rotational_speed_rpm,
    torque_nm                = EXCLUDED.torque_nm,
    tool_wear_min            = EXCLUDED.tool_wear_min,
    machine_failure          = EXCLUDED.machine_failure;