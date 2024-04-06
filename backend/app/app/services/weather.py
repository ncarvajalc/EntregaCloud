from app.models import Weather
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def get_weather_by_city(db: Session, city: str):
    weather = db.query(Weather).filter(Weather.city == city).first()
    if not weather:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Weather for city {city} not found",
        )
    return weather
