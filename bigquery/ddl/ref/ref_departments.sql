-- ref_departments
-- Grain: 1 row per department

CREATE TABLE IF NOT EXISTS `ops_engine_poc_ref.ref_departments` (
  dept_id STRING NOT NULL,
  dept_name STRING,
  dept_group STRING,
  cost_center_id STRING,
  org_level INT64,
  is_active BOOL
)
OPTIONS(
  description="Reference departments for Ops Engine POC"
);
