import math
import time
from datetime import datetime, timedelta

import numpy as np

from generator.database.db import SessionLocal
from generator.database.models.weather import WeatherData, Base
from generator.database.db import engine

Base.metadata.create_all(bind=engine)


DAYS = 365
STEP_HOURS = 1

AVG_TEMP = 10          # среднегодовая температура
TEMP_AMPLITUDE = 15    # амплитуда


def generate_weather_row(dt: datetime) -> WeatherData:
    day_of_year = dt.timetuple().tm_yday

    # годовая сезонность
    seasonal_temp = (
        AVG_TEMP
        + TEMP_AMPLITUDE * math.sin(2 * math.pi * day_of_year / 365)
    )

    # суточные колебания
    daily_variation = math.sin(2 * math.pi * dt.hour / 24) * 2

    temperature = seasonal_temp + daily_variation + np.random.normal(0, 1.5)

    humidity = 80 - temperature + np.random.normal(0, 5)
    humidity = min(max(humidity, 20), 95)

    pressure = 1013 + np.random.normal(0, 5)

    wind_speed = abs(np.random.normal(3 + abs(temperature) * 0.05, 1.5))

    return WeatherData(
        timestamp=dt,
        temperature=round(temperature, 1),
        humidity=round(humidity, 2),
        pressure=round(pressure, 2),
        wind_speed=round(wind_speed, 2),
    )


def generate_year():
    session = SessionLocal()

    end_dt = datetime.now().replace(minute=0, second=0, microsecond=0)
    start_dt = end_dt - timedelta(days=DAYS)

    current_dt = start_dt

    while current_dt <= end_dt:
        try:
            row = generate_weather_row(current_dt)
            session.add(row)
            session.commit()

            current_dt += timedelta(hours=STEP_HOURS)

            time.sleep(0.01)

        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            time.sleep(1)

    session.close()


if __name__ == "__main__":
    generate_year()
