import streamlit as st

st.set_page_config(page_title="NIDS Console", layout="wide")
st.title("🛡️ Welcome to the NIDS Application")

st.markdown("""
## Network Intrusion Detection System

This application provides real-time network traffic monitoring and intrusion detection capabilities.

### Getting Started

1. **Navigate to NIDS Control** (see sidebar) to select your network interface and start monitoring
2. **View the Home Dashboard** to see live statistics, alerts, and network traffic analysis

### Features

- 📡 Real-time packet capture and analysis
- 🚨 Signature-based intrusion detection
- 📊 Live traffic statistics and visualizations
- 🌐 Top IP talkers tracking
- 📈 Time-based traffic and alert charts
- ⬇️ Export alerts for further analysis

Use the sidebar to navigate between the control panel and dashboard.

**Note:** Packet capture requires administrator/root privileges.
""")
