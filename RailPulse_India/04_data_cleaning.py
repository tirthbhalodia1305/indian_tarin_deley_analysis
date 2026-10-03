
import pandas as pd
import os

# Dataset folder
DATA_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Load datasets
delay = pd.read_csv(os.path.join(DATA_FOLDER, "combined_delay.csv"))
schedule = pd.read_csv(os.path.join(DATA_FOLDER, "combined_schedule.csv"))
train = pd.read_csv(os.path.join(DATA_FOLDER, "train_details.csv"))
station = pd.read_csv(os.path.join(DATA_FOLDER, "station_full_names.csv"))

datasets = {
    "Delay Data": delay,
    "Schedule Data": schedule,
    "Train Details": train,
    "Station Details": station
}

print("\n========== DATA CLEANING REPORT ==========")

for name, df in datasets.items():

    print(f"\n--- {name} ---")

    print("Total Rows:", len(df))

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:", df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)

print("\n========== INSPECTION COMPLETED ==========")