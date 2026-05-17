import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="FlexSim Digital Twin Dashboard",
    page_icon="🏭",
    layout="wide"
)

# =========================================
# CUSTOM STYLE
# =========================================

st.markdown("""
<style>

.main {
    background-color: #f5f5f5;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #d71920;
}

.subtitle {
    font-size: 20px;
    color: #555;
}

.recommend-box {
    background-color: white;
    padding: 18px;
    border-left: 6px solid #d71920;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("🏭 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Introduction & Tutorial",
        "Simulation Dashboard"
    ]
)

# =========================================
# PAGE 1
# =========================================

if page == "Introduction & Tutorial":

    st.markdown(
        '<div class="big-title">FlexSim-Based Digital Twin Monitoring System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Interactive Smart Manufacturing Simulation for Assembly Production Monitoring</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # VIDEO
    st.header("🎥 Simulation Demo")

    uploaded_video = st.file_uploader(
        "Upload MP4 Simulation Video",
        type=["mp4"]
    )

    if uploaded_video is not None:
        st.video(uploaded_video)

    else:
        st.info(
            "Upload FlexSim assembly simulation video here."
        )

    st.divider()

    # OVERVIEW
    st.header("🏭 System Overview")

    st.write("""
This dashboard represents a FlexSim-based digital twin monitoring system for automotive assembly manufacturing.

Main Features:
- FlexSim production simulation
- CSV-based monitoring
- KPI visualization
- Bottleneck analysis
- Parameter adjustment
- Smart manufacturing decision support
""")

    st.divider()

    # TUTORIAL
    st.header("⚙ Tutorial Workflow")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.success("1️⃣ Run FlexSim")
    col2.info("2️⃣ Export CSV")
    col3.warning("3️⃣ Upload CSV")
    col4.success("4️⃣ Adjust Parameters")
    col5.error("5️⃣ Observe KPI")

    st.divider()

    # FUTURE SECTION
    st.header("⌚ Future Integration Concept")

    st.info("""
Future Industry 4.0 integration may include:
- Smart wearable monitoring
- AI ergonomic assistance
- Smartwatch posture notification
- Human-centered manufacturing support

This section is presented as future integration concept only.
""")

# =========================================
# PAGE 2
# =========================================

elif page == "Simulation Dashboard":

    st.markdown(
        '<div class="big-title">Interactive Simulation Dashboard</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # =========================================
    # CSV UPLOAD
    # =========================================

    st.header("📂 Upload FlexSim CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV Result",
        type=["csv"]
    )

    # =========================================
    # DATA
    # =========================================

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            st.success(
                f"Uploaded: {uploaded_file.name}"
            )

        except:
            st.error(
                "CSV format not compatible. Using sample dataset."
            )

            uploaded_file = None

    if uploaded_file is None:

        np.random.seed(42)

        df = pd.DataFrame({
            "Station": [
                "Machining",
                "Welding",
                "Painting",
                "Assembly",
                "QC"
            ],

            "Output": np.random.randint(40, 120, 5),

            "Utilization": np.random.randint(55, 98, 5),

            "Queue": np.random.randint(5, 25, 5),

            "Staytime": np.random.randint(10, 100, 5)
        })

        st.info(
            "Using sample manufacturing dataset."
        )

    st.divider()

    # =========================================
    # PARAMETER ADJUSTMENT
    # =========================================

    st.header("⚙ Interactive Parameter Adjustment")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        operator_count = st.slider(
            "Operator Count",
            1,
            10,
            3
        )

    with col2:

        machine_capacity = st.slider(
            "Machine Capacity",
            1,
            10,
            2
        )

    with col3:

        taskexecuter_count = st.slider(
            "TaskExecuter Count",
            1,
            10,
            3
        )

    with col4:

        queue_capacity = st.slider(
            "Queue Capacity",
            1,
            20,
            10
        )

    # =========================================
    # KPI CALCULATION
    # =========================================

    output_factor = 1 + (machine_capacity * 0.08)

    util_factor = max(
        0.6,
        1 - operator_count * 0.03
    )

    queue_factor = max(
        0.4,
        1 - queue_capacity * 0.02
    )

    df["Adjusted Output"] = (
        df["Output"] * output_factor
    )

    df["Adjusted Utilization"] = (
        df["Utilization"] * util_factor
    )

    df["Adjusted Queue"] = (
        df["Queue"] * queue_factor
    )

    st.divider()

    # =========================================
    # KPI
    # =========================================

    st.header("📊 Production Monitoring")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "🏭 Total Output",
        int(df["Adjusted Output"].sum())
    )

    k2.metric(
        "📈 Avg Utilization",
        f"{df['Adjusted Utilization'].mean():.1f}%"
    )

    k3.metric(
        "📦 Queue Content",
        int(df["Adjusted Queue"].sum())
    )

    k4.metric(
        "⏱ Avg Staytime",
        f"{df['Staytime'].mean():.1f}"
    )

    st.divider()

    # =========================================
    # CHARTS
    # =========================================

    st.header("📈 Manufacturing Visualization")

    chart1, chart2 = st.columns(2)

    with chart1:

        fig_output = px.bar(
            df,
            x="Station",
            y="Adjusted Output",
            color="Station",
            title="Output per Station"
        )

        st.plotly_chart(
            fig_output,
            use_container_width=True
        )

    with chart2:

        fig_util = px.pie(
            df,
            names="Station",
            values="Adjusted Utilization",
            title="Machine Utilization"
        )

        st.plotly_chart(
            fig_util,
            use_container_width=True
        )

    chart3, chart4 = st.columns(2)

    with chart3:

        fig_queue = px.bar(
            df,
            x="Station",
            y="Adjusted Queue",
            color="Station",
            title="Queue Content"
        )

        st.plotly_chart(
            fig_queue,
            use_container_width=True
        )

    with chart4:

        fig_stay = px.line(
            df,
            x="Station",
            y="Staytime",
            markers=True,
            title="Average Staytime"
        )

        st.plotly_chart(
            fig_stay,
            use_container_width=True
        )

    st.divider()

    # =========================================
    # BOTTLENECK
    # =========================================

    st.header("🚨 Bottleneck & Recommendation")

    bottleneck_station = df.loc[
        df["Adjusted Queue"].idxmax(),
        "Station"
    ]

    st.error(
        f"Bottleneck detected at: {bottleneck_station}"
    )

    recommendations = []

    if df["Adjusted Utilization"].mean() > 85:

        recommendations.append(
            "Increase operator allocation to reduce excessive utilization."
        )

    if df["Adjusted Queue"].sum() > 60:

        recommendations.append(
            "Reduce queue congestion by improving synchronization flow."
        )

    if bottleneck_station == "Assembly":

        recommendations.append(
            "Redistribute workload at Assembly Station."
        )

    if machine_capacity < 4:

        recommendations.append(
            "Increase machine capacity to improve throughput."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Production flow is currently stable."
        )

    for rec in recommendations:

        st.markdown(
            f"""
            <div class="recommend-box">
            💡 {rec}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # =========================================
    # FUTURE SECTION
    # =========================================

    st.header("⌚ Future Smart Wearable Concept")

    st.info("""
Future integration may include:
- Smartwatch notification
- Worker posture alert
- AI ergonomic assistance
- Human-centered manufacturing

This feature is conceptual only and not directly generated from FlexSim simulation output.
""")