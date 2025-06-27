Python Network Intrusion Detection System (NIDS)
A real-time, Python-based Network Intrusion Detection System designed to monitor, analyze, and detect suspicious activity on a local network.

Features
Live packet sniffing with Scapy

Signature-based alert engine (customizable YAML rules)

Real-time Streamlit dashboard

Top IP talkers and protocol breakdown

Time-based traffic and alert charts

Persistent alert logging (JSON & CSV)

Web UI for start/stop control

Tech Stack
Python 3

Scapy

Streamlit

Flask

Pandas

YAML

Project Structure
NIDS/
├── app.py # Streamlit entry point
├── api_server.py # Flask control API
├── main.py # Main runner (optional)
├── packet_sniffer.py # Packet capture logic
├── signature_engine.py # Alert detection engine
├── packet_stats.json # Real-time stats
├── alerts.csv # Exported alerts
├── alert_log.json # Alert history
├── rules.yaml # Detection rules
├── pages/
│ ├── 1_Home.py # Live dashboard
│ ├── 2_NIDS_Control.py # Control panel

Setup
Install dependencies:
pip install -r requirements.txt

Start the Flask control server:
python api_server.py

Launch the dashboard:
streamlit run app.py

Usage
Use the NIDS Control page to select your interface and start packet capture.

Monitor real-time stats and alerts on the Home page.

Download alerts as CSV for further analysis.

Notes
Requires admin/root privileges to sniff packets.

Designed for local testing and educational use.

License
MIT License
