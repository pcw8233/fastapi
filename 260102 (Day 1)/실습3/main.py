from fastapi import FastAPI

app = FastAPI()

@app.get("/products/")
def get_products(category: str = "all", page: int = 1):
    return {"category": category, "page": page}
