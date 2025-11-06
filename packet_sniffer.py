# packet_sniffer.py
from scapy.all import sniff
from scapy.layers.inet import IP
from signature_engine import load_signatures, match_signature
from collections import defaultdict
from datetime import datetime
import json
import csv
import os
import time

# File paths
ALERT_LOG_PATH = "alert_log.json"
ALERT_CSV_PATH = "alerts.csv"
STATS_LOG_PATH = "packet_stats.json"

# Load signatures
signatures = load_signatures()

# Global statistics
stats = {
    "total_packets": 0,
    "alerts": 0,
    "protocols": defaultdict(int),
    "ip_stats": defaultdict(int),
    "traffic_timeline": defaultdict(int),
    "alert_timeline": defaultdict(int)
}

# Track last save time for batched writes
last_save_time = time.time()
SAVE_INTERVAL = 10  # Save stats every 10 seconds instead of every packet


# Log alert to JSON + CSV
def log_alert(alert_data):
    alert_data["timestamp"] = datetime.now().isoformat()

    # Write to JSON
    try:
        with open(ALERT_LOG_PATH, "a") as f:
            f.write(json.dumps(alert_data) + "\n")
    except Exception as e:
        print(f"Failed to write alert to JSON: {e}")

    # Write to CSV
    try:
        file_exists = os.path.isfile(ALERT_CSV_PATH)
        with open(ALERT_CSV_PATH, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "name", "description", "summary"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(alert_data)
    except Exception as e:
        print(f"Failed to write alert to CSV: {e}")


# Save stats to JSON
def save_stats():
    try:
        # Convert defaultdicts to regular dicts for JSON serialization
        stats_to_save = {
            "total_packets": stats["total_packets"],
            "alerts": stats["alerts"],
            "protocols": dict(stats["protocols"]),
            "ip_stats": dict(stats["ip_stats"]),
            "traffic_timeline": dict(stats["traffic_timeline"]),
            "alert_timeline": dict(stats["alert_timeline"])
        }
        with open(STATS_LOG_PATH, "w") as f:
            json.dump(stats_to_save, f)
    except Exception as e:
        print(f"Failed to write stats: {e}")


# Process each packet
def packet_callback(packet):
    stats["total_packets"] += 1

    # Protocol classification
    if packet.haslayer("TCP"):
        stats["protocols"]["TCP"] += 1
    elif packet.haslayer("UDP"):
        stats["protocols"]["UDP"] += 1
    elif packet.haslayer("ICMP"):
        stats["protocols"]["ICMP"] += 1
    else:
        stats["protocols"]["Other"] += 1

    # Track IP talkers
    if packet.haslayer(IP):
        src = packet[IP].src
        dst = packet[IP].dst
        stats["ip_stats"][src] += 1
        stats["ip_stats"][dst] += 1

    # Time-based metrics
    minute_key = datetime.now().strftime("%Y-%m-%d %H:%M")
    stats["traffic_timeline"][minute_key] += 1

    # Check for signature match
    sig = match_signature(packet, signatures)
    if sig:
        stats["alerts"] += 1
        stats["alert_timeline"][minute_key] += 1

        alert = {
            "name": sig["name"],
            "description": sig["description"],
            "summary": packet.summary()
        }
        print(f"[!] ALERT: {sig['name']} - {sig['description']}")
        log_alert(alert)
    else:
        print(f"[+] Packet: {packet.summary()}")

    # Persist stats periodically instead of every packet (performance improvement)
    global last_save_time
    current_time = time.time()
    if current_time - last_save_time >= SAVE_INTERVAL:
        save_stats()
        last_save_time = current_time


# Start sniffing on interface
def start_sniffing(interface):
    print(f"[*] Sniffing on {interface}...")
    sniff(prn=packet_callback, iface=interface, store=0)
