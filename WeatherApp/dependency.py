# app/dependency.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from WeatherApp.database import get_async_session


AsyncDBSession = Annotated[AsyncSession, Depends(get_async_session)]
