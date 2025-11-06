# nids_manager.py
"""
NIDS Manager Module
Manages the packet sniffer thread lifecycle for the Streamlit dashboard.
"""
import threading
import subprocess
import sys
import os
import json
import re
from packet_sniffer import start_sniffing

# Global state
_nids_process = None
_nids_thread = None
_nids_running = False
_current_interface = None
_lock = threading.Lock()


def start_nids(interface):
    """Start the NIDS packet sniffer on the specified interface."""
    global _nids_process, _nids_thread, _nids_running, _current_interface
    
    with _lock:
        if _nids_running:
            return {"status": "already_running", "interface": _current_interface}
        
        # Validate interface string to prevent command injection
        # Interface names should only contain alphanumeric chars, hyphens, underscores, 
        # periods, colons, and brackets (for common interface naming patterns)
        if not re.match(r'^[a-zA-Z0-9\-_.:\/\[\]]+$', interface):
            return {"status": "error", "message": "Invalid interface name"}
        
        # Start packet sniffer in a separate process to allow proper interruption
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Use safer argument passing: pass interface as a JSON-encoded environment variable
        # This avoids any risk of command injection through string construction
        env = os.environ.copy()
        env['NIDS_INTERFACE'] = json.dumps(interface)
        
        import_cmd = "import json, os; from packet_sniffer import start_sniffing; start_sniffing(json.loads(os.environ['NIDS_INTERFACE']))"
        _nids_process = subprocess.Popen(
            [sys.executable, "-c", import_cmd],
            cwd=script_dir,
            env=env
        )
        
        _nids_running = True
        _current_interface = interface
        
        return {"status": "started", "interface": interface}


def stop_nids():
    """Stop the NIDS packet sniffer."""
    global _nids_process, _nids_thread, _nids_running, _current_interface
    
    with _lock:
        if not _nids_running:
            return {"status": "not_running"}
        
        # Terminate the subprocess
        if _nids_process:
            _nids_process.terminate()
            try:
                _nids_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _nids_process.kill()
            _nids_process = None
        
        _nids_running = False
        _current_interface = None
        
        return {"status": "stopped"}


def get_nids_status():
    """Get the current NIDS status."""
    global _nids_running, _current_interface
    
    with _lock:
        # Check if process is still alive
        if _nids_running and _nids_process:
            if _nids_process.poll() is not None:
                # Process has terminated
                _nids_running = False
                _current_interface = None
        
        return {
            "running": _nids_running,
            "interface": _current_interface,
            "status": "running" if _nids_running else "stopped"
        }
