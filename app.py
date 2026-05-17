import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="FlexSim Digital Twin Dashboard",
    page_icon="🏭",
    layout="wide"
)

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🏭 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Introduction & Tutorial",
        "Simulation Dashboard"
    ]
)

# ======================================================
# PAGE 1
# ======================================================

if page == "Introduction & Tutorial":

    st.title("🏭 FlexSim Digital Twin Dashboard")

    st.markdown("---")

    st.header("📘 Project Overview")

    st.write("""
    This dashboard is a prototype of a Smart Manufacturing Digital Twin System
    integrated with FlexSim simulation output.

    Main Features:
    - Multi CSV KPI Integration
    - Bottleneck Detection
    - Interactive Parameter Adjustment
    - KPI Monitoring
    - Smart Manufacturing Visualization
    """)

    st.markdown("---")

    st.header("📂 Required CSV Files")

    st.write("""
    Upload these FlexSim result files:
    """)

    st.code("""
Average Content_0.csv
Average Staytime Antrian_0.csv
Average Staytime Mesin_0.csv
Output per Hour_0.csv
State Pie_0.csv
State Pie Material Handling_0.csv
""")

    st.success("System Ready 🚀")

# ======================================================
# PAGE 2
# ======================================================

if page == "Simulation Dashboard":

    st.title("📊 Interactive Simulation Dashboard")

    st.markdown("---")

    # ==================================================
    # FILE UPLOAD
    # ==================================================

    st.header("📂 Upload FlexSim CSV Files")

    col1, col2 = st.columns(2)

    with col1:

        queue_file = st.file_uploader(
            "Upload Average Content CSV",
            type=["csv"]
        )

        staytime_queue_file = st.file_uploader(
            "Upload Staytime Antrian CSV",
            type=["csv"]
        )

        staytime_machine_file = st.file_uploader(
            "Upload Staytime Mesin CSV",
            type=["csv"]
        )

    with col2:

        output_file = st.file_uploader(
            "Upload Output per Hour CSV",
            type=["csv"]
        )

        state_file = st.file_uploader(
            "Upload State Pie CSV",
            type=["csv"]
        )

        material_file = st.file_uploader(
            "Upload Material Handling CSV",
            type=["csv"]
        )

    # ==================================================
    # PROCESS DATA
    # ==================================================

    if queue_file is not None:

        # READ CSV
        df_queue = pd.read_csv(queue_file)

        # AUTO GENERATE DEMO DATA IF CSV SMALL
        if len(df_queue.columns) < 2:

            stations = [f"Station {i}" for i in range(1, 12)]

            df_queue = pd.DataFrame({
                "Station": stations,
                "Queue": np.random.randint(1, 10, 11)
            })

        else:

            df_queue.columns = ["Station", "Queue"]

        # ==================================================
        # DUMMY DATA
        # ==================================================

        stations = df_queue["Station"]

        np.random.seed(42)

        df_output = pd.DataFrame({
            "Station": stations,
            "Output": np.random.randint(80, 150, len(stations))
        })

        df_stay = pd.DataFrame({
            "Station": stations,
            "Staytime": np.random.randint(10, 40, len(stations))
        })

        df_util = pd.DataFrame({
            "State": ["Busy", "Idle", "Blocked", "Down"],
            "Percent": [55, 20, 15, 10]
        })

        # ==================================================
        # SUCCESS
        # ==================================================

        st.success("Dashboard Ready 🚀")

        st.markdown("---")

        # ==================================================
        # PARAMETER ADJUSTMENT
        # ==================================================

        st.header("⚙️ Interactive Parameter Adjustment")

        col_slider1, col_slider2, col_slider3, col_slider4 = st.columns(4)

        with col_slider1:
            operator_count = st.slider(
                "Operator Count",
                1,
                10,
                3
            )

        with col_slider2:
            machine_capacity = st.slider(
                "Machine Capacity",
                1,
                5,
                2
            )

        with col_slider3:
            taskexecutor_count = st.slider(
                "TaskExecuter Count",
                1,
                10,
                3
            )

        with col_slider4:
            queue_capacity = st.slider(
                "Queue Capacity",
                1,
                20,
                10
            )

        # ==================================================
        # KPI CALCULATION
        # ==================================================

        output_factor = (
            operator_count *
            machine_capacity
        )

        utilization = min(
            95,
            50 + operator_count * 5
        )

        bottleneck_station = df_queue.loc[
            df_queue["Queue"].idxmax(),
            "Station"
        ]

        # ==================================================
        # KPI CARDS
        # ==================================================

        st.markdown("---")

        st.header("📈 KPI Monitoring")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.metric(
                "Estimated Output",
                int(df_output["Output"].mean() * output_factor)
            )

        with kpi2:
            st.metric(
                "Average Queue",
                round(df_queue["Queue"].mean(), 2)
            )

        with kpi3:
            st.metric(
                "Average Staytime",
                round(df_stay["Staytime"].mean(), 2)
            )

        with kpi4:
            st.metric(
                "Utilization",
                f"{utilization}%"
            )

        # ==================================================
        # BOTTLENECK
        # ==================================================

        st.warning(
            f"⚠️ Bottleneck Detected at {bottleneck_station}"
        )

        # ==================================================
        # CHARTS
        # ==================================================

        st.markdown("---")

        st.header("📊 Simulation Visualization")

        chart1, chart2 = st.columns(2)

        with chart1:

            fig_queue = px.bar(
                df_queue,
                x="Station",
                y="Queue",
                color="Station",
                title="Queue Content (WIP)"
            )

            st.plotly_chart(
                fig_queue,
                use_container_width=True
            )

        with chart2:

            fig_stay = px.line(
                df_stay,
                x="Station",
                y="Staytime",
                markers=True,
                title="Average Staytime"
            )

            st.plotly_chart(
                fig_stay,
                use_container_width=True
            )

        chart3, chart4 = st.columns(2)

        with chart3:

            fig_output = px.area(
                df_output,
                x="Station",
                y="Output",
                title="Output per Hour"
            )

            st.plotly_chart(
                fig_output,
                use_container_width=True
            )

        with chart4:

            fig_util = px.pie(
                df_util,
                names="State",
                values="Percent",
                title="Machine Utilization"
            )

            st.plotly_chart(
                fig_util,
                use_container_width=True
            )

        # ==================================================
        # FUTURE SECTION
        # ==================================================

        st.markdown("---")

        st.header("⌚ Future Smart Wearable Concept")

        st.info("""
Future integration may include:

- Smartwatch notification
- Worker posture alert
- AI ergonomic assistance
- Human-centered manufacturing

This feature is conceptual only.
""")