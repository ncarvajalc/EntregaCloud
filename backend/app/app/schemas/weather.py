from pydantic import BaseModel


class WeatherBase(BaseModel):
    city: str
    weather: str


class Weather(WeatherBase):
    pass


class WeatherNotFound(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Weather for city Quito not found",
            }
        }
