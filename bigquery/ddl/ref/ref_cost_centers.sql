-- ref_cost_centers
-- Grain: 1 row per cost center

CREATE TABLE IF NOT EXISTS `ops_engine_poc_ref.ref_cost_centers` (
  cost_center_id STRING NOT NULL,
  cost_center_name STRING,
  function_group STRING,
  owner_dept_id STRING,
  is_active BOOL
)
OPTIONS(
  description="Reference cost centers for Ops Engine POC"
);
