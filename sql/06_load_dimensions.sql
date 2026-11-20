BEGIN;

-- Une ligne par produit. PostgreSQL attribue la clé product_key.
INSERT INTO dw.dim_product (product_id, product_type)
SELECT DISTINCT product_id, product_type
FROM public.machine_observations
ON CONFLICT (product_id) DO UPDATE
SET product_type = EXCLUDED.product_type;

-- Pour chaque tranche : minimum inclus, maximum exclu.
-- NULL comme maximum signifie que la tranche reste ouverte.
INSERT INTO dw.dim_tool_wear_band
    (wear_band_key, label, min_minutes, max_minutes)
VALUES
    (1, '0–99 min',         0, 100),
    (2, '100–149 min',    100, 150),
    (3, '150–199 min',    150, 200),
    (4, '200 min et plus', 200, NULL)
ON CONFLICT (wear_band_key) DO NOTHING;

INSERT INTO dw.dim_speed_band
    (speed_band_key, label, min_rpm, max_rpm)
VALUES
    (1, 'Moins de 1 400 tr/min',    0, 1400),
    (2, '1 400 à < 1 600 tr/min', 1400, 1600),
    (3, '1 600 tr/min et plus',   1600, NULL)
ON CONFLICT (speed_band_key) DO NOTHING;

INSERT INTO dw.dim_torque_band
    (torque_band_key, label, min_nm, max_nm)
VALUES
    (1, 'Moins de 30 Nm',  0, 30),
    (2, '30 à < 50 Nm',   30, 50),
    (3, '50 Nm et plus',  50, NULL)
ON CONFLICT (torque_band_key) DO NOTHING;

-- Écart thermique = température du processus moins température de l’air.
INSERT INTO dw.dim_temperature_gap_band
    (temperature_gap_band_key, label, min_gap_k, max_gap_k)
VALUES
    (1, '0 à < 9 K',  0, 9),
    (2, '9 à < 11 K', 9, 11),
    (3, '11 K et plus', 11, NULL)
ON CONFLICT (temperature_gap_band_key) DO NOTHING;

COMMIT;