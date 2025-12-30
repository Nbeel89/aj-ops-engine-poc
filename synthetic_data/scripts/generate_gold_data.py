import yaml
import numpy as np
import pandas as pd
from datetime import datetime

CONFIG_PATH = "synthetic_data/config/poc_config.yaml"
OUTPUT_DIR = "synthetic_data/output"

CONTENT_TYPES = ["article", "video", "program", "clip"]
FIN_CATEGORIES = ["payroll", "opex", "capex", "travel", "vendors"]
CHANNELS = ["AJE", "AJ Arabic", "AJ Documentary"]

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def daterange(start_date: str, end_date: str):
    return pd.date_range(start=start_date, end=end_date, freq="D")

def month_starts(start_date: str, end_date: str):
    return pd.date_range(start=start_date, end=end_date, freq="MS")

def week_starts(start_date: str, end_date: str):
    return pd.date_range(start=start_date, end=end_date, freq="W-MON")

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def rag_from_value(value, green_min=None, green_max=None, amber_min=None, amber_max=None, direction="higher_is_better"):
    # Simple rule-based RAG
    # If higher is better: green >= green_min; amber >= amber_min; else red
    # If lower is better: green <= green_max; amber <= amber_max; else red
    if direction == "higher_is_better":
        if green_min is not None and value >= green_min:
            return "green"
        if amber_min is not None and value >= amber_min:
            return "amber"
        return "red"
    else:
        if green_max is not None and value <= green_max:
            return "green"
        if amber_max is not None and value <= amber_max:
            return "amber"
        return "red"

