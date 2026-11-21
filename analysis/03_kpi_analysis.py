import pandas as pd

# Load cleaned dataset
df = pd.read_csv("analysis/cleaned_APL_Logistics.csv")

# Total records
total = len(df)

# Delivery categories
early = (df["Delivery Gap"] < 0).sum()
on_time = (df["Delivery Gap"] == 0).sum()
delayed = (df["Delivery Gap"] > 0).sum()

# KPI 1: On-Time Delivery Rate
on_time_rate = ((early + on_time) / total) * 100

# Exact on-time rate
exact_on_time_rate = (on_time / total) * 100

# KPI 2: Average Delivery Delay
average_delay = df.loc[
    df["Delivery Gap"] > 0,
    "Delivery Gap"
].mean()

# Overall average delivery gap
average_gap = df["Delivery Gap"].mean()

# KPI 3: Late Delivery Risk Ratio
risk_ratio = df["Late_delivery_risk"].mean() * 100

# KPI 4: Shipping Mode Efficiency Index
shipping_efficiency = df.groupby("Shipping Mode").agg(
    Total_Records=("Delivery Gap", "count"),
    Average_Delay=("Delivery Gap", "mean"),
    Delayed_Records=("Delivery Gap", lambda x: (x > 0).sum()),
    Within_Schedule=("Delivery Gap", lambda x: (x <= 0).mean() * 100)
)

# KPI 5: Regional Delay Index
regional_index = df.groupby("Order Region").agg(
    Total_Records=("Delivery Gap", "count"),
    Delayed_Records=("Delivery Gap", lambda x: (x > 0).sum()),
    Average_Delay=("Delivery Gap", "mean")
)

regional_index["Regional Delay Index"] = (
    regional_index["Delayed_Records"] /
    regional_index["Total_Records"] * 100
)

# Display results
print("\n========== OFFICIAL PROJECT KPIs ==========")

print("On-Time Delivery Rate:", round(on_time_rate, 2), "%")

print("Exactly On-Time Rate:", round(exact_on_time_rate, 2), "%")

print("Average Delivery Delay:", round(average_delay, 2), "days")

print("Overall Average Gap:", round(average_gap, 2), "days")

print("Late Delivery Risk Ratio:", round(risk_ratio, 2), "%")

print("\n========== SHIPPING MODE EFFICIENCY ==========")

print(shipping_efficiency.round(2))

print("\n========== REGIONAL DELAY INDEX ==========")

print(regional_index.round(2))

# Save KPI results
shipping_efficiency.to_csv(
    "analysis/shipping_efficiency.csv"
)

regional_index.to_csv(
    "analysis/regional_delay_index.csv"
)

print("\nKPI ANALYSIS COMPLETED SUCCESSFULLY!")