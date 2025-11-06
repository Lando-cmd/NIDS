import scapy.all as scapy
from collections import defaultdict, deque
import threading


class PacketSniffer:
    """
    A class to sniff network packets and keep statistics.
    """

    def __init__(self, max_packets=1000):
        self.packets = deque(maxlen=max_packets)
        self.stop_sniffing_event = threading.Event()
        self.thread = None
        self.stats = {
            "total_packets": 0,
            "protocol_counts": defaultdict(int),
            "ip_counts": defaultdict(int)
        }
        self.lock = threading.Lock()

    def _packet_callback(self, packet):
        """Callback function to process each sniffed packet."""
        with self.lock:
            self.packets.append(packet)
            self.stats["total_packets"] += 1

            if packet.haslayer(scapy.IP):
                self.stats["ip_counts"][packet[scapy.IP].src] += 1
                self.stats["ip_counts"][packet[scapy.IP].dst] += 1

            if packet.haslayer(scapy.TCP):
                self.stats["protocol_counts"]["TCP"] += 1
            elif packet.haslayer(scapy.UDP):
                self.stats["protocol_counts"]["UDP"] += 1
            elif packet.haslayer(scapy.ICMP):
                self.stats["protocol_counts"]["ICMP"] += 1
            else:
                self.stats["protocol_counts"]["Other"] += 1

    def get_packet(self):
        """Get a packet from the queue."""
        with self.lock:
            if self.packets:
                return self.packets.popleft()
        return None

    def get_stats(self):
        """Return the current statistics."""
        with self.lock:
            # Return a copy to prevent modification outside the class
            return {
                "total_packets": self.stats["total_packets"],
                "protocol_counts": self.stats["protocol_counts"].copy(),
                "ip_counts": self.stats["ip_counts"].copy()
            }

    def start(self):
        """Start the packet sniffer in a new thread."""
        self.stop_sniffing_event.clear()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print(f"Sniffer thread started. Listening...")

    def _run(self):
        """Run the sniffer."""
        try:
            # The 'iface' argument can be specified if needed, e.g., iface="Wi-Fi"
            # Leaving it blank lets scapy choose the default interface.
            scapy.sniff(prn=self._packet_callback, store=False, stop_filter=lambda p: self.stop_sniffing_event.is_set())
            print("Sniffing stopped.")
        except Exception as e:
            print(f"Error during sniffing: {e}")

    def stop(self):
        """Stop the packet sniffer."""
        self.stop_sniffing_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join()
        print("Sniffer thread stopped.")
