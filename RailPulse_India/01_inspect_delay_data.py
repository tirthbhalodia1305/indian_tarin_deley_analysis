import pandas as pd
from pathlib import Path

file = Path(__file__).parent / "combined_delay.csv"

total_rows = 0
missing_values = None
duplicate_rows = 0
min_date = None
max_date = None

for chunk in pd.read_csv(file, chunksize=100000):

    total_rows += len(chunk)

    if missing_values is None:
        missing_values = chunk.isnull().sum()
    else:
        missing_values += chunk.isnull().sum()

    duplicate_rows += chunk.duplicated().sum()

    chunk["date"] = pd.to_datetime(
        chunk["date"], errors="coerce"
    )

    current_min = chunk["date"].min()
    current_max = chunk["date"].max()

    if pd.notna(current_min):
        min_date = current_min if min_date is None else min(min_date, current_min)

    if pd.notna(current_max):
        max_date = current_max if max_date is None else max(max_date, current_max)

print("\n========== DATASET REPORT ==========")

print("Total Rows:", total_rows)

print("\nMissing Values:")
print(missing_values)

print("\nDuplicate Rows:", duplicate_rows)

print("\nEarliest Date:", min_date)
print("Latest Date:", max_date)