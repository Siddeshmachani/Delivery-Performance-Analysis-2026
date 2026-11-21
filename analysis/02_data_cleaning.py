import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv(
    "dataset/APL_Logistics.csv",
    encoding="latin1"
)

print("ORIGINAL DATASET:", df.shape)

# 1. Remove duplicate rows
df = df.drop_duplicates()

# 2. Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# 3. Validate shipping durations
df = df.dropna(subset=[
    "Days for shipping (real)",
    "Days for shipment (scheduled)"
])

df = df[
    (df["Days for shipping (real)"] >= 0) &
    (df["Days for shipment (scheduled)"] >= 0)
].copy()

# 4. Calculate delivery gap
df["Delivery Gap"] = (
    df["Days for shipping (real)"] -
    df["Days for shipment (scheduled)"]
)

# 5. Classify deliveries

df["Delivery Classification"] = np.select(
    [
        df["Delivery Gap"] < 0,
        df["Delivery Gap"] == 0,
        df["Delivery Gap"] > 0
    ],
    [
        "Early",
        "On-time",
        "Delayed"
    ],
    default="Unknown"
)

# 6. Calculate delivery KPIs
total = len(df)

early = (df["Delivery Classification"] == "Early").sum()
on_time = (df["Delivery Classification"] == "On-time").sum()
delayed = (df["Delivery Classification"] == "Delayed").sum()

print("\n========== DELIVERY SUMMARY ==========")

print("Total Records:", total)
print("Early Deliveries:", early)
print("On-time Deliveries:", on_time)
print("Delayed Deliveries:", delayed)

print("On-time/Early Rate:",
      round((early + on_time) / total * 100, 2), "%")

print("Delayed Rate:",
      round(delayed / total * 100, 2), "%")

print("Average Delivery Gap:",
      round(df["Delivery Gap"].mean(), 2), "days")

# 7. Compare late delivery risk
print("\n========== RISK VALIDATION ==========")

print(df.groupby("Late_delivery_risk")[
    "Delivery Gap"
].mean())

# 8. Save cleaned dataset
df.to_csv(
    "analysis/cleaned_APL_Logistics.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
