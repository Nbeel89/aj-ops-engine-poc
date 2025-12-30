-- Al Jazeera Ops Engine (POC)
-- Project: aj-ops-engine-poc   -- TODO: replace with your actual project_id
-- Region/Location: <YOUR_BQ_LOCATION>  -- TODO: set once confirmed

-- Create datasets (run after project is created).
-- NOTE: BigQuery dataset location cannot be changed after creation.

CREATE SCHEMA IF NOT EXISTS `aj-ops-engine-poc.ops_engine_poc_ref`
OPTIONS(
  location="<YOUR_BQ_LOCATION>",
  description="Ops Engine POC - reference/dimension tables (calendar, departments, platforms, KPI thresholds)"
);

CREATE SCHEMA IF NOT EXISTS `aj-ops-engine-poc.ops_engine_poc_gold`
OPTIONS(
  location="<YOUR_BQ_LOCATION>",
  description="Ops Engine POC - gold executive-ready fact tables consumed by Looker"
);
