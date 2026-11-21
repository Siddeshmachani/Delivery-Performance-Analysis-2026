import pandas as pd
import os

# Load cleaned dataset
df = pd.read_csv("analysis/cleaned_APL_Logistics.csv")

# Create research output folder
os.makedirs("research_paper/results", exist_ok=True)

# --------------------------------
# 1. OVERALL DELIVERY PERFORMANCE
# --------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Early Deliveries",
        "Exactly On-Time Deliveries",
        "Delayed Deliveries",
        "On-Time Delivery Rate",
        "Delayed Delivery Rate",
        "Average Delivery Gap",
        "Average Delay Among Delayed Records",
        "Late Delivery Risk Indicator"
    ],

    "Value": [
        len(df),
        (df["Delivery Gap"] < 0).sum(),
        (df["Delivery Gap"] == 0).sum(),
        (df["Delivery Gap"] > 0).sum(),
        (df["Delivery Gap"] <= 0).mean() * 100,
        (df["Delivery Gap"] > 0).mean() * 100,
        df["Delivery Gap"].mean(),
        df.loc[df["Delivery Gap"] > 0, "Delivery Gap"].mean(),
        df["Late_delivery_risk"].mean() * 100
    ]
})

summary.to_csv(
    "research_paper/results/overall_performance.csv",
    index=False
)

# --------------------------------
# 2. SHIPPING MODE ANALYSIS
# --------------------------------

shipping = df.groupby("Shipping Mode").agg(
    Total_Records=("Delivery Gap", "count"),

    Average_Delivery_Gap=("Delivery Gap", "mean"),

    Delayed_Records=(
        "Delivery Gap",
        lambda x: (x > 0).sum()
    ),

    Delay_Rate=(
        "Delivery Gap",
        lambda x: (x > 0).mean() * 100
    ),

    Within_Schedule_Rate=(
        "Delivery Gap",
        lambda x: (x <= 0).mean() * 100
    )
).reset_index()

shipping.to_csv(
    "research_paper/results/shipping_analysis.csv",
    index=False
)

# --------------------------------
# 3. REGIONAL ANALYSIS
# --------------------------------

regional = df.groupby("Order Region").agg(
    Total_Records=("Delivery Gap", "count"),

    Delayed_Records=(
        "Delivery Gap",
        lambda x: (x > 0).sum()
    ),

    Average_Delivery_Gap=("Delivery Gap", "mean"),

    Delay_Rate=(
        "Delivery Gap",
        lambda x: (x > 0).mean() * 100
    )
).reset_index()

regional = regional.sort_values(
    "Delay_Rate",
    ascending=False
)

regional.to_csv(
    "research_paper/results/regional_analysis.csv",
    index=False
)

# --------------------------------
# 4. MARKET ANALYSIS
# --------------------------------

market = df.groupby("Market").agg(
    Total_Records=("Delivery Gap", "count"),

    Delayed_Records=(
        "Delivery Gap",
        lambda x: (x > 0).sum()
    ),

    Delay_Rate=(
        "Delivery Gap",
        lambda x: (x > 0).mean() * 100
    )
).reset_index()

market.to_csv(
    "research_paper/results/market_analysis.csv",
    index=False
)

# --------------------------------
# 5. CUSTOMER SEGMENT ANALYSIS
# --------------------------------

segment = df.groupby("Customer Segment").agg(
    Total_Records=("Delivery Gap", "count"),

    Delayed_Records=(
        "Delivery Gap",
        lambda x: (x > 0).sum()
    ),

    Average_Delivery_Gap=("Delivery Gap", "mean"),

    Delay_Rate=(
        "Delivery Gap",
        lambda x: (x > 0).mean() * 100
    )
).reset_index()

segment.to_csv(
    "research_paper/results/customer_segment_analysis.csv",
    index=False
)

# --------------------------------
# COMPLETION
# --------------------------------

print("\nRESEARCH ANALYSIS COMPLETED!")

print("\nOVERALL PERFORMANCE")
print(summary.round(2).to_string(index=False))

print("\nSHIPPING MODE ANALYSIS")
print(shipping.round(2).to_string(index=False))

print("\nTOP 5 HIGH-DELAY REGIONS")
print(regional.head(5).round(2).to_string(index=False))

print("\nMARKET ANALYSIS")
print(market.round(2).to_string(index=False))

print("\nCUSTOMER SEGMENT ANALYSIS")
print(segment.round(2).to_string(index=False))

print("\nAll research tables saved successfully!")