from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import Session

# ONE async DB URL (Postgres + asyncpg)
DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/weather_app"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # you can turn this off later
)

async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session

