-- ref_channels_platforms
-- Grain: 1 row per platform/channel

CREATE TABLE IF NOT EXISTS `ops_engine_poc_ref.ref_channels_platforms` (
  platform_id STRING NOT NULL,
  platform_name STRING,
  platform_group STRING,
  region STRING,
  language STRING,
  is_active BOOL
)
OPTIONS(
  description="Reference platforms/channels for Ops Engine POC"
);
