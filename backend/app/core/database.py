from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(
                settings.DATABASE_URL, 
                connect_args={"check_same_thread": False} # Needed for SQLite
            )
        return cls._instance

    def create_tables(self):
        """Creates the database tables based on SQLModel metadata"""
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        """Generator method for Dependency Injection"""
        with Session(self.engine) as session:
            yield session

db = Database()