def main():
    cfg = load_config()
    np.random.seed(cfg.get("random_seed", 42))

    start = cfg["date_range"]["start_date"]
    end = cfg["date_range"]["end_date"]
    currency = cfg.get("currency", "QAR")

    depts = pd.DataFrame(cfg["departments"]).rename(columns={"id": "dept_id", "name": "dept_name", "group": "dept_group"})
    plats = pd.DataFrame(cfg["platforms"]).rename(columns={"id": "platform_id", "name": "platform_name", "group": "platform_group"})
    cost_centers = pd.DataFrame(cfg["cost_centers"]).rename(columns={"id": "cost_center_id", "name": "cost_center_name"})

    days = daterange(start, end)
    months = month_starts(start, end)
    weeks = week_starts(start, end)

    generated_at = pd.Timestamp.utcnow()

    # -------------------------
    # 1) gold_media_output_daily
    # -------------------------
    media_rows = []
    for d in days:
        day_factor = 1.0 + 0.15 * np.sin(2 * np.pi * (d.dayofyear / 365.0))
        breaking_spike = 1 if np.random.rand() < 0.03 else 0  # ~3% days are "breaking spikes"
        spike_factor = 1.8 if breaking_spike else 1.0

        for _, dept in depts.iterrows():
            for _, plat in plats.iterrows():
                for ct in CONTENT_TYPES:
                    base = 40 if ct == "article" else 18 if ct == "video" else 6 if ct == "program" else 12
                    dept_mult = 1.4 if dept["dept_id"] in ["news", "digital"] else 1.0
                    plat_mult = 1.3 if plat["platform_id"] in ["web", "app"] else 1.1 if plat["platform_id"] in ["youtube"] else 0.9
                    noise = np.random.normal(0, 4)
                    count = int(max(0, (base * dept_mult * plat_mult * day_factor * spike_factor) + noise))

                    media_rows.append({
                        "activity_date": d.date(),
                        "dept_id": dept["dept_id"],
                        "platform_id": plat["platform_id"],
                        "content_type": ct,
                        "content_count": count,
                        "breaking_news_count": int(breaking_spike * np.random.randint(1, 6)) if ct == "article" else 0,
                        "avg_time_to_publish_min": float(clamp(np.random.normal(35 if breaking_spike else 55, 12), 10, 180)),
                        "corrections_count": int(max(0, np.random.poisson(0.2 if breaking_spike else 0.1))),
                        "content_risk_flags": int(max(0, np.random.poisson(0.3 if breaking_spike else 0.15))),
                        "generated_at": generated_at
                    })

    gold_media_output_daily = pd.DataFrame(media_rows)
    gold_media_output_daily.to_csv(f"{OUTPUT_DIR}/gold_media_output_daily.csv", index=False)

    # -------------------------
    # 2) gold_broadcast_ops_daily
    # -------------------------
    broadcast_rows = []
    for d in days:
        for ch in CHANNELS:
            scheduled = 24 * 60
            # adherence slightly worse on incident days
            incident = 1 if np.random.rand() < 0.05 else 0
            adherence = clamp(np.random.normal(98.5 - (1.8 if incident else 0), 0.8), 90.0, 100.0)
            aired = int(scheduled * (adherence / 100.0))

            broadcast_rows.append({
                "activity_date": d.date(),
                "channel_name": ch,
                "scheduled_minutes": scheduled,
                "aired_minutes": aired,
                "adherence_pct": float(adherence),
                "late_start_count": int(max(0, np.random.poisson(1.0 + (2.0 if incident else 0)))),
                "overrun_count": int(max(0, np.random.poisson(0.8 + (1.5 if incident else 0)))),
                "incident_count": int(incident * np.random.randint(1, 4)),
                "sev1_incident_count": int(incident and (np.random.rand() < 0.25)),
                "generated_at": generated_at
            })

    gold_broadcast_ops_daily = pd.DataFrame(broadcast_rows)
    gold_broadcast_ops_daily.to_csv(f"{OUTPUT_DIR}/gold_broadcast_ops_daily.csv", index=False)

    # -------------------------
    # 3) gold_digital_audience_daily
    # -------------------------
    audience_rows = []
    for d in days:
        seasonal = 1.0 + 0.10 * np.sin(2 * np.pi * (d.dayofyear / 365.0))
        shock = 1.4 if np.random.rand() < 0.02 else 1.0  # viral days
        for _, plat in plats.iterrows():
            base_reach = 1_400_000 if plat["platform_id"] in ["web", "app"] else 900_000 if plat["platform_id"] == "youtube" else 450_000
            reach = int(max(50_000, base_reach * seasonal * shock + np.random.normal(0, 50_000)))
            engagement_actions = int(max(1000, reach * np.random.uniform(0.006, 0.02)))
            engagement_rate = engagement_actions / max(reach, 1)

            audience_rows.append({
                "activity_date": d.date(),
                "platform_id": plat["platform_id"],
                "reach": reach,
                "sessions": int(reach * np.random.uniform(0.25, 0.45)),
                "views": int(reach * np.random.uniform(0.35, 0.75)),
                "watch_time_minutes": float(max(0, reach * np.random.uniform(0.02, 0.06))),
                "engagement_actions": engagement_actions,
                "engagement_rate": float(engagement_rate),
                "followers_net_change": int(np.random.normal(1200 if plat["platform_group"] == "Social" else 200, 400)),
                "ctr": float(clamp(np.random.normal(0.032, 0.01), 0.005, 0.12)),
                "generated_at": generated_at
            })

    gold_digital_audience_daily = pd.DataFrame(audience_rows)
    gold_digital_audience_daily.to_csv(f"{OUTPUT_DIR}/gold_digital_audience_daily.csv", index=False)

    # -------------------------
    # 4) gold_hr_workforce_daily
    # -------------------------
    hr_rows = []
    base_hc = {
        "news": 950, "tv": 600, "digital": 420, "production": 300,
        "hr": 70, "finance": 85, "procurement": 60
    }
    for d in days:
        for _, dept in depts.iterrows():
            hc_base = base_hc.get(dept["dept_id"], 120)
            drift = np.random.normal(0, 1.5)
            headcount = int(max(10, hc_base + drift))

            leavers_7d = int(max(0, np.random.poisson(0.6 if dept["dept_id"] in ["news", "digital"] else 0.3)))
            joiners_7d = int(max(0, np.random.poisson(0.7 if dept["dept_id"] in ["digital"] else 0.4)))
            leavers_30d = int(max(leavers_7d, np.random.poisson(2.5 if dept["dept_id"] in ["news", "digital"] else 1.5)))

            attr_rate = leavers_30d / max(headcount, 1)
            absence_rate = float(clamp(np.random.normal(0.032, 0.01), 0.005, 0.12))
            overtime = float(max(0, np.random.normal(140 if dept["dept_id"] in ["news", "production"] else 50, 25)))
            open_positions = int(max(0, np.random.poisson(2 if dept["dept_id"] in ["digital", "news"] else 1)))

            hr_rows.append({
                "snapshot_date": d.date(),
                "dept_id": dept["dept_id"],
                "headcount": headcount,
                "joiners_7d": joiners_7d,
                "leavers_7d": leavers_7d,
                "leavers_30d": leavers_30d,
                "attrition_rate_30d": float(attr_rate),
                "absence_rate": absence_rate,
                "overtime_hours": overtime,
                "open_positions": open_positions,
                "generated_at": generated_at
            })

    gold_hr_workforce_daily = pd.DataFrame(hr_rows)
    gold_hr_workforce_daily.to_csv(f"{OUTPUT_DIR}/gold_hr_workforce_daily.csv", index=False)

    # -------------------------
    # 5) gold_hr_hiring_weekly
    # -------------------------
    hiring_rows = []
    for w in weeks:
        for _, dept in depts.iterrows():
            req_open = int(max(0, np.random.poisson(5 if dept["dept_id"] in ["digital", "news"] else 2)))
            apps = int(max(0, req_open * np.random.randint(20, 90)))
            interviews = int(max(0, apps * np.random.uniform(0.06, 0.14)))
            offers = int(max(0, interviews * np.random.uniform(0.15, 0.35)))
            accepted = int(max(0, offers * np.random.uniform(0.55, 0.8)))

            hiring_rows.append({
                "week_start_date": w.date(),
                "dept_id": dept["dept_id"],
                "requisitions_open": req_open,
                "applications_received": apps,
                "interviews_completed": interviews,
                "offers_made": offers,
                "offers_accepted": accepted,
                "avg_time_to_fill_days": float(clamp(np.random.normal(38, 10), 14, 90)),
                "generated_at": generated_at
            })

    gold_hr_hiring_weekly = pd.DataFrame(hiring_rows)
    gold_hr_hiring_weekly.to_csv(f"{OUTPUT_DIR}/gold_hr_hiring_weekly.csv", index=False)

    # -------------------------
    # 6) gold_fin_budget_vs_actual_monthly
    # -------------------------
    fin_month_rows = []
    cc_to_dept = {
        "cc_news": "news", "cc_tv": "tv", "cc_digital": "digital", "cc_corp": "finance"
    }
    for m in months:
        for _, cc in cost_centers.iterrows():
            dept_id = cc_to_dept.get(cc["cost_center_id"], None)

            # budgets
            budget = float(max(100_000, np.random.normal(6_000_000 if cc["cost_center_id"] in ["cc_news", "cc_tv"] else 2_500_000, 300_000)))
            # actuals sometimes overshoot
            variance_factor = np.random.normal(1.02, 0.06)  # avg slightly above budget
            actual = float(max(50_000, budget * variance_factor))

            fin_month_rows.append({
                "month_start_date": m.date(),
                "cost_center_id": cc["cost_center_id"],
                "dept_id": dept_id,
                "budget_amount": budget,
                "actual_amount": actual,
                "variance_amount": actual - budget,
                "variance_pct": (actual - budget) / max(budget, 1),
                "forecast_amount": float(max(0, budget * np.random.normal(1.0, 0.03))),
                "currency": currency,
                "generated_at": generated_at
            })

    gold_fin_budget_vs_actual_monthly = pd.DataFrame(fin_month_rows)
    gold_fin_budget_vs_actual_monthly.to_csv(f"{OUTPUT_DIR}/gold_fin_budget_vs_actual_monthly.csv", index=False)

    # -------------------------
    # 7) gold_fin_spend_daily
    # -------------------------
    fin_daily_rows = []
    for d in days:
        month_factor = 1.2 if d.day >= 25 else 1.0  # month-end spend spike
        for _, cc in cost_centers.iterrows():
            dept_id = cc_to_dept.get(cc["cost_center_id"], None)
            for cat in FIN_CATEGORIES:
                base = 120_000 if cat == "payroll" else 65_000 if cat == "vendors" else 35_000
                cc_mult = 1.5 if cc["cost_center_id"] in ["cc_news", "cc_tv"] else 1.0
                spend = float(max(0, np.random.normal(base * cc_mult * month_factor, 8_000)))

                fin_daily_rows.append({
                    "spend_date": d.date(),
                    "cost_center_id": cc["cost_center_id"],
                    "dept_id": dept_id,
                    "spend_category": cat,
                    "spend_amount": spend,
                    "invoice_count": int(max(0, np.random.poisson(4 if cat == "vendors" else 1))),
                    "vendor_count": int(max(0, np.random.poisson(2 if cat == "vendors" else 0))),
                    "generated_at": generated_at
                })

    gold_fin_spend_daily = pd.DataFrame(fin_daily_rows)
    gold_fin_spend_daily.to_csv(f"{OUTPUT_DIR}/gold_fin_spend_daily.csv", index=False)

    # -------------------------
    # 8) gold_data_health_daily (synthetic monitoring)
    # -------------------------
    health_rows = []
    table_names = [
        "gold_exec_daily","gold_exceptions","gold_media_output_daily","gold_broadcast_ops_daily",
        "gold_digital_audience_daily","gold_hr_workforce_daily","gold_hr_hiring_weekly",
        "gold_fin_budget_vs_actual_monthly","gold_fin_spend_daily","gold_data_health_daily"
    ]
    for d in days:
        for t in table_names:
            # simulate occasional late refresh
            late = np.random.rand() < 0.03
            last_refresh = pd.Timestamp(d) + pd.Timedelta(hours=(12 if not late else 22))
            freshness = "green" if not late else ("amber" if np.random.rand() < 0.7 else "red")

            health_rows.append({
                "snapshot_date": d.date(),
                "table_name": t,
                "last_refresh_ts": last_refresh,
                "expected_refresh_sla_hours": 12,
                "freshness_status": freshness,
                "row_count": int(np.random.normal(10000, 800)),
                "row_count_delta_pct": float(clamp(np.random.normal(0.01, 0.05), -0.3, 0.3)),
                "null_key_pct": float(clamp(np.random.normal(0.002, 0.004), 0.0, 0.08)),
                "dq_status": "pass" if freshness == "green" else ("warn" if freshness == "amber" else "fail"),
                "dq_notes": "" if freshness == "green" else ("late refresh simulated" if freshness == "amber" else "late refresh + dq fail simulated"),
                "generated_at": generated_at
            })

    gold_data_health_daily = pd.DataFrame(health_rows)
    gold_data_health_daily.to_csv(f"{OUTPUT_DIR}/gold_data_health_daily.csv", index=False)

    # -------------------------
    # 9) gold_exceptions (generated from patterns)
    # -------------------------
    exceptions = []
    ex_id = 1
    for d in days:
        # Overspend exceptions near month-end
        if d.day >= 25 and np.random.rand() < 0.08:
            exceptions.append({
                "exception_id": f"EX-{ex_id:06d}",
                "event_ts": pd.Timestamp(d) + pd.Timedelta(hours=10),
                "event_date": d.date(),
                "domain": "finance",
                "severity": "sev2",
                "status": "open" if np.random.rand() < 0.6 else "closed",
                "title": "Overspend risk detected",
                "description": "Month-end spend spike exceeded expected threshold (synthetic).",
                "kpi_id": "fin_spend_spike",
                "observed_value": float(np.random.uniform(1.15, 1.45)),
                "expected_value": 1.00,
                "threshold_band": "amber",
                "owner_role": "CFO",
                "owner_dept_id": "finance",
                "platform_id": None,
                "link_url": None,
                "created_at": generated_at
            })
            ex_id += 1

        # Broadcast incidents
        if np.random.rand() < 0.02:
            exceptions.append({
                "exception_id": f"EX-{ex_id:06d}",
                "event_ts": pd.Timestamp(d) + pd.Timedelta(hours=7),
                "event_date": d.date(),
                "domain": "media",
                "severity": "sev1" if np.random.rand() < 0.2 else "sev2",
                "status": "closed" if np.random.rand() < 0.7 else "open",
                "title": "Broadcast incident recorded",
                "description": "Broadcast adherence dip due to incident (synthetic).",
                "kpi_id": "broadcast_adherence",
                "observed_value": float(np.random.uniform(92, 97)),
                "expected_value": 98.5,
                "threshold_band": "amber",
                "owner_role": "COO",
                "owner_dept_id": "tv",
                "platform_id": "tv",
                "link_url": None,
                "created_at": generated_at
            })
            ex_id += 1

        # Digital reach drop
        if np.random.rand() < 0.02:
            exceptions.append({
                "exception_id": f"EX-{ex_id:06d}",
                "event_ts": pd.Timestamp(d) + pd.Timedelta(hours=12),
                "event_date": d.date(),
                "domain": "media",
                "severity": "sev3",
                "status": "open" if np.random.rand() < 0.5 else "closed",
                "title": "Digital reach anomaly",
                "description": "Reach dropped compared to trailing average (synthetic).",
                "kpi_id": "digital_reach",
                "observed_value": float(np.random.uniform(0.72, 0.88)),
                "expected_value": 1.00,
                "threshold_band": "amber",
                "owner_role": "CDO",
                "owner_dept_id": "digital",
                "platform_id": np.random.choice(plats["platform_id"].tolist()),
                "link_url": None,
                "created_at": generated_at
            })
            ex_id += 1

    gold_exceptions = pd.DataFrame(exceptions)
    gold_exceptions.to_csv(f"{OUTPUT_DIR}/gold_exceptions.csv", index=False)

    # -------------------------
    # 10) gold_exec_daily (rollup)
    # -------------------------
    # rollup from the generated tables + exceptions counts
    media_daily_total = gold_media_output_daily.groupby("activity_date")["content_count"].sum().reset_index()
    media_daily_total.rename(columns={"activity_date": "snapshot_date", "content_count": "media_output_total"}, inplace=True)

    broadcast_adherence = gold_broadcast_ops_daily.groupby("activity_date")["adherence_pct"].mean().reset_index()
    broadcast_adherence.rename(columns={"activity_date": "snapshot_date", "adherence_pct": "broadcast_adherence_pct"}, inplace=True)

    digital_reach = gold_digital_audience_daily.groupby("activity_date")["reach"].sum().reset_index()
    digital_reach.rename(columns={"activity_date": "snapshot_date", "reach": "digital_reach_total"}, inplace=True)

    digital_eng = gold_digital_audience_daily.groupby("activity_date")["engagement_rate"].mean().reset_index()
    digital_eng.rename(columns={"activity_date": "snapshot_date", "engagement_rate": "digital_engagement_rate"}, inplace=True)

    hc_total = gold_hr_workforce_daily.groupby("snapshot_date")["headcount"].sum().reset_index()
    hc_total.rename(columns={"headcount": "headcount_total"}, inplace=True)

    attr_30 = gold_hr_workforce_daily.groupby("snapshot_date")["leavers_30d"].sum().reset_index()
    attr_30.rename(columns={"leavers_30d": "attrition_30d"}, inplace=True)

    overtime_total = gold_hr_workforce_daily.groupby("snapshot_date")["overtime_hours"].sum().reset_index()
    overtime_total.rename(columns={"overtime_hours": "overtime_hours_total"}, inplace=True)

    # Approximate MTD spend/budget from monthly table
    month_map = pd.to_datetime(months).to_period("M")
    monthly_fin = gold_fin_budget_vs_actual_monthly.copy()
    monthly_fin["month_period"] = pd.to_datetime(monthly_fin["month_start_date"]).dt.to_period("M")
    monthly_roll = monthly_fin.groupby("month_period")[["budget_amount","actual_amount"]].sum().reset_index()

    exceptions_daily = gold_exceptions.groupby("event_date").size().reset_index(name="open_exceptions_count")
    exceptions_daily.rename(columns={"event_date": "snapshot_date"}, inplace=True)

    exec_df = pd.DataFrame({"snapshot_date": [d.date() for d in days]})
    exec_df = exec_df.merge(media_daily_total, on="snapshot_date", how="left")
    exec_df = exec_df.merge(broadcast_adherence, on="snapshot_date", how="left")
    exec_df = exec_df.merge(digital_reach, on="snapshot_date", how="left")
    exec_df = exec_df.merge(digital_eng, on="snapshot_date", how="left")
    exec_df = exec_df.merge(hc_total, on="snapshot_date", how="left")
    exec_df = exec_df.merge(attr_30, on="snapshot_date", how="left")
    exec_df = exec_df.merge(overtime_total, on="snapshot_date", how="left")
    exec_df = exec_df.merge(exceptions_daily, on="snapshot_date", how="left")

    exec_df["open_exceptions_count"] = exec_df["open_exceptions_count"].fillna(0).astype(int)

    # Create approximate MTD values based on month totals (simple POC approach)
    exec_df["month_period"] = pd.to_datetime(exec_df["snapshot_date"]).dt.to_period("M")
    exec_df = exec_df.merge(monthly_roll, left_on="month_period", right_on="month_period", how="left")
    exec_df.rename(columns={"actual_amount": "spend_actual_mtd", "budget_amount": "budget_mtd"}, inplace=True)
    exec_df["budget_variance_mtd"] = exec_df["spend_actual_mtd"] - exec_df["budget_mtd"]

    # Domain RAGs (simple thresholds for POC)
    exec_df["media_rag"] = exec_df["broadcast_adherence_pct"].apply(lambda x: rag_from_value(x, green_min=98, amber_min=96, direction="higher_is_better"))
    exec_df["finance_rag"] = exec_df["budget_variance_mtd"].apply(lambda x: rag_from_value(x, green_max=100_000, amber_max=300_000, direction="lower_is_better"))
    exec_df["hr_rag"] = exec_df["attrition_30d"].apply(lambda x: rag_from_value(x, green_max=20, amber_max=45, direction="lower_is_better"))

    # overall org RAG: worst of the three
    rag_rank = {"green": 0, "amber": 1, "red": 2}
    def worst_rag(row):
        rags = [row["media_rag"], row["finance_rag"], row["hr_rag"]]
        return max(rags, key=lambda r: rag_rank.get(r, 0))
    exec_df["org_rag"] = exec_df.apply(worst_rag, axis=1)

    exec_df["tech_rag"] = "green"
    exec_df["risk_rag"] = "green"
    exec_df["executive_summary"] = ""
    exec_df["generated_at"] = generated_at

    # Drop helper
    exec_df.drop(columns=["month_period"], inplace=True, errors="ignore")

    gold_exec_daily = exec_df[[
        "snapshot_date","org_rag","media_rag","hr_rag","finance_rag","tech_rag","risk_rag",
        "media_output_total","broadcast_adherence_pct","digital_reach_total","digital_engagement_rate",
        "headcount_total","attrition_30d","overtime_hours_total",
        "spend_actual_mtd","budget_mtd","budget_variance_mtd",
        "open_exceptions_count","executive_summary","generated_at"
    ]]

    gold_exec_daily.to_csv(f"{OUTPUT_DIR}/gold_exec_daily.csv", index=False)

    print("GOLD data generated successfully.")

if __name__ == "__main__":
    main()
