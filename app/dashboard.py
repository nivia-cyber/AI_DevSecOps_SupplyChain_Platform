import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI CI/CD Supply Chain Security Center",
    layout="wide",
    page_icon="🛡",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(BASE_DIR,"reports","security_report.json")

# --------------------------------------------------
# THEME
# --------------------------------------------------


st.markdown("""
<style>

/* Main background */
.stApp{
background-color:#0b1220;
}

/* Sidebar */
section[data-testid="stSidebar"]{
background-color:#020617;
border-right:2px solid #0ea5e9;
}

/* Sidebar text */
section[data-testid="stSidebar"] *{
color:#ffffff !important;
font-size:16px;
}

/* Sidebar spacing */
div[role="radiogroup"] > label{
margin-bottom:12px;
}

/* Headings */
h1,h2,h3{
color:#38bdf8 !important;
font-weight:700;
}

/* Global text visibility */
p,span,label,div{
color:#e5e7eb !important;
font-size:16px;
}

/* Metric cards */
[data-testid="stMetric"]{
background-color:#111827;
padding:20px;
border-radius:14px;
box-shadow:0 0 18px #0ea5e9;
}

/* Metric labels */
[data-testid="stMetricLabel"]{
color:#cbd5f5 !important;
font-size:18px !important;
font-weight:600;
}

/* Metric numbers (VERY IMPORTANT) */
[data-testid="stMetricValue"]{
color:#ffffff !important;
font-size:32px !important;
font-weight:bold !important;
}

/* Tables */
[data-testid="stDataFrame"]{
color:white !important;
}

/* Info boxes */
[data-testid="stAlert"]{
font-size:18px;
}

/* Artifact details visibility */
.stMarkdown p{
color:#f1f5f9 !important;
font-size:17px;
}

/* Upload box styling */
[data-testid="stFileUploader"]{
background-color:#111827;
border-radius:12px;
padding:15px;
border:1px solid #0ea5e9;
}

/* Upload drag area */
[data-testid="stFileUploader"] section{
background-color:#020617 !important;
border:1px dashed #0ea5e9 !important;
}

/* Upload text */
[data-testid="stFileUploader"] label{
color:#e5e7eb !important;
font-size:15px;
}

/* Browse button */
[data-testid="stFileUploader"] button{
background-color:#0ea5e9 !important;
color:white !important;
border-radius:6px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🛡 AI DevSecOps SOC")

menu = st.sidebar.radio(
"Navigation",
[
"Dashboard",
"Threat Intelligence",
"Artifact Analysis",
"Risk Analytics",
"MITRE Mapping",
"CI/CD Status"
]
)

# --------------------------------------------------
# LOAD REPORT
# --------------------------------------------------

if not os.path.exists(REPORT_PATH):
    st.warning("⚠ Run pipeline first:\n\npython app/run_pipeline.py clean")
    st.stop()

with open(REPORT_PATH) as f:
    data = json.load(f)

if not isinstance(data,list):
    data = [data]

df = pd.DataFrame(data)

if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"],errors="coerce")
    df = df.dropna(subset=["timestamp"])

latest = df.iloc[-1]

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if menu=="Dashboard":

    st.title("🚀 AI DevSecOps CI/CD Security Center")

    total_builds = len(df)

    deployed = len(df[df["deployment"]=="DEPLOYED"]) if "deployment" in df else 0
    blocked = len(df[df["deployment"]=="BLOCKED"]) if "deployment" in df else 0

    avg_risk = round(df["risk_score"].mean(),2)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Builds",total_builds)
    c2.metric("Deployed",deployed)
    c3.metric("Blocked",blocked)
    c4.metric("Average Risk",avg_risk)

    st.divider()

    # ---------------- RISK GAUGE ----------------

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest["risk_score"],
        title={"text":"Current Risk Score"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"white"},
            "steps":[
                {"range":[0,30],"color":"green"},
                {"range":[30,60],"color":"yellow"},
                {"range":[60,85],"color":"orange"},
                {"range":[85,100],"color":"red"}
            ]
        }
    ))

    st.plotly_chart(gauge,use_container_width=True)

    st.markdown("""
### Risk Score Interpretation

🟢 **0 – 30 → LOW Risk**

🟡 **30 – 60 → MEDIUM Risk**

🟠 **60 – 85 → HIGH Risk**

🔴 **85 – 100 → CRITICAL Risk**
""")

    st.divider()

    # --------------------------------------------------
    # ARTIFACT UPLOAD
    # --------------------------------------------------

    st.subheader("📦 Upload Artifact")

    uploaded_file = st.file_uploader(
        "Upload artifact (.py or .txt)",
        type=["py","txt"]
    )

    if uploaded_file:

        save_path = os.path.join(BASE_DIR,"dataset","current_build.py")

        with open(save_path,"wb") as f:
            f.write(uploaded_file.read())

        st.success("Artifact uploaded successfully. Running security scan...")

        if st.button("Run Security Scan"):

            import subprocess

            with st.spinner("Running CI/CD Security Pipeline..."):

                subprocess.run(
                    ["python","app/run_pipeline.py"],
                    cwd=BASE_DIR
                )

            st.success("Scan completed.")

            st.rerun()


# --------------------------------------------------
# THREAT INTELLIGENCE
# --------------------------------------------------

elif menu=="Threat Intelligence":

    st.title("📈 Threat Timeline")

    df["severity"] = df["risk_score"].apply(
        lambda x:
        "LOW" if x<30 else
        "MEDIUM" if x<60 else
        "HIGH" if x<85 else
        "CRITICAL"
    )

    fig = px.line(
        df,
        x="timestamp",
        y="risk_score",
        markers=True,
        color="severity",
        color_discrete_map={
            "LOW":"green",
            "MEDIUM":"yellow",
            "HIGH":"orange",
            "CRITICAL":"red"
        },
        hover_data=["severity","deployment"]
    )

    fig.update_yaxes(range=[0,100])

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# ARTIFACT ANALYSIS
# --------------------------------------------------

elif menu=="Artifact Analysis":

    st.title("🔍 Artifact Intelligence")

    st.write("Artifact:",latest.get("artifact","N/A"))
    st.write("SHA256:",latest.get("sha256","N/A"))
    st.write("Severity:",latest.get("status","N/A"))
    st.write("Risk Score:",latest.get("risk_score","N/A"))

    st.subheader("Extracted Features")

    features = latest.get("features",{})

    if features:

        feat_df = pd.DataFrame(
        list(features.items()),
        columns=["Feature","Value"]
        )

        st.dataframe(feat_df)

    else:
        st.info("No features extracted")

# --------------------------------------------------
# RISK ANALYTICS
# --------------------------------------------------

elif menu=="Risk Analytics":

    st.title("📊 Risk Distribution")

    df["severity"] = df["risk_score"].apply(
        lambda x:
        "LOW" if x<30 else
        "MEDIUM" if x<60 else
        "HIGH" if x<85 else
        "CRITICAL"
    )

    fig = px.histogram(
        df,
        x="risk_score",
        color="severity",
        nbins=20,
        hover_data=["severity","deployment"]
    )

    fig.update_xaxes(range=[0,100])

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# MITRE MAPPING
# --------------------------------------------------

elif menu=="MITRE Mapping":

    st.title("🎯 MITRE Techniques")

    techniques = []

    for entry in data:
        techniques.extend(entry.get("mitre_techniques",[]))

    if techniques:

        tech_df = pd.DataFrame(
        techniques,
        columns=["Technique"]
        )

        count_df = tech_df.value_counts().reset_index(name="Count")

        fig = px.bar(
        count_df,
        x="Technique",
        y="Count",
        color="Count"
        )

        st.plotly_chart(fig,use_container_width=True)

    else:
        st.warning("⚠ No MITRE techniques detected")

# --------------------------------------------------
# CI/CD STATUS
# --------------------------------------------------

elif menu=="CI/CD Status":

    st.title("🚦 Deployment Panel")

    deployment = latest.get("deployment","UNKNOWN")

    if deployment=="DEPLOYED":
        st.success("✅ Artifact deployed to production")

    elif deployment=="BLOCKED":
        st.error("❌ Deployment blocked by policy")

    else:
        st.warning("⚠ Unknown deployment status")

    st.write("Risk Score:",latest["risk_score"])
    st.write("Severity:",latest["status"])
    st.write("Reason:",latest.get("reason","Policy threshold"))

    st.divider()

    st.dataframe(
    df.sort_values("timestamp",ascending=False)
    )