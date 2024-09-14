from pydantic import BaseModel, ConfigDict


class SiteInDto(BaseModel):
    name: str
    latitude: float
    longitude: float


class SiteOutDto(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(
        from_attributes=True,
    )


class SiteListOutDto(BaseModel):
    sites: list[SiteOutDto]
