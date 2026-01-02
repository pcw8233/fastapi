from fastapi import FastAPI


# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# 루트 엔드포인트 정의 (GET 요청)
@app.get("/")
def hello():
    return {"message": "Hello, FastAPI!"}
