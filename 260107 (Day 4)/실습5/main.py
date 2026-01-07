from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # 접속한 모든 소켓을 관리하는 리스트
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # handshake 수락 후 리스트에 추가
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # 연결 끊긴 소켓을 리스트에서 제거
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # 리스트에 있는 모든 클라이언트에게 메시지 전송
        for conn in self.active_connections:
            await conn.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await manager.connect(websocket)

    # 입장 알림
    await manager.broadcast(
        {
            "type": "system",
            "message": f"📢 {client_name}님이 입장하셨습니다"
        }
    )

    try:
        while True:
            # 채팅 메시지
            data = await websocket.receive_text()
            await manager.broadcast(
                {
                    "type": "chat",
                    "sender": client_name,
                    "message": data
                }
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            {
                "type": "system",
                "message": f"📢 {client_name}님이 퇴장하셨습니다"
            }
        )
