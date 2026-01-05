from fastapi import FastAPI
from pydantic import BaseModel, model_validator

app = FastAPI()

class ContactInfo(BaseModel):
    email: str | None = None
    phone_number: str | None = None

    pass

@app.post("/contact")
def create_contact(contact: ContactInfo):
    return {
        "message": "Contact info accepted",
        "data": contact
    }
