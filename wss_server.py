# wss_server.py
import asyncio
import time
import uvicorn
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Store all active WebSocket connections
active_connections = set()

# In-memory "database" for alerts
alerts_db = []


class ConnectionManager:
    def __init__(self):
        self.connections = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.add(websocket)
        print(f"New connection. Total connections: {len(self.connections)}")

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
        print(f"Connection closed. Total connections: {len(self.connections)}")

    async def broadcast(self, message: dict):
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")


manager = ConnectionManager()


async def alert_generator(file_name):
    new_alert = {
        "id": int(time.time()),
        "title": "Alert: Paralysis Detected",
        "imageName": file_name,
        "timestamp": datetime.now().isoformat(),
    }
    print(f"Alert Generator -> Processing file: {file_name}, Alert Data: {new_alert}")
    alerts_db.append(new_alert)

    await manager.broadcast({"type": "NEW_ALERT", "data": new_alert})

    print(f"Broadcasted new alert: {file_name}")


# Synchronous wrapper function for alert_generator
def sync_alert_generator(file_name):
    # Create a new event loop for this thread if needed
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the coroutine in the event loop
    loop.run_until_complete(alert_generator(file_name))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("WebSocket server started")

    yield  # App runs here

    # Shutdown code
    print("WebSocket server shutdown complete")


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    # Send initial state
    await websocket.send_json(
        {"type": "INITIAL_STATE", "data": alerts_db[-10:]}  # Last 10 alerts
    )

    try:
        while True:
            # Keep connection alive (can handle client messages here if needed)
            data = await websocket.receive_text()
            print(f"Received client message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Simple status endpoint
@app.get("/status")
async def get_status():
    return {
        "status": "running",
        "alerts_count": len(alerts_db),
        "active_connections": len(manager.connections),
    }


# For testing (optional)
@app.get("/", response_class=HTMLResponse)
async def get_root():
    return """
    <html>
        <body>
            <h1>WebSocket Alert Server</h1>
            <p>Status: Running</p>
            <p>Active connections: <span id="conn-count">0</span></p>
            <script>
                const ws = new WebSocket('ws://' + window.location.host + '/ws');
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    if (data.type === 'NEW_ALERT') {
                        console.log('New alert:', data.data);
                    }
                };
                
                // Update connection count
                setInterval(async () => {
                    const res = await fetch('/status');
                    const data = await res.json();
                    document.getElementById('conn-count').textContent = data.active_connections;
                }, 1000);
            </script>
        </body>
    </html>
    """


# Function to start the server programmatically
def start_server(host="0.0.0.0", port=3006):
    """Start the FastAPI WebSocket server"""
    print(f"Starting WebSocket server on {host}:{port}")
    print(f"Connect from Flutter using: ws://<your_machine_ip>:{port}/ws")
    uvicorn.run(app, host=host, port=port)


# For standalone execution
if __name__ == "__main__":
    start_server()
