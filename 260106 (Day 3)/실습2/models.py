from sqlalchemy import Column, Integer, String
from database import Base

# 데이터베이스 모델 정의

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
