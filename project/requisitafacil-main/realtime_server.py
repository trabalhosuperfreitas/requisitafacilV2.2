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
    print(f"Novo cliente conectado. Total: {len(clients)}")
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'ping':
                # Responde ao ping para manter a conexão ativa
                await websocket.send_text('pong')
                print(f"Ping recebido e respondido. Clientes ativos: {len(clients)}")
    except Exception as e:
        print(f"Cliente desconectado: {e}")
    finally:
        clients.remove(websocket)
        print(f"Cliente removido. Total: {len(clients)}")

async def broadcast_update(data: str):
    print(f"Broadcasting para {len(clients)} clientes: {data}")
    to_remove = set()
    for ws in clients:
        try:
            await ws.send_text(data)
            print(f"Mensagem enviada para cliente")
        except Exception as e:
            print(f"Erro ao enviar para cliente: {e}")
            to_remove.add(ws)
    for ws in to_remove:
        clients.remove(ws)
    print(f"Clientes restantes: {len(clients)}")

@app.post("/notify")
async def notify(request: FastAPIRequest):
    data = await request.json()
    action = data.get("action", "update")
    message = data.get("message", "")
    print(f"Notificação recebida: {action} - {message}")
    await broadcast_update(action)
    return JSONResponse(content={"status": "ok", "action": action}) 