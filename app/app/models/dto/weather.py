from typing import Optional
from pydantic import BaseModel

from app.models.site import Site
from app.models.weather import Weather


class WeatherInDto(BaseModel):
    site_id: int


class WeatherOutDto(BaseModel):
    site: Optional[Site]
    weather: list[Weather]
