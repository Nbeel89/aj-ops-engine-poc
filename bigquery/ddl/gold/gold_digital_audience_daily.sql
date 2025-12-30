-- gold_digital_audience_daily
-- Grain: date x platform
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_digital_audience_daily` (
  activity_date DATE NOT NULL,
  platform_id STRING NOT NULL,
  reach INT64,
  sessions INT64,
  views INT64,
  watch_time_minutes FLOAT64,
  engagement_actions INT64,
  engagement_rate FLOAT64,
  followers_net_change INT64,
  ctr FLOAT64,
  generated_at TIMESTAMP
)
PARTITION BY activity_date
CLUSTER BY platform_id
OPTIONS(description="Daily digital audience KPIs by platform for Ops Engine POC");
