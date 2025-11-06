from fastapi import FastAPI, HTTPException
from nids_manager import NIDSManager
import uvicorn

class APIServer:
    """
    A simple FastAPI server to expose NIDS functionality.
    """
    def __init__(self, nids_manager: NIDSManager):
        self.app = FastAPI()
        self.nids_manager = nids_manager
        self._setup_routes()

    def _setup_routes(self):
        """Sets up the API routes."""
        @self.app.post("/start")
        def start_nids():
            try:
                self.nids_manager.start()
                return {"message": "NIDS started"}
            except Exception as e:
                # Log the exception for debugging
                print(f"Error starting NIDS: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/stop")
        def stop_nids():
            try:
                self.nids_manager.stop()
                return {"message": "NIDS stopped"}
            except Exception as e:
                print(f"Error stopping NIDS: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/stats")
        def get_stats():
            return self.nids_manager.get_stats()

        @self.app.get("/alerts")
        def get_alerts():
            return self.nids_manager.get_alerts()

        @self.app.get("/status")
        def get_status():
            return {"is_running": self.nids_manager.is_running}

    def run(self, host="127.0.0.1", port=8000):
        """Runs the FastAPI server."""
        uvicorn.run(self.app, host=host, port=port)
