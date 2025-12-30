-- gold_exceptions
-- Grain: 1 row per exception/alert
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_exceptions` (
  exception_id STRING NOT NULL,
  event_ts TIMESTAMP,
  event_date DATE,
  domain STRING,          -- media/hr/finance/tech/risk
  severity STRING,        -- sev1/sev2/sev3
  status STRING,          -- open/ack/closed
  title STRING,
  description STRING,
  kpi_id STRING,
  observed_value FLOAT64,
  expected_value FLOAT64,
  threshold_band STRING,  -- green/amber/red
  owner_role STRING,
  owner_dept_id STRING,
  platform_id STRING,
  link_url STRING,
  created_at TIMESTAMP
)
PARTITION BY event_date
CLUSTER BY domain, severity, status
OPTIONS(description="Exceptions/alerts for Ops Engine POC control tower");
