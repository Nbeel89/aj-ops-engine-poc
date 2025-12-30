import os
import yaml
import subprocess

CONFIG_PATH = "synthetic_data/config/poc_config.yaml"
DATA_DIR = "synthetic_data/output"

REF_TABLES = {
    "ref_calendar.csv": "ops_engine_poc_ref.ref_calendar",
    "ref_departments.csv": "ops_engine_poc_ref.ref_departments",
    "ref_channels_platforms.csv": "ops_engine_poc_ref.ref_channels_platforms",
}

GOLD_TABLES = {
    "gold_media_output_daily.csv": "ops_engine_poc_gold.gold_media_output_daily",
    "gold_broadcast_ops_daily.csv": "ops_engine_poc_gold.gold_broadcast_ops_daily",
    "gold_digital_audience_daily.csv": "ops_engine_poc_gold.gold_digital_audience_daily",
    "gold_hr_workforce_daily.csv": "ops_engine_poc_gold.gold_hr_workforce_daily",
    "gold_hr_hiring_weekly.csv": "ops_engine_poc_gold.gold_hr_hiring_weekly",
    "gold_fin_budget_vs_actual_monthly.csv": "ops_engine_poc_gold.gold_fin_budget_vs_actual_monthly",
    "gold_fin_spend_daily.csv": "ops_engine_poc_gold.gold_fin_spend_daily",
    "gold_data_health_daily.csv": "ops_engine_poc_gold.gold_data_health_daily",
    "gold_exceptions.csv": "ops_engine_poc_gold.gold_exceptions",
    "gold_exec_daily.csv": "ops_engine_poc_gold.gold_exec_daily",
}

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def run(cmd):
    print(" ".join(cmd))
    subprocess.check_call(cmd)

def load_csv_to_bq(project_id, location, csv_path, table):
    run([
        "bq", "load",
        "--project_id", project_id,
        "--location", location,
        "--source_format=CSV",
        "--skip_leading_rows=1",
        "--replace",
        table,
        csv_path
    ])

def main():
    cfg = load_config()
    project_id = cfg["project_id"]
    location = cfg["bq_location"]

    print("== Loading REF tables ==")
    for csv, table in REF_TABLES.items():
        path = os.path.join(DATA_DIR, csv)
        if os.path.exists(path):
            load_csv_to_bq(project_id, location, path, table)
        else:
            print(f"Missing file: {path}")

    print("\n== Loading GOLD tables ==")
    for csv, table in GOLD_TABLES.items():
        path = os.path.join(DATA_DIR, csv)
        if os.path.exists(path):
            load_csv_to_bq(project_id, location, path, table)
        else:
            print(f"Missing file: {path}")

    print("\nAll tables loaded successfully.")

if __name__ == "__main__":
    main()
