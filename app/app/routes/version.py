from http import HTTPStatus
from fastapi import APIRouter
from app.core.logger import get_logger
from app.models.dto.version import ApiVersionOutDTO, get_api_version

class VersionRouter:
    @staticmethod
    def get_router():
        logger = get_logger()
        logger.debug('Creating health check router')
        health_check_router = APIRouter()

        @health_check_router.get(
            '/version', response_model=ApiVersionOutDTO, status_code=HTTPStatus.OK, tags=["Utils"]
        )
        def version():
            return VersionRouter.version()

        return health_check_router

    @staticmethod
    def version():
        return get_api_version()