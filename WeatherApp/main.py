
from fastapi import FastAPI
from dotenv import load_dotenv

from WeatherApp.models import create_tables
from WeatherApp.routers.users import router as users_router
from WeatherApp.routers.tasks import router as tasks_router

load_dotenv()

app = FastAPI(title="Weather Task API")


@app.on_event("startup")
def on_startup() -> None:
    create_tables()


app.include_router(users_router)
app.include_router(tasks_router)


@app.get("/")
def home():
    return {"message": "weather task api is running"}
