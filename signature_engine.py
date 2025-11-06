import yaml
import scapy.all as scapy
from collections import deque
import threading
import time


class SignatureEngine:
    """
    A signature-based engine that checks packets against a set of rules.
    """

    def __init__(self, signatures_file, max_alerts=1000):
        self.signatures = self._load_signatures(signatures_file)
        self.alerts = deque(maxlen=max_alerts)
        self.lock = threading.Lock()

    def _load_signatures(self, filename):
        """Load signatures from a YAML file."""
        with open(filename, 'r') as f:
            return yaml.safe_load(f)['signatures']

    def process_packet(self, packet):
        """Process a single packet and check for matching signatures."""
        for sig in self.signatures:
            if self._matches(packet, sig):
                self._generate_alert(packet, sig)

    def _matches(self, packet, signature):
        """Check if a packet matches a signature. Returns True on match, False otherwise."""
        # Protocol match
        if 'protocol' in signature:
            proto = signature['protocol']
            if proto == 'TCP' and not packet.haslayer(scapy.TCP): return False
            if proto == 'UDP' and not packet.haslayer(scapy.UDP): return False
            if proto == 'ICMP' and not packet.haslayer(scapy.ICMP): return False

        # IP layer checks
        if packet.haslayer(scapy.IP):
            if 'src_ip' in signature and packet[scapy.IP].src != signature['src_ip']: return False
            if 'dst_ip' in signature and packet[scapy.IP].dst != signature['dst_ip']: return False

        # Transport layer checks
        if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP):
            if 'src_port' in signature and packet.sport != signature['src_port']: return False
            if 'dst_port' in signature and packet.dport != signature['dst_port']: return False

        # Payload content check
        if 'content' in signature:
            if packet.haslayer(scapy.Raw):
                # Ensure content search is case-insensitive
                if signature['content'].lower().encode() not in packet[scapy.Raw].load.lower():
                    return False
            else:  # Signature requires content, but packet has no payload, so it's not a match.
                return False

        # If none of the checks failed, it's a match.
        return True

    def _generate_alert(self, packet, signature):
        """Generate an alert for a matching packet."""
        alert = {
            "signature_name": signature['name'],
            "message": signature['message'],
            "timestamp": time.time(),
            "src_ip": packet[scapy.IP].src if packet.haslayer(scapy.IP) else "N/A",
            "dst_ip": packet[scapy.IP].dst if packet.haslayer(scapy.IP) else "N/A",
            "src_port": packet.sport if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP) else "N/A",
            "dst_port": packet.dport if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP) else "N/A",
            "protocol": signature.get('protocol', "N/A"),
        }
        with self.lock:
            self.alerts.append(alert)
        # This print statement is useful for debugging in the backend terminal
        print(f"ALERT DETECTED: {alert['message']}")

    def get_alerts(self):
        """Return all generated alerts."""
        with self.lock:
            return list(self.alerts)
