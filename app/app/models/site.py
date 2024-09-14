from pydantic import BaseModel


class Site(BaseModel):
    name: str
    latitude: float
    longitude: float
