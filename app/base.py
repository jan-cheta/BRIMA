from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

database_url = 'sqlite:///main.sqlite'

class Database:
    _instance = None
    engine = None
    Session = None

    def __new__(cls, db_url=database_url):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(db_url)
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            Base.metadata.create_all(cls._instance.engine)
        return cls._instance
    
    def get_session(self):
        return self.Session()