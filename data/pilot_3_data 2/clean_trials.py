import pandas as pd
import numpy as np
import os

# ── Configure your paths here ────────────────────────────────────────────────
INPUT_FILE  = "A1-Indicom-pilot-results.csv"
OUTPUT_FILE = "A1-Indicom-pilot-v3-results-collapsed.csv"
# ─────────────────────────────────────────────────────────────────────────────

script_dir  = os.path.dirname(os.path.abspath(__file__))
input_path  = os.path.join(script_dir, INPUT_FILE)
output_path = os.path.join(script_dir, OUTPUT_FILE)

df = pd.read_csv(input_path, sep=";", na_values=["NA", ""])

def first_non_na(series):
    vals = series.dropna()
    return vals.iloc[0] if len(vals) > 0 else np.nan

def concat_non_na(series):
    vals = series.dropna().astype(str).str.strip()
    vals = vals[vals != ""]
    return " | ".join(vals) if len(vals) > 0 else np.nan

def collapse_group(group):
    row = {}
    for col in group.columns:
        if col in ("comment", "comments"):
            row[col] = concat_non_na(group[col])
        else:
            row[col] = first_non_na(group[col])
    return pd.Series(row)

grouped   = df.groupby(["submission_id", "itemID"], sort=False)
collapsed = grouped.apply(collapse_group).reset_index(drop=True)
collapsed = collapsed[[c for c in df.columns if c in collapsed.columns]]

# Convert any whole-number float columns (e.g. 25.0) back to integers
for col in collapsed.columns:
    if collapsed[col].dtype == float:
        if collapsed[col].dropna().apply(float.is_integer).all():
            collapsed[col] = collapsed[col].astype("Int64")  # Int64 supports NA

collapsed.to_csv(output_path, index=False, sep=";")
print(f"Done. {len(df)} rows → {len(collapsed)} rows")
print(f"Saved to: {output_path}")
