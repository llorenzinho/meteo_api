from datetime import UTC, datetime
from http import HTTPStatus
import openmeteo_requests
import requests_cache
from retry_requests import retry

from app.models.dto.empty import EmptyOutDto
from app.models.site import Site
from app.models.weather import Weather
from app.db.tables.weather import Weather as TableWeather
from app.db.dao.weather import WeatherDao
from app.db.dao.site import SiteDao
from app.core.logger import get_logger
from app.models.dto.weather import WeatherInDto, WeatherOutDto
from openmeteo_sdk.Variable import Variable


class OpenMeteoService:
    def __init__(self, sites: SiteDao, wather: WeatherDao) -> None:
        self.url = 'https://api.open-meteo.com/v1/forecast'
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)
        self.logger = get_logger()
        self.sites = sites
        self.weather = wather

    def get_weather(self, input: WeatherInDto) -> WeatherOutDto | EmptyOutDto:
        site_id = input.site_id
        site = self.sites.get_by_id(site_id)
        if not site:
            return EmptyOutDto(
                code=HTTPStatus.NOT_FOUND, message=f'Site with id {site_id} not found'
            )
        data = self.weather.get_by_site_id(site_id)
        self.logger.debug(data)
        if data:
            return WeatherOutDto(
                site=Site(
                    name=site.name,
                    latitude=site.latitude,
                    longitude=site.longitude,
                ),
                weather=[
                    Weather(
                        site_id=item.site,
                        timestamp=item.timestamp,
                        temperature=item.temperature,
                    )
                    for item in data
                ],
            )
        return EmptyOutDto(code=HTTPStatus.NO_CONTENT, message='Empty content')

    def save_and_get_weather(
        self, input: WeatherInDto
    ) -> WeatherOutDto:  # TODO: add return type
        self.logger.debug(f'Received Data: {input.model_dump_json()}')
        site = self.sites.get_by_id(input.site_id)
        if not site:
            return None
        responses = self.openmeteo.weather_api(
            self.url,
            params=dict(
                current='temperature_2m',
                latitude=site.latitude,
                longitude=site.longitude,
            ),
        )
        response = responses[0]
        self.logger.debug(
            f'Coordinates {response.Latitude()}°N {response.Longitude()}°E'
        )
        self.logger.debug(f'Elevation {response.Elevation()} m asl')
        self.logger.debug(
            f'Timezone {response.Timezone()} {response.TimezoneAbbreviation()}'
        )
        self.logger.debug(
            f'Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s'
        )

        # Current values
        current = response.Current()
        current_variables = list(
            map(lambda i: current.Variables(i), range(0, current.VariablesLength()))
        )
        current_temperature_2m = next(
            filter(
                lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2,
                current_variables,
            )
        )

        self.logger.debug(current_temperature_2m.Value())
        new_weather = TableWeather(
            site=site.id,
            temperature=current_temperature_2m.Value(),
            timestamp=datetime.now(tz=UTC),
        )
        res = self.weather.create(new_weather)
        _response = WeatherOutDto(
            site=Site(name=site.name, latitude=site.latitude, longitude=site.longitude),
            weather=[
                Weather(
                    site_id=site.id,
                    temperature=res.temperature,
                    timestamp=res.timestamp,
                )
            ],
        )
        return _response
