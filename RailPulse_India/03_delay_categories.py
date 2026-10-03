import pandas as pd
from pathlib import Path

file = Path(__file__).parent / "combined_delay.csv"

df = pd.read_csv(file, nrows=100000)

df = df.dropna(subset=["delay"])

def categorize_delay(delay):

    if delay < 0:
        return "Early"

    elif delay == 0:
        return "On Time"

    elif delay <= 60:
        return "Minor Delay"

    elif delay <= 180:
        return "Moderate Delay"

    else:
        return "Severe Delay"

df["delay_category"] = df["delay"].apply(categorize_delay)

print("\n========== DELAY CATEGORY ANALYSIS ==========")

print(df["delay_category"].value_counts())

print("\nPercentage Distribution:")

print(
    df["delay_category"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)