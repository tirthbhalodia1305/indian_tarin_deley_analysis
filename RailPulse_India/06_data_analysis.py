import pandas as pd
import os

print("=" * 60)
print("             RAILPULSE INDIA")
print("          DATA ANALYSIS & INSIGHTS")
print("=" * 60)

# Dataset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")

# Load dataset
print("\nLoading railway delay dataset...")

file_path = os.path.join(DATA_FOLDER, "combined_delay.csv")

if not os.path.exists(file_path):
    file_path = os.path.join(BASE_DIR, "combined_delay.csv")

if not os.path.exists(file_path):
    print("ERROR: combined_delay.csv not found!")
    print("Place the CSV inside the project or data folder.")
    raise SystemExit

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total Records:", len(df))

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Required columns
required = ["date", "station_name", "delay", "train_no"]

for col in required:
    if col not in df.columns:
        print(f"ERROR: Missing column {col}")
        raise SystemExit

# Convert data types
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["delay"] = pd.to_numeric(df["delay"], errors="coerce")

# Remove invalid records
df = df.dropna(subset=["date", "delay", "station_name", "train_no"])

# Remove unrealistic delay values
df = df[(df["delay"] >= 0) & (df["delay"] <= 1440)]

# Create month column
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%B")

print("\nValid Records:", len(df))

# 1. Overall statistics
print("\n" + "=" * 60)
print("OVERALL DELAY ANALYSIS")
print("=" * 60)

print("Average Delay:", round(df["delay"].mean(), 2), "minutes")
print("Median Delay:", round(df["delay"].median(), 2), "minutes")
print("Maximum Delay:", df["delay"].max(), "minutes")
print("Minimum Delay:", df["delay"].min(), "minutes")

# 2. Monthly analysis
print("\n" + "=" * 60)
print("MONTHLY DELAY ANALYSIS")
print("=" * 60)

monthly = df.groupby("month_name")["delay"].agg(
    ["mean", "median", "count"]
)

monthly = monthly.rename(columns={
    "mean": "average_delay",
    "median": "median_delay",
    "count": "total_records"
})

monthly = monthly.sort_values(
    "average_delay", ascending=False
)

print(monthly)

# 3. Station analysis
print("\n" + "=" * 60)
print("TOP 10 DELAYED STATIONS")
print("=" * 60)

station_analysis = df.groupby("station_name")["delay"].agg(
    ["mean", "count"]
)

station_analysis = station_analysis[
    station_analysis["count"] >= 100
]

station_analysis = station_analysis.sort_values(
    "mean", ascending=False
)

print(station_analysis.head(10))

# 4. Train analysis
print("\n" + "=" * 60)
print("TOP 10 DELAYED TRAINS")
print("=" * 60)

train_analysis = df.groupby("train_no")["delay"].agg(
    ["mean", "count"]
)

train_analysis = train_analysis[
    train_analysis["count"] >= 100
]

train_analysis = train_analysis.sort_values(
    "mean", ascending=False
)

print(train_analysis.head(10))

# 5. Delay severity
print("\n" + "=" * 60)
print("DELAY SEVERITY ANALYSIS")
print("=" * 60)

def categorize_delay(delay):
    if delay == 0:
        return "On Time"
    elif delay <= 15:
        return "Minor Delay"
    elif delay <= 60:
        return "Moderate Delay"
    else:
        return "Severe Delay"

df["delay_category"] = df["delay"].apply(categorize_delay)

category_counts = df["delay_category"].value_counts()

print(category_counts)

# 6. Peak delay month
print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)

highest_month = monthly.index[0]
highest_station = station_analysis.index[0]
highest_train = train_analysis.index[0]

print("1. Highest average delay month:", highest_month)

print("2. Station with highest average delay:",
      highest_station)

print("3. Train with highest average delay:",
      highest_train)

print("4. Overall average delay:",
      round(df["delay"].mean(), 2), "minutes")

print("5. Total analyzed records:", len(df))

# Save analysis results
OUTPUT_FOLDER = os.path.join(BASE_DIR, "analysis_results")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

monthly.to_csv(
    os.path.join(OUTPUT_FOLDER, "monthly_analysis.csv")
)

station_analysis.to_csv(
    os.path.join(OUTPUT_FOLDER, "station_analysis.csv")
)

train_analysis.to_csv(
    os.path.join(OUTPUT_FOLDER, "train_analysis.csv")
)

category_counts.to_csv(
    os.path.join(OUTPUT_FOLDER, "delay_severity.csv")
)

print("\nAnalysis results saved successfully!")

print("\n" + "=" * 60)
print("       DATA ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)