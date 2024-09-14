from datetime import UTC, datetime
from typing import Optional

import sqlalchemy
from app.db.dao.base import BaseDao
from app.db.tables.site import Site


class SiteDao(BaseDao):
    def get_by_id(self, id: int) -> Optional[Site]:
        with self.database.begin_session() as session:
            return session.query(Site).filter(Site.id == id).one_or_none()

    def create(self, site: Site) -> Site:
        with self.database.begin_session() as session:
            session.add(site)
            session.flush()
            return site

    def update(self, id: int, site: dict) -> Optional[Site]:
        with self.database.begin_session() as session:
            query = (
                sqlalchemy.update(Site)
                .where(Site.id == id)
                .values(**site, updated_at=datetime.now(tz=UTC))
            )
            session.execute(query)
            return session.query(Site).filter(Site.id == id).one_or_none()

    def delete(self, id: int) -> Site:
        with self.database.begin_session() as session:
            to_delete = session.query(Site).filter(Site.id == id).one_or_none()
            query = sqlalchemy.delete(Site).where(Site.id == id)
            session.execute(query)
            return to_delete

    def list(self) -> list[Site]:
        with self.database.begin_session() as session:
            return session.query(Site).all()

    def complete(self, id: int) -> Optional[Site]:
        with self.database.begin_session() as session:
            query = (
                sqlalchemy.update(Site)
                .where(Site.id == id)
                .values(completed=True, updated_at=datetime.now(tz=UTC))
            )
            session.execute(query)
            return session.query(Site).filter(Site.id == id).one_or_none()
