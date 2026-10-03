
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# RAILPULSE INDIA
# OUTLIER ANALYSIS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "combined_delay.csv")

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

print("\n====================================")
print("       RAILPULSE INDIA")
print("          OUTLIER ANALYSIS")
print("====================================")

# ==========================================
# LOAD DATA
# ==========================================

print("\nLoading dataset...")

if not os.path.exists(DATA_PATH):
    print("ERROR: combined_delay.csv not found!")
    raise SystemExit

df = pd.read_csv(
    DATA_PATH,
    usecols=["date", "station_no", "station_name", "delay", "train_no"]
)

print("Dataset loaded successfully!")
print("Original Rows:", len(df))

# ==========================================
# CLEAN DELAY COLUMN
# ==========================================

df["delay"] = pd.to_numeric(df["delay"], errors="coerce")

df = df.dropna(subset=["delay"]).copy()

# Preserve original delay values for comparison
df["original_delay"] = df["delay"]

# ==========================================
# STATISTICAL ANALYSIS
# ==========================================

Q1 = df["delay"].quantile(0.25)

Q3 = df["delay"].quantile(0.75)

IQR = Q3 - Q1

LOWER_LIMIT = Q1 - 1.5 * IQR

UPPER_LIMIT = Q3 + 1.5 * IQR

print("\n====================================")
print("       IQR OUTLIER ANALYSIS")
print("====================================")

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)

print("Lower Limit:", LOWER_LIMIT)
print("Upper Limit:", UPPER_LIMIT)

# ==========================================
# IDENTIFY OUTLIERS
# ==========================================

outlier_mask = (
    (df["delay"] < LOWER_LIMIT) |
    (df["delay"] > UPPER_LIMIT)
)

outliers = df.loc[outlier_mask].copy()

normal_data = df.loc[~outlier_mask].copy()

print("\nTotal Valid Records:", len(df))

print("Outlier Records:", len(outliers))

print("Normal Records:", len(normal_data))

outlier_percentage = (
    len(outliers) / len(df)
) * 100

print(
    "Outlier Percentage:",
    round(outlier_percentage, 2),
    "%"
)

# ==========================================
# EXTREME DELAY RECORDS
# ==========================================

print("\nTop 10 Extreme Delay Records:")

print(
    outliers.nlargest(10, "delay")[
        ["date", "station_name", "train_no", "delay"]
    ].to_string(index=False)
)

# ==========================================
# SAVE OUTLIER DATA
# ==========================================

outliers.to_csv(
    os.path.join(OUTPUT_DIR, "outlier_records.csv"),
    index=False
)

# ==========================================
# GRAPH 1: BOXPLOT
# ==========================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    y=df["delay"],
    color="orange"
)

plt.title("Railway Delay Outlier Detection")
plt.ylabel("Delay (Minutes)")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "07_outlier_boxplot.png"),
    dpi=300
)

plt.close()

# ==========================================
# GRAPH 2: NORMAL VS OUTLIERS
# ==========================================

comparison = pd.DataFrame({
    "Category": ["Normal Records", "Outlier Records"],
    "Count": [len(normal_data), len(outliers)]
})

plt.figure(figsize=(8, 6))

sns.barplot(
    data=comparison,
    x="Category",
    y="Count",
    hue="Category",
    palette="viridis",
    legend=False
)

plt.title("Normal Records vs Outliers")
plt.xlabel("Record Type")
plt.ylabel("Number of Records")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "08_outlier_comparison.png"),
    dpi=300
)

plt.close()

# ==========================================
# FILTERED DATA SUMMARY
# ==========================================

print("\n====================================")
print("       FILTERED DATA SUMMARY")
print("====================================")

print(
    "Original Average Delay:",
    round(df["delay"].mean(), 2)
)

print(
    "Average Delay Without Outliers:",
    round(normal_data["delay"].mean(), 2)
)

print(
    "Original Median Delay:",
    round(df["delay"].median(), 2)
)

print(
    "Filtered Median Delay:",
    round(normal_data["delay"].median(), 2)
)

# ==========================================
# SAVE SUMMARY
# ==========================================

summary = pd.DataFrame({
    "Metric": [
        "Total Valid Records",
        "Outlier Records",
        "Normal Records",
        "Outlier Percentage",
        "Q1",
        "Q3",
        "IQR",
        "Upper Limit",
        "Original Mean Delay",
        "Filtered Mean Delay",
        "Original Median Delay",
        "Filtered Median Delay"
    ],

    "Value": [
        len(df),
        len(outliers),
        len(normal_data),
        round(outlier_percentage, 2),
        Q1,
        Q3,
        IQR,
        UPPER_LIMIT,
        df["delay"].mean(),
        normal_data["delay"].mean(),
        df["delay"].median(),
        normal_data["delay"].median()
    ]
})

summary.to_csv(
    os.path.join(OUTPUT_DIR, "outlier_analysis_summary.csv"),
    index=False
)

print("\n====================================")
print("       ANALYSIS COMPLETED")
print("====================================")

print("\nFiles saved in outputs folder:")
print("- outlier_records.csv")
print("- outlier_analysis_summary.csv")
print("- 07_outlier_boxplot.png")
print("- 08_outlier_comparison.png")

print("\nRailPulse India Outlier Analysis Completed!")