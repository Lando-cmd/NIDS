# 2_NIDS_Control.py
import streamlit as st
import sys
import os

# Add parent directory to path to import nids_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nids_manager import start_nids, stop_nids, get_nids_status

# Try to import scapy to get interfaces
try:
    from scapy.all import get_if_list
    interfaces = get_if_list()
except Exception as e:
    st.warning(f"Could not load network interfaces: {e}")
    # Fallback interfaces
    interfaces = [
        r"\Device\NPF_{D64E4AAE-1441-464E-A7F8-17834F529DF1}",
        r"\Device\NPF_{D07FF2D0-7FCF-4CCB-BD21-CA592E080BDE}",
        r"\Device\NPF_Loopback"
    ]

st.set_page_config(page_title="NIDS Control Panel", layout="centered")
st.title("🛡️ NIDS Control Panel")

# Check status
status_info = get_nids_status()
status = status_info.get("status", "unknown")
current_interface = status_info.get("interface", "None")

st.markdown(f"**Current Status:** `{status.upper()}`")
if status == "running":
    st.markdown(f"**Monitoring Interface:** `{current_interface}`")

# Interface selection
st.subheader("🖧 Select Network Interface")

selected_iface = st.selectbox("Choose interface to monitor", interfaces)

# Start/Stop Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Start NIDS"):
        result = start_nids(selected_iface)
        if result["status"] == "started":
            st.success(f"NIDS started on {selected_iface}")
            st.rerun()
        elif result["status"] == "already_running":
            st.info(f"NIDS is already running on {result.get('interface', 'unknown interface')}")
        else:
            st.error("Failed to start NIDS")

with col2:
    if st.button("🛑 Stop NIDS"):
        result = stop_nids()
        if result["status"] == "stopped":
            st.warning("NIDS stopped.")
            st.rerun()
        elif result["status"] == "not_running":
            st.info("NIDS is not currently running")
        else:
            st.error("Failed to stop NIDS")

# Refresh Status Button
if st.button("🔁 Refresh Status"):
    st.rerun()

st.sidebar.header("Navigation")
