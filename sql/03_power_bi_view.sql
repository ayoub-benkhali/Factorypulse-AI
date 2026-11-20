CREATE OR REPLACE VIEW public.v_machine_performance AS
SELECT
    observation_id,
    product_id,
    product_type,
    air_temp_k,
    process_temp_k,
    rotational_speed_rpm,
    torque_nm,
    tool_wear_min,
    machine_failure,
    CASE
        WHEN tool_wear_min < 100 THEN '0–99 min'
        WHEN tool_wear_min < 150 THEN '100–149 min'
        WHEN tool_wear_min < 200 THEN '150–199 min'
        ELSE '200 min et plus'
    END AS wear_band,
    CASE
        WHEN tool_wear_min < 100 THEN 1
        WHEN tool_wear_min < 150 THEN 2
        WHEN tool_wear_min < 200 THEN 3
        ELSE 4
    END AS wear_band_order
FROM public.machine_observations;