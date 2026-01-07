from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import psutil
import asyncio

app = FastAPI()

@app.websocket("/ws/monitor")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent

            data = {
                "cpu": cpu_usage,
                "ram": ram_usage
            }

            await websocket.send_json(data)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("웹소켓 연결 해제")
