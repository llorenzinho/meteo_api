from http import HTTPStatus
from fastapi import APIRouter

from app.models.dto.empty import EmptyOutDto
from app.models.dto.weather import WeatherInDto, WeatherOutDto
from app.services.open_meteo import OpenMeteoService
from app.core.logger import get_logger


class MeteoRoute:
    @staticmethod
    def get_router(open_meteo_service: OpenMeteoService):
        logger = get_logger()
        logger.debug('Creating health check router')
        router = APIRouter()

        @router.post(
            '/meteo',
            status_code=HTTPStatus.OK,
            response_model=WeatherOutDto,
            tags=['Weather'],
        )
        def post(info: WeatherInDto):
            logger.debug('Getting weather')
            res = open_meteo_service.save_and_get_weather(info)
            logger.debug(res)
            return res

        @router.get(
            '/meteo{site_id}',
            status_code=HTTPStatus.OK,
            response_model=WeatherOutDto | EmptyOutDto,
            tags=['Weather'],
        )
        def get(site_id: int):
            logger.debug('Getting weather')
            logger.debug(site_id)
            return open_meteo_service.get_weather(WeatherInDto(site_id=site_id))

        return router
