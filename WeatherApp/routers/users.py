# app/routers/users.py
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from WeatherApp.dependency import AsyncDBSession
from WeatherApp.models import User
from WeatherApp.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncDBSession):
    user = User(name=user_in.name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncDBSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncDBSession):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncDBSession):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return None
