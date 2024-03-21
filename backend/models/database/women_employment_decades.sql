INSERT INTO processed.women_employment_decades
(
    decade,
    women_employment_thousands,
    total_employment_thousands,
    percentage_of_women
)
WITH women_employment AS (
    SELECT
        CAST(FLOOR(year / 10) AS INT) * 10 AS decade,
        AVG(value) AS women_employment_thousands
    FROM landing.ces_series
    WHERE series_id = 'CES9000000010'
    GROUP BY 1
),

total_employment AS (
    SELECT
        CAST(FLOOR(year / 10) AS INT) * 10 AS decade,
        AVG(value) AS total_employment_thousands
    FROM landing.ces_series
    WHERE series_id = 'CES9000000001'
    GROUP BY 1
)

SELECT
    we.decade,
    we.women_employment_thousands,
    te.total_employment_thousands,
    CAST(we.women_employment_thousands AS FLOAT)
    / CAST(te.total_employment_thousands AS FLOAT) AS percentage_of_women
FROM women_employment AS we
INNER JOIN total_employment AS te ON we.decade = te.decade
ON CONFLICT (decade) DO NOTHING;
