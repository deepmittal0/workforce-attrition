from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "employees.csv")
issues = int(df.isna().sum().sum())
headcount = len(df)
attrition = df["attrition"].mean() * 100
by_dept = (df.groupby("department")["attrition"].mean().mul(100)
           .rename("attrition_rate_pct").reset_index())
out = ROOT / "reports"
out.mkdir(exist_ok=True)
by_dept.to_csv(out / "department_attrition.csv", index=False)
(out / "summary.json").write_text(json.dumps({
    "headcount": headcount, "missing_cells": issues,
    "overall_attrition_rate_pct": round(attrition, 2)
}, indent=2))
print(f"Headcount: {headcount}; attrition: {attrition:.2f}%")
print(by_dept.to_string(index=False))
