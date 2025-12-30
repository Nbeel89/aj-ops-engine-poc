-- gold_hr_workforce_daily
-- Grain: date x dept
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_hr_workforce_daily` (
  snapshot_date DATE NOT NULL,
  dept_id STRING NOT NULL,
  headcount INT64,
  joiners_7d INT64,
  leavers_7d INT64,
  leavers_30d INT64,
  attrition_rate_30d FLOAT64,
  absence_rate FLOAT64,
  overtime_hours FLOAT64,
  open_positions INT64,
  generated_at TIMESTAMP
)
PARTITION BY snapshot_date
CLUSTER BY dept_id
OPTIONS(description="Daily HR workforce KPIs by dept for Ops Engine POC");
