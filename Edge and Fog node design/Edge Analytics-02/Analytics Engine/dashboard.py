import streamlit as st
from DatasetMaker import (
    create_database,
    get_total_detections,
    get_average_sheet_count,
    get_max_sheet_count,
    get_min_sheet_count,
    get_max_tilt,
    get_min_tilt,
    get_avg_tilt,
    get_latest_detection,
    get_data
)
import pandas as pd
import json
import time

if "db_ready" not in st.session_state:
    create_database()
    st.session_state.db_ready = True

st.sidebar.divider()
auto_refresh = st.sidebar.toggle("Auto-refresh (10s)", value=False)
if auto_refresh:
    placeholder = st.empty()
    for i in range(10, 0, -1):
        placeholder.caption(f"Refreshing in {i}s...")
        time.sleep(1)
    st.rerun()
st.markdown("""
<style>
[data-testid="stSidebar"] {
    padding-top: 2rem;
}
[data-testid="stSidebar"] .stButton button {
    width: 100%;
    text-align: left;
    background: transparent;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 15px;
    color: inherit;
    cursor: pointer;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] .stButton button:focus {
    background: rgba(255,255,255,0.12);
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Drone Parameter Dashboard")
    st.divider()
    if st.button(" Overview "):
        st.session_state.page = "Overview"
    if st.button(" Charts "):
        st.session_state.page = "Charts"
    if st.button(" Total Detections "):
        st.session_state.page = "All Detections"

if "page" not in st.session_state:
    st.session_state.page = "Overview"

page = st.session_state.page

rows = get_data()
df = pd.DataFrame(rows, columns=["id", "filename", "received_timestamp", "sheet_count", "tilt", "density",
                                 "estimation_method"]) if rows else pd.DataFrame()

if not df.empty:
    df["timestamp_short"] = pd.to_datetime(df["received_timestamp"]).dt.strftime("%d %b %y %H:%M")

# ── PAGE: Overview ──────────────────────────────────────────────────────────
if page == "Overview":
    st.title("Overview")

    st.subheader("Sheet Count Analytics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Detections", get_total_detections())
    with col2:
        st.metric("Average Sheets", get_average_sheet_count())
    with col3:
        st.metric("Max Sheets", get_max_sheet_count())
    with col4:
        st.metric("Min Sheets", get_min_sheet_count())

    st.subheader("Tilt Analytics")
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Average Tilt", f"{get_avg_tilt()}°")
    with col6:
        st.metric("Max Tilt", f"{get_max_tilt()}°")
    with col7:
        st.metric("Min Tilt", f"{get_min_tilt()}°")

    st.subheader("Latest Detection")
    latest = get_latest_detection()
    if latest:
        try:
            density = json.loads(latest[5]) if latest[5] else {}
        except (json.JSONDecodeError, TypeError):
            density = latest[5]

        ts = pd.to_datetime(latest[2]).strftime("%d %b %Y  %H:%M:%S")
        if isinstance(density, list) and len(density) > 0:
            density_str = f"{len(density)} points · avg {round(sum(density) / len(density), 3)}"
        else:
            density_str = "N/A"

        with st.container(border=True):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.caption("Filename")
                st.write(latest[1])
                st.caption("Timestamp")
                st.write(ts)
            with col_b:
                st.caption("Sheet Count")
                st.write(latest[3])
                st.caption("Tilt")
                st.write(f"{latest[4]}°")
            with col_c:
                st.caption("Method")
                st.write(latest[6])
                st.caption("Density")
                st.write(density_str)
    else:
        st.info("No detections recorded yet.")

# ── PAGE: Charts ────────────────────────────────────────────────────────────
elif page == "Charts":
    st.title("Charts")
    if not df.empty:
        st.subheader("Sheet Count Over Time")
        st.line_chart(df.set_index("timestamp_short")["sheet_count"])

        st.subheader("Sheet Count Per Image")
        st.bar_chart(df.set_index("filename")["sheet_count"])
    else:
        st.info("No data available yet.")

# ── PAGE: All Detections ────────────────────────────────────────────────────
elif page == "All Detections":
    st.title("All Detections")
    if not df.empty:
        display_df = df[["id", "filename", "timestamp_short", "sheet_count", "tilt", "estimation_method"]].rename(
            columns={
                "timestamp_short": "received_timestamp",
                "estimation_method": "method"
            })
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No data available yet.")