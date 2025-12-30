-- gold_exec_daily
-- Grain: 1 row per date
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_exec_daily` (
  snapshot_date DATE NOT NULL,
  org_rag STRING,
  media_rag STRING,
  hr_rag STRING,
  finance_rag STRING,
  tech_rag STRING,
  risk_rag STRING,

  media_output_total INT64,
  broadcast_adherence_pct FLOAT64,
  digital_reach_total INT64,
  digital_engagement_rate FLOAT64,

  headcount_total INT64,
  attrition_30d INT64,
  overtime_hours_total FLOAT64,

  spend_actual_mtd FLOAT64,
  budget_mtd FLOAT64,
  budget_variance_mtd FLOAT64,

  open_exceptions_count INT64,
  executive_summary STRING,
  generated_at TIMESTAMP
)
PARTITION BY snapshot_date
OPTIONS(description="Executive daily snapshot for Ops Engine POC control tower");
