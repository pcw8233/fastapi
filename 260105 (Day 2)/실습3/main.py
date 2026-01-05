from fastapi import FastAPI
from pydantic import BaseModel, model_validator, EmailStr
import re

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+$"
app = FastAPI()

class ContactInfo(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None

    # 입력 데이터 전처리
    @model_validator(mode="before")
    @classmethod
    def preprocess_email(cls, data):
        if isinstance(data, dict) and data.get("email"):
            data["email"] = data["email"].lower()
        return data

    # 비즈니스 로직
    @model_validator(mode="after")
    def check_contact_info(self):
        if not self.email and not self.phone_number:
            raise ValueError("이메일 또는 핸드폰 번호가 필요합니다")

        # 이메일 형식 xxx@xxx.xxx
        if self.email and not re.match(EMAIL_REGEX, self.email):
            raise ValueError("Invalid email format")

        return self






@app.post("/contact")
def create_contact(contact: ContactInfo):
    return {
        "message": "Contact info accepted",
        "data": contact
    }
