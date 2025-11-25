from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from WeatherApp.database import engine
import asyncio

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    tasks: list['Task'] = Relationship(back_populates='user')

class Task(SQLModel, table=True):
    __tablename__ = 'tasks'

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    content: str 
    user_id: int = Field(foreign_key='users.id', index=True)
    user: User | None = Relationship(back_populates='tasks')
    
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
    print("Tables created successfully.")