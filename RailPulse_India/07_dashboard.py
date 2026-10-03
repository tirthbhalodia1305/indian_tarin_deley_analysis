import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# RAILPULSE INDIA - INTERACTIVE DASHBOARD
# ==========================================

st.set_page_config(
    page_title="RailPulse India",
    page_icon="🚆",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(BASE_DIR, "analysis_results")

# ==========================================
# LOAD ANALYSIS RESULTS
# ==========================================

@st.cache_data
def load_data():

    monthly = pd.read_csv(
        os.path.join(RESULT_DIR, "monthly_analysis.csv")
    )

    stations = pd.read_csv(
        os.path.join(RESULT_DIR, "station_analysis.csv")
    )

    trains = pd.read_csv(
        os.path.join(RESULT_DIR, "train_analysis.csv")
    )

    categories = pd.read_csv(
        os.path.join(RESULT_DIR, "delay_severity.csv")
    )

    return monthly, stations, trains, categories

try:
    monthly, stations, trains, categories = load_data()

except FileNotFoundError:
    st.error(
        "Analysis files not found. Run 06_data_analysis.py first."
    )
    st.stop()

# ==========================================
# HEADER
# ==========================================

st.title("🚆 RailPulse India")

st.subheader("Indian Railway Delay Analytics Dashboard")

st.markdown(
    "An interactive data analytics platform "
    "for understanding railway delay patterns."
)

st.divider()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Dashboard Controls")

st.sidebar.info(
    "Railway Delay Analysis\n\n"
    "Data Source: RailPulse India Dataset"
)

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "Monthly Analysis",
        "Station Analysis",
        "Train Analysis",
        "Delay Severity"
    ]
)

# ==========================================
# OVERVIEW
# ==========================================

if page == "Overview":

    st.header("Railway Performance Overview")

    total_records = int(categories["count"].sum())

    avg_delay = (
        monthly["average_delay"] *
        monthly["total_records"]
    ).sum() / monthly["total_records"].sum()

    median_delay = monthly["median_delay"].median()

    on_time = int(
        categories.loc[
            categories.iloc[:, 0] == "On Time",
            "count"
        ].sum()
    )

    delayed = total_records - on_time

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{total_records:,}"
    )

    col2.metric(
        "Average Delay",
        f"{avg_delay:.2f} min"
    )

    col3.metric(
        "Median Monthly Delay",
        f"{median_delay:.2f} min"
    )

    col4.metric(
        "Delayed Records",
        f"{delayed:,}"
    )

    st.divider()

    st.subheader("Delay Category Distribution")

    fig = px.pie(
        categories,
        names=categories.columns[0],
        values="count",
        hole=0.4,
        title="Railway Delay Categories"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Average Delay")

    fig = px.bar(
        monthly,
        x="month_name",
        y="average_delay",
        title="Average Railway Delay by Month",
        labels={
            "month_name": "Month",
            "average_delay": "Average Delay (Minutes)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MONTHLY ANALYSIS
# ==========================================

elif page == "Monthly Analysis":

    st.header("Monthly Delay Analysis")

    fig = px.line(
        monthly,
        x="month_name",
        y="average_delay",
        markers=True,
        title="Monthly Railway Delay Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        monthly,
        x="month_name",
        y="total_records",
        title="Monthly Record Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Statistics")

    st.dataframe(
        monthly,
        use_container_width=True
    )

# ==========================================
# STATION ANALYSIS
# ==========================================

elif page == "Station Analysis":

    st.header("Station Performance Analysis")

    top_stations = stations.sort_values(
        "mean",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_stations,
        x="mean",
        y="station_name",
        orientation="h",
        title="Top 10 Stations by Average Delay",
        labels={
            "mean": "Average Delay (Minutes)",
            "station_name": "Station"
        }
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Station Data")

    st.dataframe(
        stations,
        use_container_width=True
    )

# ==========================================
# TRAIN ANALYSIS
# ==========================================

elif page == "Train Analysis":

    st.header("Train Delay Analysis")

    top_trains = trains.sort_values(
        "mean",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_trains,
        x="train_no",
        y="mean",
        title="Top 10 Trains by Average Delay",
        labels={
            "train_no": "Train Number",
            "mean": "Average Delay (Minutes)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Train Statistics")

    st.dataframe(
        trains,
        use_container_width=True
    )

# ==========================================
# DELAY SEVERITY
# ==========================================

elif page == "Delay Severity":

    st.header("Delay Severity Analysis")

    fig = px.bar(
        categories,
        x=categories.columns[0],
        y="count",
        title="Distribution of Railway Delay Categories",
        labels={
            categories.columns[0]: "Delay Category",
            "count": "Number of Records"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Category Statistics")

    st.dataframe(
        categories,
        use_container_width=True
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "RailPulse India | Railway Delay Analytics "
    "| Data Analytics Project"
)