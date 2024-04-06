from app.schemas.weather import Weather, WeatherNotFound
from app.services.weather import get_weather_by_city
from app.core.db import get_db
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/cities",
    response_model=Weather,
    responses={404: {"model": WeatherNotFound}},
)
async def get_weather_sync_client_by_city(
    db: Session = Depends(get_db), city: str = Query("Bogotá")
):
    """
    Gets Weather by city
    """
    weather = get_weather_by_city(db, city)
    return weather
