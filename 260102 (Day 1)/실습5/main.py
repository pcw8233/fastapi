from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/async-items/")
async def get_async_items():
    await asyncio.sleep(2) # 2초 지연
    return {"message": "2초 뒤에 나오겠죠"}
