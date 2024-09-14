from datetime import UTC, datetime
from typing import Optional

import sqlalchemy
from app.db.dao.base import BaseDao
from app.db.tables.weather import Weather


class WeatherDao(BaseDao):
    def get_by_site_id(self, site_id: int) -> Optional[list[Weather]]:
        with self.database.begin_session() as session:
            return session.query(Weather).filter(Weather.site == site_id).all()

    def get_by_id(self, id: int) -> Optional[Weather]:
        with self.database.begin_session() as session:
            return session.query(Weather).filter(Weather.id == id).one_or_none()

    def create(self, weather: Weather) -> Weather:
        with self.database.begin_session() as session:
            session.add(weather)
            session.flush()
            return weather

    def update(self, id: int, weather: dict) -> Optional[Weather]:
        with self.database.begin_session() as session:
            query = (
                sqlalchemy.update(Weather)
                .where(Weather.id == id)
                .values(**weather, updated_at=datetime.now(tz=UTC))
            )
            session.execute(query)
            return session.query(Weather).filter(Weather.id == id).one_or_none()

    def delete(self, id: int) -> Weather:
        with self.database.begin_session() as session:
            to_delete = session.query(Weather).filter(Weather.id == id).one_or_none()
            query = sqlalchemy.delete(Weather).where(Weather.id == id)
            session.execute(query)
            return to_delete

    def list(self) -> list[Weather]:
        with self.database.begin_session() as session:
            return session.query(Weather).all()

    def complete(self, id: int) -> Optional[Weather]:
        with self.database.begin_session() as session:
            query = (
                sqlalchemy.update(Weather)
                .where(Weather.id == id)
                .values(completed=True, updated_at=datetime.now(tz=UTC))
            )
            session.execute(query)
            return session.query(Weather).filter(Weather.id == id).one_or_none()
