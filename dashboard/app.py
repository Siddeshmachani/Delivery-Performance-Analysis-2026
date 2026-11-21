# APL LOGISTICS - DELIVERY PERFORMANCE DASHBOARD

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="APL Logistics Analytics",
    page_icon="🚚",
    layout="wide"
)

# --------------------------------
# LOAD DATASET
# --------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "analysis" / "cleaned_APL_Logistics.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    # Exclude identifying customer information
    sensitive_columns = [
        "Customer Fname",
        "Customer Lname",
        "Customer Street",
        "Customer Zipcode",
        "Customer Email",
        "Customer Password"
    ]

    data = data.drop(
        columns=sensitive_columns,
        errors="ignore"
    )

    return data

df = load_data()

# --------------------------------
# TITLE
# --------------------------------

st.title("🚚 APL Logistics")
st.subheader(
    "Delivery Performance, Delay Risk & Logistics Efficiency"
)

st.markdown(
    "Global Supply Chain Operations Analytics"
)

st.divider()

# --------------------------------
# SIDEBAR FILTERS
# --------------------------------

st.sidebar.title("Dashboard Filters")

shipping_modes = ["All"] + sorted(
    df["Shipping Mode"].dropna().unique().tolist()
)

markets = ["All"] + sorted(
    df["Market"].dropna().unique().tolist()
)

selected_market = st.sidebar.selectbox(
    "Market",
    markets
)

if selected_market == "All":
    region_data = df
else:
    region_data = df[
        df["Market"] == selected_market
    ]

regions = ["All"] + sorted(
    region_data["Order Region"].dropna().unique().tolist()
)

segments = ["All"] + sorted(
    df["Customer Segment"].dropna().unique().tolist()
)

selected_shipping = st.sidebar.selectbox(
    "Shipping Mode",
    shipping_modes
)

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)



selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    segments
)

st.sidebar.info(
    "Date-range filtering is unavailable because "
    "the supplied dataset has no identified date column."
)

# --------------------------------
# APPLY FILTERS
# --------------------------------

filtered = df.copy()

if selected_shipping != "All":
    filtered = filtered[
        filtered["Shipping Mode"] == selected_shipping
    ]

if selected_region != "All":
    filtered = filtered[
        filtered["Order Region"] == selected_region
    ]

if selected_market != "All":
    filtered = filtered[
        filtered["Market"] == selected_market
    ]

if selected_segment != "All":
    filtered = filtered[
        filtered["Customer Segment"] == selected_segment
    ]

# --------------------------------
# OFFICIAL KPI CALCULATIONS
# --------------------------------

total = len(filtered)

if total > 0:

    # Delivery categories
    early = (filtered["Delivery Gap"] < 0).sum()

    on_time = (filtered["Delivery Gap"] == 0).sum()

    delayed = (filtered["Delivery Gap"] > 0).sum()

    # KPI 1: On-Time Delivery Rate
    on_time_rate = (
        (early + on_time) / total
    ) * 100

    # KPI 2: Average Delivery Gap
    average_gap = filtered["Delivery Gap"].mean()

    # KPI 3: Late Delivery Risk Ratio
    delayed_ratio = (
        delayed / total
    ) * 100

    # Additional metric: Average delay among delayed records
    average_delay = filtered.loc[
        filtered["Delivery Gap"] > 0,
        "Delivery Gap"
    ].mean()

    if pd.isna(average_delay):
        average_delay = 0

    # Dataset risk indicator
    risk_indicator = (
        filtered["Late_delivery_risk"].mean()
    ) * 100

    # KPI 4: Shipping Mode Efficiency Index
    shipping_kpi = filtered.groupby(
        "Shipping Mode"
    ).agg(
        Delay_Rate=(
            "Delivery Gap",
            lambda x: (x > 0).mean() * 100
        )
    )

    best_shipping_mode = shipping_kpi[
        "Delay_Rate"
    ].idxmin()

    best_shipping_efficiency = (
        100 - shipping_kpi.loc[
            best_shipping_mode,
            "Delay_Rate"
        ]
    )

    # KPI 5: Regional Delay Index
    regional_kpi = filtered.groupby(
        "Order Region"
    ).agg(
        Delay_Rate=(
            "Delivery Gap",
            lambda x: (x > 0).mean() * 100
        )
    )

    highest_risk_region = regional_kpi[
        "Delay_Rate"
    ].idxmax()

    highest_regional_delay = (
        regional_kpi.loc[
            highest_risk_region,
            "Delay_Rate"
        ]
    )

