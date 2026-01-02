from fastapi import FastAPI

app = FastAPI()

@app.get("/orders/{order_id}")
def get_order(order_id: int, show_items: bool = False):
    if show_items:
        return {"order_id": order_id, "items": ["item1", "item2"]}
    return {"order_id": order_id}
