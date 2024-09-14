from sqlalchemy import MetaData, create_engine
from app.core.config.conf import get_config
from app.core.config.db_config import DatabaseConfig
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import Session, declarative_base, sessionmaker


class Reflected(DeferredReflection):
    __abstract__ = True


BaseTable = declarative_base(metadata=MetaData(schema=get_config().db_config.database))


class AppDatabase:
    def __init__(self, config: DatabaseConfig) -> None:
        self.db_config = config
        self._engine = None
        self._SessionFactory = None
        self._connected = False

    @property
    def connection_string(self) -> str:
        return f'mysql+pymysql://{self.db_config.user}:{self.db_config.password}@{self.db_config.host}:{self.db_config.port}/{self.db_config.database}'

    def connect(self):
        self._engine = create_engine(self.connection_string, pool_pre_ping=True)
        self._SessionFactory = sessionmaker(
            bind=self._engine,
            future=True,
            expire_on_commit=False,
        )

    def init_mappings(self):
        Reflected.prepare(self._engine)

    def begin_session(self) -> Session:
        return self._SessionFactory.begin()