else:

    on_time_rate = 0
    average_gap = 0
    delayed_ratio = 0
    average_delay = 0
    risk_indicator = 0

    best_shipping_mode = "N/A"
    best_shipping_efficiency = 0

    highest_risk_region = "N/A"
    highest_regional_delay = 0


# --------------------------------
# MODULE 1: DELIVERY OVERVIEW
# --------------------------------

st.header("📊 1. Delivery Performance Overview")

if total > 0:

    st.caption(f"Records analyzed: {total:,}")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "On-Time Delivery Rate",
        f"{on_time_rate:.2f}%"
    )

    c2.metric(
        "Average Delivery Gap",
        f"{average_gap:.2f} days"
    )

    c3.metric(
        "Late Delivery Risk Ratio",
        f"{delayed_ratio:.2f}%"
    )

    c4.metric(
        "Shipping Efficiency",
        f"{best_shipping_efficiency:.2f}%",
        help=f"Best performing mode: {best_shipping_mode}"
    )

    c5.metric(
        "Regional Delay Index",
        f"{highest_regional_delay:.2f}%",
        help=f"Highest-risk region: {highest_risk_region}"
    )

    st.info(
        f"Best shipping mode: {best_shipping_mode} | "
        f"Highest-risk region: {highest_risk_region}"
    )

    st.caption(
        f"Additional metrics: Average delay among delayed "
        f"records = {average_delay:.2f} days | "
        f"Dataset risk indicator = {risk_indicator:.2f}%"
    )

else:

    st.warning(
        "No records found for the selected filters. "
        "Please adjust your selection."
    )

st.divider()

# --------------------------------
# MODULE 2: DELAY RISK
# --------------------------------

st.header("⚠️ 2. Delay Risk Analysis")

if total > 0:

    col1, col2 = st.columns(2)

    with col1:

        classification = filtered[
            "Delivery Classification"
        ].value_counts().reset_index()

        classification.columns = [
            "Classification",
            "Count"
        ]

        fig = px.pie(
            classification,
            names="Classification",
            values="Count",
            title="Delivery Classification Distribution",
            hole=0.45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.histogram(
            filtered,
            x="Delivery Gap",
            nbins=30,
            title="Delivery Gap Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# --------------------------------
# MODULE 3: SHIPPING COMPARISON
# --------------------------------

st.header("🚢 3. Shipping Mode Comparison")

if total > 0:

    shipping = filtered.groupby(
        "Shipping Mode"
    ).agg(
        Total_Records=("Delivery Gap", "count"),

        Average_Gap=("Delivery Gap", "mean"),

        Delayed_Rate=(
            "Delivery Gap",
            lambda x: (x > 0).mean() * 100
        ),

        Within_Schedule=(
            "Delivery Gap",
            lambda x: (x <= 0).mean() * 100
        )

    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            shipping,
            x="Shipping Mode",
            y="Delayed_Rate",
            title="Delayed Delivery Rate by Shipping Mode",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            shipping,
            x="Shipping Mode",
            y="Within_Schedule",
            title="Shipping Mode SLA Compliance",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.dataframe(
        shipping.round(2),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------
# MODULE 4: REGIONAL ANALYSIS
# --------------------------------

st.header("🌍 4. Regional & Market Analysis")

if total > 0:

    regional = filtered.groupby(
        ["Market", "Order Region"]
    ).agg(
        Total_Records=("Delivery Gap", "count"),

        Delayed_Rate=(
            "Delivery Gap",
            lambda x: (x > 0).mean() * 100
        )

    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            regional,
            x="Order Region",
            y="Delayed_Rate",
            color="Market",
            title="Regional Delay Rate"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        heatmap_data = regional.pivot(
            index="Market",
            columns="Order Region",
            values="Delayed_Rate"
        )

        fig = px.imshow(
            heatmap_data,
            text_auto=".1f",
            aspect="auto",
            color_continuous_scale="RdYlGn_r",
            title="Market vs Regional Delay Heatmap"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.dataframe(
        regional.round(2),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.markdown(
    """
    **Project:** Delivery Performance, Delay Risk,
    and Logistics Efficiency Analysis

    **Technology:** Python, Pandas, Plotly, Streamlit

    **Dataset:** APL Logistics Internship Dataset

    **Note:** All displayed metrics are calculated
    from the supplied historical dataset.
    """
)