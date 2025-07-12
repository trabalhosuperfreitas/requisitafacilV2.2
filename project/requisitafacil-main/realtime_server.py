from fastapi import FastAPI, WebSocket, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantém a conexão aberta
    except Exception:
        pass
    finally:
        clients.remove(websocket)

async def broadcast_update(data: str):
    to_remove = set()
    for ws in clients:
        try:
            await ws.send_text(data)
        except Exception:
            to_remove.add(ws)
    for ws in to_remove:
        clients.remove(ws)

@app.post("/notify")
async def notify(request: FastAPIRequest):
    data = await request.json()
    await broadcast_update(data.get("action", "update"))
    return JSONResponse(content={"status": "ok"}) 