from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class Item(BaseModel):
    name: str
    quantity: int = Field(..., ge=1, description="1이상")

class Order(BaseModel):
    id: int
    items: List[Item]
    total_price: float = Field(..., ge=0, description="total price는 0 이상")

@app.post("/orders/")
def create_order(order: Order):
    return {"order": order}
