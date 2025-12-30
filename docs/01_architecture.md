# Architecture (POC) - Al Jazeera Ops Engine

## Overview
The POC provides executive dashboards in Looker for:
- Control Tower (Executive landing page)
- Media Operations
- HR & Workforce
- Finance & Spend
- (Optional) Data Health

## Data Approach
- BigQuery hosts POC datasets.
- Initial data is synthetic but realistic.
- Gold tables are pre-aggregated for fast Looker performance.

## BigQuery Datasets
- ops_engine_poc_ref  : reference/dimension tables (calendar, departments, platforms, KPI thresholds)
- ops_engine_poc_gold : executive-ready fact tables (daily/weekly/monthly grains)

## Core Flow
Synthetic Generator → BigQuery (REF + GOLD) → Looker (LookML explores) → Dashboards
