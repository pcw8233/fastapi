from fastapi import FastAPI, WebSocket, WebSocketDisconnect
app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"서버 응답: {data}")

    except WebSocketDisconnect:
        print("웹소켓 연결 해제")
