# signature_engine.py
import yaml

def load_signatures(path="signatures.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def match_signature(packet, signatures):
    for sig in signatures:
        proto = sig.get("protocol", "").upper()
        port = sig.get("port", None)
        keyword = sig.get("keyword", None)

        # Match protocol
        if proto == "TCP" and packet.haslayer("TCP"):
            l4 = packet["TCP"]
        elif proto == "UDP" and packet.haslayer("UDP"):
            l4 = packet["UDP"]
        elif proto == "ICMP" and packet.haslayer("ICMP"):
            l4 = packet["ICMP"]
        else:
            continue

        # Match port
        if port and hasattr(l4, "dport") and l4.dport != port:
            continue

        # Match keyword (if payload exists)
        if keyword:
            raw = bytes(packet).decode(errors="ignore")
            if keyword not in raw:
                continue

        return sig  # Match found

    return None
