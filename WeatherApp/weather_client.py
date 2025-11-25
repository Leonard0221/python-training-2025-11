# app/weather_client.py
from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, status

from WeatherApp.schemas import WeatherInfo


class ForecastClient:
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    async def _get_coordinates(self, city: str) -> tuple[float, float]:
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.GEO_URL, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results")
        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

        first = results[0]
        return float(first["latitude"]), float(first["longitude"])

    async def get_current_weather(self, city: str) -> WeatherInfo:
        lat, lon = await self._get_coordinates(city)

        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.WEATHER_URL, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

        cw = data.get("current_weather")
        if not cw:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Weather service error",
            )

        return WeatherInfo(
            temperature=cw["temperature"],
            windspeed=cw["windspeed"],
            weathercode=cw["weathercode"],
            time=cw["time"],
        )


_forecast_client = ForecastClient()


def get_forecast_client() -> ForecastClient:
    return _forecast_client


ForecastDep = Annotated[ForecastClient, Depends(get_forecast_client)]
