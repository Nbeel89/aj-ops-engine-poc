-- gold_hr_hiring_weekly
-- Grain: week_start_date x dept
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_hr_hiring_weekly` (
  week_start_date DATE NOT NULL,
  dept_id STRING NOT NULL,
  requisitions_open INT64,
  applications_received INT64,
  interviews_completed INT64,
  offers_made INT64,
  offers_accepted INT64,
  avg_time_to_fill_days FLOAT64,
  generated_at TIMESTAMP
)
PARTITION BY week_start_date
CLUSTER BY dept_id
OPTIONS(description="Weekly hiring pipeline KPIs by dept for Ops Engine POC");
