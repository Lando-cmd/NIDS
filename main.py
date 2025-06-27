# main.py
from packet_sniffer import start_sniffing
from scapy.all import get_if_list
import logging
import threading

def main():
    logging.basicConfig(level=logging.INFO)
    print("[*] Available interfaces:")

    interfaces = get_if_list()
    for iface in interfaces:
        print(" -", iface)

    # UPDATE this to match one of the printed interface names exactly:
    interface = r"\Device\NPF_{D64E4AAE-1441-464E-A7F8-17834F529DF1}"  # or "Ethernet", based on your system

    print(f"[*] Starting NIDS on interface: {interface}")
    try:
        start_sniffing(interface=interface)
    except KeyboardInterrupt:
        print("\n[*] Stopping NIDS. Goodbye.")

nids_thread = None
nids_running = False

def start_nids(interface):
    global nids_thread, nids_running
    if not nids_running:
        nids_thread = threading.Thread(target=start_sniffing, args=(interface,), daemon=True)
        nids_thread.start()
        nids_running = True

def stop_nids():
    global nids_running
    nids_running = False
    # Scapy sniff loop is blocking, so in practice you’d use scapy-async or subprocess control

def get_nids_status():
    return "running" if nids_running else "stopped"

if __name__ == "__main__":
    iface = r"\Device\NPF_{YOUR_INTERFACE_ID}"  # Replace with your interface
    start_nids(iface)
