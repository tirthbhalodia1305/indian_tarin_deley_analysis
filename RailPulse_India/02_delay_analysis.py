
import pandas as pd
from pathlib import Path

file = Path(__file__).parent / "combined_delay.csv"

df = pd.read_csv(file, nrows=100000)

print("\n========== DELAY DATA ANALYSIS ==========")

print("\nDelay Data Type:")
print(df["delay"].dtype)

print("\nDelay Statistics:")
print(df["delay"].describe())

print("\nFirst 20 Delay Values:")
print(df["delay"].head(20).to_list())

print("\nNegative Delay Count:")
print((df["delay"] < 0).sum())

print("\nZero Delay Count:")
print((df["delay"] == 0).sum())

print("\nMissing Delay Count:")
print(df["delay"].isnull().sum())