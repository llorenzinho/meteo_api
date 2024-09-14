from app.db.tables.site import Site
from app.models.dto.site import SiteInDto, SiteListOutDto, SiteOutDto
from app.core.logger import get_logger
from app.db.dao.site import SiteDao


class SiteService:
    def __init__(self, dao: SiteDao) -> None:
        self.dao = dao
        self.logger = get_logger()

    def create(self, data: SiteInDto) -> SiteOutDto:
        self.logger.debug(f'Creating Site: {data.model_dump()}')
        new_site: Site = Site(**data.model_dump())
        created = self.dao.create(new_site)
        return created

    def get(self, id: int) -> SiteOutDto:
        self.logger.debug(f'Getting Site: {id}')
        site = self.dao.get_by_id(id)
        return site

    def list(self) -> SiteListOutDto:
        self.logger.debug('Listing Sites')
        sites = self.dao.list()
        self.logger.debug(sites)
        return SiteListOutDto(sites=[SiteOutDto.model_validate(site) for site in sites])
