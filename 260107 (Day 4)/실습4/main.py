from fastapi import FastAPI, WebSocket, WebSocketDisconnect
app = FastAPI()

@app.websocket("/ws/{nickname}")
async def websocket_endpoint(websocket: WebSocket, nickname: str):
    await websocket.accept()
    await websocket.send_text(f"{nickname}님 환영합니다!")

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{nickname}님의 메시지: {data}")

    except WebSocketDisconnect:
        print("웹소켓 연결 해제")
