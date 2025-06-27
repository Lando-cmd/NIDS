# Python Network Intrusion Detection System (NIDS)

This Python-based real-time Network Intrusion Detection System monitors and analyzes local network traffic to detect suspicious activity. It uses Scapy for packet sniffing, a YAML-driven signature engine for alerts, and provides a Streamlit dashboard with live stats, IP talkers, protocol breakdown, and persistent alert logging.

## Features
- Live packet sniffing with Scapy
- Signature-based alert detection using customizable YAML rules
- Real-time dashboard built with Streamlit
- Top IP talkers and protocol traffic breakdown
- Time-based charts for traffic and alerts
- Persistent alert logs saved in JSON and CSV formats
- Web UI to control start/stop of packet capture via Flask API

## Tech Stack
- Python 3
- Scapy
- Streamlit
- Flask
- Pandas
- YAML

## Project Structure
NIDS/
├── app.py               # Streamlit dashboard entry point
├── api_server.py        # Flask API for control
├── main.py              # Optional main runner
├── packet_sniffer.py    # Packet capture logic
├── signature_engine.py  # Alert detection engine
├── packet_stats.json    # Real-time stats file
├── alerts.csv           # Exported alert logs
├── alert_log.json       # Alert history logs
├── rules.yaml           # Detection rules file
├── pages/
│   ├── 1_Home.py        # Live dashboard page
│   ├── 2_NIDS_Control.py # Control panel page

## Setup
Install dependencies:
pip install -r requirements.txt

Start the Flask control server:
python api_server.py

Launch the Streamlit dashboard:
streamlit run app.py

## Usage
- Select network interface and start packet capture via the NIDS Control page
- Monitor live network traffic and alerts on the Home dashboard
- Export alerts to CSV for further analysis

## Notes
- Requires administrator/root privileges to capture packets
- Intended for local testing and educational purposes

## License
MIT License
