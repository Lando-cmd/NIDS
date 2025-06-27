from scapy.all import get_if_list, get_if_addr

for iface in get_if_list():
    try:
        ip = get_if_addr(iface)
        print(f"{iface} -> {ip}")
    except Exception:
        print(f"{iface} -> [No IP]")

#\Device\NPF_{D64E4AAE-1441-464E-A7F8-17834F529DF1}
#streamlit run 1_Home.py

#Starts API Server
#python api_server.py

#Starts Streamlit Dashboard
#streamlit run app.py