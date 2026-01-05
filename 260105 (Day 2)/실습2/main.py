from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

app = FastAPI()

class Reservation(BaseModel):
    pass

@app.post("/reservations/")
def create_reservation(reservation: Reservation):
    return {"reservation": reservation}
