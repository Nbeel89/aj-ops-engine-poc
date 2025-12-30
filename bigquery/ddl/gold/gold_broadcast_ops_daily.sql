-- gold_broadcast_ops_daily
-- Grain: date x channel_name
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_broadcast_ops_daily` (
  activity_date DATE NOT NULL,
  channel_name STRING NOT NULL,
  scheduled_minutes INT64,
  aired_minutes INT64,
  adherence_pct FLOAT64,
  late_start_count INT64,
  overrun_count INT64,
  incident_count INT64,
  sev1_incident_count INT64,
  generated_at TIMESTAMP
)
PARTITION BY activity_date
CLUSTER BY channel_name
OPTIONS(description="Daily broadcast operations KPIs for Ops Engine POC");
