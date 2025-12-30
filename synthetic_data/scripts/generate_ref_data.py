import yaml
import pandas as pd
from datetime import date

CONFIG_PATH = "synthetic_data/config/poc_config.yaml"
OUTPUT_DIR = "synthetic_data/output"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def generate_calendar(start, end):
    dates = pd.date_range(start=start, end=end)
    df = pd.DataFrame({"calendar_date": dates})
    df["year"] = df.calendar_date.dt.year
    df["quarter"] = df.calendar_date.dt.quarter
    df["month"] = df.calendar_date.dt.month
    df["month_name"] = df.calendar_date.dt.month_name()
    df["week_of_year"] = df.calendar_date.dt.isocalendar().week
    df["day_of_week"] = df.calendar_date.dt.weekday + 1
    df["day_name"] = df.calendar_date.dt.day_name()
    df["is_weekend"] = df.day_of_week >= 6
    return df

def main():
    cfg = load_config()

    start = cfg["date_range"]["start_date"]
    end = cfg["date_range"]["end_date"]

    # Calendar
    calendar_df = generate_calendar(start, end)
    calendar_df.to_csv(f"{OUTPUT_DIR}/ref_calendar.csv", index=False)

    # Departments
    pd.DataFrame(cfg["departments"]).assign(is_active=True) \
        .rename(columns={"id": "dept_id", "name": "dept_name", "group": "dept_group"}) \
        .to_csv(f"{OUTPUT_DIR}/ref_departments.csv", index=False)

    # Platforms
    pd.DataFrame(cfg["platforms"]).assign(is_active=True) \
        .rename(columns={"id": "platform_id", "name": "platform_name", "group": "platform_group"}) \
        .to_csv(f"{OUTPUT_DIR}/ref_channels_platforms.csv", index=False)

    print("REF data generated successfully.")

if __name__ == "__main__":
    main()
