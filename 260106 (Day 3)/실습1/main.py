from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, text
import asyncio

# 비동기 SQLite 데이터베이스 URL 설정
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 비동기 SQLAlchemy 엔진 생성
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL 쿼리 로그 출력
)

# 비동기 세션 생성
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base 클래스 생성
Base = declarative_base()

# 데이터베이스 모델 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# 데이터베이스 초기화 함수
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 비동기 세션 생성 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# CRUD 함수 정의

# 1. Create (데이터 삽입)
async def create_user(name: str, email: str):
    async with AsyncSessionLocal() as session:
        new_user = User(name=name, email=email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

# 2. Read (데이터 조회)
async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT * FROM users"))
        users = result.fetchall()
        return users

async def get_user_by_email(email: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        )
        user = result.fetchone()
        return user

# 3. Update (데이터 수정)
async def update_user(user_id: int, name: str, email: str):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return None

        user.name = name
        user.email = email
        await session.commit()
        await session.refresh(user)
        return user

# 4. Delete (데이터 삭제)
async def delete_user(user_id: int):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return None
        await session.delete(user)
        await session.commit()
        return user_id

# 실행 및 테스트 함수
if __name__ == "__main__":

    async def main():
        # 데이터베이스 초기화
        await init_db()

        ##### 아래는 예시며 자유롭게 진행해보세요
        # 사용자 생성
        print("=== Create Users ===")
        user1 = await create_user(name="Alice", email="alice@example.com")
        user2 = await create_user(name="Bob", email="bob@example.com")
        print(user1, user2)

        # 모든 사용자 조회
        print("\n=== Get All Users ===")
        users = await get_all_users()
        for user in users:
            print(user)

        # 특정 사용자 조회
        print("\n=== Get User by Email ===")
        user = await get_user_by_email(email="alice@example.com")
        print(user)

        # 사용자 수정
        print("\n=== Update User ===")
        updated_user = await update_user(user_id=user1.id, name="Alice Smith", email="alice.smith@example.com")
        print(updated_user)

        # 사용자 삭제
        print("\n=== Delete User ===")
        deleted_id = await delete_user(user_id=user2.id)
        print(f"Deleted User ID: {deleted_id}")

    asyncio.run(main())
