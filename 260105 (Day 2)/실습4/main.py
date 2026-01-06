from fastapi import FastAPI
from pydantic import BaseModel, computed_field, field_validator

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    discount: float = 0

    # 할인율 검증
    @field_validator("discount")
    @classmethod
    def validate_discount(cls, value):
        if not (0 <= value <= 100):
            raise ValueError("할인은 0-100% 사이로만 가능")
        return value

    # final_price 자동 계산 필드
    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount / 100), 1)     # 할인가 = 원가 * (1-할인율)


@app.post("/products")
def create_product(product: Product):
    return product
