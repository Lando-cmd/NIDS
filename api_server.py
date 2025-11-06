# api_server.py
# NOTE: This Flask API is kept for backward compatibility but is no longer required.
# The NIDS can now be fully controlled via the Streamlit dashboard (streamlit run app.py).
# To use this legacy API, run: python api_server.py

from flask import Flask, jsonify, request
from threading import Thread
import json
import os
from main import start_nids, stop_nids, get_nids_status

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "NIDS API is live!"})

@app.route("/start", methods=["POST"])
def start():
    interface = request.json.get("interface")
    if not interface:
        return jsonify({"error": "Missing interface"}), 400

    if get_nids_status() == "running":
        return jsonify({"status": "already running"})

    Thread(target=start_nids, args=(interface,), daemon=True).start()
    return jsonify({"status": "started", "interface": interface})

@app.route("/stop", methods=["POST"])
def stop():
    stop_nids()
    return jsonify({"status": "stopped"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": get_nids_status()})

@app.route("/stats", methods=["GET"])
def stats():
    if not os.path.exists("packet_stats.json"):
        return jsonify({})
    with open("packet_stats.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)
