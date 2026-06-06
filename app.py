import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import datetime

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="NIDS AI System", layout="wide")

st.title("🔐 Network Intrusion Detection System (AI Powered)")
st.caption("Machine Learning-based Cybersecurity Monitoring Dashboard (NSL-KDD)")

# ----------------------------
# LOAD MODEL
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "nids_model.pkl")
model = joblib.load(model_path)

# ----------------------------
# SIDEBAR INPUTS (PROFESSIONAL STYLE)
# ----------------------------
st.sidebar.header("⚙️ Network Parameters")

duration = st.sidebar.number_input("Duration", 0)
src_bytes = st.sidebar.number_input("Source Bytes", 0)
dst_bytes = st.sidebar.number_input("Destination Bytes", 0)
count = st.sidebar.number_input("Connection Count", 0)
srv_count = st.sidebar.number_input("Service Count", 0)

protocol_type = st.sidebar.selectbox("Protocol", ["tcp", "udp", "icmp"])
service = st.sidebar.selectbox("Service", ["http", "ftp", "smtp", "dns", "other"])
flag = st.sidebar.selectbox("Flag", ["SF", "S0", "REJ", "RSTO"])

# ----------------------------
# ENCODING
# ----------------------------
protocol_map = {"tcp": 0, "udp": 1, "icmp": 2}
service_map = {"http": 0, "ftp": 1, "smtp": 2, "dns": 3, "other": 4}
flag_map = {"SF": 0, "S0": 1, "REJ": 2, "RSTO": 3}

# ----------------------------
# MAIN DASHBOARD
# ----------------------------
st.subheader("📡 Intrusion Detection Panel")

col1, col2, col3 = st.columns(3)

if st.button("🚨 Run Intrusion Detection"):

    # ----------------------------
    # FEATURE VECTOR (41 FEATURES)
    # ----------------------------
    features = np.zeros(41)

    features[0] = duration
    features[1] = protocol_map[protocol_type]
    features[2] = service_map[service]
    features[3] = flag_map[flag]
    features[4] = src_bytes
    features[5] = dst_bytes
    features[22] = count
    features[23] = srv_count

    # ----------------------------
    # PREDICTION
    # ----------------------------
    prediction = model.predict([features])
    proba = model.predict_proba([features])

    result_text = "ATTACK DETECTED" if prediction[0] == 1 else "NORMAL TRAFFIC"
    risk_level = "HIGH" if prediction[0] == 1 else "LOW"

    # ----------------------------
    # DISPLAY METRICS
    # ----------------------------
    with col1:
        st.metric("Prediction", result_text)

    with col2:
        st.metric("Confidence", f"{max(proba[0]) * 100:.2f}%")

    with col3:
        st.metric("Risk Level", risk_level)

    # ----------------------------
    # LOGGING SYSTEM
    # ----------------------------
    log = {
        "time": datetime.datetime.now(),
        "protocol": protocol_type,
        "service": service,
        "flag": flag,
        "result": int(prediction[0]),
        "confidence": float(max(proba[0]))
    }

    df_log = pd.DataFrame([log])

    log_file = os.path.join(BASE_DIR, "logs.csv")

    if os.path.exists(log_file):
        df_log.to_csv(log_file, mode="a", header=False, index=False)
    else:
        df_log.to_csv(log_file, index=False)

    st.success("Prediction saved to logs.csv")

# ----------------------------
# ANALYTICS DASHBOARD
# ----------------------------
st.subheader("📊 Security Analytics")

log_file = os.path.join(BASE_DIR, "logs.csv")

if os.path.exists(log_file):
    df = pd.read_csv(log_file)

    attack_count = (df["result"] == 1).sum()
    normal_count = (df["result"] == 0).sum()

    col1, col2 = st.columns(2)

    col1.metric("Total Attacks", attack_count)
    col2.metric("Normal Traffic", normal_count)

    st.bar_chart(df["result"].value_counts())
else:
    st.info("No logs found yet. Run predictions to generate data.")