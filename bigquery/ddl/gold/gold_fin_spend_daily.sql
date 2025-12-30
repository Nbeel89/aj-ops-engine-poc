-- gold_fin_spend_daily
-- Grain: date x cost_center x spend_category
CREATE TABLE IF NOT EXISTS `ops_engine_poc_gold.gold_fin_spend_daily` (
  spend_date DATE NOT NULL,
  cost_center_id STRING NOT NULL,
  dept_id STRING,
  spend_category STRING,  -- payroll/capex/opex/travel/vendors
  spend_amount FLOAT64,
  invoice_count INT64,
  vendor_count INT64,
  generated_at TIMESTAMP
)
PARTITION BY spend_date
CLUSTER BY cost_center_id, spend_category
OPTIONS(description="Daily spend trend by cost center/category for Ops Engine POC");
