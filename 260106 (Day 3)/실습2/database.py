from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 비동기 SQLite 데이터베이스 URL 설정
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

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

# 비동기 세션 생성 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
