-- ref_kpi_thresholds
-- Grain: 1 row per KPI per scope

CREATE TABLE IF NOT EXISTS `ops_engine_poc_ref.ref_kpi_thresholds` (
  kpi_id STRING NOT NULL,
  kpi_name STRING,
  scope_type STRING,   -- global / dept / platform
  scope_id STRING,     -- nullable for global
  green_min FLOAT64,
  green_max FLOAT64,
  amber_min FLOAT64,
  amber_max FLOAT64,
  red_min FLOAT64,
  red_max FLOAT64,
  direction STRING,    -- higher_is_better / lower_is_better
  unit STRING
)
OPTIONS(
  description="Reference KPI thresholds for RAG evaluation in Ops Engine POC"
);
