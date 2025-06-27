# 1_Home.py
import streamlit as st
import json
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="NIDS Dashboard", layout="wide")
st.title("📡 Python NIDS Dashboard")

col1, col2 = st.columns(2)

# Load and display stats
try:
    with open("packet_stats.json", "r") as f:
        stats = json.load(f)
except Exception as e:
    st.error(f"Failed to load packet stats: {e}")
    stats = {
        "total_packets": 0,
        "alerts": 0,
        "protocols": {},
        "ip_stats": {},
        "traffic_timeline": {},
        "alert_timeline": {}
    }

# Debug: uncomment to see raw data
# st.write("DEBUG: packet_stats.json content:", stats)

col1.metric("📦 Total Packets", stats.get("total_packets", 0))
col2.metric("🚨 Alerts Triggered", stats.get("alerts", 0))

# Protocol Breakdown
st.subheader("📊 Protocol Breakdown")
if stats.get("protocols"):
    st.bar_chart(stats["protocols"])
else:
    st.write("No protocol data yet.")

# Top IP Talkers
st.subheader("🌐 Top IP Talkers")
ip_stats = stats.get("ip_stats", {})

if ip_stats:
    top_ips = sorted(ip_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    ip_labels = [ip for ip, _ in top_ips]
    ip_counts = [count for _, count in top_ips]

    st.bar_chart(data=dict(zip(ip_labels, ip_counts)))
else:
    st.write("No IP traffic recorded yet.")

# Time-Based Packet & Alert Stats
st.subheader("📈 Packet & Alert Timeline (per minute)")
timeline = stats.get("traffic_timeline", {})
alertline = stats.get("alert_timeline", {})

if timeline:
    df = pd.DataFrame({
        "Packets": pd.Series(timeline),
        "Alerts": pd.Series(alertline)
    }).fillna(0).astype(int).sort_index()

    st.line_chart(df)
else:
    st.write("No time-based data recorded yet.")

# Alert Log
st.subheader("🚨 Alert Log")
log_file = Path("alert_log.json")

if not log_file.exists():
    st.info("Waiting for alerts...")
else:
    with open(log_file, "r") as f:
        lines = f.readlines()

    if not lines:
        st.info("No alerts yet.")
    else:
        lines = lines[-50:]  # Limit to last 50
        for line in reversed(lines):
            try:
                alert = json.loads(line)
                with st.expander(f"🔴 {alert['name']} @ {alert['timestamp']}"):
                    st.write(f"**Description**: {alert['description']}")
                    st.code(alert['summary'])
            except json.JSONDecodeError:
                continue

st.subheader("⬇️ Download Alerts as CSV")
alerts_csv = Path("alerts.csv")
if alerts_csv.exists():
    with open(alerts_csv, "rb") as f:
        st.download_button("Download alerts.csv", f, file_name="alerts.csv")
else:
    st.info("No alerts have been exported yet.")

st.sidebar.header("Navigation")
