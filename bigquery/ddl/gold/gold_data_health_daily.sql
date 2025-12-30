-- gold_data_health_daily
-- Grain: date x table_name
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_data_health_daily` (
  snapshot_date DATE NOT NULL,
  table_name STRING NOT NULL,
  last_refresh_ts TIMESTAMP,
  expected_refresh_sla_hours INT64,
  freshness_status STRING,    -- green/amber/red
  row_count INT64,
  row_count_delta_pct FLOAT64,
  null_key_pct FLOAT64,
  dq_status STRING,           -- pass/warn/fail
  dq_notes STRING,
  generated_at TIMESTAMP
)
PARTITION BY snapshot_date
CLUSTER BY table_name, freshness_status
OPTIONS(description="Daily data health metrics for Ops Engine POC");
