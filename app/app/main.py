from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.version import VersionRouter
from app.core.exceptions.base import base_ex_handler
from app.db.dao.weather import WeatherDao
from app.routes.site_route import SiteRouter
from app.db.dao.site import SiteDao
from app.services.site import SiteService
from app.routes.meteo_route import MeteoRoute
from app.services.open_meteo import OpenMeteoService
from app.routes.healthz import HealthCheckRouter
from app.core.config.conf import get_config
from app.db.database import AppDatabase
from app.core.logger import get_logger

from mangum import Mangum


logger = get_logger()
database = AppDatabase(get_config().db_config)

site_dao = SiteDao(database)
weather_dao = WeatherDao(database)

site_service = SiteService(site_dao)
openmeteo = OpenMeteoService(site_dao, weather_dao)


@asynccontextmanager
async def lifespan(fastapi: FastAPI):
    logger.info('Starting service ...')
    database.connect()
    database.init_mappings()
    logger.info('Service started')
    yield
    logger.info('Stopping service ...')


app = FastAPI(title='3Bee App', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=[
        'access-control-allow-origin',
        'content-type',
    ],
)

app.include_router(HealthCheckRouter.get_router())
app.include_router(VersionRouter.get_router())
app.include_router(MeteoRoute.get_router(openmeteo))
app.include_router(SiteRouter.get_router(site_service))

app.add_exception_handler(Exception, base_ex_handler)

handler = Mangum(app)