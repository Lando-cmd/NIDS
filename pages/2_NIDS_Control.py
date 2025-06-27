# 2_NIDS_Control.py
import streamlit as st
import requests

API_BASE = "http://localhost:5000"

st.set_page_config(page_title="NIDS Control Panel", layout="centered")
st.title("🛡️ NIDS Control Panel")

# Check status
status_response = requests.get(f"{API_BASE}/status")
status = status_response.json().get("status", "unknown")
st.markdown(f"**Current Status:** `{status.upper()}`")

# Interface selection
st.subheader("🖧 Select Network Interface")

# Manually define or auto-load these if you want
interfaces = [
    r"\Device\NPF_{D64E4AAE-1441-464E-A7F8-17834F529DF1}",
    r"\Device\NPF_{D07FF2D0-7FCF-4CCB-BD21-CA592E080BDE}",
    r"\Device\NPF_Loopback"
]

selected_iface = st.selectbox("Choose interface to monitor", interfaces)

# Start/Stop Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Start NIDS"):
        res = requests.post(f"{API_BASE}/start", json={"interface": selected_iface})
        if res.status_code == 200:
            st.success(f"NIDS started on {selected_iface}")
        else:
            st.error(res.json().get("error", "Unknown error"))

with col2:
    if st.button("🛑 Stop NIDS"):
        res = requests.post(f"{API_BASE}/stop")
        if res.status_code == 200:
            st.warning("NIDS stopped.")
        else:
            st.error("Failed to stop NIDS.")

# Refresh Status Button
if st.button("🔁 Refresh Status"):
    st.rerun()

st.sidebar.header("Navigation")
