-- gold_fin_budget_vs_actual_monthly
-- Grain: month_start_date x cost_center
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_fin_budget_vs_actual_monthly` (
  month_start_date DATE NOT NULL,
  cost_center_id STRING NOT NULL,
  dept_id STRING,
  budget_amount FLOAT64,
  actual_amount FLOAT64,
  variance_amount FLOAT64,
  variance_pct FLOAT64,
  forecast_amount FLOAT64,
  currency STRING,
  generated_at TIMESTAMP
)
PARTITION BY month_start_date
CLUSTER BY cost_center_id, dept_id
OPTIONS(description="Monthly budget vs actual by cost center for Ops Engine POC");
