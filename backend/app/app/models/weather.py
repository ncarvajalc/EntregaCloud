from app.core.db import Base
from sqlalchemy import Column, Integer, String


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    weather = Column(String, index=True)
