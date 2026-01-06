from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptoContext

app = FastAPI()



######################
# utils
######################
pwd_context = CryptoContext(
    schemes=["argon2"], # 암호화 알고리즘 (bcrypt, argon2)
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)





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
