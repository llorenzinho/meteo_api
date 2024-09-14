from app.db.database import AppDatabase


class BaseDao:
    def __init__(self, database: AppDatabase) -> None:
        self.database = database
