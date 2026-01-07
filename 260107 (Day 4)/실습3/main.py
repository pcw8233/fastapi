import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/game")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    secret_number = random.randint(1, 100)
    attemps = 0
    await websocket.send_text("게임 시작합니다. 1부터 100 사이에서 숫자를 맞히세요")

    try:
        while True:
            # 클라이언트에서 숫자 받기
            data = await websocket.receive_text()

            guess = int(data) # 사용자가 추론한 숫자
            attemps += 1

            # 숫자 비교 검증
            if guess < secret_number:
                await websocket.send_text(f"⬆️ (현재 {attemps}회 시도)")
            elif guess > secret_number:
                await websocket.send_text(f"⬇️ (현재 {attemps}회 시도)")
            else:
                await websocket.send_text(f"정답! (총 {attemps}회 시도)")
                break

    except WebSocketDisconnect:
        print("웹소켓 연결 해제")
