import pandas as pd
from pathlib import Path

folder = Path(__file__).parent

files = [
    "train_details.csv",
    "station_full_names.csv",
    "combined_schedule.csv"
]

for name in files:

    file = folder / name

    print("\n==========", name, "==========")

    df = pd.read_csv(file, nrows=5)

    print("Columns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))