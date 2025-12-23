from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Numeric
from datetime import datetime


class Base(DeclarativeBase):
    pass


class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    temperature: Mapped[float] = mapped_column(Numeric(4, 1))
    humidity: Mapped[float] = mapped_column(Numeric(5, 2))
    pressure: Mapped[float] = mapped_column(Numeric(6, 2))
    wind_speed: Mapped[float] = mapped_column(Numeric(4, 2))
