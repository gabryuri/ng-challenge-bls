INSERT INTO processed.women_employment
(
    date,
    women_employment_thousands,
    total_employment_thousands,
    percentage_of_women
)
WITH women_employment AS (
    SELECT
        value AS women_employment_thousands,
        TO_DATE(
            CAST(year AS TEXT)
            || '-'
            || LPAD(TRIM(LEADING 'M' FROM period), 2, '0'),
            'YYYY-MM'
        ) AS date
    FROM landing.ces_series
    WHERE series_id = 'CES9000000010'
),

total_employment AS (
    SELECT
        value AS total_employment_thousands,
        TO_DATE(
            CAST(year AS TEXT)
            || '-'
            || LPAD(TRIM(LEADING 'M' FROM period), 2, '0'),
            'YYYY-MM'
        ) AS date
    FROM landing.ces_series
    WHERE series_id = 'CES9000000001'
)

SELECT
    we.date,
    we.women_employment_thousands,
    te.total_employment_thousands,
    CAST(we.women_employment_thousands AS FLOAT)
    / CAST(te.total_employment_thousands AS FLOAT) AS percentage_of_women
FROM women_employment AS we
INNER JOIN total_employment AS te ON we.date = te.date
ON CONFLICT (date) DO NOTHING;
