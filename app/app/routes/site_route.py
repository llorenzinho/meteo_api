from http import HTTPStatus
from fastapi import APIRouter

from app.models.dto.site import SiteInDto, SiteListOutDto, SiteOutDto
from app.services.site import SiteService
from app.core.logger import get_logger


class SiteRouter:
    @staticmethod
    def get_router(service: SiteService):
        logger = get_logger()
        logger.debug('Creating site router')
        router = APIRouter()

        @router.get(
            '/sites',
            response_model=SiteListOutDto,
            status_code=HTTPStatus.OK,
            tags=['Sites'],
        )
        def list():
            logger.debug('Listing sites')
            sites = service.list()
            return sites

        @router.get(
            '/site/{id}',
            response_model=SiteOutDto,
            status_code=HTTPStatus.OK,
            tags=['Sites'],
        )
        def get(id: int):
            logger.debug(f'Getting site: {id}')
            site = service.get(id)
            return site

        @router.post(
            '/site',
            response_model=SiteOutDto,
            status_code=HTTPStatus.OK,
            tags=['Sites'],
        )
        def create(data: SiteInDto):
            logger.debug(f'Creating site: {data.model_dump()}')
            site = service.create(data)
            return site

        return router
