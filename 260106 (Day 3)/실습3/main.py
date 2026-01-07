# fastapi
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

# 암호화
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# db
from database import get_db
from models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# TODO: 인증 관련
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """ TODO
    1. 전달된 JWT 토큰을 검증하여 사용자 정보를 가져옴
    2. 토큰이 유효하지 않거나 만료되면 401 반환
    3. DB에서 사용자 존재 여부 확인
    4. 사용자가 없거나 토큰이 유효하지 않다면, 401 Unauthorized 오류를 반환
    """
    credential_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="무효한 토큰값")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        exp = payload.get("exp")

        if username is None:
            raise credential_error

        if exp is None or (datetime.utcfromtimestamp(exp) < datetime.utcnow()):
            raise credential_error

    except JWTError:
        raise credential_error

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credential_error

    return {
        "id": user.id,
        "username": user.username
    }


######################
# pydantic
######################
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


######################
# api
######################
@app.post("/register")
async def register(
    user: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    # 유저가 이미 가입했는지 확인하기
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 가입한 사람")

    # 새로운 유저를 db 추가
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    return {"message": "회원가입 성공"}


@app.post("/login", response_model=Token)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    # 유저가 등록되어 있는지 확인하기
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    db_user = result.scalar_one_or_none()

    # 유저가 없거나 비밀번호 오류
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="아이디나 비밀번호가 잘못됨")

    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/profile")
async def profile(current_user: dict = Depends(get_current_user)):
    return current_user
