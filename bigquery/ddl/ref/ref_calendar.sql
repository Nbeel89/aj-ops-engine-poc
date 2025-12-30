-- ref_calendar
-- Grain: 1 row per calendar date

CREATE TABLE IF NOT EXISTS `ops_engine_poc_ref.ref_calendar` (
  calendar_date DATE NOT NULL,
  year INT64,
  quarter INT64,
  month INT64,
  month_name STRING,
  week_of_year INT64,
  day_of_week INT64,
  day_name STRING,
  is_weekend BOOL,
  fiscal_year INT64,
  fiscal_period INT64
)
OPTIONS(
  description="Reference calendar table for Ops Engine POC"
);
