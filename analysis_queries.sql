-- Run after importing the cleaned CSV into a table named launches.
-- Example: pandas + SQLite can create the table from data/spacex_launches.csv.

-- 1. Outcome distribution
SELECT landing_success, COUNT(*) AS launches
FROM launches
GROUP BY landing_success
ORDER BY landing_success;

-- 2. Landing outcomes by launch site
SELECT launchpad_name,
       COUNT(*) AS known_outcomes,
       SUM(landing_success) AS successful_landings,
       ROUND(100.0 * AVG(landing_success), 1) AS success_rate_pct
FROM launches
WHERE landing_success IS NOT NULL
GROUP BY launchpad_name
HAVING COUNT(*) >= 3
ORDER BY success_rate_pct DESC;

-- 3. Outcomes by year
SELECT launch_year,
       COUNT(*) AS known_outcomes,
       ROUND(100.0 * AVG(landing_success), 1) AS success_rate_pct
FROM launches
WHERE landing_success IS NOT NULL
GROUP BY launch_year
ORDER BY launch_year;

-- 4. Reuse vs outcome (interpret cautiously; selection effects apply)
SELECT core_reused, COUNT(*) AS n,
       ROUND(100.0 * AVG(landing_success), 1) AS success_rate_pct
FROM launches
WHERE landing_success IS NOT NULL
GROUP BY core_reused;
