# export_stats.py
import json
import csv

with open("packet_stats.json", "r") as f:
    stats = json.load(f)

with open("stats.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Metric", "Value"])

    writer.writerow(["Total Packets", stats.get("total_packets", 0)])
    writer.writerow(["Total Alerts", stats.get("alerts", 0)])

    writer.writerow([])
    writer.writerow(["Protocol", "Count"])
    for proto, count in stats.get("protocols", {}).items():
        writer.writerow([proto, count])

    writer.writerow([])
    writer.writerow(["Top IPs", "Packets"])
    sorted_ips = sorted(stats.get("ip_stats", {}).items(), key=lambda x: x[1], reverse=True)[:10]
    for ip, count in sorted_ips:
        writer.writerow([ip, count])
