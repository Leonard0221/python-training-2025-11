from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func
from sqlmodel import select

from WeatherApp.dependency import AsyncDBSession
from WeatherApp.models import Task, User
from WeatherApp.schemas import TaskCreate, TaskRead, TaskReadWithWeather, TaskUpdate
from WeatherApp.weather_client import ForecastDep

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, db: AsyncDBSession):
    user = await db.get(User, task_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = Task(
        title=task_in.title,
        content=task_in.content,
        city=task_in.city,
        user_id=task_in.user_id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/", response_model=list[TaskRead])
async def list_tasks(
    db: AsyncDBSession,
    user_id: Optional[int] = Query(None),
    city: Optional[str] = Query(None),
):
    stmt = select(Task)
    if user_id is not None:
        stmt = stmt.where(Task.user_id == user_id)
    if city is not None:
        stmt = stmt.where(func.lower(Task.city) == city.lower())

    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskReadWithWeather)
async def get_task(
    task_id: int,
    db: AsyncDBSession,
    forecast_client: ForecastDep,
):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    weather = await forecast_client.get_current_weather(task.city)

    return TaskReadWithWeather(
        id=task.id,
        title=task.title,
        content=task.content,
        city=task.city,
        user_id=task.user_id,
        weather=weather,
    )


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task_in: TaskUpdate, db: AsyncDBSession):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncDBSession):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return None
