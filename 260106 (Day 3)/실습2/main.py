from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()



######################
# utils
######################

# Password
pwd_context = CryptContext(
    schemes=["argon2"], # 암호화 알고리즘 (bcrypt, argon2)
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# Access Token (JWT 형태)
ALGORITHM = "HS256"
SECRET_KEY = "be16-oz" # 자물쇠
ACCESS_TOKEN_EXPIRE_MINS = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


######################
# pydantic
######################
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


######################
# api
######################
@app.post("/register")
def register():
    pass

@app.post("/login")
def login():
    pass
