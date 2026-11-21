import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned dataset
df = pd.read_csv("analysis/cleaned_APL_Logistics.csv")

# Create output folder
os.makedirs("visualizations", exist_ok=True)

sns.set_theme(style="whitegrid")

# ==================================
# CHART 1: DELIVERY CLASSIFICATION
# ==================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="Delivery Classification",
    order=["Early", "On-time", "Delayed"]
)

plt.title("Delivery Classification Distribution")
plt.xlabel("Delivery Classification")
plt.ylabel("Number of Records")

plt.tight_layout()

plt.savefig("visualizations/delivery_classification.png")
plt.close()


# ==================================
# CHART 2: SHIPPING MODE PERFORMANCE
# ==================================

shipping = df.groupby("Shipping Mode").agg(
    Delayed=("Delivery Gap", lambda x: (x > 0).mean() * 100)
).reset_index()

plt.figure(figsize=(9, 5))

sns.barplot(
    data=shipping,
    x="Shipping Mode",
    y="Delayed"
)

plt.title("Delayed Delivery Rate by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Delayed Delivery Rate (%)")

plt.tight_layout()

plt.savefig("visualizations/shipping_mode_performance.png")
plt.close()


# ==================================
# CHART 3: REGIONAL DELAY ANALYSIS
# ==================================

regional = df.groupby("Order Region").agg(
    Delay_Rate=("Delivery Gap", lambda x: (x > 0).mean() * 100)
).sort_values("Delay_Rate", ascending=False)

plt.figure(figsize=(12, 8))

sns.barplot(
    x=regional["Delay_Rate"],
    y=regional.index
)

plt.title("Regional Delivery Delay Rate")
plt.xlabel("Delayed Delivery Rate (%)")
plt.ylabel("Order Region")

plt.tight_layout()

plt.savefig("visualizations/regional_delay_analysis.png")
plt.close()


# ==================================
# CHART 4: DELIVERY GAP DISTRIBUTION
# ==================================

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="Delivery Gap",
    bins=30,
    kde=True
)

plt.title("Distribution of Delivery Gap")
plt.xlabel("Delivery Gap (Days)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("visualizations/delivery_gap_distribution.png")
plt.close()


print("ALL FOUR VISUALIZATIONS CREATED SUCCESSFULLY!")