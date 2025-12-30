# IAM Notes - Al Jazeera Ops Engine (POC)

## Recommended minimal roles (POC owner / data engineer)
Project-level:
- BigQuery Job User

Dataset-level (ops_engine_poc_ref, ops_engine_poc_gold):
- BigQuery Data Editor

Optional (if using GCS staging for loads):
- Storage Object Admin (POC bucket only)

## Notes
- Keep HR/Finance POC data synthetic until approvals for real extracts.
- Prefer separate project for clean cost tracking and IAM isolation.
