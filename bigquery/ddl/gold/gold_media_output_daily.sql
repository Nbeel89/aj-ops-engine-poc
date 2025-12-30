-- gold_media_output_daily
-- Grain: date x dept x platform x content_type
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_media_output_daily` (
  activity_date DATE NOT NULL,
  dept_id STRING NOT NULL,
  platform_id STRING NOT NULL,
  content_type STRING NOT NULL,   -- article/video/program/clip
  content_count INT64,
  breaking_news_count INT64,
  avg_time_to_publish_min FLOAT64,
  corrections_count INT64,
  content_risk_flags INT64,
  generated_at TIMESTAMP
)
PARTITION BY activity_date
CLUSTER BY dept_id, platform_id, content_type
OPTIONS(description="Daily media output metrics by dept/platform/type for Ops Engine POC");
