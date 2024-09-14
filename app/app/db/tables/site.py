from sqlalchemy import Column, Float, Integer, String
from app.db.database import BaseTable


class Site(BaseTable):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        'NAME',
        String(100),
        nullable=False,
    )
    latitude = Column('LATITUDE', Float, nullable=False)
    longitude = Column('LONGITUDE', Float, nullable=False)
