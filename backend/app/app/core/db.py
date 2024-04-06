from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # True for debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


def seed_data():
    from app.models.weather import Weather

    db = SessionLocal()
    try:
        db.add(Weather(city="Quito", weather="cloudy"))
        db.add(Weather(city="Bogotá", weather="sunny"))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
