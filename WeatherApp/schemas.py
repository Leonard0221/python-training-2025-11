# app/schemas.py
from pydantic import BaseModel, Field


# -------- User Schemas --------

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


# -------- Task Schemas --------

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1, max_length=255)
    user_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=255)
    content: str | None = Field(None, min_length=1)
    city: str | None = Field(None, min_length=1, max_length=255)
    user_id: int | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    content: str
    city: str
    user_id: int

    class Config:
        from_attributes = True


# -------- Weather Schemas --------

class WeatherInfo(BaseModel):
    temperature: float
    windspeed: float
    weathercode: int
    time: str


class TaskReadWithWeather(TaskRead):
    weather: WeatherInfo
