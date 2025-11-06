import threading
import time
from nids_manager import NIDSManager
from api_server import APIServer

def main():
    """
    Main function to run the NIDS.
    It initializes the NIDS components and starts the API server.
    The NIDS Manager (and the sniffer) will be started via an API call.
    """
    # 1. Initialize the manager, but DO NOT start it.
    nids_manager = NIDSManager()

    # 2. Initialize and start the API Server in a separate thread.
    #    The API server holds a reference to the nids_manager.
    api_server = APIServer(nids_manager)
    api_thread = threading.Thread(target=api_server.run, daemon=True)
    api_thread.start()

    # 3. Keep the main thread alive to listen for a shutdown command (Ctrl+C).
    #    The API server will run in the background.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutdown signal received. Stopping NIDS...")
        # If the NIDS was running, stop it gracefully.
        if nids_manager.is_running:
            nids_manager.stop()
        print("NIDS stopped.")

if __name__ == "__main__":
    main()
