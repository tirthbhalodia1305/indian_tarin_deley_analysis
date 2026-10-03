
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# RAILPULSE INDIA
# EXPLORATORY DATA ANALYSIS
# ==========================================

print("=" * 55)
print("          RAILPULSE INDIA")
print("      EXPLORATORY DATA ANALYSIS")
print("=" * 55)

# Project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Possible dataset locations
possible_paths = [
    os.path.join(BASE_DIR, "combined_delay.csv"),
    os.path.join(BASE_DIR, "data", "combined_delay.csv"),
    os.path.join(BASE_DIR, "datasets", "combined_delay.csv")
]

file_path = next(
    (path for path in possible_paths if os.path.exists(path)),
    None
)

if file_path is None:
    print("\nERROR: combined_delay.csv not found!")
    print("Place the CSV in the project folder or data folder.")
    raise SystemExit

# Load dataset
print("\nLoading railway delay data...")

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

# Check required columns
required = ["date", "station_name", "delay", "train_no"]

missing = [col for col in required if col not in df.columns]

if missing:
    print("Missing columns:", missing)
    raise SystemExit

# Clean data
df["delay"] = pd.to_numeric(df["delay"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.dropna(subset=["delay", "date"])

# Remove impossible negative delays
df = df[df["delay"] >= 0].copy()

# Convert delay into categories
df["delay_category"] = pd.cut(
    df["delay"],
    bins=[-1, 0, 15, 60, float("inf")],
    labels=[
        "On Time",
        "Minor Delay",
        "Moderate Delay",
        "Severe Delay"
    ]
)

print("\nCleaned Rows:", len(df))

# Output folder
output_dir = os.path.join(BASE_DIR, "eda_charts")
os.makedirs(output_dir, exist_ok=True)

sns.set_theme(style="whitegrid")

# ==========================================
# 1. DELAY DISTRIBUTION
# ==========================================

print("\nGenerating Delay Distribution...")

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="delay",
    bins=50,
    color="steelblue"
)

plt.title("Railway Delay Distribution")
plt.xlabel("Delay (Minutes)")
plt.ylabel("Frequency")
plt.xlim(0, df["delay"].quantile(0.99))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "01_delay_distribution.png"))
plt.close()

# ==========================================
# 2. DELAY CATEGORY
# ==========================================

print("Generating Delay Category Chart...")

category_counts = df["delay_category"].value_counts()

plt.figure(figsize=(9, 6))

category_counts.plot(
    kind="bar",
    color="teal",
    edgecolor="black"
)

plt.title("Railway Delay Category Distribution")
plt.xlabel("Delay Category")
plt.ylabel("Number of Records")
plt.xticks(rotation=20)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "02_delay_categories.png"))
plt.close()

# ==========================================
# 3. TOP 10 DELAYED STATIONS
# ==========================================

print("Finding Top 10 Delayed Stations...")

station_delay = (
    df.groupby("station_name")["delay"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(11, 7))

station_delay.sort_values().plot(
    kind="barh",
    color="coral"
)

plt.title("Top 10 Stations by Average Delay")
plt.xlabel("Average Delay (Minutes)")
plt.ylabel("Station")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "03_top_stations.png"))
plt.close()

# ==========================================
# 4. MONTHLY DELAY TREND
# ==========================================

print("Analyzing Monthly Delay Trend...")

df["month"] = df["date"].dt.to_period("M").astype(str)

monthly_delay = df.groupby("month")["delay"].mean()

plt.figure(figsize=(12, 6))

monthly_delay.plot(
    marker="o",
    color="darkorange"
)

plt.title("Monthly Average Railway Delay")
plt.xlabel("Month")
plt.ylabel("Average Delay (Minutes)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "04_monthly_trend.png"))
plt.close()

# ==========================================
# 5. TOP 10 TRAINS BY AVERAGE DELAY
# ==========================================

print("Analyzing Train Delays...")

train_delay = (
    df.groupby("train_no")["delay"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(11, 7))

train_delay.sort_values().plot(
    kind="barh",
    color="mediumpurple"
)

plt.title("Top 10 Trains by Average Delay")
plt.xlabel("Average Delay (Minutes)")
plt.ylabel("Train Number")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "05_train_delays.png"))
plt.close()

# ==========================================
# 6. DELAY BOXPLOT
# ==========================================

print("Generating Delay Boxplot...")

# Sample to reduce memory usage
sample_size = min(100000, len(df))

sample = df["delay"].sample(
    n=sample_size,
    random_state=42
)

plt.figure(figsize=(10, 6))

sns.boxplot(x=sample, color="lightgreen")

plt.title("Railway Delay Boxplot")
plt.xlabel("Delay (Minutes)")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "06_delay_boxplot.png"))
plt.close()

# ==========================================
# FINAL REPORT
# ==========================================

print("\n" + "=" * 55)
print("             EDA SUMMARY")
print("=" * 55)

print("Total Records:", len(df))
print("Average Delay:", round(df["delay"].mean(), 2), "minutes")
print("Median Delay:", round(df["delay"].median(), 2), "minutes")
print("Maximum Delay:", df["delay"].max(), "minutes")
print("Minimum Delay:", df["delay"].min(), "minutes")

print("\nDelay Category Distribution:")
print(df["delay_category"].value_counts())

print("\nTop 10 Delayed Stations:")
print(station_delay)

print("\nTop 10 Delayed Trains:")
print(train_delay)

print("\nCharts saved in:", output_dir)

print("\n" + "=" * 55)
print("       EDA COMPLETED SUCCESSFULLY")
print("=" * 55)