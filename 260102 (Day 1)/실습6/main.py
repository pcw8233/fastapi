from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    description: str = "No description"

@app.post("/products/")
def create_product(product: Product):
    return {"product": product}
