INSERT INTO processed.supervisory_vs_production
(
    decade,
    total_private_production_employees,
    total_supervisory_employees,
    pct_production_employees,
    pct_supervisory_employees
)
WITH base_query AS (
    SELECT
        cast(floor(year) / 10 AS int) * 10 AS decade,
        max(
            CASE WHEN cs.series_id = 'CES0500000001' THEN value END
        ) AS total_private_employees,
        max(
            CASE WHEN cs.series_id = 'CES0500000006' THEN value END
        ) AS total_private_production_employees
    FROM landing.ces_series AS cs INNER
    JOIN landing.series_definitions AS sd
        ON cs.series_id = sd.series_id
    WHERE
        data_type_code IN ('01', '06')
        AND seasonal = 'S'
        AND industry_code IN ('05000000')
        AND period <> 'M13'
    GROUP BY 1
)
SELECT
    decade,
    total_private_production_employees,
    total_private_employees
    - total_private_production_employees AS total_supervisory_employees,
    cast(total_private_production_employees AS float)
    / cast(total_private_employees AS float) AS pct_production_employees,
    cast(total_private_employees - total_private_production_employees AS float)
    / cast(total_private_employees AS float) AS pct_supervisory_employees
FROM base_query
WHERE
    total_private_employees IS NOT null
    AND total_private_production_employees IS NOT null
ORDER BY decade ASC
ON CONFLICT (decade) DO NOTHING;