# Python Network Intrusion Detection System (NIDS)

This Python-based real-time Network Intrusion Detection System monitors and analyzes local network traffic to detect suspicious activity. It uses Scapy for packet sniffing, a YAML-driven signature engine for alerts, and provides a Streamlit dashboard with live stats, IP talkers, protocol breakdown, and persistent alert logging.

## Features
- Live packet sniffing with Scapy
- Signature-based alert detection using customizable YAML rules
- Real-time dashboard built with Streamlit
- Top IP talkers and protocol traffic breakdown
- Time-based charts for traffic and alerts
- Persistent alert logs saved in JSON and CSV formats
- Integrated control panel to start/stop packet capture directly from the dashboard

## Tech Stack
- Python 3
- Scapy
- Streamlit
- Pandas
- YAML

## Project Structure
NIDS/
├── app.py               # Streamlit dashboard entry point
├── nids_manager.py      # NIDS control module
├── packet_sniffer.py    # Packet capture logic
├── signature_engine.py  # Alert detection engine
├── packet_stats.json    # Real-time stats file
├── alerts.csv           # Exported alert logs
├── alert_log.json       # Alert history logs
├── signatures.yaml      # Detection rules file
├── pages/
│   ├── 1_Home.py        # Live dashboard page
│   ├── 2_NIDS_Control.py # Control panel page

## Setup
Install dependencies:
pip install -r requirements.txt

Launch the application:
streamlit run app.py

## Usage
- Navigate to the NIDS Control page from the sidebar
- Select your network interface and click "Start NIDS" to begin packet capture
- Monitor live network traffic and alerts on the Home dashboard
- Use the Control page to stop/start the packet sniffer as needed
- Export alerts to CSV for further analysis

## Notes
- Requires administrator/root privileges to capture packets
- Intended for local testing and educational purposes

## License
MIT License
