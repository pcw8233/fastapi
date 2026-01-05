from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

app = FastAPI()

class Reservation(BaseModel):
    name: str = Field(..., max_length=50, description="이름 길이는 최대 50자입니다")
    email: str
    date: datetime
    special_requests: str = Field(default="", description="optional")

    # date validation
    @field_validator("date")
    @classmethod
    def validate_date(cls, value: datetime):
        if value < datetime.now(): # 과거
            raise ValueError("반드시 미래여야해요")
        return value

    # name validation
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if len(value) > 50:
            raise ValueError("50자 이내로 하세요")
        return value


@app.post("/reservations/")
def create_reservation(reservation: Reservation):
    return {"reservation": reservation}
