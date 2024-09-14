from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Weather(BaseModel):
    temperature: float
    timestamp: datetime
    site_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
