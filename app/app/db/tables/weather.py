from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column
from app.db.database import BaseTable


class Weather(BaseTable):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column('TEMPERATURE', Float, nullable=False)
    timestamp = Column('TIMESTAMP', DateTime, nullable=False)
    site = mapped_column(ForeignKey('site.id'))
