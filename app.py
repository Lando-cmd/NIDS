import streamlit as st
import requests
import pandas as pd

# --- Configuration ---
st.set_page_config(
    page_title="NIDS Dashboard",
    page_icon="🛡️",
    layout="wide",
)
API_URL = "http://127.0.0.1:8000"
REFRESH_INTERVAL_SECONDS = 5


# --- Functions ---

def auto_refresh(timeout_secs=5):
    """Injects a meta refresh tag to reload the page."""
    st.html(f'<meta http-equiv="refresh" content="{timeout_secs}">')


def display_dashboard():
    """
    Fetches the latest data from the NIDS API and displays it.
    Returns True if NIDS is running, False otherwise.
    """
    is_running = False  # Default to False
    try:
        # Check NIDS status first
        status_response = requests.get(f"{API_URL}/status", timeout=1)
        if status_response.status_code == 200:
            is_running = status_response.json().get("is_running", False)

        # --- Sidebar Controls ---
        with st.sidebar:
            st.header("🕹️ NIDS Control")
            if is_running:
                st.success("NIDS is RUNNING", icon="🟢")
            else:
                st.warning("NIDS is STOPPED", icon="🟡")

            if st.button("▶️ Start NIDS"):
                try:
                    requests.post(f"{API_URL}/start", timeout=1)
                    st.success("Start command sent!")
                    st.rerun()
                except requests.RequestException:
                    st.error("API connection failed.")

            if st.button("⏹️ Stop NIDS"):
                try:
                    requests.post(f"{API_URL}/stop", timeout=1)
                    st.success("Stop command sent!")
                    st.rerun()
                except requests.RequestException:
                    st.error("API connection failed.")

        # --- Main Dashboard Area ---
        # Display a status message at the top if NIDS is stopped, but DON'T exit.
        if not is_running:
            st.info("NIDS is stopped. Displaying last captured data. Auto-refresh is paused.", icon="ℹ️")

        # --- Always attempt to render the data ---
        stats_response = requests.get(f"{API_URL}/stats", timeout=2)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            st.subheader("Real-time Statistics")
            st.metric(label="Total Packets Captured", value=stats.get("total_packets", 0))

            col1, col2 = st.columns(2)
            with col1:
                st.write("Protocol Distribution")
                proto_counts = stats.get("protocol_counts", {})
                if proto_counts:
                    proto_df = pd.DataFrame(proto_counts.items(), columns=['Protocol', 'Count'])
                    st.bar_chart(proto_df.set_index('Protocol'))
                else:
                    st.write("No protocol data available.")

            with col2:
                st.write("Top Talkers (IP Addresses)")
                ip_counts = stats.get("ip_counts", {})
                if ip_counts:
                    ip_df = pd.DataFrame(ip_counts.items(), columns=['IP Address', 'Count'])
                    ip_df = ip_df.nlargest(10, 'Count')
                    st.table(ip_df)
                else:
                    st.write("No IP data available.")

        st.divider()

        alerts_response = requests.get(f"{API_URL}/alerts", timeout=2)
        if alerts_response.status_code == 200:
            alerts = alerts_response.json()
            st.subheader("🚨 Security Alerts")
            if alerts:
                alerts_df = pd.DataFrame(alerts)
                alerts_df = alerts_df.sort_values(by="timestamp", ascending=False)
                alerts_df['timestamp'] = pd.to_datetime(alerts_df['timestamp'], unit='s').dt.strftime(
                    '%Y-%m-%d %H:%M:%S')
                st.dataframe(
                    alerts_df[['timestamp', 'message', 'src_ip', 'dst_ip', 'protocol', 'dst_port']],
                    use_container_width=True
                )
            else:
                st.info("No security alerts detected.")

        return is_running

    except requests.exceptions.RequestException:
        st.sidebar.error("NIDS is OFFLINE", icon="🔴")
        st.error("API connection failed. Please ensure the main NIDS application (`main.py`) is running.", icon="🔴")
        return False


# --- Main Logic ---
is_nids_active = display_dashboard()

# Only enable auto-refresh if the NIDS is confirmed to be active.
if is_nids_active:
    auto_refresh(REFRESH_INTERVAL_SECONDS)
